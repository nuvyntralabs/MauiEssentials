using NuvyntraLabs.NET.Guard;

namespace NuvyntraLabs.NET.Guard.Tests;

public class GuardTests
{
    [Fact]
    public void NotNull_returns_value()
    {
        var request = new object();

        Assert.Same(request, Guard.NotNull(request));
    }

    [Fact]
    public void NotNull_names_the_argument()
    {
        object? request = null;

        ArgumentNullException ex = Assert.Throws<ArgumentNullException>(() => Guard.NotNull(request));

        Assert.Equal("request", ex.ParamName);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void NotEmpty_rejects_blank_strings(string? name)
    {
        ArgumentException ex = Assert.Throws<ArgumentException>(() => Guard.NotEmpty(name));

        Assert.Equal("name", ex.ParamName);
    }

    [Fact]
    public void NotEmpty_returns_the_original_string()
    {
        Assert.Equal("ada", Guard.NotEmpty("ada"));
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void Positive_rejects_non_positive_integers(int amount)
    {
        ArgumentOutOfRangeException ex = Assert.Throws<ArgumentOutOfRangeException>(() => Guard.Positive(amount));

        Assert.Equal("amount", ex.ParamName);
    }

    [Fact]
    public void Positive_accepts_a_positive_decimal()
    {
        Assert.Equal(0.5m, Guard.Positive(0.5m));
    }

    [Theory]
    [InlineData(17)]
    [InlineData(101)]
    public void InRange_rejects_values_outside_inclusive_bounds(int age)
    {
        ArgumentOutOfRangeException ex = Assert.Throws<ArgumentOutOfRangeException>(() => Guard.InRange(age, 18, 100));

        Assert.Equal("age", ex.ParamName);
    }

    [Theory]
    [InlineData(18)]
    [InlineData(100)]
    public void InRange_accepts_inclusive_bounds(int age)
    {
        Assert.Equal(age, Guard.InRange(age, 18, 100));
    }
}
