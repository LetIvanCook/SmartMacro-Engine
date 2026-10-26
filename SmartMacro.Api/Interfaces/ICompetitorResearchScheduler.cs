namespace SmartMacro.Api.Interfaces;

public interface ICompetitorResearchScheduler
{
    Task<bool> TriggerRunNowAsync(CancellationToken cancellationToken = default);
}
