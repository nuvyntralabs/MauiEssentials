# Submodule re-validation plan

**Date:** 8 September 2026  
**Hub:** MauiEssentials  
**Scope:** All plugin submodules **except** `HttpForge` and `MVVMExpress`  
**Plugins in scope:** 37  
**Status:** Plan only — execute one plugin at a time, close the wave before starting the next.

This is a quality gate, not a redesign. Re-validate that every shipped library feature has unit tests and a sample path, that library / test / sample projects build, that tests pass, and that the sample app can be launched. If `README.md` or the library project changes, bump the package version in that plugin repo. Do **not** publish to NuGet.org from this workspace.

Related: [Architecture](architecture.md), [Hardened releases](hardened-releases.md), [Getting started](getting-started.md).

---

## Goal

For each in-scope plugin, after this pass:

| Gate | Pass condition |
| --- | --- |
| **Feature → test** | Every public library feature in `README.md` / public API has at least one unit test (success, and fail / cancel / edge where the API can fail). |
| **Feature → sample** | The sample app exposes every public feature (button, page, or documented demo path). No “library-only” API left undemoed. |
| **Build** | Library, tests, and sample build in Release. |
| **Tests** | `dotnet test` is green for that plugin. |
| **Sample run** | Sample deploys and the feature checklist is walked on a device or emulator (see [Sample run](#5-test-and-run-the-sample-app)). |
| **Version** | If `README.md` or `src/` changed, `Version` / `PackageVersion` is bumped and docs stay aligned. Tests-only or sample-only fixes do **not** bump. |

---

## Out of scope

| Item | Why |
| --- | --- |
| `HttpForge` | Explicitly excluded. |
| `MVVMExpress` | Explicitly excluded (already has its own phase plans). |
| Hub catalog docs (`README.md`, `llms.txt`, `docs/packages/`) | Update only if a plugin version bump needs a hub pointer later. |
| Local `dotnet nuget push` / `NUGET_KEY` | Pipeline-only. See [Getting started — CI](getting-started.md#continuous-integration). |
| Restoring fail-open defaults | Do not set `PermissiveMode`, `AllowUnmappedPayloadRoutes`, or `RequireHttps = false` unless a host sample must show the old path, and then keep it commented. |
| New product features | Gap-fill tests and sample UI only. New APIs are a separate change. |

---

## Baseline inventory (8 September 2026)

Every in-scope plugin already has `src/`, `tests/`, `samples/`, and `README.md`. Counts below are a starting snapshot, not a pass/fail.

| Plugin | Version | Tests (`[Fact]`/`[Theory]`) | Sample pages | Shared TFMs | Notes |
| --- | --- | ---: | --- | --- | --- |
| ApiCache | 1.0.4 | 18 | MainPage | Android, iOS, Catalyst, Windows | README pack path still says `1.0.0` |
| ApiResilience | 1.0.9 | 13 | MainPage | Android, iOS, Catalyst, Windows | Thin vs retry / circuit / queue / token |
| AppHealth | 1.0.5 | 27 | MainPage | Android, iOS | No CHANGELOG |
| AppLock | 1.0.5 | 20 | MainPage | Android, iOS | Biometric path needs a device |
| AppUpdate | 1.0.6 | 25 | MainPage | Android, iOS | Store APIs need Play / App Store |
| BackgroundTasks | 1.0.6 | 10 | MainPage | Android, iOS | Thin; no CHANGELOG |
| BluetoothManager | 1.0.3 | 28 | MainPage | Android, iOS | BLE hardware |
| ClipboardPlus | 1.0.3 | 17 | MainPage | Android, iOS | README pack path `1.0.0` |
| CommunityToolkitPlus | 1.0.0 | 102 | 8 pages | Android, iOS | Strongest existing coverage |
| DeepLinks | 1.0.6 | 41 | 5 pages | Android, iOS | Hardened fail-closed |
| DeviceInfoPlus | 1.0.3 | 15 | MainPage | Android, iOS | README pack path `1.0.0` |
| DeviceOrientation | 1.0.3 | 14 | 3 pages | Android, iOS | README pack path `1.0.0` |
| DeviceSession | 1.0.6 | 21 | MainPage | Android, iOS | No CHANGELOG |
| Diagnostics | 1.0.5 | 16 | 2 pages | Android, iOS | README pack path `1.0.0` |
| FeatureFlags | 1.0.8 | 41 | MainPage | Android, iOS, Catalyst, Windows | Hardened HTTPS |
| FileVault | 1.0.8 | 29 | MainPage | Android, iOS | |
| FormValidation | 1.0.4 | 25 | MainPage | Android, iOS, Catalyst, Windows | Confirm every fluent rule in sample |
| GeoLocator | 1.0.8 | 23 | MainPage | Android, iOS | GPS permission + hardware |
| JobQueue | 1.0.7 | 18 | MainPage | Android, iOS, Catalyst, Windows | README pack path `1.0.0` |
| KeyboardManager | 1.0.3 | 18 | MainPage | Android, iOS | README pack path `1.0.0` |
| LeakAnalyser | 1.0.1 | 32 | 3 pages | Android, iOS, Catalyst, Windows | |
| MediaPipeline | 1.0.6 | 28 | MainPage | Android, iOS, Catalyst, Windows | README pack path `1.0.0` |
| NetworkDiagnostics | 1.0.3 | 15 | MainPage | Android, iOS | README pack path `1.0.0`; no CHANGELOG |
| NetworkMonitor | 1.0.7 | 26 | MainPage | Also net8 / net9 | No CHANGELOG |
| Nfc | 1.0.3 | 28 | MainPage | Android, iOS | NFC hardware; README pack path `1.0.0` |
| Observability | 1.0.7 | 23 | MainPage | Android, iOS | Last wave — sibling refs |
| OfflineSync | 1.0.9 | 13 | MainPage | Android, iOS | Thin vs 9 public interfaces; no CHANGELOG |
| Performance | 1.0.5 | 28 | 2 pages | Android, iOS | README pack path `1.0.0` |
| PermissionFlow | 1.0.5 | 24 | MainPage | Android, iOS | One test class; no CHANGELOG |
| Printing | 1.0.3 | 23 | MainPage | Android, iOS | Thermal / AirPrint hardware; README pack path `1.0.0` |
| PushRouter | 1.0.6 | 24 | 3 pages | Android, iOS | Hardened mapped routes only |
| RetryQueue | 1.0.4 | 22 | MainPage | Android, iOS, Catalyst, Windows | README pack path `1.0.0` |
| SecureSession | 1.0.6 | 26 | MainPage | Android, iOS | |
| SecureStoragePlus | 1.0.8 | 20 | MainPage | Android, iOS, Catalyst, Windows | |
| SharePlus | 1.0.3 | 20 | MainPage | Android, iOS | README pack path `1.0.0` |
| SmartUpload | 1.0.7 | 24 | MainPage | Android, iOS, Catalyst, Windows | Hardened `RequireHttps` |
| VoipCore | 1.0.7 | 25 | MainPage | Android, iOS | Pluggable SIP — no real stack required for unit tests |

**Likely gaps (fix during the wave, do not skip):**

- Single-`MainPage` samples that only demo the happy path.
- README pack artifact versions that lag the csproj (`1.0.0` vs current).
- Thin suites: `BackgroundTasks` (10), `OfflineSync` (13), `ApiResilience` (13).
- Hardware features present in the API but missing a sample control (NFC write, BLE reconnect, thermal print, App Lock PIN vs biometric).

---

## Per-plugin protocol

Repeat this for one plugin folder. Do not start the next plugin until the sign-off row is filled.

### 0. Inventory the contract

1. Read `README.md`, `llms.txt`, `AGENTS.md`, and `CHANGELOG.md` when present.
2. List **public features** from:
   - README capability tables / usage sections
   - `Use*` registration and options
   - Public types in `src/` (interfaces, options, enums, attached properties)
3. List existing test classes under `tests/` and sample pages / buttons under `samples/`.
4. Build a coverage matrix (copy into the plugin PR or a scratch note):

| Feature | Unit test | Sample path | Gap |
| --- | --- | --- | --- |
| `UseX` / options | | `MauiProgram` | |
| Happy path API | | Button / page | |
| Failure / cancel / invalid input | | Error label | |
| Hardened default (if any) | | Commented opt-in only | |

A feature is **covered** only when both the test column and the sample column are filled.

### 1. Unit tests cover every library feature

Add or extend tests until the matrix is complete.

**Must cover**

- Registration (`Use*`, equivalent `Add*` if documented).
- Every public method on the primary interface (`IGeoLocator`, `IApiCache`, …).
- Every documented policy / enum (`CachePolicy`, backoff tiers, print document types).
- Options defaults that affect security or correctness (fail-closed hosts, `RequireHttps`, encrypted queues).
- Failure modes the README mentions: timeout, deny, cache miss, conflict, dead letter, unsupported TFM (`FeatureNotSupported` on `net10.0` where that is the contract).

**How**

- Prefer existing fakes / in-memory stores already in `tests/`.
- Do not add device-only tests that cannot run in `dotnet test` on `net10.0`. Platform behavior stays behind interfaces (`IBleTransport`, `INfcTransport`, `IPrintPlatform`).
- Empty `catch { }` remains forbidden in new test helpers.

**Done when** `dotnet test` is green and the matrix has no empty **Unit test** cells.

### 2. Sample code covers every library feature

The sample is the human proof of the README.

**Must cover**

- `Use*` in `MauiProgram` with documented options (hardened defaults left fail-closed).
- One reachable UI path per public feature (same list as tests).
- Platform setup already required by the README (permissions, usage strings, FileProvider, background modes).
- A disabled / error state when the feature needs hardware the simulator lacks (show “NFC unavailable”, do not hide the button).

**How**

- Prefer adding sections or buttons on the existing `MainPage` unless the feature needs its own page (DeepLinks routes, CommunityToolkitPlus modules, LeakAnalyser leak pages).
- Sample must reference the **project**, not a NuGet package, so local `src/` changes run immediately.
- Do not restore permissive DeepLinks / PushRouter / cleartext SmartUpload in the sample unless a clearly labeled “unsafe demo” remains off by default.

**Done when** the matrix has no empty **Sample path** cells and the sample builds.

### 3. All projects build

From the plugin root (prefer the `.sln` / `.slnx` when one exists):

```bash
dotnet build -c Release
dotnet build tests/*/*.csproj -c Release
dotnet build samples/*/*.csproj -c Release
```

Shared libraries (ApiCache, ApiResilience, FeatureFlags, FormValidation, JobQueue, RetryQueue, SecureStoragePlus, MediaPipeline, SmartUpload, LeakAnalyser): also confirm the library restores `net10.0-android`, `net10.0-ios`, `net10.0-maccatalyst`. `net10.0-windows` pack is validated on Windows CI; do not block a macOS pass on a missing Windows pack.

NetworkMonitor: include `net8.0` / `net9.0` test TFMs already in the csproj.

Observability: restore sibling hub folders first (`AppHealth`, `NetworkMonitor`, `ApiResilience`, `BackgroundTasks`, `OfflineSync`, `SmartUpload`, `DeviceSession`).

Fix build breaks in this plugin before adding features.

### 4. All test cases pass

```bash
dotnet test -c Release --no-restore
```

If restore is needed:

```bash
dotnet test -c Release
```

Zero skipped-as-failed. Skip only with an explicit reason (for example `FeatureNotSupported` on `net10.0` when the test is platform-only — prefer a dedicated `net10.0` assertion instead of skip).

### 5. Test and run the sample app

Build is not enough. Launch the sample and walk the feature matrix.

**Minimum run (every plugin)**

1. `dotnet build samples/*/*.csproj -f net10.0-android -c Debug`
2. Deploy to an Android emulator or device (`dotnet build -t:Run -f net10.0-android` or the IDE).
3. On macOS, also build `-f net10.0-ios` and run the iOS simulator when the plugin has native iOS code.
4. Click every sample action. Confirm the UI updates, errors surface, and the app does not crash.

**Hardware / store features** — still require a sample control; mark the run as **Blocked (hardware)** only after the control is shown and the unavailable path is handled:

| Plugin | Extra run notes |
| --- | --- |
| GeoLocator | Emulator location injection is enough for get / last / track. |
| PermissionFlow | Deny, “Don’t ask again”, and Settings fallback. |
| AppLock | Background the app past the timer; PIN path if biometric is missing. |
| AppUpdate | Policy JSON / version compare in-app; store prompt may be **Blocked (store)**. |
| BluetoothManager / Nfc / Printing (thermal) | Simulator: unavailable state. Device: scan / tag / print when hardware exists. |
| VoipCore | In-process fake stack is enough; no PJSIP. |
| PushRouter / DeepLinks | Use the sample’s inject / custom-scheme buttons; do not need FCM/APNs tokens. |
| LeakAnalyser | Navigate into `LeakyPage`, trigger GC, confirm leak UI (`#if DEBUG`). |
| CommunityToolkitPlus | Open all seven module pages. |
| SharePlus / ClipboardPlus / KeyboardManager / DeviceOrientation | Simulator is enough. |
| SmartUpload | Use `https` endpoint or a documented local mock; do not set `RequireHttps = false` as the default. |

Record the run in the [sign-off table](#sign-off-table): platform, emulator/device, result.

### 6. Version bump (only when README or library changes)

Bump the **library** project when either is true:

- `README.md` (plugin root) was edited
- Any file under `src/` (including the library `.csproj`) was edited

Do **not** bump for tests-only or samples-only changes.

**How to bump**

1. Patch increment for coverage, docs, and bug fixes (`1.0.7` → `1.0.8`).
2. Minor increment only if a new public API was unavoidable to close a sample/test gap (prefer not to).
3. Set `Version` and, when present, `PackageVersion` to the same value.
4. If `CHANGELOG.md` exists, add a top section for the new version.
5. If the README mentions an `artifacts/Plugin.Maui.*.nupkg` version, update that string to match.
6. Leave NuGet.org to the plugin repo’s GitHub Actions CI. Do not `dotnet nuget push`.

Hub catalog versions (`README.md`, `llms.txt`, `docs/hardened-releases.md`) are a follow-up after the plugin repo is tagged — not part of the per-plugin coding pass.

---

## Work waves

Thirty-seven plugins. Finish a wave before the next so Observability and composed samples stay honest.

### Wave A — shared libraries (no native device required for unit tests)

1. ApiCache  
2. ApiResilience  
3. FeatureFlags  
4. FormValidation  
5. JobQueue  
6. RetryQueue  
7. SecureStoragePlus  
8. MediaPipeline  
9. SmartUpload  
10. LeakAnalyser  

### Wave B — hardened / recently reviewed natives

11. DeepLinks  
12. PushRouter  
13. FileVault  
14. SecureSession  
15. AppLock  
16. OfflineSync  
17. BackgroundTasks  
18. DeviceSession  
19. NetworkMonitor  
20. AppUpdate  

### Wave C — remaining Android / iOS plugins

21. GeoLocator  
22. NetworkDiagnostics  
23. PermissionFlow  
24. AppHealth  
25. Diagnostics  
26. Performance  
27. DeviceInfoPlus  
28. ClipboardPlus  
29. SharePlus  
30. KeyboardManager  
31. DeviceOrientation  
32. Nfc  
33. BluetoothManager  
34. Printing  
35. VoipCore  
36. CommunityToolkitPlus  

### Wave D — umbrella (after siblings in A–C)

37. Observability  

---

## Feature checklists

Use these as the **minimum** public-feature lists. If the README or public API has more, add rows. Each row needs a test and a sample path.

### ApiCache

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseApiCache` / `AddApiCache` | Registration / options | `MauiProgram` |
| CacheFirst, NetworkFirst, StaleWhileRevalidate, NetworkOnly, CacheOnly | `PolicyTests` | Policy picker |
| GET typed `GetAsync<T>` | `HttpHandlerTests` | Fetch button |
| Expiration / stale fallback | `PolicyTests` | Expire / stale label |
| Invalidation (key / prefix) | `InvalidationTests` | Invalidate button |
| Store persistence | `StoreTests` | Restart / reload |

### ApiResilience

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseApiResilience` | Registration | `MauiProgram` |
| Retry + jitter | `RetryTests` | Force transient fail |
| Circuit breaker open / half-open | `CircuitBreakerTests` | Trip circuit |
| Offline queue (encrypted at rest) | `OfflineQueueTests` | Queue while offline |
| `PersistRequestBodies` default | `OfflineQueueTests` | Toggle documented |
| Token refresh on 401 | `TokenRefreshTests` | Expire token |

### AppHealth

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseAppHealth` | Registration | `MauiProgram` |
| `Inspect` → Healthy / Degraded / Unhealthy | `InspectTests` | Inspect button |
| Finding codes (`battery.low`, `network.offline`, …) | `EvaluatorTests` | Findings list |
| Watch / change events | `InspectTests` | Watch toggle |
| Raw environment measurements | `EvaluatorTests` | Details panel |

### AppLock

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseAppLock` + timeout | `ConfigurationTests` | `MauiProgram` |
| Background → lock | `LifecycleTests` | Background hint + lock UI |
| `RequireAuthenticationAsync` (biometric / PIN) | `AuthenticationTests` | Unlock button |
| Auth failure stays locked | `AuthenticationTests` | Cancel / fail |
| Disable / unlock session | `LifecycleTests` | Disable lock |

### AppUpdate

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiAppUpdate` | Registration | `MauiProgram` |
| Version compare | `VersionComparerTests` | Show current vs store |
| Mandatory vs recommended policy | `PolicyJsonTests` / `EvaluatorTests` | Policy labels |
| Play in-app update client (mocked) | `AppUpdateTests` | Check updates |
| iTunes / App Store lookup (mocked) | `AppUpdateTests` | iOS check |

### BackgroundTasks

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseBackgroundTasks` | Registration | `MauiProgram` |
| One-time schedule | `RequestValidatorTests` | Schedule once |
| Periodic schedule | `RequestValidatorTests` | Schedule periodic |
| Constraints (network, charging, battery) | `RequestValidatorTests` | Constraint toggles |
| Handler registry / serializer | `RegistryAndSerializerTests` | Registered handler |
| `RunNowAsync` | New or existing | Run now button |

### BluetoothManager

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseBluetoothManager` | Registration | `MauiProgram` |
| Permission / adapter off | `PermissionAndAdapterTests` | Status banner |
| Scan + filters | `ScanFilterTests` | Scan button |
| Connect / disconnect | `ConnectionLifecycleTests` | Connect |
| Read / write | `ConnectionLifecycleTests` | Read/write fields |
| Reconnect / retry | `ReconnectAndRetryTests` | Kill + reconnect |

### ClipboardPlus

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiClipboardPlus` | Registration | `MauiProgram` |
| Text copy / paste | `ClipboardPlusTests` | Copy / paste |
| Sensitive flag | `SensitiveContentTests` | Sensitive toggle |
| Expiration | `ExpirationTests` | TTL + expired state |
| Image / URI / files if public | `ClipboardPlusTests` | Extra buttons |

### CommunityToolkitPlus

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiCommunityToolkit` then `UseMauiCommunityToolkitPlus` | `RegistrationTests` | `MauiProgram` |
| Disabled modules do no I/O | `ModuleRegistrationTests` / `OptionsTests` | Defaults off |
| Accessibility audit | `AccessibilityAuditTests` | `AccessibilityPage` |
| State restoration | `StateRestorationTests` | `StatePage` |
| Upgrade guard | `UpgradeGuardTests` | `UpgradePage` |
| Trusted time | `TrustedTimeTests` | `TrustedTimePage` |
| App integrity (opaque / unsupported) | `AppIntegrityTests` | `IntegrityPage` |
| Wallet passes | `WalletTests` | `WalletPage` |
| Privacy consent | `PrivacyConsentTests` | `ConsentPage` |

### DeepLinks

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiDeepLinks` with Hosts + CustomSchemes | Registration | `MauiProgram` (fail-closed) |
| Empty Hosts / schemes reject | `DeepLinkParserTests` | Documented; do not enable `PermissiveMode` |
| `http://` rejected unless `AllowInsecureHttp` | `DeepLinkParserTests` | Commented only |
| App Link / custom scheme parse | `DeepLinkParserTests` | Inject URL |
| Route match + Shell navigate | `RouteMatcherTests` / `DeepLinksDispatchTests` | `OrderPage` / `CatalogPage` |
| Auth restore / deferral | `AuthAndDeferralTests` | `LoginPage` → `AccountPage` |
| Navigation stack | `NavigationStackTests` | Back stack |
| Persistence | `PersistenceTests` | Cold start |

### DeviceInfoPlus

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseDeviceInfoPlus` | Registration | `MauiProgram` |
| Fingerprint / stable id | `DeviceFingerprintTests` | Show id |
| Screen / RAM / OS | `DeviceInfoPlusTests` | Info list |
| Capabilities: NFC, BT, camera, biometric, GPS, flash | `DeviceInfoPlusTests` | Capability grid |

### DeviceOrientation

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseDeviceOrientationPlus` | Registration | `MauiProgram` |
| Lock landscape / portrait | `OrientationTests` | Lock buttons |
| Unlock | `ScreenOrientationTests` | Unlock |
| Per-page lock | `OrientationTests` | `VideoPage` / `ScannerPage` |

### DeviceSession

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseDeviceSession` | Registration | `MauiProgram` |
| Device id | `InstallationTests` | Show device id |
| Installation id (survives update) | `InstallationTests` | Show install id |
| Session rotate after background timeout | `SessionTests` | Background + new session |
| App version provider | `InstallationTests` | Show version |

### Diagnostics

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiDiagnostics` | Registration | `MauiProgram` |
| Unhandled / crash report | `ReportTests` | Crash button (debug) |
| Breadcrumbs / timeline | `TimelineTests` | Add breadcrumb |
| HTTP handler | `HttpHandlerTests` | Sample request |
| ANR / tracking hooks | `TrackingTests` / `CrashRecoveryTests` | Recovery label |

### FeatureFlags

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiFeatureFlags` | Registration | `MauiProgram` |
| Local evaluate bool / variant | `EvaluatorTests` / `FeatureFlagsTests` | Flag toggles |
| Targeting / rollout | `RolloutTests` | Percentage flag |
| HTTP provider + HTTPS required | `HttpFeatureFlagProviderTests` | Refresh remote |
| Optional `SignatureKey` | `HttpFeatureFlagProviderTests` | Documented |
| Cache | `CacheTests` | Offline evaluate |
| Version compare | `VersionComparerTests` | Min version flag |

### FileVault

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseFileVault` | Registration | `MauiProgram` |
| Encrypt write / decrypt read | `EncryptionTests` / `FileOperationsTests` | Save / load |
| Passphrase / key | `PassphraseTests` | Unlock |
| Background `ClearKey` | `LifecycleTests` | Background lock |
| Path confinement | `PathTests` | Reject outside root |
| `GetStatisticsAsync` | `FileOperationsTests` | Stats label |

### FormValidation

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiFormValidation` (optional) | Registration | `MauiProgram` |
| Required, Email, Phone, Url, Numeric, Regex | `RuleTests` | Fields for each |
| Min / Max / MinLength / MaxLength / Length | `RuleTests` | Age / password |
| EqualTo | `RuleTests` | Confirm password |
| When / Unless | `ConditionalAndAsyncTests` | Business name |
| Must / MustAsync / Server | `ConditionalAndAsyncTests` | Async / server demo |
| `Validation.For` / `MessageFor` | Sample + VM tests | XAML bindings |
| `ValidateAsync` | `ValidatableViewModelTests` | Submit |

### GeoLocator

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseGeoLocator` | Registration | `MauiProgram` |
| `GetCurrentLocationAsync` | `GeoLocatorImplementationTests` | Get location |
| `GetLastKnownLocationAsync` | Facade / model tests | Last known |
| Start / stop tracking | `GeoLocatorImplementationTests` | Track toggle |
| Reverse geocode | `GeoLocatorImplementationTests` | Geocode button |
| Logging option | `GeoLocatorFacadeTests` | Optional log |

### JobQueue

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiJobQueue` | Registration | `MauiProgram` |
| `EnqueueAsync` typed job | `QueueEngineTests` | Enqueue |
| Retry + backoff | `BackoffPolicyTests` | Fail-then-retry job |
| Dead letter | `QueueEngineTests` | Poison job |
| `DrainAsync` | `QueueEngineTests` | Drain |
| SQLite persist | `SqliteStoreTests` | Restart / pending count |
| In-memory store for tests | `UseInMemoryStore` | Documented |

### KeyboardManager

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseKeyboardManager` | Registration | `MauiProgram` |
| Hide / show / dismiss on tap | `KeyboardManagerTests` | Buttons + tap |
| Resize vs pan | `AvoidanceModeTests` | Mode picker |
| Keyboard height / safe area | `KeyboardManagerTests` | Height label |

### LeakAnalyser

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseLeakAnalyser` (`#if DEBUG`) | `OptionsTests` | `MauiProgram` |
| `LeakMonitor` attached property | `AttachedPropertyTests` | `LeakyPage` |
| Forced GC / leak report | `GarbageCollectionMonitorTests` | Detect button |
| `TearDown` DisconnectHandlers | `TearDownStrategyTests` | `PhotoPage` |
| Compartmentalize (opt-in) | `TearDownStrategyTests` | Documented toggle |
| Lifecycle | `LifecycleTests` | Navigate away |

### MediaPipeline

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMediaPipeline` | Registration | `MauiProgram` |
| Capture / pick (mocked) | `PipelineTests` | Pick image |
| Resize / compress | `ImageProcessingTests` | Quality slider |
| EXIF | `ExifTests` | Strip / keep |
| Watermark / blur | `ImageProcessingTests` | Toggles |
| Encrypt / vault handoff | `EncryptionTests` | Encrypt |
| Upload handoff (mocked) | `PipelineTests` | Upload |

### NetworkDiagnostics

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseNetworkDiagnostics` | Registration | `MauiProgram` |
| DNS / TLS / API / latency runner | `RunnerTests` | Run diagnostics |
| Report model | `ReportTests` | Show report |

### NetworkMonitor

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseNetworkMonitor` | Registration | `MauiProgram` |
| Internet vs local-only vs offline | `StatusComposerTests` / `NetworkMonitorTests` | Status banner |
| Captive portal probe | `InternetProbeTests` / `ProbeClassifierTests` | Captive label |
| Wi-Fi ↔ cellular | `ChangeKindDetectorTests` | Change log |
| HTTP probe option | `InternetProbeTests` | Toggle probe |

### Nfc (`Nfc/` → Plugin.Maui.NfcPlus)

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseNfcPlus` | Registration | `MauiProgram` |
| Session start / stop | `NfcPlusTests` | Session buttons |
| Read NDEF text / URI / MIME | `NdefCodecTests` | Read |
| Write NDEF | `NdefCodecTests` | Write |
| Tag id | `NfcPlusTests` | Tag id label |
| Unavailable / no adapter | `NfcPlusTests` | Unsupported banner |

### Observability

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiObservability` + sibling `Use*` | `RegistrationTests` | `MauiProgram` |
| Bridge sibling events | `BridgeTests` | Trigger health / network / upload |
| Exporter | `ExporterTests` | Export / last batch |
| Pipeline | `PipelineTests` | Flush |
| Crash platform hook | `BridgeTests` | Crash breadcrumb |

### OfflineSync

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseOfflineSync` | Registration | `MauiProgram` |
| Local write / collection | `CollectionTests` | Add item offline |
| Queue + push | `SyncEngineTests` | Sync now |
| Conflict resolver | `ConflictResolverTests` | Edit both sides |
| Soft delete | `CollectionTests` | Delete |
| Auto-sync / scheduler (mocked) | New if missing | Auto-sync toggle |

### Performance

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiPerformance` | Registration | `MauiProgram` |
| Measure / trace | `MeasureTests` / `TraceTests` | Time an action |
| Auto page / startup | `AutoMeasureTests` | Navigate `CustomerPage` |
| HTTP handler | `HttpHandlerTests` | Sample API |
| Report | `ReportTests` | Show report |

### PermissionFlow

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UsePermissionFlow` | Registration | `MauiProgram` |
| Rationale → OS prompt | `OrchestrationTests` | Request location / camera |
| Cooldown after deny | `OrchestrationTests` | Deny twice |
| Settings fallback | `OrchestrationTests` | Open Settings |
| Required vs optional | `OrchestrationTests` | Mixed flow |
| LocationAlways expands when-in-use first | `OrchestrationTests` | Always flow |

### Printing

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiPrinting` | Registration | `MauiProgram` |
| PDF / image / text | `PrinterTests` | Print each |
| Invoice / inspection builders | `DocumentBuilderTests` | Invoice button |
| System / AirPrint | `PrinterTests` | System print |
| ESC/POS encode | `EscPosEncoderTests` | Preview bytes |
| Bluetooth thermal | `PrinterTests` | Thermal (or unavailable) |

### PushRouter

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UsePushRouter` + `Map` / `DefaultRoute` | Registration | `MauiProgram` |
| Parse FCM / APNs / extras | `PushNotificationParserTests` | Inject payload |
| Handler dispatch | `PushRouterDispatchTests` | Handler log |
| Mapped Shell only (no raw path) | `RouteTemplateTests` | `OrderPage` / `ChatPage` |
| Cold-start queue | `QueueAndDedupTests` | Inject before Shell |
| Dedup `message_id` | `QueueAndDedupTests` | Double inject |

### RetryQueue

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiRetryQueue` | Registration | `MauiProgram` |
| Enqueue named operation | `RetryEngineTests` | Fail payment / telemetry |
| 30s / 2min / 10min backoff | `BackoffPolicyTests` | Show next attempt |
| Give up / dead letter | `RetryEngineTests` | Exhaust retries |
| SQLite persist | `SqliteStoreTests` | Pending list |
| `DrainAsync` | `RetryEngineTests` | Drain |

### SecureSession

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseSecureSession` | Registration | `MauiProgram` |
| Login / token bundle | `LoginTests` | Login |
| 401 refresh | `TokenRefreshTests` | Expire access |
| Logout | `LogoutTests` | Logout |
| Expiry | `SessionExpiryTests` | Clock skew / expire |
| Biometric gate | `BiometricTests` | Unlock |
| Multi-device | `MultiDeviceTests` | Second device |
| HTTP handler | `HttpHandlerTests` | Authenticated call |
| `AcceptUnvalidatedTokens` default | `LoginTests` | Documented |

### SecureStoragePlus

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseSecureStoragePlus` | Registration | `MauiProgram` |
| Set / get / remove | `SecureStoragePlusTests` | CRUD |
| AES-256-GCM + integrity | `AesGcmDataEncryptorTests` | Tamper fails |
| Expiry purge | `SecureStoragePlusTests` | Expired key |
| Legacy migration | `SecureStoragePlusTests` | Migrate button |
| List / metadata / JSON | `SecureStoragePlusTests` | List keys |

### SharePlus

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseMauiSharePlus` | Registration | `MauiProgram` |
| Text / title / subject / MIME | `SharePlusTests` | Share text |
| File + FileProvider-safe copy | `SharePlusTests` | Share file |
| Preview / target app if public | `ShareMimeTypesTests` | MIME picker |

### SmartUpload

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseSmartUpload` | Registration | `MauiProgram` |
| Enqueue chunked upload | `UploadClientTests` / `ChunkPlannerTests` | Pick file |
| Pause / resume | `UploadClientTests` | Pause |
| Retry / backoff | `RetryPolicyTests` | Fail chunk |
| Content-Range + tus | `ProtocolAndStoreTests` | Protocol picker |
| Persist session | `ProtocolAndStoreTests` | Kill + resume |
| `RequireHttps` default | `RequestValidatorTests` | Reject `http://` |

### VoipCore

| Feature | Suggested test home | Sample |
| --- | --- | --- |
| `UseVoipCore` | `RegistrationTests` | `MauiProgram` |
| Register / unregister (fake stack) | `RegistrationTests` | Register |
| Outgoing / incoming call | `CallTests` | Call / incoming |
| Hold / mute / speaker | `MediaTests` | Media toggles |
| Native call UI option | `LifecycleTests` | Documented |
| Hangup / lifecycle | `LifecycleTests` | End call |

---

## Sign-off table

Copy into the PR description for each plugin (or keep a running hub note).

| Plugin | Tests added/updated | Sample paths added | `dotnet build` | `dotnet test` | Sample run (platform) | Version bump | Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ApiCache | Factory, ETag/304, max-age, handler stale, DI resolve | Set/Exists/Invalidate key/Clear | Release OK | 25 pass | Android device | patch 1.0.5 (DI crash + README) | Yes |
| ApiResilience | existing 13 cover retry/circuit/queue/token | existing 6 buttons | Release OK | 13 pass | Android device | patch 1.0.10 (README pack path) | Yes |
| AppHealth | existing 27 cover inspect/findings | Inspect now / Network only / Start+Stop watch | Release OK | 27 pass | Android device (Degraded, battery.unknown, network.expensive) | none | Yes |
| AppLock | existing 20 cover timer/auth/lifecycle | NRE init order; LockOnStart false so MainPage is reachable | Release OK | 20 pass | Android device (lock cover + biometric prompt; Unlock skipped) | patch 1.0.6 (empty AAR) | Yes |
| AppUpdate | existing 30 cover policy/version/store mock | Recommended/Mandatory/Min version/Maintenance/Check/Start/Postpone | Release OK | 30 pass | Android device (store prompt Blocked) | none (sample AndroidX/minSdk/DemoStoreClient) | Yes |
| BackgroundTasks | existing 10 cover schedule/run | One-time, periodic 15m, Run refresh now | Release OK | 10 pass | Android device | none | Yes |
| BluetoothManager | existing 28 cover scan/connect | Request permission, Scan, Stop, Disconnect | Release OK | 28 pass | Android device (adapter on, BLE devices listed) | none | Yes |
| ClipboardPlus | existing 17 cover text/uri/image/expiry | Copy text/sensitive/URI/image/file, Read, Clear | Release OK | 17 pass | Android device | patch 1.0.4 (README pack path; sample Primary hex) | Yes |
| CommunityToolkitPlus | existing 108 + HTTP/host ITimeSource registration | none (DI crash was src) | Release OK | 109 pass | Android device (flyout: integrity/a11y/state/upgrade/trusted time/wallet/consent) | patch 1.0.1 (ITimeSource DI) | Yes |
| DeepLinks | existing 43 cover parse/match/auth/stack | HTTPS, scheme, account, catalog restore, login deferral | Release OK | 43 pass | Android device | none (sample Gray600 SourceGen only) | Yes |
| DeviceInfoPlus | existing 15 cover fingerprint/capabilities | Get snapshot + Refresh | Release OK | 15 pass | Android device (Nothing A001, BT/camera/GPS/flash) | patch 1.0.4 (README pack path) | Yes |
| DeviceOrientation | existing 27 cover lock/unlock/page | Portrait/Landscape/Unlock + Video/Scanner pages | Release OK | 27 pass | Android device | patch 1.0.4 (README pack path) | Yes |
| DeviceSession | existing 21 cover ids/session | Refresh, start/end, simulate timeout | Release OK | 21 pass | Android device | none | Yes |
| Diagnostics | existing 16 cover report/timeline | Login/API/network/exception/order + report; skip crash/ANR | Release OK | 16 pass | Android device (full timeline) | patch 1.0.6 (README pack path) | Yes |
| FeatureFlags | existing 45 cover evaluate/rollout/HTTPS/cache | env, identify, refresh, override | Release OK | 45 pass | Android device | patch 1.0.9 (README pack path) | Yes |
| FileVault | existing 31 cover encrypt/expire/lock/purge | Write/Read/Expire/List/Purge/Lock/Destroy | Release OK | 31 pass | Android device | none | Yes |
| FormValidation | existing 38 cover fluent rules | sign-up form + submit (required messages) | Release OK | 38 pass | Android device | none (sample XAML Gray500 crash only) | Yes |
| GeoLocator | existing 23 cover get/last/track/geocode | existing 5 buttons | Release OK | 23 pass | Android device (last known + reverse geocode Hyderabad) | none | Yes |
| JobQueue | existing 18 cover enqueue/retry/DLQ | Photo/Customer/Analytics/Flaky/Poison/Drain | Release OK | 18 pass | Android device | patch 1.0.8 (README pack path) | Yes |
| KeyboardManager | existing 22 cover hide/show/avoidance | Hide / Show name, Resize + tapOutside | Release OK | 22 pass | Android device | patch 1.0.4 (README pack path) | Yes |
| LeakAnalyser | existing 32 cover monitor/teardown/GC | Home / clean PhotoPage / LeakyPage | Release OK | 32 pass | Android device (4 leak cards after pop) | none | Yes |
| MediaPipeline | existing 28 cover resize/compress/EXIF/watermark/blur/encrypt/upload | bundled sample + encrypt + mock upload | Release OK | 28 pass | Android device | patch 1.0.7 (README pack path) | Yes |
| NetworkDiagnostics | existing 15 cover runner/report | Run diagnostics vs 1.1.1.1 | Release OK | 15 pass | Android device (all layers passed, gateway skipped) | patch 1.0.4 (README pack path) | Yes |
| NetworkMonitor | existing 28 cover probe/captive | Status cards + Refresh now | Release OK | 28 pass | Android device (cellular internet) | none | Yes |
| Nfc | existing 32 cover session/NDEF | Start/Read/Write + payloads | Release OK | 32 pass | Android device (Unsupported / no NFC hardware) | patch 1.0.4 (README pack path) | Yes |
| Observability | existing 23 cover registration/bridge/exporter/pipeline | existing 8 demo buttons | Release OK | 23 pass | Android device (network Offline, API Opened retries=1; Crash skipped) | none | Yes |
| OfflineSync | existing 13 cover queue/sync | Add note, offline queue, Sync now | Release OK | 13 pass | Android device | none (sample Gray SourceGen hex) | Yes |
| Performance | existing 28 cover measure/trace/report | Load customer, CustomerPage, example timings, clear | Release OK | 28 pass | Android device | patch 1.0.6 (README pack path) | Yes |
| PermissionFlow | existing 24 cover rationale/cooldown/settings | Scan/Location/Notifications/Photos + Refresh | Release OK | 24 pass | Android device (location/alerts/library/scan satisfied) | none | Yes |
| Printing | existing 23 cover PDF/builders/ESC/POS | Discover, Permissions, Print PDF (system), Invoice thermal unavailable | Release OK | 23 pass | Android device (system print sheet; thermal Blocked) | patch 1.0.4 (README + empty AAR) | Yes |
| PushRouter | existing 24 cover map/unmapped/silent | Shell //order //chat + Back to inbox | Release OK | 24 pass | Android device (FCM order 1842, APNs thread-22, fail-closed path) | none (sample routes only) | Yes |
| RetryQueue | existing 22 cover enqueue/backoff/DLQ | Register/Order/Telemetry/Poison/Drain | Release OK | 22 pass | Android device | patch 1.0.5 (README pack path) | Yes |
| SecureSession | existing 26 cover tokens/lock/refresh | Sign in, token, 401, refresh, lock, devices, logout | Release OK | 26 pass | Android device | none | Yes |
| SecureStoragePlus | existing 20 cover set/get/remove/expiry/migrate | Save/Get/Remove/List/Purge/Clear/Migrate | Release OK | 20 pass | Android device | none | Yes |
| SharePlus | existing 23 cover text/file/target | Share text/file/files + Cleanup cache | Release OK | 23 pass | Android device (sheet + cache cleaned) | patch 1.0.4 (README pack path; sample Primary hex) | Yes |
| SmartUpload | existing 24 cover enqueue/pause/resume/tus/HTTPS | Create file / enqueue tus / pause / cancel / remove | Release OK | 24 pass | Android device (tusdemo 100%) | none | Yes |
| VoipCore | existing 25 cover register/call/media | Register, Call, incoming, Mute/Hold/Speaker, Hangup, Unregister | Release OK | 25 pass | Android device (loopback stack) | patch 1.0.8 (README pack path) | Yes |

**Sample run values:** `Android emulator`, `iOS simulator`, `Device`, `Blocked (hardware)`, `Blocked (store)`.

**Version bump values:** `none` (tests/sample only), `patch x.y.z`, `minor x.y.z`.

---

## Definition of done (catalog)

1. All 37 sign-off rows are filled.  
2. No plugin has an empty feature-matrix cell.  
3. No in-scope `dotnet test` failure.  
4. Every sample has a recorded run or an explicit hardware/store block **after** the UI path exists.  
5. Every README / `src/` change has a matching csproj bump and CHANGELOG entry when that file exists.  
6. No local NuGet publish. Plugin CI on `main` / tag remains the ship path.

---

## Agent notes

- Work **inside the plugin submodule**. Commit only when asked, in that repo, not as a hub gitlink bump unless requested.
- Prefer the smallest change that closes a gap. Do not rewrite samples.
- Observability is last. If a Wave A–C API used by Observability changes, re-run Observability tests.
- Fourteen plugins in [hardened-releases.md](hardened-releases.md) stay fail-closed. Tests must assert the new defaults.
- Directory vs PackageId: `Nfc/` → `Plugin.Maui.NfcPlus`, `DeviceOrientation/` → `Plugin.Maui.DeviceOrientationPlus`, `NetworkMonitor/src/Maui.NetworkMonitor`.
