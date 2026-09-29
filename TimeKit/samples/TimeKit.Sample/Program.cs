using NuvyntraLabs.NET.TimeKit;

var friday = new DateOnly(2026, 1, 2);
var saturday = new DateOnly(2026, 1, 3);
var holidays = new HolidayCalendar(WeekendCalendar.Instance, [new DateOnly(2026, 1, 5)]);
var instant = new DateTimeOffset(2026, 1, 15, 0, 0, 0, TimeSpan.Zero);

Console.WriteLine($"{saturday.IsWeekend()} {friday.IsBusinessDay()} {friday.IsBusinessDay(holidays)}");
Console.WriteLine(friday.AddBusinessDays(5).ToString("yyyy-MM-dd"));
Console.WriteLine(saturday.AddBusinessDays(0).ToString("yyyy-MM-dd"));
Console.WriteLine(friday.AddBusinessDays(1, holidays).ToString("yyyy-MM-dd"));
Console.WriteLine(new DateOnly(2026, 1, 5).AddBusinessDays(-1).ToString("yyyy-MM-dd"));
Console.WriteLine(friday.StartOfMonth().ToString("yyyy-MM-dd"));
Console.WriteLine(new DateOnly(2026, 2, 15).EndOfQuarter().ToString("yyyy-MM-dd"));
Console.WriteLine(instant.ToUnixTimestamp());
Console.WriteLine(instant.ToTimeZone("Asia/Kolkata").Offset);
Show(() => instant.ToTimeZone("Not/AZone"));
Show(() => friday.AddBusinessDays(1, new ClosedCalendar()));

static void Show(Action call)
{
    try
    {
        call();
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.GetType().Name);
    }
}

sealed class ClosedCalendar : IBusinessCalendar
{
    public bool IsBusinessDay(DateOnly day) => false;
}
