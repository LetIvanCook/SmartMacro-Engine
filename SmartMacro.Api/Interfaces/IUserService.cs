using SmartMacro.Api.Models;

namespace SmartMacro.Api.Interfaces;

public interface IUserService
{
    Task<User?> GetUserByIdAsync(long userId);
    Task<User?> GetUserByEmailAsync(string email);
    Task<User> CreateUserAsync(User user);
    Task UpdateUserAsync(User user);
    Task DeleteUserAsync(long userId);
}
