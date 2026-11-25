using SmartMacro.Api.DTOs;

namespace SmartMacro.Api.Interfaces;

public interface ICompetitorResearchService
{
    Task<CompetitorAnalysisResult> AnalyzeCompetitorAsync(CompetitorAnalysisRequest request, CancellationToken cancellationToken = default);
}
