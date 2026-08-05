namespace SmartMacro.Api.Exceptions;

public class EmptyInventoryException : Exception
{
    public EmptyInventoryException(string message) : base(message)
    {
    }
}
