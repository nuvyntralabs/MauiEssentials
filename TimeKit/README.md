# NuvyntraLabs.NET.TimeKit

Add business days, find month and quarter bounds, and convert a `DateTimeOffset` to an IANA time zone.

**Version:** 0.1.0. Not published to nuget.org yet. Do not `dotnet nuget push` from a local clone.

```bash
dotnet add package NuvyntraLabs.NET.TimeKit
```

```csharp
date.IsWeekend();
date.IsBusinessDay();
date.IsBusinessDay(calendar);
date.AddBusinessDays(5);
date.AddBusinessDays(-1);
date.AddBusinessDays(1, calendar);
date.StartOfMonth();
date.EndOfQuarter();
instant.ToUnixTimestamp();
instant.ToTimeZone("Asia/Kolkata");
```

`IsWeekend` is Saturday and Sunday. It does not consult a calendar. A different weekend is an `IBusinessCalendar`.

| Type | Rule |
| --- | --- |
| `WeekendCalendar` | Saturday and Sunday are closed. This is the default. |
| `HolidayCalendar` | Wraps another calendar and removes a host-supplied set of `DateOnly` holidays. |

`AddBusinessDays` does not count the start date. `0` returns the same date, including a weekend. A negative count walks backward. A calendar that never opens throws `InvalidOperationException`.

`StartOfMonth` and `EndOfQuarter` use calendar quarters (Jan–Mar, Apr–Jun, Jul–Sep, Oct–Dec). `ToTimeZone` calls `TimeZoneInfo.FindSystemTimeZoneById`. An unknown id throws `TimeZoneNotFoundException`. There is no holiday database and no `DateTime` overload.

The console sample calls every method:

```bash
dotnet run --project samples/TimeKit.Sample
dotnet test NuvyntraLabs.NET.TimeKit.sln
```

Prefer first: [NodaTime](https://nodatime.org/) when the host needs a chronology.

Target frameworks: `net8.0`, `net9.0`, and `net10.0`. No package dependencies. Nullable, trim, and Native AOT compatible.

Author: Niladri Prasad Padhy. License: MIT.
