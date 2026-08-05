using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;

namespace SmartMacro.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(long id)
    {
        var user = await _userService.GetUserByIdAsync(id);
        if (user == null)
        {
            return NotFound();
        }

        var userDto = new UserDto
        {
            UserId = user.UserId,
            Email = user.Email,
            FullName = user.FullName,
            DateOfBirth = user.DateOfBirth,
            BiologicalSex = user.BiologicalSex,
            ActivityLevel = user.ActivityLevel,
            GoalType = user.GoalType,
            Status = user.Status,
            CreatedAt = user.CreatedAt
        };

        return Ok(userDto);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateUser(long id, [FromBody] UpdateUserRequestDto request)
    {
        var user = await _userService.GetUserByIdAsync(id);
        if (user == null)
        {
            return NotFound();
        }

        if (request.FullName != null) user.FullName = request.FullName;
        if (request.DateOfBirth.HasValue) user.DateOfBirth = request.DateOfBirth.Value;
        if (request.BiologicalSex != null) user.BiologicalSex = request.BiologicalSex;
        if (request.ActivityLevel != null) user.ActivityLevel = request.ActivityLevel;
        if (request.GoalType != null) user.GoalType = request.GoalType;

        await _userService.UpdateUserAsync(user);

        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteUser(long id)
    {
        var user = await _userService.GetUserByIdAsync(id);
        if (user == null)
        {
            return NotFound();
        }

        await _userService.DeleteUserAsync(id);

        return NoContent();
    }
}
