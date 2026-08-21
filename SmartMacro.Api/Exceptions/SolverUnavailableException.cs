namespace SmartMacro.Api.Exceptions;

public class SolverUnavailableException : Exception
{
    public SolverUnavailableException(string message) : base(message)
    {
    }

    public SolverUnavailableException(string message, Exception innerException) : base(message, innerException)
    {
    }
}
