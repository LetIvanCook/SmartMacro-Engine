using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface IOptimizationService
{
    Task<OptimizationResultDto> GenerateMealPlanAsync(long userId, OptimizationRequestDto request);
}
