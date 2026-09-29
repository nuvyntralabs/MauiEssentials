using NuvyntraLabs.NET.TimeKit;

namespace NuvyntraLabs.NET.TimeKit.Tests;

public class TimeKitCoverageTests
{
    [Fact]
    public void Sunday_is_a_weekend()
    {
        var sunday = new DateOnly(2026, 1, 4);

        Assert.True(sunday.IsWeekend());
        Assert.False(WeekendCalendar.Instance.IsBusinessDay(sunday));
    }

    [Fact]
    public void IsBusinessDay_uses_the_supplied_calendar()
    {
        var monday = new DateOnly(2026, 1, 5);
        var calendar = new HolidayCalendar(WeekendCalendar.Instance, [monday]);

        Assert.False(monday.IsBusinessDay(calendar));
        Assert.False(new DateOnly(2026, 1, 3).IsBusinessDay(calendar));
        Assert.True(new DateOnly(2026, 1, 6).IsBusinessDay(calendar));
        Assert.True(monday.IsBusinessDay());
    }

    [Fact]
    public void HolidayCalendar_rejects_null_arguments()
    {
        Assert.Throws<ArgumentNullException>(() => new HolidayCalendar(null!, []));
        Assert.Throws<ArgumentNullException>(() => new HolidayCalendar(WeekendCalendar.Instance, null!));
    }

    [Fact]
    public void AddBusinessDays_throws_when_the_calendar_never_opens()
    {
        var friday = new DateOnly(2026, 1, 2);

        Assert.Throws<InvalidOperationException>(() => friday.AddBusinessDays(1, new ClosedCalendar()));
    }

    [Fact]
    public void EndOfQuarter_covers_the_fourth_quarter()
    {
        Assert.Equal(new DateOnly(2026, 12, 31), new DateOnly(2026, 11, 1).EndOfQuarter());
    }

    [Fact]
    public void ToTimeZone_rejects_a_blank_id()
    {
        var instant = DateTimeOffset.UnixEpoch;

        Assert.Throws<ArgumentException>(() => instant.ToTimeZone(""));
        Assert.Throws<ArgumentException>(() => instant.ToTimeZone(" "));
        Assert.Throws<ArgumentNullException>(() => instant.ToTimeZone(null!));
    }

    private sealed class ClosedCalendar : IBusinessCalendar
    {
        public bool IsBusinessDay(DateOnly day) => false;
    }
}
