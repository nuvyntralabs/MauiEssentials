using NuvyntraLabs.NET.TimeKit;

namespace NuvyntraLabs.NET.TimeKit.Tests;

public class TimeKitTests
{
    [Fact]
    public void Saturday_is_a_weekend()
    {
        var saturday = new DateOnly(2026, 1, 3);

        Assert.True(saturday.IsWeekend());
        Assert.False(saturday.IsBusinessDay());
    }

    [Fact]
    public void Friday_is_a_business_day()
    {
        var friday = new DateOnly(2026, 1, 2);

        Assert.False(friday.IsWeekend());
        Assert.True(friday.IsBusinessDay());
    }

    [Fact]
    public void AddBusinessDays_skips_the_weekend()
    {
        var friday = new DateOnly(2026, 1, 2);

        Assert.Equal(new DateOnly(2026, 1, 9), friday.AddBusinessDays(5));
    }

    [Fact]
    public void AddBusinessDays_zero_keeps_a_weekend()
    {
        var saturday = new DateOnly(2026, 1, 3);

        Assert.Equal(saturday, saturday.AddBusinessDays(0));
    }

    [Fact]
    public void AddBusinessDays_walks_backward()
    {
        var monday = new DateOnly(2026, 1, 5);

        Assert.Equal(new DateOnly(2026, 1, 2), monday.AddBusinessDays(-1));
    }

    [Fact]
    public void HolidayCalendar_skips_a_holiday()
    {
        var friday = new DateOnly(2026, 1, 2);
        var calendar = new HolidayCalendar(WeekendCalendar.Instance, [new DateOnly(2026, 1, 5)]);

        Assert.Equal(new DateOnly(2026, 1, 6), friday.AddBusinessDays(1, calendar));
    }

    [Fact]
    public void EndOfQuarter_uses_calendar_quarters()
    {
        Assert.Equal(new DateOnly(2026, 3, 31), new DateOnly(2026, 2, 15).EndOfQuarter());
        Assert.Equal(new DateOnly(2026, 6, 30), new DateOnly(2026, 4, 1).EndOfQuarter());
    }

    [Fact]
    public void StartOfMonth_is_the_first()
    {
        Assert.Equal(new DateOnly(2026, 2, 1), new DateOnly(2026, 2, 15).StartOfMonth());
    }

    [Theory]
    [InlineData("2026-01-15T00:00:00Z")]
    [InlineData("2026-07-15T00:00:00Z")]
    public void Kolkata_stays_five_hours_thirty_minutes_ahead(string instant)
    {
        var value = DateTimeOffset.Parse(instant);

        DateTimeOffset local = value.ToTimeZone("Asia/Kolkata");

        Assert.Equal(TimeSpan.FromHours(5.5), local.Offset);
    }

    [Fact]
    public void ToUnixTimestamp_matches_the_bcl()
    {
        var value = new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);

        Assert.Equal(value.ToUnixTimeSeconds(), value.ToUnixTimestamp());
    }

    [Fact]
    public void Unknown_zone_throws()
    {
        var value = DateTimeOffset.UnixEpoch;

        Assert.Throws<TimeZoneNotFoundException>(() => value.ToTimeZone("Not/AZone"));
    }
}
