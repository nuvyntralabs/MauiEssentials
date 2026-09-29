using NuvyntraLabs.NET.Result;

namespace NuvyntraLabs.NET.Result.Tests;

public class ResultTests
{
    [Fact]
    public void Success_exposes_the_value()
    {
        Result<string> result = Result<string>.Success("ada");

        Assert.True(result.IsSuccess);
        Assert.Equal("ada", result.Value);
        Assert.Equal("ada", result.Match(value => value, error => error.Code));
    }

    [Fact]
    public void Failure_exposes_the_error()
    {
        Result<string> result = Result<string>.Failure(new NotFoundError("User is missing."));

        Assert.False(result.IsSuccess);
        Assert.Equal("not_found", result.Error.Code);
        Assert.Equal("missing", result.Match(_ => "ok", error => "missing"));
        Assert.Throws<InvalidOperationException>(() => result.Value);
    }

    [Fact]
    public void Success_has_no_error()
    {
        Result<int> result = Result<int>.Success(1);

        Assert.Throws<InvalidOperationException>(() => result.Error);
    }

    [Fact]
    public void Result_without_a_value_matches_success()
    {
        Result result = Result.Success();

        Assert.True(result.IsSuccess);
        Assert.Equal("ok", result.Match(() => "ok", error => error.Message));
    }

    [Fact]
    public void ValidationError_uses_the_validation_code()
    {
        var error = new ValidationError("Email", "Email is required.");

        Assert.Equal("validation", error.Code);
        Assert.Equal("Email", error.PropertyName);
    }

    [Fact]
    public void Failure_rejects_a_null_error()
    {
        Assert.Throws<ArgumentNullException>(() => Result.Failure(null!));
    }
}
