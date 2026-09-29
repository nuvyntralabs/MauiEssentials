# NuvyntraLabs.NET.Identifiers

Validate a PAN, a GSTIN checksum, an Aadhaar Verhoeff checksum, or an IBAN.

**Version:** 0.1.0. Not published to nuget.org yet. Do not `dotnet nuget push` from a local clone.

```bash
dotnet add package NuvyntraLabs.NET.Identifiers
```

```csharp
Pan.IsValid("ABCDE1234F");              // true
Gstin.IsValid("27AAPFU0939F1ZV");       // true
Aadhaar.IsValid("2341 2341 2346");      // true
Iban.IsValid("GB82 WEST 1234 5698 7654 32"); // true
```

Each method returns `bool`. None of them throw, and none of them mask. Input is trimmed or space-stripped, then compared in uppercase.

| Method | Accepts |
| --- | --- |
| `Pan.IsValid` | `^[A-Z]{5}[0-9]{4}[A-Z]$`. PAN has no checksum. |
| `Gstin.IsValid` | 15 characters, state `01`–`38`, an embedded PAN, an entity code, `Z`, and the mod-36 checksum. |
| `Aadhaar.IsValid` | 12 digits and a Verhoeff checksum. Spaces are ignored. |
| `Iban.IsValid` | A known country length and a mod-97 checksum of 1. Spaces are ignored. |

The console sample calls every method:

```bash
dotnet run --project samples/Identifiers.Sample
dotnet test NuvyntraLabs.NET.Identifiers.sln
```

Prefer first: `Plugin.Maui.FormValidation` for email, phone, and required fields.

Target frameworks: `net8.0`, `net9.0`, and `net10.0`. No package dependencies. Nullable, trim, and Native AOT compatible.

Author: Niladri Prasad Padhy. License: MIT.
