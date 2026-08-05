using Microsoft.EntityFrameworkCore;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Services;

public class UserService : IUserService
{
    private readonly SmartMacroDbContext _context;

    public UserService(SmartMacroDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetUserByIdAsync(long userId)
    {
        return await _context.Users.FirstOrDefaultAsync(u => u.UserId == userId);
    }

    public async Task<User?> GetUserByEmailAsync(string email)
    {
        return await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
    }

    public async Task<User> CreateUserAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user;
    }

    public async Task UpdateUserAsync(User user)
    {
        _context.Users.Update(user);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteUserAsync(long userId)
    {
        var user = await GetUserByIdAsync(userId);
        if (user != null)
        {
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
        }
    }
}
