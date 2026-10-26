namespace SmartMacro.Api.Exceptions;

public class InvalidResearchTargetException : Exception
{
    public InvalidResearchTargetException(string message) : base(message)
    {
    }
}
