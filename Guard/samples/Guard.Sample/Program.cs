using NuvyntraLabs.NET.Guard;

object request = Guard.NotNull(new object());
string name = Guard.NotEmpty("ada");
decimal amount = Guard.Positive(12.5m);
int age = Guard.InRange(36, 18, 100);

Console.WriteLine($"{request.GetType().Name} {name} {age} {amount}");
Show(() => Guard.NotNull((object?)null));
Show(() => Guard.NotEmpty(" "));
Show(() => Guard.Positive(0));
Show(() => Guard.InRange(17, 18, 100));

static void Show(Action call)
{
    try
    {
        call();
    }
    catch (ArgumentException ex)
    {
        Console.WriteLine($"{ex.GetType().Name}:{ex.ParamName}");
    }
}
