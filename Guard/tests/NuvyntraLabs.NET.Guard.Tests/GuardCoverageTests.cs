using NuvyntraLabs.NET.Guard;

namespace NuvyntraLabs.NET.Guard.Tests;

public class GuardCoverageTests
{
    [Fact]
    public void Positive_rejects_a_negative_decimal()
    {
        decimal amount = -0.1m;
        ArgumentOutOfRangeException ex = Assert.Throws<ArgumentOutOfRangeException>(() => Guard.Positive(amount));

        Assert.Equal("amount", ex.ParamName);
    }

    [Fact]
    public void InRange_accepts_a_value_strictly_inside_the_bounds()
    {
        Assert.Equal(50, Guard.InRange(50, 18, 100));
    }
}
