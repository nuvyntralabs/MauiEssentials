using NuvyntraLabs.NET.Identifiers;

namespace NuvyntraLabs.NET.Identifiers.Tests;

public class IdentifierTests
{
    [Theory]
    [InlineData("ABCDE1234F", true)]
    [InlineData("abcde1234f", true)]
    [InlineData("ABCDE1234", false)]
    [InlineData(null, false)]
    public void Pan_checks_the_format(string? value, bool expected)
    {
        Assert.Equal(expected, Pan.IsValid(value));
    }

    [Theory]
    [InlineData("27AAPFU0939F1ZV", true)]
    [InlineData("29AAGCB7383J1Z4", true)]
    [InlineData("27AAPFU0939F1Z5", false)]
    [InlineData("99AAPFU0939F1ZV", false)]
    public void Gstin_checks_the_checksum(string value, bool expected)
    {
        Assert.Equal(expected, Gstin.IsValid(value));
    }

    [Theory]
    [InlineData("234123412346", true)]
    [InlineData("2341 2341 2346", true)]
    [InlineData("234123412347", false)]
    public void Aadhaar_checks_verhoeff(string value, bool expected)
    {
        Assert.Equal(expected, Aadhaar.IsValid(value));
    }

    [Theory]
    [InlineData("GB82WEST12345698765432", true)]
    [InlineData("DE89 3704 0044 0532 0130 00", true)]
    [InlineData("GB82WEST12345698765433", false)]
    [InlineData("XX82WEST12345698765432", false)]
    public void Iban_checks_length_and_mod97(string value, bool expected)
    {
        Assert.Equal(expected, Iban.IsValid(value));
    }
}
