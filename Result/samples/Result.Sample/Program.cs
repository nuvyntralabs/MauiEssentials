using NuvyntraLabs.NET.Result;

Result<string> found = Result<string>.Success("ada");
Result<string> missing = Result<string>.Failure(new NotFoundError("User is missing."));
Result<string> invalid = Result<string>.Failure(new ValidationError("Email", "Email is required."));
Result done = Result.Success();
Result failed = Result.Failure(new Error("unavailable", "Service is down."));

Console.WriteLine(found.IsSuccess ? found.Value : found.Error.Message);
Console.WriteLine(missing.Match(_ => "ok", error => error.Code));
Console.WriteLine($"{invalid.Error.Code} {((ValidationError)invalid.Error).PropertyName}");
Console.WriteLine(done.Match(() => "ok", error => error.Message));
Console.WriteLine(failed.Error.Message);
Show(() => _ = found.Error);
Show(() => _ = missing.Value);

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
