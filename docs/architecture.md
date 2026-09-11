# Architecture

MauiEssentials is a **catalog**, not a monorepo product. Each plugin is an independent git repository, NuGet package, and submodule. Most plugins target .NET MAUI. `Plugin.Wpf.MVVMExpress`, `Plugin.WinUI.MVVMExpress`, `Plugin.Avalonia.MVVMExpress`, and `Plugin.Uno.MVVMExpress` are separate desktop families in the same catalog — they are not Windows TFMs of `Plugin.Maui.MVVMExpress` and do not PackageReference each other.

```
Developer requirement
        ↓
README / llms.txt requirement map
        ↓
One plugin repository
        ↓
src/          library
samples/      MAUI host app
tests/        unit tests
README.md     human + LLM docs
llms.txt      LLM index
AGENTS.md     coding-agent guide
```

`MauiDev/` is a developer tool (`Plugin.Maui.MauiDev.Cli` / `maui-dev`), not a runtime plugin. nuget.org reserved the ID `MauiDev.Cli`. `Biometric/` ships `Plugin.Maui.BiometricPlus` because nuget.org reserved `Plugin.Maui.Biometric`.

## Design rules

1. **One problem per package.** Descriptions name the problem (captive portal, durable queue, resumable upload), not “part of MauiEssentials”.
2. **Android and iOS first.** Shared `net10.0` exists so tests and class libraries can reference the API. Native calls typically throw `FeatureNotSupported` on that TFM.
3. **MAUI builder registration.** Plugins expose `UseX(...)` and a `Current` / `Default` accessor.
4. **Compose, do not replace the OS.** BackgroundTasks wraps JobScheduler / BGTaskScheduler. JobQueue is an in-process SQLite worker. RetryQueue retries failed named operations. PushRouter does not register FCM tokens. VoipCore does not ship PJSIP.
5. **Prefer the framework when it is enough.** `Connectivity`, `Geolocation`, `SecureStorage`, and `Permissions` remain the default if they already solve the request.

## How plugins relate

| Need | Start with | Often compose with |
| --- | --- | --- |
| Location | GeoLocator | PermissionFlow |
| Connectivity | NetworkMonitor | AppHealth, OfflineSync, ApiResilience, ApiCache |
| Production connectivity troubleshooting | NetworkDiagnostics | NetworkMonitor (watch vs diagnose) |
| Typed REST client | HttpForge | ApiResilience, ApiCache, SecureSession, SmartUpload ([integration](https://github.com/nuvyntralabs/Plugin.Maui.HttpForge/blob/main/Docs/integration.md)) |
| HTTP GET cache | ApiCache | ApiResilience, NetworkMonitor, OfflineSync, HttpForge |
| Uploads | SmartUpload | MediaPipeline, FileVault, JobQueue, HttpForge (JSON around the file) |
| Background work | BackgroundTasks | JobQueue |
| Durable jobs | JobQueue | BackgroundTasks, SmartUpload |
| Failed API / telemetry / payment retries | RetryQueue | JobQueue, ApiResilience, BackgroundTasks |
| Offline data | OfflineSync | NetworkMonitor, BackgroundTasks |
| Auth tokens | SecureSession | SecureStoragePlus, ApiResilience, HttpForge |
| Encrypted files | FileVault | MediaPipeline, SecureStoragePlus |
| Push taps | PushRouter | DeepLinks |
| Telemetry suite | Observability | AppHealth, Diagnostics, NetworkMonitor |
| Visual-tree leak detection | LeakAnalyser | Diagnostics (optional breadcrumbs), Performance (timings) |
| BLE peripherals | BluetoothManager | PermissionFlow |
| Clipboard | ClipboardPlus | — |
| Device fingerprint / capabilities | DeviceInfoPlus | FeatureFlags, Diagnostics |
| NFC NDEF read/write | NfcPlus | DeviceInfoPlus (`HasNfc`) |
| App lock after background | AppLock | SecureSession (tokens), DeviceInfoPlus (`HasBiometric`), Biometric (one-shot prompt) |
| One-shot biometric / PIN | Biometric | AppLock (workflow), DeviceInfoPlus (`HasBiometric`) |
| Keep screen on | KeepAwake | — |
| Block screenshots / recents | ScreenGuard | AppLock (cover after background) |
| In-app store review | AppReview | AppUpdate (binary update) |
| Scheduled local notifications | LocalNotifications | PushRouter (remote FCM / APNs routing) |
| Circular geofence | Geofence | GeoLocator (on-demand GPS) |
| Classic Bluetooth SPP | BluetoothSerial | BluetoothManager (BLE GATT), Printing (ESC/POS documents) |
| Camera/gallery video pipeline | VideoPipeline | MediaPipeline (images), FileVault, SmartUpload |
| HttpClient TLS / SPKI pin | TlsPin | ApiResilience (retry), HttpForge (typed clients) |
| Form validation / `Validation.For` | FormValidation | — |
| Soft keyboard hide / show / dismiss / avoidance | KeyboardManager | FormValidation |
| Screen orientation lock / per-page landscape | DeviceOrientationPlus | — |

## Observability

`Plugin.Maui.Observability` is the only umbrella package. It depends on AppHealth, NetworkMonitor, ApiResilience, BackgroundTasks, OfflineSync, SmartUpload, and DeviceSession. Recommend it only when the user wants a unified export path.

## Repository inspection order for agents

1. Hub [README.md](../README.md) or [llms.txt](../llms.txt)
2. [Hardened releases](hardened-releases.md) when upgrading DeepLinks, PushRouter, SmartUpload, FeatureFlags, or the other September 2026 1.x ships
3. Matching plugin README
4. Plugin `llms.txt` / `AGENTS.md`
5. `src/` public types
6. `samples/` registration and platform files
7. `tests/` for expected error behavior
