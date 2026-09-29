using System.Numerics;
using System.Runtime.CompilerServices;

namespace NuvyntraLabs.NET.Guard;

/// <summary>
/// Rejects null, empty, non-positive, and out-of-range arguments at a public boundary.
/// </summary>
public static class Guard
{
    /// <summary>Returns <paramref name="value"/> when it is not null.</summary>
    /// <exception cref="ArgumentNullException"><paramref name="value"/> is null.</exception>
    public static T NotNull<T>(
        T? value,
        [CallerArgumentExpression(nameof(value))] string? paramName = null)
        where T : class
    {
        ArgumentNullException.ThrowIfNull(value, paramName);
        return value;
    }

    /// <summary>Returns <paramref name="value"/> when it contains a non-whitespace character.</summary>
    /// <exception cref="ArgumentException"><paramref name="value"/> is null, empty, or whitespace.</exception>
    public static string NotEmpty(
        string? value,
        [CallerArgumentExpression(nameof(value))] string? paramName = null)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            throw new ArgumentException("Value cannot be empty or whitespace.", paramName);
        }

        return value;
    }

    /// <summary>Returns <paramref name="value"/> when it is greater than zero.</summary>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="value"/> is less than or equal to zero.</exception>
    public static T Positive<T>(
        T value,
        [CallerArgumentExpression(nameof(value))] string? paramName = null)
        where T : INumber<T>
    {
        if (value.CompareTo(T.Zero) <= 0)
        {
            throw new ArgumentOutOfRangeException(paramName, value, "Value must be positive.");
        }

        return value;
    }

    /// <summary>Returns <paramref name="value"/> when it is inside the inclusive range.</summary>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="value"/> is outside <paramref name="min"/> and <paramref name="max"/>.</exception>
    public static T InRange<T>(
        T value,
        T min,
        T max,
        [CallerArgumentExpression(nameof(value))] string? paramName = null)
        where T : IComparable<T>
    {
        if (value.CompareTo(min) < 0 || value.CompareTo(max) > 0)
        {
            throw new ArgumentOutOfRangeException(paramName, value, $"Value must be between {min} and {max}.");
        }

        return value;
    }
}
