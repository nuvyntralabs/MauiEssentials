# NuvyntraLabs.NET.Guard

Reject null, empty, non-positive, and out-of-range arguments at a public boundary.

**Version:** 0.1.0. Not published to nuget.org yet. Do not `dotnet nuget push` from a local clone.

```bash
dotnet add package NuvyntraLabs.NET.Guard
```

```csharp
object request = Guard.NotNull(request);
string name = Guard.NotEmpty(name);
decimal amount = Guard.Positive(amount);
int age = Guard.InRange(age, 18, 100);
```

Each method returns the same value when the check passes. The exception names the argument through `CallerArgumentExpression`.

| Method | Throws |
| --- | --- |
| `NotNull` | `ArgumentNullException` |
| `NotEmpty` | `ArgumentException` for null, empty, or whitespace |
| `Positive` | `ArgumentOutOfRangeException` when the number is not greater than zero |
| `InRange` | `ArgumentOutOfRangeException` when the value is outside the inclusive bounds |

The console sample calls every method, including the rejection paths:

```bash
dotnet run --project samples/Guard.Sample
dotnet test NuvyntraLabs.NET.Guard.sln
```

Prefer first: `ArgumentNullException.ThrowIfNull`, then [Ardalis.GuardClauses](https://github.com/ardalis/GuardClauses).

Target frameworks: `net8.0`, `net9.0`, and `net10.0`. No package dependencies. Nullable, trim, and Native AOT compatible.

Author: Niladri Prasad Padhy. License: MIT.
