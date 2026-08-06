using AutoMapper;
using AutoMapper.QueryableExtensions;
using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Engines;
using SmartMacro.Api.Exceptions;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class OptimizationService : IOptimizationService
{
    private readonly SmartMacroDbContext _db;
    private readonly IMapper _mapper;
    private readonly IMacroOptimizationEngine _engine;

    public OptimizationService(
        SmartMacroDbContext db, 
        IMapper mapper, 
        IMacroOptimizationEngine engine)
    {
        _db = db;
        _mapper = mapper;
        _engine = engine;
    }

    public async Task<OptimizationResultDto> GenerateMealPlanAsync(long userId, OptimizationRequestDto request)
    {
        // 1. Query DailyTargets
        DailyTargetDto? target;
        if (request.DailyTargetId.HasValue)
        {
            target = await _db.DailyTargets
                .Where(dt => dt.UserId == userId && dt.TargetId == request.DailyTargetId.Value)
                .ProjectTo<DailyTargetDto>(_mapper.ConfigurationProvider)
                .FirstOrDefaultAsync();
        }
        else
        {
            var today = DateOnly.FromDateTime(DateTime.Now);
            target = await _db.DailyTargets
                .Where(dt => dt.UserId == userId && dt.TargetDate == today)
                .ProjectTo<DailyTargetDto>(_mapper.ConfigurationProvider)
                .FirstOrDefaultAsync();
        }

        if (target == null)
        {
            throw new NotFoundException("Không tìm thấy mục tiêu macro hợp lệ để tối ưu.");
        }

        // 2. Query UserFoodInventories
        var inventoryQuery = _db.UserFoodInventories
            .Where(inv => inv.UserId == userId && inv.QuantityGrams > 0);

        if (request.IncludeFoodIds != null && request.IncludeFoodIds.Any())
        {
            inventoryQuery = inventoryQuery.Where(inv => request.IncludeFoodIds.Contains(inv.FoodId));
        }

        var availableInventory = await inventoryQuery
            .ProjectTo<InventoryItemResponseDto>(_mapper.ConfigurationProvider)
            .ToListAsync();

        // 3. Nếu inventory rỗng
        if (availableInventory == null || availableInventory.Count == 0)
        {
            throw new EmptyInventoryException("Kho thực phẩm hiện tại đang trống hoặc không có nguyên liệu phù hợp.");
        }

        // 4 & 5. Gọi Engine
        var engineResult = _engine.CalculateOptimalMeal(target, availableInventory);

        // 6 & 7. Map kết quả
        var resultDto = new OptimizationResultDto
        {
            SolverStatus = engineResult.IsSuccessful 
                ? (engineResult.Message.Contains("OPTIMAL") ? "OPTIMAL" : "FEASIBLE") 
                : "INFEASIBLE",
            TargetMacros = new MacroSummaryDto
            {
                Kcal = target.TargetKcal,
                ProteinG = target.TargetProteinG,
                CarbsG = target.TargetCarbsG,
                FatG = target.TargetFatG
            },
            AchievedMacros = new MacroSummaryDto
            {
                Kcal = engineResult.TotalKcal,
                ProteinG = engineResult.TotalProtein,
                CarbsG = engineResult.TotalCarbs,
                FatG = engineResult.TotalFat
            },
            // Total deviation could be mapped from objective value if engine exposed it, but we can calculate it roughly here.
            // Engine objective is |TotalKcal - TargetKcal|.
            TotalDeviationScore = Math.Abs(engineResult.TotalKcal - target.TargetKcal)
        };

        if (engineResult.IsSuccessful)
        {
            foreach (var item in engineResult.Items)
            {
                // Find matching inventory item to get macros per 100g to calculate macros for this allocation
                var invItem = availableInventory.First(i => i.FoodId == item.FoodId);
                
                resultDto.AllocatedItems.Add(new AllocatedFoodItemDto
                {
                    FoodId = item.FoodId,
                    FoodName = item.FoodName,
                    QuantityGrams = item.CalculatedGrams,
                    Kcal = Math.Round(item.CalculatedGrams * invItem.KcalPer100g / 100m, 2),
                    ProteinG = Math.Round(item.CalculatedGrams * invItem.ProteinGPer100g / 100m, 2),
                    CarbsG = Math.Round(item.CalculatedGrams * invItem.CarbsGPer100g / 100m, 2),
                    FatG = Math.Round(item.CalculatedGrams * invItem.FatGPer100g / 100m, 2)
                });
            }
        }

        return resultDto;
    }
}
