using AutoMapper;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging.Abstractions;
using Moq;
using SmartMacro.Api.Controllers;
using SmartMacro.Api.DTOs;
using SmartMacro.Api.Interfaces;
using SmartMacro.Api.Models;
using SmartMacro.Api.Profiles;

namespace SmartMacro.Tests;

/// <summary>
/// Unit tests cho UsersController.
/// Xác minh AutoMapper refactor cho UpdateUser: partial update, full update,
/// edge cases (empty string vs null), và xử lý lỗi 404.
/// </summary>
public class UsersControllerTests
{
    private readonly Mock<IUserService> _userServiceMock;
    private readonly IMapper _mapper;
    private readonly UsersController _sut;

    public UsersControllerTests()
    {
        _userServiceMock = new Mock<IUserService>();

        var mapperConfig = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<SmartMacroMappingProfile>();
        }, NullLoggerFactory.Instance);
        mapperConfig.AssertConfigurationIsValid();
        _mapper = mapperConfig.CreateMapper();

        _sut = new UsersController(_userServiceMock.Object, _mapper);
    }

    [Fact]
    public async Task UpdateUser_WhenPartialPayload_ShouldOnlyUpdateProvidedFieldsAndKeepOthers()
    {
        // Arrange: User ban đầu có đầy đủ thông tin
        var initialUser = new User
        {
            UserId = 1,
            Email = "user@example.com",
            FullName = "Original Name",
            DateOfBirth = new DateOnly(1995, 6, 15),
            BiologicalSex = "male",
            ActivityLevel = "moderate",
            GoalType = "cut",
            Status = "active",
            CreatedAt = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc)
        };

        _userServiceMock.Setup(x => x.GetUserByIdAsync(1))
            .ReturnsAsync(initialUser);

        // Chỉ gửi duy nhất FullName
        var request = new UpdateUserRequestDto
        {
            FullName = "Updated Name"
        };

        // Act
        var result = await _sut.UpdateUser(1, request);

        // Assert
        result.Should().BeOfType<NoContentResult>();
        initialUser.FullName.Should().Be("Updated Name", "vì FullName được cung cấp trong request");
        initialUser.Email.Should().Be("user@example.com", "vì Email không nằm trong DTO và không được bị null hóa");
        initialUser.DateOfBirth.Should().Be(new DateOnly(1995, 6, 15), "vì DateOfBirth = null trong request nên phải giữ nguyên");
        initialUser.BiologicalSex.Should().Be("male", "vì BiologicalSex = null trong request nên phải giữ nguyên");
        initialUser.ActivityLevel.Should().Be("moderate", "vì ActivityLevel = null trong request nên phải giữ nguyên");
        initialUser.GoalType.Should().Be("cut", "vì GoalType = null trong request nên phải giữ nguyên");
        initialUser.Status.Should().Be("active", "vì Status không nằm trong DTO và phải giữ nguyên");

        _userServiceMock.Verify(x => x.UpdateUserAsync(It.Is<User>(u => u.FullName == "Updated Name")), Times.Once);
    }

    [Fact]
    public async Task UpdateUser_WhenFullPayload_ShouldUpdateAllFields()
    {
        // Arrange
        var initialUser = new User
        {
            UserId = 2,
            Email = "full@example.com",
            FullName = "Old Full Name",
            DateOfBirth = new DateOnly(1990, 1, 1),
            BiologicalSex = "male",
            ActivityLevel = "sedentary",
            GoalType = "maintenance",
            Status = "active"
        };

        _userServiceMock.Setup(x => x.GetUserByIdAsync(2))
            .ReturnsAsync(initialUser);

        var request = new UpdateUserRequestDto
        {
            FullName = "New Full Name",
            DateOfBirth = new DateOnly(2000, 12, 31),
            BiologicalSex = "female",
            ActivityLevel = "very_active",
            GoalType = "bulk"
        };

        // Act
        var result = await _sut.UpdateUser(2, request);

        // Assert
        result.Should().BeOfType<NoContentResult>();
        initialUser.FullName.Should().Be("New Full Name");
        initialUser.DateOfBirth.Should().Be(new DateOnly(2000, 12, 31));
        initialUser.BiologicalSex.Should().Be("female");
        initialUser.ActivityLevel.Should().Be("very_active");
        initialUser.GoalType.Should().Be("bulk");
        initialUser.Email.Should().Be("full@example.com");

        _userServiceMock.Verify(x => x.UpdateUserAsync(initialUser), Times.Once);
    }

    [Fact]
    public async Task UpdateUser_WhenEmptyStringField_ShouldUpdateFieldToEmptyString()
    {
        // Arrange: Edge case kiểm tra chuỗi rỗng "" (khác null)
        var initialUser = new User
        {
            UserId = 3,
            Email = "empty@example.com",
            FullName = "Existing Name",
            BiologicalSex = "male",
            ActivityLevel = "moderate",
            GoalType = "cut",
            DateOfBirth = new DateOnly(1992, 3, 10),
            Status = "active"
        };

        _userServiceMock.Setup(x => x.GetUserByIdAsync(3))
            .ReturnsAsync(initialUser);

        // Gửi FullName là chuỗi rỗng "" và BiologicalSex là chuỗi rỗng ""
        var request = new UpdateUserRequestDto
        {
            FullName = "",
            BiologicalSex = ""
        };

        // Act
        var result = await _sut.UpdateUser(3, request);

        // Assert
        result.Should().BeOfType<NoContentResult>();
        initialUser.FullName.Should().Be("", "vì chuỗi rỗng \"\" != null nên được gán đúng theo semantics cũ");
        initialUser.BiologicalSex.Should().Be("", "vì chuỗi rỗng \"\" != null nên được gán đúng theo semantics cũ");
        initialUser.ActivityLevel.Should().Be("moderate", "vì ActivityLevel = null nên giữ nguyên");
        initialUser.GoalType.Should().Be("cut", "vì GoalType = null nên giữ nguyên");
        initialUser.Email.Should().Be("empty@example.com", "vì Email không bị ảnh hưởng");

        _userServiceMock.Verify(x => x.UpdateUserAsync(initialUser), Times.Once);
    }

    [Fact]
    public async Task UpdateUser_WhenUserNotFound_ShouldReturnNotFound()
    {
        // Arrange
        _userServiceMock.Setup(x => x.GetUserByIdAsync(999))
            .ReturnsAsync((User?)null);

        var request = new UpdateUserRequestDto { FullName = "Ghost" };

        // Act
        var result = await _sut.UpdateUser(999, request);

        // Assert
        result.Should().BeOfType<NotFoundResult>();
        _userServiceMock.Verify(x => x.UpdateUserAsync(It.IsAny<User>()), Times.Never);
    }

    [Fact]
    public async Task GetUser_WhenUserExists_ShouldReturnOkWithUserDto()
    {
        // Arrange
        var user = new User
        {
            UserId = 10,
            Email = "getuser@example.com",
            FullName = "Test User",
            DateOfBirth = new DateOnly(1998, 7, 20),
            BiologicalSex = "female",
            ActivityLevel = "light",
            GoalType = "maintenance",
            Status = "active",
            CreatedAt = new DateTime(2026, 2, 1, 10, 0, 0, DateTimeKind.Utc)
        };

        _userServiceMock.Setup(x => x.GetUserByIdAsync(10))
            .ReturnsAsync(user);

        // Act
        var result = await _sut.GetUser(10);

        // Assert
        var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
        var dto = okResult.Value.Should().BeOfType<UserDto>().Subject;
        dto.UserId.Should().Be(10);
        dto.Email.Should().Be("getuser@example.com");
        dto.FullName.Should().Be("Test User");
        dto.DateOfBirth.Should().Be(new DateOnly(1998, 7, 20));
        dto.BiologicalSex.Should().Be("female");
        dto.ActivityLevel.Should().Be("light");
        dto.GoalType.Should().Be("maintenance");
        dto.Status.Should().Be("active");
        dto.CreatedAt.Should().Be(new DateTime(2026, 2, 1, 10, 0, 0, DateTimeKind.Utc));
    }

    [Fact]
    public async Task GetUser_WhenUserNotFound_ShouldReturnNotFound()
    {
        // Arrange
        _userServiceMock.Setup(x => x.GetUserByIdAsync(404))
            .ReturnsAsync((User?)null);

        // Act
        var result = await _sut.GetUser(404);

        // Assert
        result.Result.Should().BeOfType<NotFoundResult>();
    }

    [Fact]
    public async Task DeleteUser_WhenUserExists_ShouldReturnNoContent()
    {
        // Arrange
        var user = new User { UserId = 5, Email = "delete@example.com" };
        _userServiceMock.Setup(x => x.GetUserByIdAsync(5))
            .ReturnsAsync(user);
        _userServiceMock.Setup(x => x.DeleteUserAsync(5))
            .Returns(Task.CompletedTask);

        // Act
        var result = await _sut.DeleteUser(5);

        // Assert
        result.Should().BeOfType<NoContentResult>();
        _userServiceMock.Verify(x => x.DeleteUserAsync(5), Times.Once);
    }

    [Fact]
    public async Task DeleteUser_WhenUserNotFound_ShouldReturnNotFound()
    {
        // Arrange
        _userServiceMock.Setup(x => x.GetUserByIdAsync(999))
            .ReturnsAsync((User?)null);

        // Act
        var result = await _sut.DeleteUser(999);

        // Assert
        result.Should().BeOfType<NotFoundResult>();
        _userServiceMock.Verify(x => x.DeleteUserAsync(It.IsAny<long>()), Times.Never);
    }
}
