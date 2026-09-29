# Shared utilities — design plan

**Status:** Hub submodules at 0.1.0 (`Guard/`, `DataMask/`, `TimeKit/`, `Identifiers/`, `Result/`, `ObjectKit/`). Each is its own repository. Not published.  
**Catalog:** [MauiEssentials](https://github.com/nuvyntralabs/MauiEssentials) — related products, same standing as UIKit and NuvexaDB. Shared `net8.0`, `net9.0`, and `net10.0` class libraries a MAUI host references directly. These are not `Plugin.Maui.*` packages and they do not register with the MAUI builder.  
**Author:** Niladri Prasad Padhy  
**License:** MIT  
**TFM:** `net8.0`, `net9.0`, `net10.0`  
**First publish:** `0.1.0` after Wave 1 tests are green. Pipeline-only.

This plan turns the utility-library list into a ship order. Wave 1 is three small products. Later waves stay separate repositories. The short names in discussion (`DataMask`, `TimeKit`, `Guard`) are product names. NuGet ids stay on the catalog prefix.

## 1. Problem

Application code keeps reimplementing the same four helpers:

| Host still writes | Why the framework is not enough |
| --- | --- |
| Redact a phone, PAN, card, or connection string before it hits a log | `Microsoft.Extensions.Compliance.Redaction` wants a data-classification taxonomy. It does not know PAN, Aadhaar, or GSTIN shapes. |
| Add five business days, or convert `DateTimeOffset` to `Asia/Kolkata` | BCL date arithmetic is calendar-naive. NodaTime is the right library when the app needs a chronology. Most hosts need a weekend rule and a holiday set. |
| Reject null, empty, and out-of-range arguments at a public boundary | `ArgumentNullException.ThrowIfNull` covers null. Range and empty-string checks are still copied per method. |
| Check a GSTIN, Aadhaar, or IBAN checksum | Data annotations check shape. The checksums are easy to get wrong and are not in the BCL. |

Everything else on the original list is either already a one-liner in .NET 10, or already owned by a library this catalog should keep recommending.

## 2. Positioning

These packages sit in the MauiEssentials catalog as related products. DataMask answers how a log line hides a PAN. A MAUI host adds the one package that matches the requirement. Plugins do not take a dependency on them.

The differentiator is the set of formats and calendars a .NET 10 host in this ecosystem actually touches: Indian tax and identity numbers, card and connection-string redaction for logs, and business-day arithmetic with an explicit calendar. Zero package dependencies, nullable reference types, and a trim/AOT-clean public surface are the packaging bar, not a second product.

Usual alternatives stay in the README of each package:

| Need | Prefer first | Ship a Nuvyntra package when |
| --- | --- | --- |
| Argument checks | `ArgumentNullException.ThrowIfNull`, then [Ardalis.GuardClauses](https://github.com/ardalis/GuardClauses) | The host wants the four checks below and no extra guard vocabulary |
| Log redaction | `Microsoft.Extensions.Compliance.Redaction` | The call site has a string and a known kind (phone, PAN, connection string) |
| Calendars and time zones | [NodaTime](https://nodatime.org/) | The host wants business days and an IANA zone, and does not want a chronology library |
| Slugs, humanized durations, pluralization | [Humanizer](https://github.com/Humanizr/Humanizer) | Do not ship |
| Object mapping | [Mapperly](https://github.com/riok/mapperly) | Do not ship |
| Result / error unions | [ErrorOr](https://github.com/amantinband/error-or), [FluentResults](https://github.com/altmann/FluentResults) | Wave 2 only if those packages are heavier than the host will take |
| CLI tables and prompts | [Spectre.Console](https://spectreconsole.net/) | Do not ship |
| Fake data | [Bogus](https://github.com/bchavez/Bogus) | Do not ship |
| Validation framework | `Plugin.Maui.FormValidation`, FluentValidation, DataAnnotations | Checksums only, as Identifiers in Wave 2. Email, phone, and required stay on FormValidation. |

## 3. Locked decisions

1. **One problem, one repository, one NuGet id.** Guard, DataMask, and TimeKit are three products. Each is a git repository and a MauiEssentials submodule, same model as UIKit.
2. **No umbrella package.** There is no `Nuvyntra.Toolkit`, no `NuvyntraLabs.Toolkit`, and no meta-package that `PackageReference`s the others. The docs site already uses “toolkits” for Nuvyn, MauiDev, Pulse, and NuvLoc. A utilities meta-package would also fight the catalog rule that a host installs the package that matches the requirement.
3. **No sibling `PackageReference`.** DataMask does not reference Guard or TimeKit. `Plugin.Maui.*`, UIKit, and NuvexaDB do not reference these packages. A host that wants both installs both.
4. **Guard is for application boundaries.** Other Nuvyntra repositories keep their own one-line checks. They do not take a dependency on Guard to share twenty lines.
5. **Package prefix is `NuvyntraLabs.NET.{Product}`.** Root namespace matches the package id. Discussion names (`Nuvyntra.DataMask`) are not the NuGet id. The id is not `Plugin.Maui.*`: there is no `UseX` and no `Current` accessor.
6. **`net8.0`, `net9.0`, and `net10.0`.** The libraries multi-target from .NET 8 upward. Samples stay on `net10.0`. Tests run on every packed framework.
7. **AOT and trim are a constraint.** Public APIs are static methods and concrete types. No reflection mapper, no runtime `GetProperty` walk, no regex compiled with `RegexOptions.Compiled` against a user pattern. `IsAotCompatible` and `EnableTrimAnalyzer` are on in every shippable project.
8. **Logging helpers must not throw on bad input.** DataMask returns a masked string. Unrecognized input is masked entirely. TimeKit and Guard do throw, because they are caller bugs, not log data.
9. **No embedded holiday database and no embedded regex catalog.** Holiday dates go stale. A shared regex bag becomes a junk drawer. Patterns live next to the type that owns them.
10. **Publishing is pipeline-only.** Do not `dotnet nuget push` from a local clone. Each product repository packs `net8.0`, `net9.0`, and `net10.0` (nupkg and snupkg) and publishes nuget.org and GitHub Packages from its own GitHub Actions workflow.

## 4. Ship order

| Wave | Product | Package | Problem | Why this order |
| --- | --- | --- | --- | --- |
| 1 | Guard | `NuvyntraLabs.NET.Guard` | Reject null, empty, non-positive, and out-of-range arguments | Smallest surface. Proves the repo template. |
| 1 | DataMask | `NuvyntraLabs.NET.DataMask` | Mask a known sensitive string before logging | Clearest gap versus the BCL and Compliance.Redaction. |
| 1 | TimeKit | `NuvyntraLabs.NET.TimeKit` | Business days, month and quarter bounds, Unix time, IANA zones | Useful on its own. Calendar stays an interface the host implements. |
| 2 | Identifiers | `NuvyntraLabs.NET.Identifiers` | PAN format, GSTIN checksum, Aadhaar Verhoeff, IBAN mod-97 | The only part of ValidationKit worth a package. Depends on nothing in Wave 1. |
| 2 | Result | `NuvyntraLabs.NET.Result` | `Result<T>` for a MAUI call that can fail without throwing | Only if Wave 1 is published and a host still refuses ErrorOr. No ASP.NET adapter in this catalog. |
| 3 | ObjectKit | `NuvyntraLabs.NET.ObjectKit` | Source-generated structural copy and equality | Reflection deep-clone and property paths are out. Start this only after a generator prototype trims clean. |

Wave 1 packages ship independently. Wave 2 does not start because Wave 1 exists. It starts when a host hits the checksum or Result gap and the Wave 1 APIs are frozen.

### Accepted layout

```
MauiEssentials/
├── docs/plans/utilities.md
├── Guard/        → github.com/nuvyntralabs/NuvyntraLabs.NET.Guard
├── DataMask/     → github.com/nuvyntralabs/NuvyntraLabs.NET.DataMask
├── TimeKit/      → github.com/nuvyntralabs/NuvyntraLabs.NET.TimeKit
├── Identifiers/  → github.com/nuvyntralabs/NuvyntraLabs.NET.Identifiers
├── Result/       → github.com/nuvyntralabs/NuvyntraLabs.NET.Result
└── ObjectKit/    → github.com/nuvyntralabs/NuvyntraLabs.NET.ObjectKit
```

Each repository:

```
{Product}/
├── src/NuvyntraLabs.NET.{Product}/
├── tests/NuvyntraLabs.NET.{Product}.Tests/
├── README.md
├── llms.txt
├── AGENTS.md
├── LICENSE
└── Directory.Build.props
```

Result is one package. A MAUI page checks `IsSuccess`. There is no ASP.NET Core adapter in this catalog.

## 5. Disposition of the original list

| Proposed name | Decision | Where it goes |
| --- | --- | --- |
| Nuvyntra.Guard | Ship in Wave 1 | `NuvyntraLabs.NET.Guard` |
| Nuvyntra.DataMask | Ship in Wave 1 | `NuvyntraLabs.NET.DataMask` |
| Nuvyntra.TimeKit | Ship in Wave 1 | `NuvyntraLabs.NET.TimeKit` |
| Nuvyntra.DateKit | Fold into TimeKit | A second date package splits one problem. |
| Nuvyntra.ValidationKit | Split | Checksums become Identifiers (Wave 2). Email, phone, URL, and password rules stay on DataAnnotations or FluentValidation. |
| Nuvyntra.ObjectKit | Wave 3, generator only | Runtime deep clone, deep compare, and `GetPath` are out. |
| Nuvyntra.ObjectMapper | Out | `MapTo<T>()` by reflection breaks the AOT rule. Mapperly already source-generates member maps, including a `ForMember` equivalent. Revisit only for a mapping shape Mapperly cannot express. |
| Nuvyntra.Result | Wave 2, conditional | `NuvyntraLabs.NET.Result`. A MAUI page reads `IsSuccess`. |
| Nuvyntra.StringKit | Out | Slug and humanize stay on Humanizer. Masking stays on DataMask. Similarity is a product of its own if a host ever needs it, and it is not in this plan. |
| Nuvyntra.TextKit | Out | Same surface as StringKit (count, truncate, mask, normalize). Truncate and word count are not a package. |
| Nuvyntra.CollectionKit | Out | `Chunk`, `DistinctBy`, and `ExceptBy` are in `System.Linq`. |
| Nuvyntra.JsonKit | Out | `System.Text.Json` covers parse, DOM, and merge-by-hand. Flatten and unflatten can be a later product if a host shows a config-document case. They are not Wave 1. |
| Nuvyntra.FileKit | Out | Hashing is `SHA256.HashData`. Zip is `System.IO.Compression`. Safe file names are a single method; they can land on DataMask only if a path is being logged. MIME sniffing is a different product and is not scheduled. |
| Nuvyntra.HashKit | Out | MD5, SHA, and HMAC are `System.Security.Cryptography`. Do not wrap MD5. Content fingerprints are `SHA256` over the bytes. |
| Nuvyntra.EnumKit | Out | Display names are `[Display]`. Flag parsing is `Enum.Parse`. A source generator would duplicate CommunityToolkit enum extensions. |
| Nuvyntra.NumericKit | Out | Rounding and percents are `decimal` arithmetic. Safe conversion is `T.TryParse` and `INumber<T>`. |
| Nuvyntra.RandomKit | Out | Ids are `Guid.CreateVersion7()`. Test data is Bogus. |
| Nuvyntra.ConsoleKit | Out | Spectre.Console. |
| Nuvyntra.UriKit | Out | `Uri` and `QueryHelpers` (ASP.NET) already merge and normalize. A BCL-only query builder is a gist, not a product. |
| Nuvyntra.RegexKit | Out | Patterns ship inside DataMask and Identifiers. There is no public regex catalog. |
| Nuvyntra.Toolkit (meta) | Out | See locked decision 2. |

## 6. Wave 1 — Guard

`NuvyntraLabs.NET.Guard` throws BCL exceptions and returns the checked value so a boundary can assign it.

```csharp
var request = Guard.NotNull(request);
var name = Guard.NotEmpty(name);
var amount = Guard.Positive(amount);
var age = Guard.InRange(age, 18, 100);
```

| Method | Accepts | Throws | Returns |
| --- | --- | --- | --- |
| `NotNull<T>` | `T?` where `T : class` | `ArgumentNullException` | `T` |
| `NotEmpty` | `string?` | `ArgumentException` when null, empty, or whitespace | the original string |
| `Positive<T>` | `INumber<T>` | `ArgumentOutOfRangeException` when `<= 0` | the value |
| `InRange<T>` | `IComparable<T>` | `ArgumentOutOfRangeException` when outside inclusive bounds | the value |

`[CallerArgumentExpression]` supplies the parameter name. v1 has no custom exception types, no `GuardAgainst` extension vocabulary, and no `out` parameters.

`NotEmpty` treats whitespace as empty. That is the logged decision. Callers who must allow `"   "` check length themselves.

## 7. Wave 1 — DataMask

`NuvyntraLabs.NET.DataMask` is a static class. Extension methods live in `NuvyntraLabs.NET.DataMask.Extensions` so a global usings file does not attach `MaskPhone` to every `string` in the solution.

```csharp
DataMask.Phone("9876543210");             // ******3210
DataMask.Email("john.doe@gmail.com");     // j*******@gmail.com
DataMask.Card("4111111111111111");        // ************1111
DataMask.Aadhaar("234123412346");         // **** **** 2346
DataMask.Pan("ABCDE1234F");               // *****1234F
DataMask.Gstin("27ABCDE1234F1Z5");        // 27**********1Z5
DataMask.Jwt(token);                      // {header}.***.***
DataMask.ApiKey("sk_live_51Abcd1234");    // sk_l***********1234
DataMask.ConnectionString(raw);
DataMask.Json(json, new MaskRules { PropertyNames = ["password", "pan"] });
```

The samples above are the contract. Tests pin them.

### Mask rules

| Kind | Keep | Mask | Notes |
| --- | --- | --- | --- |
| Phone | last 4 digits | every other digit | Separators (`+`, space, `-`) stay. `+91 98765 43210` → `+** ***** **3210`. |
| Email | first character of the local part, and the domain | the rest of the local part | Missing `@` masks the whole string. |
| Card | last 4 digits | every other digit | Spaces stay. Length is preserved. Luhn failure still masks; this is not a validator. |
| Aadhaar | last 4 digits, grouped `**** **** nnnn` | the first 8 digits | 12 digits required after stripping spaces. Anything else is fully masked. |
| PAN | four digits and the final character | the five leading letters | Those letters encode name and holder type. Format is `[A-Z]{5}[0-9]{4}[A-Z]`. |
| GSTIN | first 2 (state) and last 3 | the middle 10 | 15 characters required. The middle is the embedded PAN plus entity code. |
| JWT | header segment | payload and signature, each replaced by `***` | Three dot-separated segments required. The header is kept because `alg` is what a failing verifier needs. The payload is always masked in v1. |
| API key | first 4 and last 4 when length ≥ 12 | the middle | Shorter keys keep only the last 2. |
| Connection string | keys that are not secrets | secret values become `***` | Keys, case-insensitive: `Password`, `Pwd`, `AccountKey`, `SharedAccessKey`, `SharedAccessSignature`, `AccessToken`, `ClientSecret`, `ApiKey`. Unparseable input is fully masked. |
| JSON | structure and non-secret property names | values of named properties | Default names: `password`, `secret`, `token`, `apiKey`, `api_key`, `pan`, `aadhaar`, `gstin`, `card`, `cardNumber`, `cvv`, `connectionString`. Match is ordinal-ignore-case. Nested objects and arrays are walked. |

`null` returns `""`. DataMask never returns the original value when the kind was requested and the shape did not match. A 3-digit string passed to `Phone` comes back as `***`.

v1 does not scan free text for things that look like cards. Auto-detection false-positives belong in a later opt-in (`MaskEmbeddedValues`), and that method ships only with a golden corpus. v1 also does not mask by reflection over a POCO. Typed masking, if it ever exists, is a source generator with `[Mask(MaskKind.Pan)]` on a property. It is not in Wave 1.

JSON uses `JsonNode`. Invalid JSON is fully masked, not thrown. The implementation does not take a `PackageReference` on `Microsoft.Extensions.Compliance.Redaction`. A host that already has classifiers can call `DataMask` from an `IRedactor`.

Card masking is a logging aid. It is not a PCI scope reduction by itself. READMEs say that in one sentence. CVV is never accepted as a dedicated API. A property named `cvv` in JSON is masked because it is on the default name list.

## 8. Wave 1 — TimeKit

Business-day methods take `DateOnly`. Zone conversion takes `DateTimeOffset`. Unix time is seconds since the Unix epoch, UTC. The two kinds do not share an overload.

```csharp
date.IsWeekend();
date.IsBusinessDay();
date.AddBusinessDays(5);
date.StartOfMonth();
date.EndOfQuarter();
instant.ToUnixTimeSeconds(); // BCL, preferred when the value is already DateTimeOffset
dateTimeOffset.ToTimeZone("Asia/Kolkata");
```

`ToUnixTimestamp` exists as an extension on `DateTimeOffset` that calls the BCL, so call sites in this ecosystem share one name. Do not add a `DateTime` overload. Unspecified `DateTime` is how hosts stamp the wrong offset.

### Calendar

```csharp
public interface IBusinessCalendar
{
    bool IsBusinessDay(DateOnly day);
}
```

| Type | Rule |
| --- | --- |
| `WeekendCalendar` | Saturday and Sunday are not business days. This is the default when the caller does not pass a calendar. |
| `HolidayCalendar` | Wraps another calendar and removes a host-supplied set of `DateOnly` holidays. |

`AddBusinessDays` walks forward or backward one civil day at a time and counts days for which `IsBusinessDay` is true. The start date is not counted. `0` returns the same date even when it is a weekend. Negative counts walk backward.

`IsWeekend` on the extension method uses Saturday and Sunday. A host whose weekend is Friday and Saturday uses `IBusinessCalendar` and does not call `IsWeekend`.

`ToTimeZone` calls `TimeZoneInfo.FindSystemTimeZoneById`. On `net8.0` and later those ids are IANA (`Asia/Kolkata`). An unknown id throws `TimeZoneNotFoundException`. There is no Windows-id translation table in the package.

`StartOfMonth` and `EndOfQuarter` return `DateOnly`. Quarters are calendar quarters (Jan–Mar, Apr–Jun, Jul–Sep, Oct–Dec), not fiscal quarters. A fiscal calendar is a host `IBusinessCalendar` plus host code. It is not a v1 type.

Relative English strings (`3 days ago`) are out. Humanizer owns them, and localized copy belongs to the host (NuvLoc for MAUI resource files). TimeKit does not format for humans beyond ISO dates the BCL already produces.

No dependency on NodaTime. A host that needs `LocalDate` plus a calendar system uses NodaTime and does not wrap it here.

## 9. Wave 2 — Identifiers

`NuvyntraLabs.NET.Identifiers` returns `bool`. It does not throw and it does not mask. Masking stays on DataMask so a logger does not need a validator.

| Method | Rule |
| --- | --- |
| `Pan.IsValid` | `^[A-Z]{5}[0-9]{4}[A-Z]$` after ASCII uppercasing. PAN has no checksum. |
| `Gstin.IsValid` | 15 characters, state code `01`–`38`, embedded PAN, entity code, `Z`, and the mod-36 checksum. |
| `Aadhaar.IsValid` | 12 digits and the Verhoeff checksum. Spaces are stripped first. |
| `Iban.IsValid` | Country length plus mod-97. |

Password strength, email, phone, and URL stay out. Those rules are product policy.

Identifiers does not reference DataMask. The GSTIN and PAN patterns are duplicated on purpose. A shared regex package is decision 9.

## 10. Wave 2 — Result

Ship this only if a real host asks and ErrorOr is still the wrong weight. v1 surface:

```csharp
Result<User> result = await GetUserAsync();

if (result.IsSuccess)
{
    User user = result.Value;
}
else
{
    Error error = result.Error;
}
```

| Type | Role |
| --- | --- |
| `Result<T>` | Success value or `Error`. `Value` throws `InvalidOperationException` on failure. |
| `Result` | Success or `Error`, no value. |
| `Error` | `Code` and `Message`. |
| `ValidationError` | `Error` plus a property name. |
| `NotFoundError` | `Error` with a stable `not_found` code. |

No `Map`, `Bind`, or LINQ operators in v1. `Match` is the one functional escape hatch.

A page checks `IsSuccess`. This catalog does not ship an ASP.NET Core ProblemDetails adapter.

## 11. Wave 3 — ObjectKit

The useful version is a source generator:

- `Copy<T>()` generated from public init/set properties
- structural `Equals` and `GetHashCode` for a marked type

Runtime `DeepClone`, recursive `Equals`, and string property paths (`"Address.City"`) use reflection and fail trimming. They are out, including as an opt-in package. If the generator cannot see a member, the build fails. There is no reflection fallback.

Object mapping stays on Mapperly. ObjectKit does not grow `CreateMap`.

## 12. Packaging

Match a MauiEssentials related-product `Directory.Build.props` (UIKit is the reference):

- `Nullable` enable, `ImplicitUsings` enable, `TreatWarningsAsErrors` true
- `IsAotCompatible` true, `EnableTrimAnalyzer` true
- MIT, author Niladri Prasad Padhy, company Nuvyntra Labs
- README and LICENSE packed
- `Version` `0.1.0` until the first nuget.org publish
- Package tags include `nuvyntra` and the product name
- Description names the problem, not “part of MauiEssentials”

Tests are xUnit, in the product repository, with no shared test project across products. DataMask tests include the contract table in section 7 plus null, short input, and invalid JSON. TimeKit tests pin a known weekend, a holiday skipped by `HolidayCalendar`, a quarter end, and `Asia/Kolkata` offset for a winter and a summer instant (India has no DST; the winter/summer pair guards a regression that assumes DST). Guard tests pin the exception type and the parameter name from `CallerArgumentExpression`.

Samples are a single `net10.0` console project per repository, used by the README. A MAUI sample is not required: these libraries have no MAUI types.

## 13. Catalog entries

The six products are MauiEssentials submodules at `0.1.0`. Each repository is public. They are not published to nuget.org, so the hub rows do not include an install line.

When the first nupkg is published, the same change adds the install line:

- `README.md` related-products section and requirement map
- `docs/packages/README.md`
- `docs/plans/README.md`
- `llms.txt`, `llms-full.txt`, and `AGENTS.md`
- Hub CI dispatch list, if that workflow dispatches product repositories

## 14. Explicitly out

- An umbrella `Toolkit` package or a single repository that holds every kit
- Reflection mappers, reflection deep clone, and property-path access
- A holiday feed, fiscal calendars, and localized relative time
- A public regex catalog
- MD5 wrappers, MIME sniffing, compression helpers, fake data, CLI chrome
- Password-strength scoring
- Scanning arbitrary log text for numbers that might be cards
- A `Plugin.Maui.*` id, a `UseX` registration, or a MAUI `FrameworkReference` on these libraries
- `PackageReference`s from UIKit, NuvexaDB, or `Plugin.Maui.*` into these libraries
