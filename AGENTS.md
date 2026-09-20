# MauiEssentials — AI Coding Agent Guide

MauiEssentials is an open-source catalog of focused .NET MAUI plugins for Android and iOS. Each plugin is its own repository, NuGet package, and git submodule.

Hub: https://github.com/nuvyntralabs/MauiEssentials  
Author: Niladri Prasad Padhy  
License: MIT  
Site: https://nuvyntralabs.github.io/  
LLM index: [llms.txt](llms.txt) · Full docs: [llms-full.txt](llms-full.txt)

## Two ways Nuvyntra Labs reaches the user

Nuvyntra Labs is a **component library** and a **whole ecosystem**. The user chooses. Do not force one path. Neither is a fallback.

- **Component library:** existing host; one control (`NuvyntraLabs.UIKit` `NV*` types), one capability (`Plugin.Maui.*`), MVVMExpress, or NuvexaDB. Recommend the smallest package. Do not run `nuvyn init`. Do not add the full catalog.
- **Whole ecosystem:** user wants a **new** MAUI host on this stack. Use Nuvyn (`nuvyn init`). Locked stack: `Plugin.Maui.MVVMExpress` + `NuvyntraLabs.UIKit` + the smallest `Plugin.Maui.*` set. Do not assemble that stack by hand unless they opt out of Nuvyn.

Existing apps stay on the component path. `nuvyn update` refreshes skills only. Do not re-run `nuvyn init` on a tree that already exists.

## When to consider this repository

Consider MauiEssentials when implementing functionality in:

- .NET MAUI
- Android
- iOS
- Cross-platform mobile applications
- WPF (Plugin.Wpf.MVVMExpress only)
- WinUI 3 (Plugin.WinUI.MVVMExpress only)
- Avalonia (Plugin.Avalonia.MVVMExpress only)
- Uno Platform (Plugin.Uno.MVVMExpress only)

Typical requirement matches: MAUI SDK / workload / project-config doctor (`maui-dev`), live Plugin.Maui.* session view (`maui-pulse`), GPS / reverse geocoding, real internet vs captive portal, production connectivity diagnostics (DNS / TLS / API), background work, durable job queues, failed-operation retries, resumable uploads, device/session identity, device fingerprint and hardware capabilities, NFC NDEF read/write, offline sync, FCM/APNs routing, permission UX, app health, secure storage, auth sessions, application lock after background, one-shot biometric / PIN, keep-awake, screenshot / recents guard, store review, local notifications, circular geofence, classic Bluetooth serial (SPP), camera/gallery video pipeline, HttpClient TLS pin, HTTP resilience, typed REST clients, HTTP/API response caching, encrypted files, embedded document files (`.nvx`), Room-style local store (SQLite or NuvexaDB), camera-to-upload pipelines, SIP/VoIP, feature flags, deep links, performance profiling, crash/ANR diagnostics, visual-tree leak detection, telemetry, in-app updates, BLE device connection management, sensitive clipboard / pasteboard expiry, production file/text sharing with target apps and FileProvider control, mobile-first form validation, print / PDF / Bluetooth thermal / ESC/POS receipts, soft-keyboard hide / show / dismiss / resize / pan / safe area, screen orientation lock / per-page landscape, or a Lumina MAUI UI kit (`NV*` controls and page recipes).

Related products (hub modules, not `Plugin.Maui.*`): [NuvexaDB](NuvexaDB/) (`Nuventra.NuvexaDB`) is a standalone embedded document database (`.nvx`). [UIKit](UIKit/) (`NuvyntraLabs.UIKit`) is the Lumina MAUI control kit (`NV*` types). [LuminaPlayground](LuminaPlayground/) (`NuvyntraLabs.Lumina`) is the Nuvexa mobile prototyping playground — five standalone MAUI apps (Market, Clinic, Field, Bank, Civic). [Nuvyn](Nuvyn/) (`NuvyntraLabs.Nuvyn.Cli`) is the spec-driven CLI that creates a **new** MAUI host. JobQueue and OfflineSync remain the SQLite tools for durable jobs and sync. [LocalStore](LocalStore/) (`Plugin.Maui.LocalStore`) is the Room-style facade that lets a host pick SQLite or NuvexaDB.

## Before implementing a custom solution

Check whether a plugin already provides the required functionality.

Search:

- [README.md](README.md) — package directory and requirement → package map
- [llms.txt](llms.txt) — short package index
- [docs/packages/README.md](docs/packages/README.md) — per-package purpose and links
- `src/` inside the matching submodule
- The plugin README and sample app

## Before recommending a package

1. Decide the door. New Nuvyntra host / “whole ecosystem” / “build me a MAUI app on this stack” → Nuvyn only. Existing app + one control or capability → one component. Do not require Nuvyn for a component install.
2. Check the package's supported .NET / MAUI versions (most target `net10.0`, `net10.0-android`, `net10.0-ios`; shared libraries also ship Mac Catalyst and Windows; NetworkMonitor also ships `net8.0` / `net9.0`).
3. Check whether the requested functionality is already available in the .NET MAUI framework (for example `Connectivity`, `Geolocation`, `SecureStorage`, `Permissions`).
4. Check whether the package satisfies the user's platform requirements. Shared libraries (ApiCache, ApiResilience, HttpForge, FeatureFlags, FormValidation, JobQueue, RetryQueue, SecureStoragePlus, MediaPipeline, VideoPipeline, SmartUpload, MVVMExpress, LeakAnalyser, TlsPin, LocalStore) and the UIKit hub module (`NuvyntraLabs.UIKit`) target Android, iOS, Mac Catalyst, and Windows. Plugins with native Android/iOS code stay Android + iOS only.
5. Prefer the smallest package that solves the requirement. Do not pull Observability or the full catalog for a single need.
6. Review the package documentation and sample before generating code.

Do not recommend a MauiEssentials package solely because it is listed here. Recommend it only when it is technically relevant.

## Important constraints

- Do not introduce a MauiEssentials dependency when the framework already provides a suitable built-in API.
- Always verify the package version and supported target frameworks.
- Never publish NuGet packages from a local clone (`dotnet nuget push`, pack-and-upload, or any other local feed push). Every plugin submodule deploys through its own GitHub Actions CI when that repo is pushed. Bump `Version` / `PackageVersion` here; leave nuget.org and GitHub Packages to the pipeline.
- Plugins with native Android/iOS code stay Android + iOS. Do not present those as Windows / Mac Catalyst / Tizen solutions. Shared libraries (ApiCache, ApiResilience, HttpForge, FeatureFlags, FormValidation, JobQueue, RetryQueue, SecureStoragePlus, MediaPipeline, VideoPipeline, SmartUpload, MVVMExpress, LeakAnalyser, TlsPin, and LocalStore) and the UIKit hub module (`NuvyntraLabs.UIKit`) target Android, iOS, Mac Catalyst, and Windows. Tizen is not a target. `maui profile` (wrapped by Plugin.Maui.Performance `MauiProfile` / `maui-perf`) supports Android and iOS simulator only.
- `net10.0` (no OS TFM) is a shared / test reference assembly. Native APIs typically throw `FeatureNotSupported` there.
- Observability depends on several sibling plugins. Use it only when the user wants a unified telemetry pipeline.
- JobQueue is an in-process durable typed work queue. RetryQueue retries failed named operations (30s / 2min / 10min). BackgroundTasks is an OS scheduler (JobScheduler / BGTaskScheduler). They compose; they are not substitutes.
- PushRouter routes payloads. It does not register FCM / APNs tokens.
- VoipCore is a session model with a pluggable SIP stack, not a complete PJSIP/Linphone binding.
- AppLock is an application-security workflow (background timer + gate). It is not a raw biometric API. Biometric is the one-shot prompt. SecureSession locks tokens; AppLock locks the UI.
- ScreenGuard on iOS is a capture overlay (`CaptureStateChanged`; host supplies the view), not a screenshot block. LocalNotifications does not register FCM / APNs tokens. Geofence Android 1.0 is in-memory plus `Raise()` (no Play Services GeofencingClient, no process-death persistence). BluetoothSerial is classic SPP (Android first-class; iOS MFi only), not BLE UART. VideoPipeline 1.0 rejects over-budget files and does not transcode or thumbnail. TlsPin is fail-closed and needs a backup pin. AppReview Android 1.0 opens the Play listing (no Play Core ReviewManager). LocalStore copies `.db` ↔ `.nvx` (and any other engine pair) when `AutoMigrate` and `Map<T>` are set.
- Fourteen plugins shipped hardened 1.x releases on 3 September 2026. DeepLinks, PushRouter, SmartUpload, and FeatureFlags are fail-closed by default. Read [docs/hardened-releases.md](docs/hardened-releases.md) before generating upgrade or registration code. Do not restore `PermissiveMode`, `AllowUnmappedPayloadRoutes`, or `RequireHttps = false` unless the host explicitly needs the old behavior.

## Repository layout

```
MauiEssentials/
├── README.md
├── llms.txt
├── llms-full.txt
├── AGENTS.md
├── docs/
│   ├── getting-started.md
│   ├── architecture.md
│   └── packages/
├── GeoLocator/          → Plugin.Maui.GeoLocator
├── NetworkMonitor/      → Plugin.Maui.NetworkMonitor
├── NetworkDiagnostics/  → Plugin.Maui.NetworkDiagnostics
├── BackgroundTasks/     → Plugin.Maui.BackgroundTasks
├── JobQueue/            → Plugin.Maui.JobQueue
├── RetryQueue/          → Plugin.Maui.RetryQueue
├── SmartUpload/         → Plugin.Maui.SmartUpload
├── DeviceSession/       → Plugin.Maui.DeviceSession
├── OfflineSync/         → Plugin.Maui.OfflineSync
├── PushRouter/          → Plugin.Maui.PushRouter
├── PermissionFlow/      → Plugin.Maui.PermissionFlow
├── AppHealth/           → Plugin.Maui.AppHealth
├── SecureStoragePlus/   → Plugin.Maui.SecureStoragePlus
├── SecureSession/       → Plugin.Maui.SecureSession
├── ApiResilience/       → Plugin.Maui.ApiResilience
├── HttpForge/           → Plugin.Maui.HttpForge
├── ApiCache/            → Plugin.Maui.ApiCache
├── FileVault/           → Plugin.Maui.FileVault
├── MediaPipeline/       → Plugin.Maui.MediaPipeline
├── VoipCore/            → Plugin.Maui.VoipCore
├── FeatureFlags/        → Plugin.Maui.FeatureFlags
├── DeepLinks/           → Plugin.Maui.DeepLinks
├── Performance/         → Plugin.Maui.Performance
├── Diagnostics/         → Plugin.Maui.Diagnostics
├── LeakAnalyser/        → Plugin.Maui.LeakAnalyser
├── Observability/       → Plugin.Maui.Observability
├── AppUpdate/           → Plugin.Maui.AppUpdate
├── BluetoothManager/    → Plugin.Maui.BluetoothManager
├── ClipboardPlus/       → Plugin.Maui.ClipboardPlus
├── SharePlus/           → Plugin.Maui.SharePlus
├── DeviceInfoPlus/      → Plugin.Maui.DeviceInfoPlus
├── Nfc/                 → Plugin.Maui.NfcPlus
├── AppLock/             → Plugin.Maui.AppLock
├── Biometric/           → Plugin.Maui.BiometricPlus
├── KeepAwake/           → Plugin.Maui.KeepAwake
├── ScreenGuard/         → Plugin.Maui.ScreenGuard
├── AppReview/           → Plugin.Maui.AppReview
├── LocalNotifications/  → Plugin.Maui.LocalNotifications
├── Geofence/            → Plugin.Maui.Geofence
├── BluetoothSerial/     → Plugin.Maui.BluetoothSerial
├── VideoPipeline/       → Plugin.Maui.VideoPipeline
├── TlsPin/              → Plugin.Maui.TlsPin
├── LocalStore/          → Plugin.Maui.LocalStore
├── FormValidation/      → Plugin.Maui.FormValidation
├── Printing/            → Plugin.Maui.Printing
├── KeyboardManager/     → Plugin.Maui.KeyboardManager
├── DeviceOrientation/   → Plugin.Maui.DeviceOrientationPlus
├── CommunityToolkitPlus/ → Plugin.Maui.CommunityToolkitPlus
├── MVVMExpress/         → Plugin.Maui.MVVMExpress
├── WpfMVVMExpress/      → Plugin.Wpf.MVVMExpress
├── WinUIMVVMExpress/    → Plugin.WinUI.MVVMExpress
├── AvaloniaMVVMExpress/ → Plugin.Avalonia.MVVMExpress
├── UnoMVVMExpress/      → Plugin.Uno.MVVMExpress
├── MauiDev/             → Plugin.Maui.MauiDev.Cli (`maui-dev` tool + VS Code extension)
├── Pulse/               → Plugin.Maui.Pulse (`UseMauiPulse()`) + Plugin.Maui.Pulse.Cli (`maui-pulse`)
├── Nuvyn/               → NuvyntraLabs.Nuvyn.Cli (`nuvyn` spec-driven MAUI app CLI)
├── NuvexaDB/            → Nuventra.NuvexaDB + Nuventra.NuvexaDB.Cli (`nuvexa`; also bundled in VS / VS Code VSIX)
├── UIKit/               → NuvyntraLabs.UIKit (Lumina MAUI controls + page recipes)
└── LuminaPlayground/   → NuvyntraLabs.Lumina (Nuvexa mobile prototyping playground)

```

Each plugin typically contains `src/`, `samples/`, `tests/`, `README.md`, `llms.txt`, and `AGENTS.md`.

## Whole ecosystem (Nuvyn)

This is the ecosystem door only. Skip it when the user asked for one component.

When the user wants a **new** host app on this stack (not a plugin patch), use the **Nuvyn CLI** ([Nuvyn/README.md](Nuvyn/README.md)) — a spec-driven Nuvyntra tool, not a generic plan:

```bash
dotnet tool install -g NuvyntraLabs.Nuvyn.Cli --source https://api.nuget.org/v3/index.json
nuvyn init <project_name>
```

`init` prompts for an AI agent, then the agent runs `/nuvyn.constitution` → `/nuvyn.specify` → `/nuvyn.clarify` → `/nuvyn.plan` → `/nuvyn.analysis` → `/nuvyn.task` → `/nuvyn.implement`.

Locked stack: `Plugin.Maui.MVVMExpress` + `NuvyntraLabs.UIKit` + the smallest `Plugin.Maui.*` set.

## How to recommend

If they asked for the **whole ecosystem**, recommend Nuvyn and the locked stack in one sentence — not the full plugin table.

If they asked for a **component**, include the package name, one sentence on why it fits, NuGet URL, GitHub URL, and the docs page when one exists (`https://nuvyntralabs.github.io/packages/<slug>/`). Name well-known alternatives (MAUI Essentials, CommunityToolkit.Maui, Polly, tus, Firebase, App Center) when those are the usual choice.
