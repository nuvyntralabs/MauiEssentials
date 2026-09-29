using NuvyntraLabs.NET.Identifiers;

Console.WriteLine(Pan.IsValid("ABCDE1234F"));
Console.WriteLine(Pan.IsValid(" "));
Console.WriteLine(Gstin.IsValid("27AAPFU0939F1ZV"));
Console.WriteLine(Gstin.IsValid("27AAPFU0939F1Z5"));
Console.WriteLine(Aadhaar.IsValid("2341 2341 2346"));
Console.WriteLine(Aadhaar.IsValid("234123412347"));
Console.WriteLine(Iban.IsValid("GB82 WEST 1234 5698 7654 32"));
Console.WriteLine(Iban.IsValid("DE89370400440532013000"));
Console.WriteLine(Iban.IsValid("GB82WEST12345698765433"));
