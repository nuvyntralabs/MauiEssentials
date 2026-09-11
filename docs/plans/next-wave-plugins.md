# Next-wave plugins — design plan

**Status:** Implemented in the hub (source, tests, samples). Separate plugin remotes and nuget.org `1.0.0` nupkgs are not published yet.  
**Wave:** MauiEssentials next-wave runtime plugins (post MauiDev 1.2 / desktop MVVMExpress 1.0)  
**Catalog:** [MauiEssentials](https://github.com/nuvyntralabs/MauiEssentials)  
**Authoring rule:** one independent git repository, NuGet package, and hub submodule per plugin — same model as GeoLocator, AppLock, and BluetoothManager.

This document is the seed for each new repo’s `ARCHITECTURE.md` / `API-DESIGN.md` / `README.md`. Do not generate nine frameworks in one change. Ship Wave 1 first. Publishing stays in GitHub Actions. Never `dotnet nuget push` from this workspace.

Barcode / QR scanning is **out of this wave**. Do not add a scanner package, sample page, or catalog row while executing this plan.

Usual alternatives stay the .NET MAUI built-ins, CommunityToolkit.Maui, Plugin.LocalNotification, Plugin.Fingerprint, Shiny, Play Core, StoreKit, and Polly. Recommend a new plugin only when those do not already solve the host’s problem.

---

## 1. Problem

The catalog already covers field GPS, offline sync, BLE GATT, NFC NDEF, image pipelines, app lock, token sessions, HTTP resilience, and push **routing**. Production hosts still reimplement a second row of native plumbing that MAUI does not ship and that existing plugins explicitly refuse:

| Host still writes | Closest shipped plugin | Why it is not enough |
| --- | --- | --- |
| One-shot Face ID / fingerprint / device PIN | AppLock, DeviceInfoPlus, SecureSession | AppLock is a background timer + UI gate. DeviceInfoPlus only probes `HasBiometric`. SecureSession locks tokens. |
| Keep the screen on during scan / POS / video | DeviceOrientationPlus | Orientation lock does not touch the idle timer. |
| Block screenshots and recents thumbnails | AppLock, FileVault | AppLock covers the window after background. FileVault encrypts files. Neither is `FLAG_SECURE`. |
| In-app store review prompt | AppUpdate | AppUpdate installs or opens a **binary** update. It does not ask for a rating. |
| Scheduled local alerts (“sync finished”, “retry later”) | PushRouter, JobQueue | PushRouter routes **remote** FCM/APNs payloads and does not register tokens or schedule local work. |
| Enter / exit a geographic region | GeoLocator | GeoLocator is on-demand + foreground tracking. It is not a geofence monitor. |
| Classic Bluetooth serial (SPP / RFCOMM) | BluetoothManager, Printing | BluetoothManager is BLE/GATT only. Printing owns ESC/POS documents, not a general serial session. |
| Camera/gallery **video** → compress → thumbnail → upload | MediaPipeline | MediaPipeline is still images only. |
| Certificate / SPKI pin on `HttpClient` | ApiResilience, HttpForge | Those retry, cache, and generate clients. They do not pin TLS. |

This wave fills those gaps as **nine focused plugins**. It does not reopen shipped 1.x APIs and does not create an umbrella nupkg.

---

## 2. Principles (catalog contract)

Unchanged from [architecture.md](../architecture.md). Every plugin in this wave must satisfy all of them.

1. **One problem per package.** The README names the problem (local notification schedule, geofence transition, TLS pin), not “part of MauiEssentials”.
2. **Android and iOS first.** Shared `net10.0` exists so tests and class libraries can reference the API. Native calls throw `FeatureNotSupported` / a typed `*Exception` with that code on that TFM.
3. **MAUI builder registration.** `UseX(...)` plus `Current` / `Default`. Resolve the interface from DI.
4. **Compose, do not replace the OS.** Wrap `BiometricPrompt`, `UNUserNotificationCenter`, `GeofencingClient`, `CLCircularRegion`, `FLAG_SECURE`, Play In-App Review, `SKStoreReviewController`. Do not replace FCM, JobScheduler, or `HttpClient`.
5. **Prefer the framework when it is enough.** Do not wrap `Permissions.RequestAsync` as a product. Do not wrap `DeviceDisplay` only to read orientation.
6. **No sibling `PackageReference`.** Hosts compose plugins. Optional handoff uses small interfaces the host implements (`IMediaUploader`, tap → `PushRouter.Handle`, pin failure → Diagnostics breadcrumb).
7. **Fail closed where secrets or navigation are involved.** Empty pin sets reject. Unregistered notification actions do not navigate. Report-only TLS pinning is opt-in.
8. **Pipeline-only publish.** CI pushes nuget.org (`NUGET_KEY` for `Plugin.Maui.*`) and GitHub Packages (`GITHUB_TOKEN`).
9. **AOT / trim is a constraint.** Public APIs are typed. No reflection fallback for pinning, notification routing, or video transcode presets.

---

## 3. Wave contents

| # | Package | Hub folder | Problem | Platforms | Closest sibling |
| --- | --- | --- | --- | --- | --- |
| 1 | `Plugin.Maui.Biometric` | `Biometric/` | One-shot biometric / device-credential prompt | Android API 23+, iOS 15+ | AppLock, DeviceInfoPlus |
| 2 | `Plugin.Maui.KeepAwake` | `KeepAwake/` | Keep the screen on (reference-counted) | Android API 21+, iOS 15+ | DeviceOrientationPlus |
| 3 | `Plugin.Maui.ScreenGuard` | `ScreenGuard/` | Block screenshots / recents leaks; capture events | Android API 21+, iOS 15+ | AppLock |
| 4 | `Plugin.Maui.AppReview` | `AppReview/` | In-app review + open store listing | Android API 21+, iOS 15+ | AppUpdate |
| 5 | `Plugin.Maui.LocalNotifications` | `LocalNotifications/` | Schedule / cancel local notifications + tap routing | Android API 21+, iOS 15+ | PushRouter |
| 6 | `Plugin.Maui.Geofence` | `Geofence/` | Circular geofence enter / exit / dwell | Android API 21+, iOS 15+ | GeoLocator |
| 7 | `Plugin.Maui.BluetoothSerial` | `BluetoothSerial/` | Classic SPP / RFCOMM serial session | Android API 21+ first-class; iOS MFi only | BluetoothManager |
| 8 | `Plugin.Maui.VideoPipeline` | `VideoPipeline/` | Camera/gallery video → compress / thumbnail / encrypt / handoff | Android, iOS, Mac Catalyst, Windows | MediaPipeline |
| 9 | `Plugin.Maui.TlsPin` | `TlsPin/` | HttpClient SPKI / public-key pin | Shared: Android, iOS, Mac Catalyst, Windows | ApiResilience |

**Explicitly excluded from this wave**

- Barcode / QR / ML Kit scanner (deferred; do not sneak a sample into VideoPipeline or Geofence)
- Maps SDK, IAP, ads, contacts, calendar, SMS
- FCM / APNs **token registration** (stays host / Firebase)
- Full PJSIP / CallKit stack (stays VoipCore session model)
- Classic BLE GATT (stays BluetoothManager)
- Image processing (stays MediaPipeline)
- Heuristic `maui-dev` / Roslyn work (stays MauiDev)

---

## 4. Recommended implementation order

Three waves. Each wave is independently publishable. Later waves may compose earlier ones at the **host** level only.

| Wave | Theme | Ships | Why this order |
| --- | --- | --- | --- |
| **1** | Thin native gates | Biometric, KeepAwake, ScreenGuard, AppReview | Small surface, high adoption, unblocks AppLock / POS / enterprise samples. Low store-policy risk except AppReview (OS quotas). |
| **2** | Field loop | LocalNotifications, Geofence | Completes OfflineSync / JobQueue / GeoLocator stories. Needs careful background-permission docs. |
| **3** | Hardware / media / TLS | BluetoothSerial, VideoPipeline, TlsPin | Largest native and breakage risk. Serial is Android-honest. Video and pinning need golden tests before nuget.org. |

Do not start Wave 3 until Wave 1 has samples on a device and Wave 2 permission matrices are written. VideoPipeline and TlsPin can be designed in parallel after Wave 1 APIs freeze.

---

## 5. Shared packaging

### 5.1 Target frameworks

| Kind | TFMs | Min OS |
| --- | --- | --- |
| Native Android + iOS (1–7 except BluetoothSerial iOS note) | `net10.0`; `net10.0-android`; `net10.0-ios` | Android API 21+ (Biometric **23+**); iOS 15+ |
| Shared libraries (VideoPipeline, TlsPin) | those plus `net10.0-maccatalyst`; `net10.0-windows10.0.17763.0` | Catalyst 15+; Windows 10 17763+. Windows pack on `windows-latest` only. |

`net10.0` without an OS TFM is a shared / test reference assembly. Do not no-op silently — throw or return a typed `NotSupported` result so tests can assert.

Tizen is not a target. Do not present native plugins as Windows / Mac Catalyst solutions.

### 5.2 Naming

| Role | Pattern | Example |
| --- | --- | --- |
| Product / PackageId | `Plugin.Maui.{Name}` | `Plugin.Maui.Geofence` |
| Root namespace | `Plugin.Maui.{Name}` | `Plugin.Maui.Geofence` |
| Registration | `Use{Name}` | `UseGeofence` |
| Accessor | `{Name}.Current` | `Geofence.Current` |
| Options | `{Name}Options` | `GeofenceOptions` |
| GitHub | `nuvyntralabs/Plugin.Maui.{Name}` | `nuvyntralabs/Plugin.Maui.Geofence` |
| Hub submodule | `{Name}/` | `Geofence/` |
| Docs slug | `plugin-maui-{kebab}` | `plugin-maui-geofence` |
| Docs | `https://nuvyntralabs.github.io/packages/{slug}/` | same slug |

Type names stay collision-free with MAUI (`Permissions`, `Geolocation`, `DeviceDisplay`) and with CommunityToolkit.

### 5.3 Repository layout (every plugin)

```
Plugin.Maui.{Name}/
├── AGENTS.md
├── README.md
├── llms.txt
├── CHANGELOG.md
├── Directory.Build.props
├── Directory.Packages.props
├── {Name}.sln
├── src/Plugin.Maui.{Name}/
├── tests/Plugin.Maui.{Name}.Tests/
├── samples/{Name}Sample/
└── .github/workflows/ci.yml
```

Copy an existing native plugin (AppLock or DeviceOrientationPlus) for Wave 1. Copy MediaPipeline for VideoPipeline. Copy ApiResilience for TlsPin.

Required docs sections, same as shipped plugins:

- Problem → Installation → Configuration → Code → Expected result → Platform limitations
- “Do not use this when…” (point at the sibling or the MAUI built-in)
- AndroidManifest / Info.plist host setup
- Compose-with table (no PackageReference)

### 5.4 Tests and sample

| Surface | Rule |
| --- | --- |
| Unit tests | Public API + fail-closed paths on `net10.0` with injected fakes. No device required for CI. |
| Sample | One MAUI host, Android + iOS. Shared-library plugins also run Catalyst; Windows when the CI agent is Windows. |
| Device pass | Wave exit requires at least one Android device run for every native API (see [revalidation-plan.md](../revalidation-plan.md) style). |
| Version | Start at `1.0.0`. Align `Version` / `PackageVersion` / README badge path. |

### 5.5 Hub wiring (after the plugin’s 1.0.0 CI is green)

Update in the same hub PR that adds the submodule:

- Root `README.md` package table + requirement map
- `llms.txt` / `llms-full.txt`
- `AGENTS.md` layout list
- `docs/packages/README.md`
- `docs/architecture.md` compose row
- `docs/getting-started.md` example bullet
- Skill catalog `catalog.md` (outside this repo)

Do not add catalog rows for unshipped packages.

---

## 6. Wave 1 — thin native gates

### 6.1 Plugin.Maui.Biometric

**Problem:** Hosts need a single `AuthenticateAsync` (Face ID, fingerprint, device PIN) without adopting AppLock’s timer and cover page.

**This is not:** AppLock, SecureSession, DeviceInfoPlus, or a liveness / anti-spoof SDK.

**Usual alternatives:** `Plugin.Fingerprint`, `Plugin.Maui.Biometric` community ports, raw `BiometricPrompt` / `LAContext`.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseBiometric(o =>
{
    o.AllowDeviceCredential = true;
    o.DefaultReason = "Confirm it is you";
});

var availability = await Biometric.Current.GetAvailabilityAsync();
var result = await Biometric.Current.AuthenticateAsync(new BiometricRequest
{
    Reason = "Unlock payroll",
    AllowDeviceCredential = true,
    CancelTitle = "Cancel"
});

if (result.Succeeded)
    await OpenPayrollAsync();
```

| Type | Role |
| --- | --- |
| `IBiometric` | `GetAvailabilityAsync`, `AuthenticateAsync` |
| `BiometricAvailability` | `Available`, `NotEnrolled`, `NotAvailable`, `Unknown` |
| `BiometricRequest` | Reason (required), allow device credential, cancel title |
| `BiometricResult` | `Succeeded`, `Canceled`, `Failed`, `NotEnrolled`, `NotAvailable`, `LockedOut`, `NotSupported` |
| `BiometricException` | Unexpected platform faults only |

`net10.0` returns `NotSupported` — do not throw from `AuthenticateAsync` for “no hardware”. Throw only on misuse (empty reason).

#### Platform map

| OS | Implementation |
| --- | --- |
| Android 23+ | `BiometricManager` + `BiometricPrompt`. Host activity from MAUI current. `USE_BIOMETRIC` / `USE_FINGERPRINT` documented. |
| iOS 15+ | `LAContext` (`DeviceOwnerAuthentication` when device credential is allowed, else `DeviceOwnerAuthenticationWithBiometrics`). `NSFaceIDUsageDescription` required. |
| `net10.0` | Fake in tests |

#### Compose

| Host need | Use |
| --- | --- |
| Lock the whole app after background | AppLock (may call this plugin later; **no** PackageReference in 1.0) |
| Lock tokens | SecureSession |
| “Does this device have biometrics?” | DeviceInfoPlus |

#### Out of 1.0

Custom PIN UI, enrolled-biometric change detection, crypto-bound `BiometricPrompt` `CryptoObject` / Secure Enclave key unlock (FileVault / SecureStoragePlus can add that later), Wear OS.

#### Acceptance

- Tests cover every `BiometricResult` via a fake authenticator
- Sample: “Prompt”, “Prompt without device PIN”, disabled state when `NotEnrolled`
- Android device: fingerprint or device PIN path. iOS simulator: passcode / Face ID enrolled
- README first paragraph: not AppLock

#### Phases

1. Interface + fake + tests  
2. Android `BiometricPrompt`  
3. iOS `LAContext`  
4. Sample + docs + CI pack  

---

### 6.2 Plugin.Maui.KeepAwake

**Problem:** POS, scanning, navigation, and video pages must keep the screen on without each page poking platform APIs.

**This is not:** a CPU wake lock, a foreground service, BackgroundTasks, or “run work after the app is killed”.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseKeepAwake();

using (KeepAwake.Current.Acquire())
{
    await ScanLoopAsync();
}

// or per page
KeepAwake.SetEnabled(this, true);   // attached / behavior
```

Reference-counted: two `Acquire()` calls require two dispose/`Release()` calls before the idle timer returns. Nested page + explicit acquire must not flicker.

| Type | Role |
| --- | --- |
| `IKeepAwake` | `Acquire()` → `IDisposable`, `IsActive`, `ActiveCount` |
| `KeepAwake` | `Current`, attached `Enabled` property |

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | `Window.AddFlags(FlagKeepScreenOn)` on the current activity window. Clear only when count hits 0. |
| iOS | `UIApplication.SharedApplication.IdleTimerDisabled`. Same ref-count. Hop to main thread. |
| `net10.0` | In-memory counter only |

Do not use Android `PowerManager.WakeLock` in 1.0 (permissions, leaks, Play policy). Screen flag is enough.

#### Compose

DeviceOrientationPlus (landscape scan page + keep awake), KeyboardManager (no interaction), VideoPipeline sample (keep awake while recording).

#### Out of 1.0

Partial wake locks, proximity-screen-off, dim-but-awake, CarPlay / Android Auto.

#### Acceptance

- Tests: nested acquire, dispose order, `IsActive`  
- Sample: toggle + a page that enables on appear / disables on disappear  
- Device: screen stays on for 60s on the sample page; other pages sleep normally  

---

### 6.3 Plugin.Maui.ScreenGuard

**Problem:** Banking, clinical, and payroll screens must not appear in recents thumbnails or be screenshottable.

**This is not:** AppLock’s cover page, FileVault, or a DRM / Widevine stack.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseScreenGuard(o =>
{
    o.ProtectOnStart = false;
    o.BlurAppSwitcher = true;   // Android: FLAG_SECURE covers this
});

ScreenGuard.Current.Protect();
ScreenGuard.Current.Unprotect();
ScreenGuard.SetProtected(payrollPage, true);

ScreenGuard.Current.CaptureStateChanged += (_, e) =>
{
    // e.IsCaptured — iOS screen recording / AirPlay; Android best-effort
};
```

| Type | Role |
| --- | --- |
| `IScreenGuard` | `Protect`, `Unprotect`, `IsProtected`, `CaptureStateChanged` |
| `ScreenGuardCaptureEvent` | `IsCaptured` |

Per-page attached property uses the same ref-count idea as KeepAwake so navigating away lifts protection unless the app called `Protect()` globally.

#### Platform map

| OS | What 1.0 can honestly do |
| --- | --- |
| Android | `Window.SetFlags(FlagSecure)`. This blocks screenshots **and** recents preview. There is no public callback for “user took a screenshot” on all API levels — do not fake one. |
| iOS | No `FLAG_SECURE`. 1.0: hide / blur a host-supplied overlay when `UIScreen.MainScreen.Captured` is true; listen `CapturedDidChangeNotification`. Screenshots of the current frame cannot be fully prevented — document that. |
| `net10.0` | State only |

#### Compose

AppLock (lock after background **and** protect while visible), FileVault (ciphertext still needs a screen guard on the viewer page), ClipboardPlus (no interaction).

#### Out of 1.0

Watermark overlays, Android 14+ screenshot detection as a guaranteed event, jailbreak/root detection (CommunityToolkitPlus integrity), blocking screen **sharing** on conference APIs.

#### Acceptance

- Tests: ref-count protect/unprotect; `net10.0` does not touch UI  
- Android device: recents thumbnail is black/secure; `screencap` fails while protected  
- iOS device: overlay appears during screen recording  
- README states the iOS limitation in the first “Platform limitations” paragraph  

---

### 6.4 Plugin.Maui.AppReview

**Problem:** Hosts want Play In-App Review and `SKStoreReviewController` with a cooldown, plus a fallback that opens the store listing.

**This is not:** AppUpdate, a review-analytics SaaS, or a fake five-star dialog.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseAppReview(o =>
{
    o.MinimumLaunchCount = 5;
    o.MinimumDaysSinceFirstLaunch = 7;
    o.Cooldown = TimeSpan.FromDays(90);
    o.AndroidPackageName = null;          // default: AppInfo.PackageName
    o.iOSAppStoreId = "1234567890";       // required for OpenStoreListing on iOS
});

var outcome = await AppReview.Current.RequestAsync();
if (outcome.Kind is AppReviewKind.NotEligible or AppReviewKind.Unavailable)
    await AppReview.Current.OpenStoreListingAsync();
```

| Type | Role |
| --- | --- |
| `IAppReview` | `RequestAsync`, `OpenStoreListingAsync`, `GetEligibilityAsync` |
| `AppReviewOutcome` | `Shown`, `NotEligible`, `Unavailable`, `Canceled`, `NotSupported` |
| `AppReviewOptions` | Thresholds + store ids |

Eligibility is **local** (launches, days, cooldown) stored in MAUI `Preferences`. The OS may still no-op `RequestAsync` (iOS annual quota, Play quota). Treat `Shown` as “we asked the OS”, not “the user rated us”.

Do not PackageReference DeviceSession. The host may increment launches itself via `IAppReviewLaunchCounter` if it wants a custom store.

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | Play Core `ReviewManager`. Only works for Play-installed builds (same honesty as AppUpdate). `OpenStoreListing` → `market://` then `https://play.google.com/store/apps/details?id=` |
| iOS | `SKStoreReviewController.RequestReview` on the current window scene. `OpenStoreListing` → `itms-apps://` with `iOSAppStoreId` |
| `net10.0` | Eligibility engine + fake store |

#### Compose

AppUpdate (binary vs rating), FeatureFlags (`reviews_enabled`), DeviceSession (host passes install age).

#### Out of 1.0

Huawei / Amazon stores, “write a review” in-app forms, prompting after every crash-free session automatically (host policy).

#### Acceptance

- Tests: eligibility math, cooldown, missing iOS id fails `OpenStoreListing` with a typed result  
- Sample: “Request review”, “Open listing”, debug “reset counters”  
- Document: never call `RequestAsync` from a button labeled Rate us as the only path — Apple/Google reject incentive patterns. Sample uses a Settings page **and** an automatic check after a successful action.  

---

## 7. Wave 2 — field loop

### 7.1 Plugin.Maui.LocalNotifications

**Problem:** JobQueue, RetryQueue, and OfflineSync hosts need a local “work finished / try again at 17:00” alert without Firebase.

**This is not:** FCM/APNs token registration, a system-notification display SDK for **remote** payloads, or PushRouter.

PushRouter continues to parse **incoming remote** extras. This plugin **creates** local entries and raises `NotificationTapped` when the user opens one.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseLocalNotifications(o =>
{
    o.AndroidDefaultChannelId = "general";
    o.AndroidDefaultChannelName = "General";
    o.RequestPermissionOnRegister = false;   // host should use PermissionFlow
});

await LocalNotifications.Current.EnsureChannelAsync(new NotificationChannelRequest
{
    Id = "sync",
    Name = "Sync",
    Importance = NotificationImportance.Default
});

await LocalNotifications.Current.ScheduleAsync(new NotificationRequest
{
    Id = 1001,
    Title = "Upload ready",
    Body = "3 photos waiting to sync",
    ChannelId = "sync",
    Schedule = NotificationSchedule.At(DateTimeOffset.Now.AddMinutes(30)),
    Payload = new Dictionary<string, string> { ["route"] = "//uploads" },
    Actions =
    {
        new NotificationAction("open", "Open"),
        new NotificationAction("later", "Later")
    }
});

LocalNotifications.Current.NotificationTapped += (_, e) =>
{
    // Host may call PushRouter or DeepLinks. Do not navigate from this plugin.
};

await LocalNotifications.Current.CancelAsync(1001);
await LocalNotifications.Current.CancelAllAsync();
var pending = await LocalNotifications.Current.GetPendingAsync();
```

| Type | Role |
| --- | --- |
| `ILocalNotifications` | Channels, schedule, cancel, pending, tap event, `AreEnabledAsync` |
| `NotificationRequest` | Id (int), title, body, schedule, channel, payload, actions (max 3) |
| `NotificationSchedule` | `Immediate`, `At(DateTimeOffset)`, `Interval(TimeSpan, repeat)` |
| `NotificationTapEvent` | Id, action id, payload |

Fail closed: `Interval` below 60s on iOS is rejected (OS will coerce — we refuse instead). Android exact alarms (`SCHEDULE_EXACT_ALARM`) are **opt-in** (`Schedule.Exact = true`) and documented as Play-policy sensitive. Default is inexact.

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | `NotificationCompat` + `AlarmManager` or `WorkManager` for delayed. Channels on API 26+. `POST_NOTIFICATIONS` on API 33+. Tap via a documented `BroadcastReceiver` / `Activity` extra. |
| iOS | `UNUserNotificationCenter`. Categories for actions. Tap via `UNUserNotificationCenterDelegate` forwarded from the MAUI app delegate hook. |
| `net10.0` | In-memory scheduler for tests |

Permission UX is **not** this product. Document PermissionFlow key `"notifications"`. `RequestPermissionOnRegister` default `false`.

#### Compose

| Sibling | How |
| --- | --- |
| PushRouter | Host maps tap payload → `PushRouter.Handle` if the extras look like a remote route |
| DeepLinks | Host maps payload URI → `DeepLinks` |
| JobQueue / RetryQueue / OfflineSync | Host schedules a local notification from `JobFinished` / `SyncCompleted` |
| PermissionFlow | Named flow for notifications |
| FeatureFlags | Disable alerts remotely |

#### Out of 1.0

Rich media notifications, Notification Center history sync, Android foreground-service notifications as a product, iOS time-sensitive entitlement, scheduled location triggers (that is Geofence).

#### Acceptance

- Tests: schedule / cancel / pending / tap payload on the fake  
- Sample: immediate, +30s, repeating (min 60s), action buttons, permission denied state  
- Android 13+ device: deny → no crash; grant → tap opens sample page with payload  
- iOS: background tap restored after process death  

---

### 7.2 Plugin.Maui.Geofence

**Problem:** Field and attendance apps need enter / exit / dwell on a circular region that survives process death.

**This is not:** GeoLocator, a maps SDK, beacon / iBeacon, or a turn-by-turn navigator.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseGeofence(o =>
{
    o.MaxRegions = 20;                 // iOS hard cap — Android hosts should stay honest
    o.DefaultRadiusMeters = 100;
    o.MinimumRadiusMeters = 50;
});

await Geofence.Current.AddAsync(new GeofenceRegion
{
    Id = "depot",
    Latitude = 12.97,
    Longitude = 77.59,
    RadiusMeters = 150,
    NotifyOnEntry = true,
    NotifyOnExit = true,
    NotifyOnDwell = true,
    Dwell = TimeSpan.FromMinutes(5)
});

Geofence.Current.Transition += (_, e) =>
{
    // e.RegionId, e.Kind = Enter | Exit | Dwell
    // Host may JobQueue.Enqueue or LocalNotifications.Schedule
};

var regions = await Geofence.Current.GetMonitoredAsync();
await Geofence.Current.RemoveAsync("depot");
await Geofence.Current.RemoveAllAsync();
```

Persist the region list in app-private storage so a process restart re-registers with the OS. Do not use this plugin as a location cache.

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | `GeofencingClient` + `BroadcastReceiver`. Background location (`ACCESS_BACKGROUND_LOCATION`) documented for Android 10+. Play policy: show a prominent disclosure in the host. |
| iOS | `CLLocationManager` circular regions. **20 region cap** enforced in the plugin. `Always` authorization required for background transitions. Significant-change is not a substitute. |
| `net10.0` | In-memory regions + test `Raise(transition)` |

`net10.0` and missing permission return typed results (`Denied`, `LimitReached`, `InvalidRadius`). Do not throw for “user said no”.

#### Compose

GeoLocator (one-shot fix to *create* a region around “here”), PermissionFlow (`location`, `locationAlways`), BackgroundTasks / JobQueue (do the work), LocalNotifications (alert the user), OfflineSync (clock-in).

#### Out of 1.0

Polygons, dwell on Android without a custom timer if the OS dwell is insufficient (document), beacon UUIDs, fused activity-transition API, Windows/Catalyst.

#### Acceptance

- Tests: persist/reload, 21st region → `LimitReached`, radius below minimum rejected  
- Sample: add region at current GeoLocator fix **or** typed lat/lon, list, remove, log transitions  
- Device: enter/exit a large test radius (office/campus). Simulator location overrides acceptable for CI notes, not as the only proof  

---

## 8. Wave 3 — hardware, media, TLS

### 8.1 Plugin.Maui.BluetoothSerial

**Problem:** POS scales, medical serial cables, and many thermal printers speak **classic SPP / RFCOMM**, which BluetoothManager refuses.

**This is not:** BLE/GATT (BluetoothManager), ESC/POS document encoding (Printing), a generic Bluetooth explorer, or iOS RFCOMM (the OS does not expose it).

#### Honesty rule (lock this before code)

| Platform | 1.0 support |
| --- | --- |
| Android | First-class. `BluetoothSocket` RFCOMM. Default UUID `00001101-0000-1000-8000-00805F9B34FB` (Serial Port Profile). Custom UUID allowed. |
| iOS | **MFi External Accessory only** (`EASession`). If the accessory is not in `UISupportedExternalAccessoryProtocols`, return `NotSupported`. Do **not** pretend Nordic UART / BLE is serial in this package. |
| Windows / Catalyst | Out of 1.0 |

iOS hosts that need BLE printers keep using Printing + BluetoothManager. The sample on iOS shows the MFi path and a clear unsupported state for SPP.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseBluetoothSerial(o =>
{
    o.ConnectTimeout = TimeSpan.FromSeconds(10);
    o.DefaultUuid = BluetoothSerialUuids.SerialPort;
});

var devices = await BluetoothSerial.Current.ScanAsync(new SerialScanOptions
{
    Duration = TimeSpan.FromSeconds(8),
    NameContains = "Printer"
});

await using var session = await BluetoothSerial.Current.ConnectAsync(devices[0]);
await session.WriteAsync(escPosBytes);
var n = await session.ReadAsync(buffer);
```

Connection lifecycle: `Disconnected` event, explicit `DisconnectAsync`, `IsConnected`. No GATT discover. No auto-reconnect storm — one retry is enough in 1.0 (`MaxReconnectAttempts` default 0).

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | Paired-device list + optional discovery. `BLUETOOTH` / `BLUETOOTH_ADMIN` (legacy) and `BLUETOOTH_CONNECT` / `BLUETOOTH_SCAN` (API 31+). Never scan without the README permission block. |
| iOS | `EAAccessoryManager` connected accessories filtered by protocol strings the host registers. |
| `net10.0` | Loopback session for tests |

#### Compose

Printing (host encodes ESC/POS, this plugin writes bytes), PermissionFlow (`bluetooth`), DeviceInfoPlus (`HasBluetooth`).

#### Out of 1.0

BLE UART bridges, HID, A2DP, pairing UI beyond the OS prompt, macOS, Windows RFCOMM.

#### Acceptance

- Tests: loopback write/read, connect timeout, iOS-without-protocol → `NotSupported`  
- Android device: write a short ESC/POS sequence to a known SPP printer **or** a USB Bluetooth SPP dongle  
- README first paragraph states the iOS MFi limit  

---

### 8.2 Plugin.Maui.VideoPipeline

**Problem:** Inspection and claims apps capture video, then must compress, thumbnail, strip metadata, optionally encrypt, and hand off to SmartUpload / FileVault.

**This is not:** MediaPipeline (images), a timeline editor, a streaming live-camera control, or a replacement for `MediaPicker`.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseVideoPipeline();

var artifact = await VideoPipeline.FromCameraAsync()
    .MaxDuration(TimeSpan.FromSeconds(30))
    .MaxResolution(1280, 720)
    .MaxBytes(8 * 1024 * 1024)
    .ThumbnailAt(TimeSpan.FromSeconds(1))
    .StripMetadata()
    .Encrypt(key)          // same envelope idea as MediaPipeline; host may skip
    .SaveAsync();

// artifact.VideoPath, artifact.ThumbnailPath, artifact.Duration, artifact.Bytes
```

Gallery: `FromGalleryAsync()`. Handoff interfaces copy MediaPipeline’s `IMediaUploader` / `IMediaVault` **shapes** (duplicate the small interfaces; do not reference MediaPipeline).

#### Platform map

| OS | Implementation |
| --- | --- |
| Android | `MediaPicker` capture + `MediaMetadataRetriever` thumbnail + `MediaMuxer` / transcode when over budget. If the device cannot transcode, return `Unsupported` rather than shipping a huge FFmpeg binary in 1.0. |
| iOS / Catalyst | `AVAssetExportSession` presets (`640x480`, `1280x720`) + `AVAssetImageGenerator`. |
| Windows | `MediaPicker` + thumbnail via WinRT if available; transcode is best-effort. Document “copy + thumbnail” as the Windows 1.0 floor. |
| `net10.0` | Fake picker + no-op transform for tests |

Do **not** bundle FFmpeg or LibVLC in 1.0. If Android transcode proves too thin, ship “reject if over `MaxBytes` / `MaxDuration`” plus thumbnail — still useful — and record a decision to add a transcode provider interface.

#### Compose

SmartUpload, FileVault, KeepAwake (while recording), PermissionFlow (`camera`, `microphone`, `photos`), DeviceOrientationPlus (landscape capture page).

#### Out of 1.0

Trim UI, filters, audio ducking, HLS, live streaming, barcode-from-frame (excluded from this wave), HEIF stills (MediaPipeline).

#### Acceptance

- Tests: options validation, fake pipeline, encrypt envelope round-trip  
- Sample: record / pick → show duration, size, thumbnail → optional “upload” mock  
- Android + iOS device: a 10–20s clip comes down in size or fails with a typed “too large / cannot transcode” result — never a crash  

---

### 8.3 Plugin.Maui.TlsPin

**Problem:** Finance and health hosts need SPKI pins on `HttpClient` without replacing ApiResilience or HttpForge.

**This is not:** a custom CA store, a MITM toolkit, user-installed cert trust, or Polly.

#### API (1.0)

```csharp
builder.UseMauiApp<App>().UseTlsPin();

builder.Services.AddHttpClient("payments", c =>
{
    c.BaseAddress = new Uri("https://payments.example.com");
})
.AddTlsPin(o =>
{
    o.RequireHttps = true;
    o.ReportOnly = false;
    o.Pins.Add("payments.example.com", new TlsPinSet
    {
        SpkiSha256 =
        {
            "base64-primary-pin",
            "base64-backup-pin"
        }
    });
});
```

Empty pin set for a requested host → fail closed (do not attach a no-op handler). Unknown hosts on that client → fail closed unless `AllowUnpinnedHosts = true` (default **false**).

`ReportOnly = true` validates and invokes `OnPinFailure` but still sends the request — for staging only. Production samples leave it false.

Also expose `TlsPin.Validate(certificate, pinSet)` for tests and for non-HttpClient sockets if the host wants it. 1.0 handler covers HTTPS `HttpClient` only.

#### Platform map

Shared managed code. Use `HttpClientHandler` / `SocketsHttpHandler.SslOptions.RemoteCertificateValidationCallback` (or the MAUI platform handler) to compute SPKI SHA-256 over the leaf (and optionally intermediates if `PinKind.LeafOrIntermediate`).

Windows / Catalyst / Android / iOS share the same pin math. No native plugin.

#### Compose

HttpForge (`AddHttpForgeClient` then `AddTlsPin` on the same builder), ApiResilience (pin **inside** the handler chain; document order: pin before retry so a pin failure is not retried as a transient), NetworkDiagnostics (optional “pin mismatch” finding is **out** of 1.0).

#### Out of 1.0

HPKP headers, DANE, mTLS client certs, dynamic pin download (that is how pinning gets bypassed — do not), public-key pin expiration timestamps (nice-to-have, not blocker).

#### Acceptance

- Tests: good pin, backup pin, bad pin, empty set, `ReportOnly`, HTTP rejected when `RequireHttps`  
- Sample: two clients — pinned public endpoint with documented pins, and a report-only client  
- Document pin rotation: always ship a backup pin; rotating CA without a backup **bricks** the app  

---

## 9. Cross-plugin composition (hosts, not PackageReferences)

```
Field clock-in
  GeoLocator (optional “here”) → Geofence.Add
  Geofence.Transition → JobQueue / OfflineSync
                     → LocalNotifications.Schedule

POS / printer
  BluetoothSerial.Write(Printing-encoded bytes)
  KeepAwake.Acquire during the ticket
  DeviceOrientationPlus landscape

Enterprise viewer
  ScreenGuard.Protect on the page
  AppLock for background
  Biometric.Authenticate for step-up
  FileVault for the file
  TlsPin on the download client

Inspection clip
  VideoPipeline.FromCamera → SmartUpload / FileVault
  KeepAwake while recording
```

Do not create `Plugin.Maui.FieldKit`. Recipes belong in hub `docs/` after two or more of these ship.

---

## 10. Shared phases (each plugin)

### Phase 0 — Design lock

- [ ] PackageId / hub folder / slug approved (this document)
- [ ] “What this is not” paragraph approved
- [ ] Empty repo `nuvyntralabs/Plugin.Maui.{Name}` + hub submodule (no NuGet)

**Exit:** repo has README stub, `AGENTS.md`, `llms.txt`, and this plan copied as `DESIGN-PLAN.md`.

### Phase 1 — Contract + fakes

Public interfaces, options, typed results, `net10.0` fake, unit tests. Sample compiles against fakes.

### Phase 2 — Native / shared implementation

Android then iOS for native plugins. Shared implementation first for VideoPipeline / TlsPin, then platform gaps.

### Phase 3 — Productization (`1.0.0`)

Sample on device, CHANGELOG, hub catalog rows, CI pack + test, nuget.org / GitHub Packages via the plugin repo’s workflow.

**Definition of Done** (same bar as hardened 1.x plugins)

- README Problem → Limitations complete  
- `llms.txt` + `AGENTS.md`  
- Tests on `net10.0` for fail-closed paths  
- Sample `UseX` in `MauiProgram`  
- Root `.sln`  
- AndroidManifest / Info.plist documented  
- No sibling PackageReference  
- Version aligned  
- Hub tables updated only after the nupkg exists  

---

## 11. CI and publish

Copy a native plugin workflow (AppLock) or a shared-library workflow (MediaPipeline / ApiResilience).

| Job | Agent | Does |
| --- | --- | --- |
| test | `ubuntu-latest` | `dotnet test` (`net10.0`) |
| pack-android-ios | `macos-latest` | pack `net10.0` + android + ios (+ catalyst for shared) |
| pack-windows | `windows-latest` | VideoPipeline + TlsPin only |
| publish | on tag / main as today | nuget.org `NUGET_KEY`, GitHub Packages `GITHUB_TOKEN` |

Do not publish from the hub. Do not share a nupkg across plugins.

---

## 12. Risks

| Risk | Plugin | Mitigation |
| --- | --- | --- |
| Confused with AppLock | Biometric | README first line; AGENTS “do not recommend for app lock” |
| iOS cannot block screenshots | ScreenGuard | Document; ship recording overlay only |
| Play / Apple review quotas look like bugs | AppReview | Outcome `Shown` ≠ rated; cooldown + Settings fallback |
| Exact alarms / Play policy | LocalNotifications | Inexact default; exact opt-in |
| Always-on location rejection | Geofence | PermissionFlow + disclosure copy in the sample; no hidden background add |
| iOS has no RFCOMM | BluetoothSerial | MFi-only; BLE stays in BluetoothManager |
| FFmpeg weight / Play size | VideoPipeline | No native binary in 1.0; typed cannot-transcode |
| Pin rotation bricks apps | TlsPin | Require ≥1 backup pin in sample; fail closed; report-only for staging |
| Background tap lost after process death | LocalNotifications / Geofence | Persist ids; re-register on `UseX`; sample kills and restores |
| Agents generate a barcode plugin | Hub | This plan forbids it; do not add scanner pages to VideoPipeline |

---

## 13. Decision log

| ID | Decision | Status |
| --- | --- | --- |
| N1 | Nine plugins; barcode / QR **excluded** from this wave | Proposed |
| N2 | Ship Wave 1 → 2 → 3; no umbrella nupkg | Proposed |
| N3 | No sibling PackageReferences; hosts compose | Proposed |
| N4 | Biometric is the one-shot prompt; AppLock stays the workflow | Proposed |
| N5 | KeepAwake is screen-only (`FlagKeepScreenOn` / idle timer), not `WakeLock` | Proposed |
| N6 | ScreenGuard Android = `FLAG_SECURE`; iOS = capture overlay, not a lie | Proposed |
| N7 | AppReview eligibility is local Preferences; OS may still no-op | Proposed |
| N8 | LocalNotifications does not register FCM/APNs tokens | Proposed |
| N9 | Geofence max 20 regions (iOS cap applied on all platforms) | Proposed |
| N10 | BluetoothSerial Android SPP first-class; iOS MFi only | Proposed |
| N11 | VideoPipeline does not bundle FFmpeg in 1.0 | Proposed |
| N12 | TlsPin fail-closed; `ReportOnly` opt-in; `AllowUnpinnedHosts` default false | Proposed |
| N13 | Shared TFMs only for VideoPipeline and TlsPin | Proposed |
| N14 | Start every package at `1.0.0`; pipeline-only publish | Proposed |

---

## 14. How to use this document

1. Lock the decision log (especially N1, N10, N11, N12).  
2. Create **one** empty repo per Wave 1 plugin. Do not batch-create Wave 3.  
3. Copy this section for that plugin into the repo as `DESIGN-PLAN.md`.  
4. Implement Phase 1 (contract + tests) before native code.  
5. When `1.0.0` is on nuget.org, add the hub submodule and catalog rows.  
6. After Wave 1 ships, write short hub recipes (enterprise viewer, POS ticket) — not a new package.

Publishing stays in GitHub Actions.
