using NuvyntraLabs.NET.Result;

namespace NuvyntraLabs.NET.Result.Tests;

public class ResultCoverageTests
{
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData(" ")]
    public void Error_rejects_a_blank_code(string? code)
    {
        Assert.Throws<ArgumentException>(() => new Error(code!, "message"));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData(" ")]
    public void Error_rejects_a_blank_message(string? message)
    {
        Assert.Throws<ArgumentException>(() => new Error("code", message!));
    }

    [Fact]
    public void ValidationError_rejects_a_blank_property()
    {
        Assert.Throws<ArgumentException>(() => new ValidationError(" ", "Email is required."));
    }

    [Fact]
    public void NotFoundError_keeps_the_message()
    {
        var error = new NotFoundError("User is missing.");

        Assert.Equal("not_found", error.Code);
        Assert.Equal("User is missing.", error.Message);
    }

    [Fact]
    public void Result_failure_exposes_the_error_and_matches_it()
    {
        Result result = Result.Failure(new Error("unavailable", "Service is down."));

        Assert.False(result.IsSuccess);
        Assert.Equal("unavailable", result.Error.Code);
        Assert.Equal("down", result.Match(() => "ok", error => "down"));
        Assert.Throws<InvalidOperationException>(() => Result.Success().Error);
    }

    [Fact]
    public void Result_match_rejects_null_delegates()
    {
        Result result = Result.Success();

        Assert.Throws<ArgumentNullException>(() => result.Match(null!, _ => "x"));
        Assert.Throws<ArgumentNullException>(() => result.Match(() => "x", null!));
    }

    [Fact]
    public void Generic_failure_rejects_a_null_error_and_null_match_delegates()
    {
        Result<string> result = Result<string>.Failure(new ValidationError("Email", "Email is required."));

        Assert.IsType<ValidationError>(result.Error);
        Assert.Throws<ArgumentNullException>(() => Result<string>.Failure(null!));
        Assert.Throws<ArgumentNullException>(() => result.Match(null!, _ => "x"));
        Assert.Throws<ArgumentNullException>(() => result.Match(_ => "x", null!));
    }

    [Fact]
    public void Success_can_hold_a_null_value()
    {
        Result<string?> result = Result<string?>.Success(null);

        Assert.True(result.IsSuccess);
        Assert.Null(result.Value);
    }
}
