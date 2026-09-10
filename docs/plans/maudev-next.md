# MauiDev — next development plan (1.1 / 1.2)

**Status:** 1.1 and 1.2 implemented at `1.2.0`. 1.0 shipped at `1.0.1` — see [maudev.md](maudev.md).  
**Product:** MauiDev — developer productivity toolkit for .NET MAUI  
**Package:** `Plugin.Maui.MauiDev.Cli` (`PackAsTool`, command `maui-dev`). nuget.org reserved `MauiDev.Cli`.  
**Extension:** `nuvyntralabs.maui-dev`  
**Repo / hub:** `nuvyntralabs/MauiDev` · hub folder `MauiDev/`

This plan turns the README **Later (not 1.0)** list into implementable slices. It does not reopen 1.0 decisions.

Usual alternatives stay [maui-check](https://github.com/Redth/dotnet-maui-check), `dotnet workload`, Visual Studio’s MAUI installer, and the Microsoft `maui` CLI. Runtime work stays in `Plugin.Maui.Performance` / `maui-perf`, LeakAnalyser, AppHealth, and Diagnostics.

---

## 1. Problem

1.0 answers “is this machine and csproj a viable MAUI tree?” It does not answer the follow-up questions developers ask next:

- Which permissions and usage strings are required vs leftover?
- Is the `Platforms/` layout and `#if` / TFM split sound?
- What must exist in CI before a store or NuGet publish?
- Can versions, PackageReferences, and icons be aligned without a human diff?
- Can we migrate TFMs or hand off a startup trace without a second tool hunt?

Those are still **developer-tool** problems. They are not runtime plugins.

## 2. Principles (unchanged)

1. **Toolchain, not a PackageReference.** Install remains `dotnet tool install -g Plugin.Maui.MauiDev.Cli`.
2. **`MauiDev.Core` stays internal** (`IsPackable=false`). Only the CLI nupkg publishes.
3. **Same report contract.** Every new command emits `DoctorReport` → human / JSON / SARIF. Exit codes stay `0` pass/skip, `1` fail (or warning with `--warn-as-error` / `--ci`), `2` usage.
4. **`--fix` is an allow-list.** New fixes must be named in this plan before they ship. Never bump min SDK, remove permissions, write signing secrets, install workloads, or push packages.
5. **Pipeline-only publish.** Never `dotnet nuget push` or `vsce publish` from a local clone. `package --pack` and any future `publish` command stay local / validate-only.
6. **No CLI telemetry collection.** The `telemetry` command inspects the **app** for crash / analytics SDKs. It does not phone home.
7. **Do not replace sibling tools.** `benchmark` shells to `maui-perf`. `analyze` stays heuristic (not Roslyn).
8. **net10.0 only** for the tool. Linux CI remains enough to test and pack.

## 3. What 1.0 already covers

Do not reimplement these as greenfield engines. Dedicated 1.1 commands **reuse** `ProjectGraph`, `CheckBase`, and the existing doctor checks, then add depth.

| Area | 1.0 surface | Gap the new command fills |
| --- | --- | --- |
| Permissions | `PermissionsCheck` — unused/duplicate Android `UsesPermission` (`MD020`–`MD021`) | iOS usage strings, Info.plist / entitlements, `--fix` for duplicates only |
| Platform | `TargetFrameworkCheck` + analyze `MD105` (platform type without `#if`) | `Platforms/` layout, missing iOS/Android folders, Windows/Mac Catalyst notes |
| Signing | `SigningCheck` — warn if AndroidSigning\* / plist missing | CI checklist (keystore path exists? profile named?) — still never writes secrets |
| Workload | `MauiWorkloadCheck` — present / missing | Print exact `dotnet workload` repair commands; never run them |
| Version | `package --validate` — packable versions must match (`MD401`) | Dedicated bump / align with `--dry-run` |
| Resources / icons | `resources` — duplicate / missing / unused MauiImage, splash, font | AppIcon / adaptive-icon / asset-catalog completeness |
| Analyze | Regex heuristics `MD100`–`MD106` | Stays heuristic. Not a Roslyn analyzer. |
| Pack | `package --validate` / `--pack` | Store-identity validate (`publish`); no feed push |

Global options stay: `--path`, `--format human|json|sarif`, `--ci`, `--fix`, `--dry-run`, `--warn-as-error`, `--timeout`.

## 4. Releases

| Release | Theme | Ships |
| --- | --- | --- |
| **1.1.0** | Dedicated diagnose (+ small allow-listed fix) commands | `permissions`, `platform`, `signing`, `workload`, `version`, `dependencies`, `icons` |
| **1.2.0** | Store / migrate / sibling-tool handoff | `publish`, `migrate`, `telemetry`, `benchmark` |

Bump `Version` / `PackageVersion` in `Directory.Build.props`, the CLI csproj, and `extension/vscode/package.json` together. CI already enforces that alignment.

## 5. Diagnostic ID map

Keep existing IDs stable. New commands take unused ranges.

| Range | Owner |
| --- | --- |
| `MD010`–`MD012` | TFM (doctor) |
| `MD020`–`MD029` | Permissions (doctor + `permissions`) |
| `MD030` | Duplicate MAUI resource items (doctor `--fix`) |
| `MD050`–`MD069` | `platform` |
| `MD070`–`MD079` | `signing` (dedicated report; doctor check stays) |
| `MD100`–`MD199` | `analyze` (heuristic). `MD104` is unused — reserve for IDisposable / handler disconnect |
| `MD200`–`MD209` | `resources` |
| `MD210`–`MD229` | `icons` |
| `MD300`–`MD399` | `clean` |
| `MD400`–`MD409` | `package` |
| `MD410`–`MD429` | `version` |
| `MD500`–`MD529` | `dependencies` |
| `MD600`–`MD629` | `migrate` |
| `MD700`–`MD729` | `telemetry` (app SDK scan) |
| `MD800`–`MD829` | `publish --validate` |
| `MD900`–`MD919` | `benchmark` (missing `maui-perf` / `maui`) |

`.maui-dev.json` `ignore` continues to suppress **check ids** (`android-permissions`, `signing`, …) and should also accept diagnostic ids (`MD020`) in 1.1.

## 6. 1.1 commands

Each command is an engine in `MauiDev.Core` plus a `CliHost` subcommand. The VS Code extension adds a matching `mauiDev.*` command that shells the same verb and maps JSON into the Problems panel.

### 6.1 `maui-dev permissions`

**Purpose:** Android + iOS permission / usage-string audit.

**Checks**

- Reuse unused / duplicate Android hints (`MD020`, `MD021`).
- `MD022` — iOS `NS*UsageDescription` missing when source/XAML references Camera, Location, Bluetooth, Contacts, Photo Library, Microphone, or NFC.
- `MD023` — Info.plist usage string present but no matching API reference (warn).
- `MD024` — Android 13+ media / notification permission declared without a `maxSdkVersion` or 13+ code path (warn).

**`--fix` allow-list:** deduplicate identical `UsesPermission` / manifest permission nodes only. Never remove a permission or a usage string.

**Out:** writing Info.plist keys, changing `minSdk`, PermissionFlow registration.

### 6.2 `maui-dev platform`

**Purpose:** TFM ↔ folder ↔ compile-guard consistency.

**Checks**

- `MD050` — `net*-android` TFM without `Platforms/Android`.
- `MD051` — `net*-ios` TFM without `Platforms/iOS` (or `Info.plist`).
- `MD052` — shared `.cs` uses `Android.` / `UIKit.` / `WinRT` without `#if` or a platform-specific file path (promote analyze `MD105` here; keep `MD105` as an analyze alias).
- `MD053` — Windows / Mac Catalyst TFM present; report as info/warn that native MauiEssentials plugins stay Android+iOS (do not fail a valid multi-TFM app).
- `MD054` — `SupportedOSPlatformVersion` missing or below MAUI defaults (warn, no `--fix`).

**`--fix`:** none in 1.1.

### 6.3 `maui-dev signing`

**Purpose:** CI signing checklist. Report-only.

**Checks**

- Keep doctor’s “AndroidSigning\* unset” and “no Info.plist” warnings.
- `MD070` — `AndroidSigningKeyStore` path set but file missing on disk.
- `MD071` — iOS entitlements file referenced but missing.
- `MD072` — remind that store signing belongs in CI secrets (`NUGET_KEY*` is irrelevant here; this is app signing).

**`--fix`:** none. Never create a keystore or write a provisioning profile.

### 6.4 `maui-dev workload`

**Purpose:** Diagnose the MAUI workload and print the exact repair command.

**Checks**

- Reuse `MauiWorkloadCheck` / `MauiCliCheck`.
- `MD080` range is unused; attach extra workload detail to the existing machine checks or add `MD055` if a second result is cleaner — prefer **one** `workload` result with `NextStep` = `dotnet workload install maui` (or the current official repair).

**`--fix` / `--apply`:** not in 1.1. Installing workloads is a machine-wide side effect and is out of the allow-list.

### 6.5 `maui-dev version`

**Purpose:** Align or bump packable `Version` / `PackageVersion` (and the VS Code `package.json` when this repo is MauiDev itself).

**Checks**

- `MD410` — packable src versions diverge (same as `MD401`; emit both or fold into `MD410` and keep `MD401` on `package`).
- `MD411` — CLI `Version` ≠ `extension/vscode/package.json` version when that file exists.
- `MD412` — `Version` missing.

**`--fix` allow-list**

- `--align` — write every packable src + `Directory.Build.props` + extension `package.json` to the highest existing version.
- `--bump patch|minor|major` — increment that aligned version.

Always honor `--dry-run`. Do not create git tags.

### 6.6 `maui-dev dependencies`

**Purpose:** PackageReference hygiene for a MAUI tree.

**Checks**

- `MD500` — duplicate PackageReference ids with different versions in one project.
- `MD501` — `Microsoft.Maui.Controls` / `Microsoft.Maui.Controls.Build.Tasks` version drift across projects.
- `MD502` — Central package management (`Directory.Packages.props`) vs a project-local Version attribute (warn).
- `MD503` — `Plugin.Maui.MauiDev.Cli` referenced as a library PackageReference (fail; it is a tool).

**`--fix`:** none in 1.1 (do not rewrite PackageReference versions).

Do not call nuget.org from this command. A later “outdated” mode can be a 1.2 flag if tests can fake the feed.

### 6.7 `maui-dev icons`

**Purpose:** App icon / splash completeness beyond `resources`.

**Checks**

- `MD210` — no `MauiIcon` / `MauiSplashScreen` item.
- `MD211` — `MauiIcon` file missing (overlap with `MD201`; icons command can include it).
- `MD212` — Android adaptive icon foreground without a background (warn).
- `MD213` — iOS asset catalog `AppIcon` set incomplete (missing 1024 marketing size when an `.appiconset` exists).

**`--fix`:** none. Do not generate PNG densities in 1.1.

`resources` stays the cheap duplicate/missing/unused pass. `icons` is the store-asset pass.

## 7. 1.2 commands

### 7.1 `maui-dev publish --validate`

Default is validate. There is no `--push`.

**Checks**

- `MD800` — Android `applicationId` / `ApplicationId` missing or default `com.companyname.*`.
- `MD801` — iOS `CFBundleIdentifier` missing or `com.companyname.*`.
- `MD802` — missing privacy manifest / `PrivacyInfo.xcprivacy` when iOS TFM is present (warn until the required-reason set is encoded).
- `MD803` — `package --validate` failures (reuse `PackageValidator`) when the tree looks packable.

Never invoke `dotnet nuget push`, Play Developer API, or App Store Connect.

### 7.2 `maui-dev migrate`

**Purpose:** Point at TFM and obsolete-project leftovers. Not a Xamarin.Forms rewriter.

**Checks**

- `MD600` — `net8.0-*` / `net9.0-*` MAUI TFMs (warn: catalog default is `net10.0`).
- `MD601` — `Xamarin.Forms` / `Xamarin.Essentials` PackageReference.
- `MD602` — `MainActivity` still using `Forms.Init` / `LoadApplication` (heuristic).

**`--fix`:** none. Print a next-step; do not edit TFMs.

### 7.3 `maui-dev telemetry`

**Purpose:** Scan the **app** for crash / analytics SDKs and recommend the catalog sibling when it fits.

**Checks**

- `MD700` — App Center, Firebase Crashlytics, Sentry, Application Insights, or `Plugin.Maui.Diagnostics` / `Observability` detected (info).
- `MD701` — no crash reporter found in a MAUI app project (warn). Next step: Diagnostics, not this CLI.
- `MD702` — App Center `Analytics` / `Crashes` still referenced (warn: retired product).

The CLI itself continues to collect nothing.

### 7.4 `maui-dev benchmark`

**Purpose:** Thin handoff to [Plugin.Maui.Performance.Cli](https://www.nuget.org/packages/Plugin.Maui.Performance.Cli) (`maui-perf`).

**Behavior**

- Resolve `maui-perf` on PATH (or `~/.dotnet/tools`).
- If missing: `MD900` fail with `dotnet tool install -g Plugin.Maui.Performance.Cli`.
- If present: run `maui-perf --help` or forward remaining args (`startup`, `screen`, …). Do not reimplement `maui profile`.
- Honor `--timeout`. Android / iOS simulator only — same constraint as `maui-perf`.

`--fix` is meaningless here.

## 8. `--fix` allow-list after 1.1 / 1.2

| Action | Command | Notes |
| --- | --- | --- |
| Deduplicate identical `MauiSplashScreen` / `MauiImage` / `MauiIcon` / `MauiFont` | `doctor` | Already 1.0 |
| Insert `<UseMaui>true</UseMaui>` | `doctor` | Already 1.0 |
| Deduplicate identical Android permissions | `permissions` | 1.1 |
| Align / bump `Version` + extension `package.json` | `version --align` / `--bump` | 1.1 |

Still never: remove permissions, bump min SDK, write signing files, install workloads, generate icons, rewrite TFMs, push NuGet or store binaries.

## 9. Extension (1.1 and 1.2)

Add one Command Palette entry per new verb. Reuse `runMauiDev` + Problems mapping. No new settings required for 1.1.

| Palette title | CLI |
| --- | --- |
| MauiDev: Permissions | `permissions` |
| MauiDev: Platform | `platform` |
| MauiDev: Signing | `signing` |
| MauiDev: Workload | `workload` |
| MauiDev: Version | `version` |
| MauiDev: Dependencies | `dependencies` |
| MauiDev: Icons | `icons` |
| MauiDev: Validate Publish | `publish --validate` (1.2) |
| MauiDev: Migrate | `migrate` (1.2) |
| MauiDev: Telemetry scan | `telemetry` (1.2) |
| MauiDev: Benchmark | `benchmark` (1.2; may be long-running — show output channel) |

Marketplace / Open VSX remain secret-gated (`VSCE_PAT`, `OVSX_PAT`). That is ops, not a 1.1 code task. CI already packages the VSIX.

No Visual Studio (VS) extension in this plan.

## 10. Implementation order

Do this in the `MauiDev` submodule, one slice per PR if possible.

1. **Scaffold** — `LooksLikeKnownCommand` + `Usage` text + empty engines that return Skip, plus CLI tests for “unknown command” vs new verbs. Bump to `1.1.0` when the first real engine lands.
2. **`permissions` + `platform`** — highest value, most of the graph already exists. Fixtures: extend `fixtures/known-bad`.
3. **`signing` + `workload`** — report-only; cheap tests with fakes (`IProcess`, `IFileSystem`).
4. **`version` + `dependencies`** — XML edits only for `version --align/--bump`.
5. **`icons`** — last 1.1 command; needs a small icon fixture.
6. **Extension palette** for 1.1 verbs. Version-align `package.json`.
7. **Hub docs** — `MauiDev/README.md` Later section becomes a 1.1 command table; `CHANGELOG.md`; hub `llms.txt` / `llms-full.txt` / `docs/packages/README.md` command list.
8. **1.2** — `publish`, `migrate`, `telemetry`, `benchmark` in that order (`benchmark` last; it is a process spawn).

## 11. Tests

Follow 1.0: `MauiDev.Core.Tests` (fakes + fixtures) and `MauiDev.Cli.Tests` (parse / exit codes). No device tests.

| Slice | Minimum coverage |
| --- | --- |
| Each new command | known-good → Pass/Skip; known-bad → expected `MDxxx` |
| `--fix` / `--dry-run` | permissions dedupe; version align/bump; no write when dry-run |
| `--ci` | JSON + exit `1` on warn |
| `benchmark` | missing tool → `MD900`; present → fake process receives `maui-perf` |
| Extension | existing `sample-report.json` style fixture for a new command |

Do not hit nuget.org, workload install, or Xcode from tests.

## 12. Docs to update when a slice ships

In **MauiDev**: `README.md`, `CHANGELOG.md`, `llms.txt`, `AGENTS.md`, `CliHost.Usage`, extension README / `package.json`.

In **hub** (this repo): `docs/plans/README.md` status, `llms.txt`, `llms-full.txt`, `docs/packages/README.md`, `README.md` MauiDev row if the command list is summarized there.

Keep the 1.0 sentence: *It does not replace runtime plugins.*

## 13. Out of scope

- Visual Studio (Windows IDE) extension
- Installing / repairing workloads, Android SDK, JDK, Xcode, or CocoaPods
- Writing keystores, provisioning profiles, or API keys
- Generating PNG / SVG icon densities
- Xamarin.Forms → MAUI rewrite
- Local or CI `dotnet nuget push` from a developer machine
- CLI usage analytics
- Replacing `maui-check` or the Microsoft `maui` CLI
- Windows / Mac Catalyst / Tizen as native plugin targets (the **tool** may still diagnose those TFMs)
- Roslyn analyzer package (`MauiDev.Analyzers`)
- `dotnet new` templates (`MauiDev.Templates`)

## 14. Acceptance

**1.1 is done when**

- The seven 1.1 commands exist, have fixture tests, and appear in `--help` / Usage.
- `--fix` only performs the rows in §8.
- Extension palette covers those seven commands.
- Versions align and CI packs `Plugin.Maui.MauiDev.Cli` + a VSIX.

**1.2 is done when**

- `publish` validates and never pushes.
- `benchmark` shells to `maui-perf` or fails with `MD900`.
- `telemetry` scans the app and does not send data.
