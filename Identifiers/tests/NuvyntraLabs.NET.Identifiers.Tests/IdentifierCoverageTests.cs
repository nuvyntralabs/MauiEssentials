using NuvyntraLabs.NET.Identifiers;

namespace NuvyntraLabs.NET.Identifiers.Tests;

public class IdentifierCoverageTests
{
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData("ABCDE12345")]
    public void Pan_rejects_blank_and_wrong_shapes(string? value)
    {
        Assert.False(Pan.IsValid(value));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("27AAPFU0939F1Z")]
    [InlineData("27AAPFU0939F1YV")]
    [InlineData("00AAPFU0939F1ZV")]
    [InlineData("39AAPFU0939F1ZV")]
    [InlineData("27123451234F1ZV")]
    [InlineData("27AAPFU0939F-ZV")]
    [InlineData("  27AAPFU0939F1Z5  ")]
    public void Gstin_rejects_each_failed_check(string? value)
    {
        Assert.False(Gstin.IsValid(value));
    }

    [Theory]
    [InlineData("01AAPFU0939F1Z9")]
    [InlineData("38AAPFU0939F1ZS")]
    [InlineData("  27aapfu0939f1zv  ")]
    public void Gstin_accepts_state_bounds_and_lowercase_input(string value)
    {
        Assert.True(Gstin.IsValid(value));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("23412341234")]
    [InlineData("2341234123467")]
    [InlineData("23412341234A")]
    public void Aadhaar_rejects_blank_wrong_length_and_letters(string? value)
    {
        Assert.False(Aadhaar.IsValid(value));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("GB82")]
    [InlineData("XX82WEST12345698765432")]
    [InlineData("GB82WEST1234569876543")]
    [InlineData("GB82WEST1234569876543!")]
    [InlineData("gb82west12345698765433")]
    public void Iban_rejects_blank_unknown_short_and_non_alphanumeric_values(string? value)
    {
        Assert.False(Iban.IsValid(value));
    }

    [Fact]
    public void Iban_accepts_a_lowercase_valid_number()
    {
        Assert.True(Iban.IsValid("gb82west12345698765432"));
    }
}
