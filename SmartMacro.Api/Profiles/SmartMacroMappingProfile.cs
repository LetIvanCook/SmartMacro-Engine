using AutoMapper;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Profiles;

/// <summary>
/// Tập trung toàn bộ mapping rules của dự án.
/// Lưu ý: Các rule ở đây được thiết kế để tương thích với ProjectTo&lt;T&gt;(),
/// nghĩa là AutoMapper sẽ dịch chúng thành Expression Tree → EF Core dịch tiếp
/// thành câu SQL SELECT chỉ lấy đúng các cột cần thiết.
/// </summary>
public class SmartMacroMappingProfile : Profile
{
    public SmartMacroMappingProfile()
    {
        // ──────────────────────────────────────────────────────────────
        // UserFoodInventory → InventoryItemResponseDto
        // ──────────────────────────────────────────────────────────────
        // Khi dùng ProjectTo, EF Core sẽ sinh JOIN giữa user_food_inventory
        // và foods, rồi SELECT chỉ 5 cột: inventory_id, food_name,
        // quantity_grams, kcal_per_100g, protein_g_per_100g.
        // Không có Include(), không kéo toàn bộ entity lên RAM.
        CreateMap<UserFoodInventory, InventoryItemResponseDto>()
            .ForMember(dest => dest.FoodId,
                       opt => opt.MapFrom(src => src.FoodId))
            .ForMember(dest => dest.FoodName,
                       opt => opt.MapFrom(src => src.Food.FoodName))
            .ForMember(dest => dest.KcalPer100g,
                       opt => opt.MapFrom(src => src.Food.KcalPer100g))
            .ForMember(dest => dest.ProteinGPer100g,
                       opt => opt.MapFrom(src => src.Food.ProteinGPer100g))
            .ForMember(dest => dest.CarbsGPer100g,
                       opt => opt.MapFrom(src => src.Food.CarbsGPer100g))
            .ForMember(dest => dest.FatGPer100g,
                       opt => opt.MapFrom(src => src.Food.FatGPer100g));

        // ──────────────────────────────────────────────────────────────
        // DailyTarget → DailyTargetDto
        // ──────────────────────────────────────────────────────────────
        // Mapping 1:1, chỉ giữ lại 4 cột macro — bỏ qua TargetId,
        // UserId, ComputedFromRuleId, CreatedAt.
        CreateMap<DailyTarget, DailyTargetDto>();

        // ──────────────────────────────────────────────────────────────
        // Food → FoodResponseDto
        // ──────────────────────────────────────────────────────────────
        // Hầu hết field map 1:1 theo convention.
        // CategoryName được project từ navigation property Category
        // → EF Core sinh LEFT JOIN food_categories, SELECT category_name.
        CreateMap<Food, FoodResponseDto>()
            .ForMember(dest => dest.CategoryName,
                       opt => opt.MapFrom(src => src.Category != null
                           ? src.Category.CategoryName
                           : null));

        // ──────────────────────────────────────────────────────────────
        // FoodCategory → FoodCategoryResponseDto
        // ──────────────────────────────────────────────────────────────
        // Mapping 1:1 theo convention — CategoryId, CategoryName.
        CreateMap<FoodCategory, FoodCategoryResponseDto>();
    }
}
