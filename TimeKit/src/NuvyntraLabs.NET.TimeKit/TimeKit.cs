namespace NuvyntraLabs.NET.TimeKit;

/// <summary>Decides which civil dates count as business days.</summary>
public interface IBusinessCalendar
{
    /// <summary>Returns <see langword="true"/> when <paramref name="day"/> is a business day.</summary>
    bool IsBusinessDay(DateOnly day);
}

/// <summary>Saturday and Sunday are not business days.</summary>
public sealed class WeekendCalendar : IBusinessCalendar
{
    /// <summary>Shared Saturday/Sunday calendar.</summary>
    public static WeekendCalendar Instance { get; } = new();

    /// <inheritdoc />
    public bool IsBusinessDay(DateOnly day) =>
        day.DayOfWeek is not DayOfWeek.Saturday and not DayOfWeek.Sunday;
}

/// <summary>Removes a host-supplied set of holidays from an inner calendar.</summary>
public sealed class HolidayCalendar : IBusinessCalendar
{
    private readonly IBusinessCalendar _inner;
    private readonly HashSet<DateOnly> _holidays;

    /// <summary>Creates a calendar that treats <paramref name="holidays"/> as closed.</summary>
    /// <exception cref="ArgumentNullException"><paramref name="inner"/> or <paramref name="holidays"/> is null.</exception>
    public HolidayCalendar(IBusinessCalendar inner, IEnumerable<DateOnly> holidays)
    {
        ArgumentNullException.ThrowIfNull(inner);
        ArgumentNullException.ThrowIfNull(holidays);
        _inner = inner;
        _holidays = new HashSet<DateOnly>(holidays);
    }

    /// <inheritdoc />
    public bool IsBusinessDay(DateOnly day) =>
        _inner.IsBusinessDay(day) && !_holidays.Contains(day);
}

/// <summary>Business-day and calendar-bound helpers for <see cref="DateOnly"/>.</summary>
public static class DateOnlyExtensions
{
    /// <summary>Saturday or Sunday. This does not consult <see cref="IBusinessCalendar"/>.</summary>
    public static bool IsWeekend(this DateOnly date) =>
        date.DayOfWeek is DayOfWeek.Saturday or DayOfWeek.Sunday;

    /// <summary>
    /// <see langword="true"/> when <paramref name="date"/> is a business day.
    /// The default calendar is <see cref="WeekendCalendar"/>.
    /// </summary>
    public static bool IsBusinessDay(this DateOnly date, IBusinessCalendar? calendar = null) =>
        (calendar ?? WeekendCalendar.Instance).IsBusinessDay(date);

    /// <summary>
    /// Moves <paramref name="days"/> business days. The start date is not counted.
    /// Zero returns <paramref name="date"/>. A negative count walks backward.
    /// </summary>
    /// <exception cref="InvalidOperationException">The calendar has no business day in range.</exception>
    public static DateOnly AddBusinessDays(this DateOnly date, int days, IBusinessCalendar? calendar = null)
    {
        if (days == 0)
        {
            return date;
        }

        IBusinessCalendar active = calendar ?? WeekendCalendar.Instance;
        int step = days > 0 ? 1 : -1;
        int remaining = Math.Abs(days);
        int walked = 0;
        int limit = (remaining * 366) + 7;
        DateOnly cursor = date;
        while (remaining > 0)
        {
            if (++walked > limit)
            {
                throw new InvalidOperationException("Calendar has no business day in range.");
            }

            cursor = cursor.AddDays(step);
            if (active.IsBusinessDay(cursor))
            {
                remaining--;
            }
        }

        return cursor;
    }

    /// <summary>The first day of the month containing <paramref name="date"/>.</summary>
    public static DateOnly StartOfMonth(this DateOnly date) => new(date.Year, date.Month, 1);

    /// <summary>The last day of the calendar quarter containing <paramref name="date"/>.</summary>
    public static DateOnly EndOfQuarter(this DateOnly date)
    {
        int endMonth = ((date.Month - 1) / 3 + 1) * 3;
        return new DateOnly(date.Year, endMonth, DateTime.DaysInMonth(date.Year, endMonth));
    }
}

/// <summary>Unix time and IANA zone conversion for <see cref="DateTimeOffset"/>.</summary>
public static class DateTimeOffsetExtensions
{
    /// <summary>Seconds since the Unix epoch, UTC.</summary>
    public static long ToUnixTimestamp(this DateTimeOffset value) => value.ToUnixTimeSeconds();

    /// <summary>Converts <paramref name="value"/> to an IANA time zone such as <c>Asia/Kolkata</c>.</summary>
    /// <exception cref="TimeZoneNotFoundException"><paramref name="timeZoneId"/> is unknown.</exception>
    /// <exception cref="ArgumentException"><paramref name="timeZoneId"/> is null or empty.</exception>
    public static DateTimeOffset ToTimeZone(this DateTimeOffset value, string timeZoneId)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(timeZoneId);
        TimeZoneInfo zone = TimeZoneInfo.FindSystemTimeZoneById(timeZoneId);
        return TimeZoneInfo.ConvertTime(value, zone);
    }
}
