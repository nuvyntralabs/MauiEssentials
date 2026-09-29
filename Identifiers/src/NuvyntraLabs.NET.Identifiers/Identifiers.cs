using System.Text.RegularExpressions;

namespace NuvyntraLabs.NET.Identifiers;

/// <summary>Indian Permanent Account Number format. PAN has no checksum.</summary>
public static partial class Pan
{
    /// <summary>Returns <see langword="true"/> when <paramref name="value"/> matches <c>^[A-Z]{5}[0-9]{4}[A-Z]$</c> after ASCII uppercasing.</summary>
    public static bool IsValid(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        return Pattern().IsMatch(value.Trim().ToUpperInvariant());
    }

    [GeneratedRegex("^[A-Z]{5}[0-9]{4}[A-Z]$", RegexOptions.CultureInvariant)]
    private static partial Regex Pattern();
}

/// <summary>Indian GSTIN, including the mod-36 checksum.</summary>
public static class Gstin
{
    private const string Alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    /// <summary>
    /// Returns <see langword="true"/> for a 15-character GSTIN: state <c>01</c>–<c>38</c>, embedded PAN, entity code, <c>Z</c>, and checksum.
    /// </summary>
    public static bool IsValid(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        string gstin = value.Trim().ToUpperInvariant();
        if (gstin.Length != 15 || gstin[13] != 'Z')
        {
            return false;
        }

        if (!int.TryParse(gstin.AsSpan(0, 2), out int state) || state is < 1 or > 38)
        {
            return false;
        }

        if (!Pan.IsValid(gstin.Substring(2, 10)))
        {
            return false;
        }

        char entity = gstin[12];
        if (!char.IsAsciiLetterOrDigit(entity))
        {
            return false;
        }

        return gstin[14] == CheckCharacter(gstin.AsSpan(0, 14));
    }

    private static char CheckCharacter(ReadOnlySpan<char> body)
    {
        int factor = 2;
        int sum = 0;
        for (int i = body.Length - 1; i >= 0; i--)
        {
            int codePoint = Alphabet.IndexOf(body[i]);
            if (codePoint < 0)
            {
                return '\0';
            }

            int digit = factor * codePoint;
            factor = factor == 2 ? 1 : 2;
            digit = (digit / 36) + (digit % 36);
            sum += digit;
        }

        return Alphabet[(36 - (sum % 36)) % 36];
    }
}

/// <summary>Aadhaar number, including the Verhoeff checksum.</summary>
public static class Aadhaar
{
    private static readonly int[,] Multiplication =
    {
        { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 },
        { 1, 2, 3, 4, 0, 6, 7, 8, 9, 5 },
        { 2, 3, 4, 0, 1, 7, 8, 9, 5, 6 },
        { 3, 4, 0, 1, 2, 8, 9, 5, 6, 7 },
        { 4, 0, 1, 2, 3, 9, 5, 6, 7, 8 },
        { 5, 9, 8, 7, 6, 0, 4, 3, 2, 1 },
        { 6, 5, 9, 8, 7, 1, 0, 4, 3, 2 },
        { 7, 6, 5, 9, 8, 2, 1, 0, 4, 3 },
        { 8, 7, 6, 5, 9, 3, 2, 1, 0, 4 },
        { 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 },
    };

    private static readonly int[,] Permutation =
    {
        { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 },
        { 1, 5, 7, 6, 2, 8, 3, 0, 9, 4 },
        { 5, 8, 0, 3, 7, 9, 6, 1, 4, 2 },
        { 8, 9, 1, 6, 0, 4, 3, 5, 2, 7 },
        { 9, 4, 5, 3, 1, 2, 6, 8, 7, 0 },
        { 4, 2, 8, 6, 5, 7, 3, 9, 0, 1 },
        { 2, 7, 9, 3, 8, 0, 6, 4, 1, 5 },
        { 7, 0, 4, 6, 9, 1, 3, 2, 5, 8 },
    };

    /// <summary>Returns <see langword="true"/> for 12 digits with a valid Verhoeff checksum. Spaces are stripped first.</summary>
    public static bool IsValid(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        Span<char> digits = stackalloc char[12];
        int count = 0;
        foreach (char character in value)
        {
            if (character == ' ')
            {
                continue;
            }

            if (character is < '0' or > '9' || count == 12)
            {
                return false;
            }

            digits[count++] = character;
        }

        if (count != 12)
        {
            return false;
        }

        int checksum = 0;
        for (int index = 0; index < 12; index++)
        {
            int digit = digits[11 - index] - '0';
            checksum = Multiplication[checksum, Permutation[index % 8, digit]];
        }

        return checksum == 0;
    }
}

/// <summary>International Bank Account Number, including country length and mod-97.</summary>
public static class Iban
{
    private static readonly Dictionary<string, int> Lengths = new(StringComparer.Ordinal)
    {
        ["AD"] = 24, ["AE"] = 23, ["AL"] = 28, ["AT"] = 20, ["AZ"] = 28,
        ["BA"] = 20, ["BE"] = 16, ["BG"] = 22, ["BH"] = 22, ["BR"] = 29, ["BY"] = 28,
        ["CH"] = 21, ["CR"] = 22, ["CY"] = 28, ["CZ"] = 24,
        ["DE"] = 22, ["DK"] = 18, ["DO"] = 28,
        ["EE"] = 20, ["EG"] = 29, ["ES"] = 24,
        ["FI"] = 18, ["FO"] = 18, ["FR"] = 27,
        ["GB"] = 22, ["GE"] = 22, ["GI"] = 23, ["GL"] = 18, ["GR"] = 27, ["GT"] = 28,
        ["HR"] = 21, ["HU"] = 28,
        ["IE"] = 22, ["IL"] = 23, ["IQ"] = 23, ["IS"] = 26, ["IT"] = 27,
        ["JO"] = 30,
        ["KW"] = 30, ["KZ"] = 20,
        ["LB"] = 28, ["LC"] = 32, ["LI"] = 21, ["LT"] = 20, ["LU"] = 20, ["LV"] = 21,
        ["MC"] = 27, ["MD"] = 24, ["ME"] = 22, ["MK"] = 19, ["MR"] = 27, ["MT"] = 31, ["MU"] = 30,
        ["NL"] = 18, ["NO"] = 15,
        ["PK"] = 24, ["PL"] = 28, ["PS"] = 29, ["PT"] = 25,
        ["QA"] = 29,
        ["RO"] = 24, ["RS"] = 22,
        ["SA"] = 24, ["SC"] = 31, ["SE"] = 24, ["SI"] = 19, ["SK"] = 24, ["SM"] = 27, ["ST"] = 25,
        ["TL"] = 23, ["TN"] = 24, ["TR"] = 26,
        ["UA"] = 29,
        ["VA"] = 22, ["VG"] = 24,
        ["XK"] = 20,
    };

    /// <summary>Returns <see langword="true"/> when the country length matches and the mod-97 checksum is 1. Spaces are ignored.</summary>
    public static bool IsValid(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        string iban = value.Replace(" ", "", StringComparison.Ordinal).ToUpperInvariant();
        if (iban.Length < 5 || !Lengths.TryGetValue(iban[..2], out int expected) || iban.Length != expected)
        {
            return false;
        }

        foreach (char character in iban)
        {
            if (!char.IsAsciiLetterOrDigit(character))
            {
                return false;
            }
        }

        string rearranged = string.Concat(iban.AsSpan(4), iban.AsSpan(0, 4));
        int mod = 0;
        foreach (char character in rearranged)
        {
            if (character is >= '0' and <= '9')
            {
                mod = ((mod * 10) + (character - '0')) % 97;
            }
            else
            {
                int converted = character - 'A' + 10;
                mod = ((mod * 10) + (converted / 10)) % 97;
                mod = ((mod * 10) + (converted % 10)) % 97;
            }
        }

        return mod == 1;
    }
}
