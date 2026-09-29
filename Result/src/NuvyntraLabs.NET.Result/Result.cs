namespace NuvyntraLabs.NET.Result;

/// <summary>A failure with a stable code and a message.</summary>
public class Error
{
    /// <summary>Creates an error.</summary>
    /// <exception cref="ArgumentException"><paramref name="code"/> or <paramref name="message"/> is null or empty.</exception>
    public Error(string code, string message)
    {
        if (string.IsNullOrWhiteSpace(code))
        {
            throw new ArgumentException("Code is required.", nameof(code));
        }

        if (string.IsNullOrWhiteSpace(message))
        {
            throw new ArgumentException("Message is required.", nameof(message));
        }

        Code = code;
        Message = message;
    }

    /// <summary>Stable machine-readable code.</summary>
    public string Code { get; }

    /// <summary>Human-readable message.</summary>
    public string Message { get; }
}

/// <summary>A validation failure tied to one property.</summary>
public sealed class ValidationError : Error
{
    /// <summary>Creates a validation error. <see cref="Error.Code"/> is <c>validation</c>.</summary>
    public ValidationError(string propertyName, string message)
        : base("validation", message)
    {
        if (string.IsNullOrWhiteSpace(propertyName))
        {
            throw new ArgumentException("Property name is required.", nameof(propertyName));
        }

        PropertyName = propertyName;
    }

    /// <summary>Name of the invalid property.</summary>
    public string PropertyName { get; }
}

/// <summary>A missing resource. <see cref="Error.Code"/> is <c>not_found</c>.</summary>
public sealed class NotFoundError : Error
{
    /// <summary>Creates a not-found error.</summary>
    public NotFoundError(string message)
        : base("not_found", message)
    {
    }
}

/// <summary>Success or a failure, with no success value.</summary>
public readonly struct Result
{
    private readonly Error? _error;

    private Result(Error? error, bool isSuccess)
    {
        _error = error;
        IsSuccess = isSuccess;
    }

    /// <summary><see langword="true"/> when the operation succeeded.</summary>
    public bool IsSuccess { get; }

    /// <summary>The failure. Throws when <see cref="IsSuccess"/> is <see langword="true"/>.</summary>
    /// <exception cref="InvalidOperationException">The result succeeded.</exception>
    public Error Error => IsSuccess
        ? throw new InvalidOperationException("Result has no error.")
        : _error!;

    /// <summary>A successful result.</summary>
    public static Result Success() => new(null, true);

    /// <summary>A failed result.</summary>
    /// <exception cref="ArgumentNullException"><paramref name="error"/> is null.</exception>
    public static Result Failure(Error error)
    {
        ArgumentNullException.ThrowIfNull(error);
        return new Result(error, false);
    }

    /// <summary>Maps success and failure to one value.</summary>
    public TResult Match<TResult>(Func<TResult> success, Func<Error, TResult> failure)
    {
        ArgumentNullException.ThrowIfNull(success);
        ArgumentNullException.ThrowIfNull(failure);
        return IsSuccess ? success() : failure(_error!);
    }
}

/// <summary>A success value or a failure.</summary>
/// <typeparam name="T">Type of the success value.</typeparam>
public readonly struct Result<T>
{
    private readonly T? _value;
    private readonly Error? _error;

    private Result(T? value, Error? error, bool isSuccess)
    {
        _value = value;
        _error = error;
        IsSuccess = isSuccess;
    }

    /// <summary><see langword="true"/> when the operation succeeded.</summary>
    public bool IsSuccess { get; }

    /// <summary>The success value. Throws when <see cref="IsSuccess"/> is <see langword="false"/>.</summary>
    /// <exception cref="InvalidOperationException">The result failed.</exception>
    public T Value => IsSuccess
        ? _value!
        : throw new InvalidOperationException("Result has no value.");

    /// <summary>The failure. Throws when <see cref="IsSuccess"/> is <see langword="true"/>.</summary>
    /// <exception cref="InvalidOperationException">The result succeeded.</exception>
    public Error Error => IsSuccess
        ? throw new InvalidOperationException("Result has no error.")
        : _error!;

    /// <summary>A successful result.</summary>
    public static Result<T> Success(T value) => new(value, null, true);

    /// <summary>A failed result.</summary>
    /// <exception cref="ArgumentNullException"><paramref name="error"/> is null.</exception>
    public static Result<T> Failure(Error error)
    {
        ArgumentNullException.ThrowIfNull(error);
        return new Result<T>(default, error, false);
    }

    /// <summary>Maps success and failure to one value.</summary>
    public TResult Match<TResult>(Func<T, TResult> success, Func<Error, TResult> failure)
    {
        ArgumentNullException.ThrowIfNull(success);
        ArgumentNullException.ThrowIfNull(failure);
        return IsSuccess ? success(_value!) : failure(_error!);
    }
}
