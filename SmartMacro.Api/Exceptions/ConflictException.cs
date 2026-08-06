namespace SmartMacro.Api.Exceptions;

/// <summary>
/// Ném khi tạo resource vi phạm ràng buộc unique (ví dụ: trùng tên FoodCategory).
/// GlobalExceptionHandler map sang HTTP 409 Conflict.
/// </summary>
public class ConflictException : Exception
{
    public ConflictException(string message) : base(message)
    {
    }
}
