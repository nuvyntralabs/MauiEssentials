# NuvyntraLabs.NET.Result

Return a success value or a typed error without throwing.

**Version:** 0.1.0. Not published to nuget.org yet. Do not `dotnet nuget push` from a local clone.

```bash
dotnet add package NuvyntraLabs.NET.Result
```

```csharp
Result<User> found = Result<User>.Success(user);
Result<User> missing = Result<User>.Failure(new NotFoundError("User is missing."));
Result<User> invalid = Result<User>.Failure(new ValidationError("Email", "Email is required."));
Result done = Result.Success();
Result failed = Result.Failure(new Error("unavailable", "Service is down."));

string label = found.Match(value => value.Name, error => error.Code);
```

`Value` throws `InvalidOperationException` on failure. `Error` throws on success. `Failure(null)` throws `ArgumentNullException`. `Match` is the only functional method. There is no `Map`, `Bind`, or LINQ operator.

| Type | Role |
| --- | --- |
| `Result<T>` | A success value or an `Error`. |
| `Result` | Success or an `Error`, with no value. |
| `Error` | A required `Code` and `Message`. |
| `ValidationError` | Code `validation`, plus a property name. |
| `NotFoundError` | Code `not_found`. |

A page checks `IsSuccess`. This package does not ship an ASP.NET Core ProblemDetails adapter.

The console sample calls every type:

```bash
dotnet run --project samples/Result.Sample
dotnet test NuvyntraLabs.NET.Result.sln
```

Prefer first: [ErrorOr](https://github.com/amantinband/error-or) when the host wants a larger result library.

Target frameworks: `net8.0`, `net9.0`, and `net10.0`. No package dependencies. Nullable, trim, and Native AOT compatible.

Author: Niladri Prasad Padhy. License: MIT.
