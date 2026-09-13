# Getting started

MauiEssentials is a catalog of focused .NET MAUI plugins. You do not reference this repository as a single NuGet package. Install the plugin that matches the requirement.

## 1. Pick a package

Use the [requirement → package map](packages/README.md) or the tables in the [root README](../README.md).

Examples:

- Real internet vs captive portal → `Plugin.Maui.NetworkMonitor`
- Internet works but the API does not → `Plugin.Maui.NetworkDiagnostics`
- GPS + reverse geocoding → `Plugin.Maui.GeoLocator`
- Durable work that must survive process death → `Plugin.Maui.JobQueue`
- Retry a failed API call (orders, telemetry, payments) → `Plugin.Maui.RetryQueue`
- OS-scheduled refresh → `Plugin.Maui.BackgroundTasks`
- BLE printer / POS / sensor connection manager → `Plugin.Maui.BluetoothManager`
- Sensitive clipboard / OTP expiry / image clips → `Plugin.Maui.ClipboardPlus`
- Device fingerprint / NFC / biometric / GPS capability → `Plugin.Maui.DeviceInfoPlus`
- NFC NDEF read/write, tag ID, attendance / inventory → `Plugin.Maui.NfcPlus`
- Lock the app after background (Face ID / PIN / lock timer) → `Plugin.Maui.AppLock`
- One-shot Face ID / fingerprint / device PIN → `Plugin.Maui.BiometricPlus`
- Keep the screen on during scan / POS / video → `Plugin.Maui.KeepAwake`
- Block screenshots / recents thumbnail → `Plugin.Maui.ScreenGuard`
- In-app store review / open listing → `Plugin.Maui.AppReview`
- Scheduled local notifications (not FCM) → `Plugin.Maui.LocalNotifications`
- Circular geofence enter / exit / dwell → `Plugin.Maui.Geofence`
- Classic Bluetooth serial (SPP / RFCOMM) → `Plugin.Maui.BluetoothSerial`
- Camera/gallery video compress / encrypt → `Plugin.Maui.VideoPipeline`
- HttpClient TLS / SPKI pin → `Plugin.Maui.TlsPin`
- Typed REST client / Refit-style interfaces → `Plugin.Maui.HttpForge` ([vs Refit](https://github.com/nuvyntralabs/Plugin.Maui.HttpForge/blob/main/Docs/refit-comparison.md))
- HTTP GET cache / CacheFirst / StaleWhileRevalidate → `Plugin.Maui.ApiCache`
- Form validation / email / phone / `Validation.For` → `Plugin.Maui.FormValidation`
- Hide / show keyboard, dismiss on tap, resize vs pan → `Plugin.Maui.KeyboardManager`
- Lock / unlock landscape or portrait, per-page orientation → `Plugin.Maui.DeviceOrientationPlus`
- MAUI visual-tree leak detection after navigation → `Plugin.Maui.LeakAnalyser`
- WPF MVVM application shell (Frame navigation, dialogs) → `Plugin.Wpf.MVVMExpress` (`dotnet new wpf-mvvmexpress`)
- Native WinUI 3 MVVM application shell → `Plugin.WinUI.MVVMExpress` (`dotnet new winui-mvvmexpress`)
- Avalonia MVVM application shell → `Plugin.Avalonia.MVVMExpress` (`dotnet new avalonia-mvvmexpress`)
- Uno Platform MVVM application shell → `Plugin.Uno.MVVMExpress` (`dotnet new uno-mvvmexpress`)
- Diagnose MAUI SDK / workloads / project config / permissions / platform layout → `Plugin.Maui.MauiDev.Cli` (`dotnet tool install -g Plugin.Maui.MauiDev.Cli` then `maui-dev doctor`)
- Embedded Mongo-like document file (`.nvx`) → `Nuventra.NuvexaDB` (hub module `NuvexaDB/`; not a `Plugin.Maui.*` package). JobQueue / OfflineSync stay SQLite.

## 2. Install

```bash
dotnet add package Plugin.Maui.NetworkMonitor
```

Confirm the package supports your target frameworks. Most plugins ship `net10.0`, `net10.0-android`, and `net10.0-ios`. NetworkMonitor also ships `net8.0` / `net9.0`.

## 3. Register

Each plugin adds a MAUI builder extension. Typical pattern:

```csharp
builder
    .UseMauiApp<App>()
    .UseNetworkMonitor(options =>
    {
        options.EnableHttpProbe = true;
        options.EnableCaptivePortalDetection = true;
    });
```

Resolve the interface from DI, or use the static `Current` / `Default` accessor documented in that plugin's README.

## 4. Platform setup

Read the plugin README before generating code. Every Android + iOS plugin lists **both** platforms under Permissions / Host app setup — including when a platform needs no extra key.

Typical host declarations:

- Android `AndroidManifest.xml` permissions
- iOS `Info.plist` usage strings or background modes (Face ID, location, camera, Bluetooth, NFC)
- iOS privacy manifest entries for User Defaults
- Host-app Firebase / APNs / Play Core setup (PushRouter, AppUpdate)

## 5. Verify with the sample

Each repository includes `samples/` and usually `tests/`. Prefer the sample over inventing a new registration sequence.

## 6. Compose, do not stack blindly

These plugins are designed to compose:

- BackgroundTasks can call `JobQueue.Current.DrainAsync()` or `RetryQueue.Current.DrainAsync()`
- MediaPipeline can hand off to FileVault or SmartUpload
- SecureSession persists tokens with SecureStoragePlus
- HttpForge generates the typed client; ApiCache caches GET responses; ApiResilience retries them; SecureSession attaches tokens; SmartUpload owns resumable bytes; OfflineSync owns local writes. Recipes: [HttpForge integration](https://github.com/nuvyntralabs/Plugin.Maui.HttpForge/blob/main/Docs/integration.md)
- Observability registers several sibling plugins — only use it when you want that umbrella
- NuvexaDB owns the encrypted `.nvx` document file. JobQueue and OfflineSync stay SQLite for durable jobs and sync.

Do not add Observability or the full catalog for a single feature.

## 7. Upgrade hardened 1.x plugins

Fourteen plugins shipped fail-closed and correctness fixes on 3 September 2026. DeepLinks, PushRouter, SmartUpload, and FeatureFlags changed defaults. See [Hardened releases](hardened-releases.md) before bumping:

```bash
dotnet add package Plugin.Maui.DeepLinks --version 1.0.6
dotnet add package Plugin.Maui.PushRouter --version 1.0.6
dotnet add package Plugin.Maui.SmartUpload --version 1.0.6
dotnet add package Plugin.Maui.FeatureFlags --version 1.0.9
dotnet add package Plugin.Maui.ApiResilience --version 1.0.10
```

## Continuous integration

The hub workflow at `.github/workflows/ci.yml` is **manual only** (`workflow_dispatch`). It does not run on push to the hub repo. A manual run dispatches each plugin submodule’s own `CI` workflow and waits for the results. The hub does not build or publish packages itself.

Store a GitHub token that can dispatch workflows on `nuvyntralabs/Plugin.Maui.*` as the `HUB_DISPATCH_TOKEN` Actions secret on the hub (or the `nuvyntralabs` organization). The optional **plugin** input limits the dispatch to one submodule folder.

Publish from the plugin repository that owns the package (for example `Plugin.Maui.MVVMExpress`, which ships several `Plugin.Maui.MVVMExpress.*` packages). Each dispatched submodule pipeline is fail-fast and runs in this order:

1. **Version alignment.** All packable `src` `Version` / `PackageVersion` values must match.
2. **NuGet release.** Validate `NUGET_KEY` (or `NUGET_KEY_WPF` / `NUGET_KEY_WINUI` / `NUGET_KEY_AVALONIA` / `NUGET_KEY_UNO` for those families), then compare each packable csproj version with NuGet.org. An empty, expired, or rejected key fails the pipeline. If that version is already deployed, the pipeline fails. Bump the csproj version to continue. Tests and pack do not start after this job fails.
3. **Unit tests.** Any failing test fails the pipeline and does not start pack.
4. **linux / macos / windows packs** in parallel. A failed pack skips **nuget.org and GitHub Packages**. Unmatched Windows TFMs are skipped on native Android/iOS plugins.
5. **nuget.org and GitHub Packages.** Merge the Windows-packed `net*-windows*` TFMs into the macOS `.nupkg` / `.snupkg` when those artifacts exist, then push (`--skip-duplicate`) to both feeds. nuget.org gets the nupkg and snupkg. GitHub Packages gets the nupkg at `https://nuget.pkg.github.com/nuvyntralabs/index.json`. Without the Windows merge, nuget.org shows `net10.0-windows` only as a compatibility hint. PackAsTool packages (`Plugin.Maui.*.Cli`, for example `Plugin.Maui.Performance.Cli`) publish the nupkg only.

Store the nuget.org API key as the `NUGET_KEY` Actions secret on the `nuvyntralabs` organization or on that plugin repo — never in YAML. Desktop MVVMExpress families use scoped keys: `NUGET_KEY_WPF` (`Plugin.Wpf.*`), `NUGET_KEY_WINUI` (`Plugin.WinUI.*`), `NUGET_KEY_AVALONIA` (`Plugin.Avalonia.*`), `NUGET_KEY_UNO` (`Plugin.Uno.*`). MauiDev (`Plugin.Maui.MauiDev.Cli`) uses `NUGET_KEY_MAUIDEV_CLI`. NuvexaDB (`Nuventra.NuvexaDB`) uses its own `NuvexaDB/.github/workflows/ci.yml`. It packs **nupkg + snupkg** and uploads them as GitHub artifacts next to Explorer / VS Code / Visual Studio / language SDK packs. nuget.org, GitHub Packages, version alignment, and NuGet validation are commented out until multi-host publishing is decided. All families still push GitHub Packages with the job’s `GITHUB_TOKEN` (`packages: write`). Copy `.github/plugin-repo-ci.yml` when adding a new MAUI plugin repo.

The first GitHub Packages version is private. After CI publishes, open [nuvyntralabs packages](https://github.com/orgs/nuvyntralabs/packages), open the package, and set visibility to Public if the plugin repo is public. Restoring from GitHub Packages still requires a GitHub token (`read:packages`); nuget.org stays the unauthenticated public feed.

- Ubuntu: `net10.0`
- macOS: `net10.0`, `net10.0-android`, `net10.0-ios` (and Mac Catalyst when the plugin declares it)
- Windows: `net10.0` plus `net10.0-windows` for shared libraries and MAUI MVVMExpress. `Plugin.Wpf.MVVMExpress` Host / Navigation / Dialogs pack on Windows only (`net10.0-windows10.0.17763.0` + `UseWPF`). `Plugin.WinUI.MVVMExpress` Host / Navigation / Dialogs pack on Windows (`net10.0-windows10.0.19041.0` + `UseWinUI`). `Plugin.Avalonia.MVVMExpress` packs all libraries on Linux. `Plugin.Uno.MVVMExpress` packs Core on Linux and Host heads that the runner can build.

Each plugin repo can reuse the same job via `.github/plugin-repo-ci.yml`.

## Next

- [Hardened releases](hardened-releases.md)
- [Architecture](architecture.md)
- [Package directory](packages/README.md)
- [AGENTS.md](../AGENTS.md)
