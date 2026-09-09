# Plugin.Uno.MVVMExpress — design plan

**Status:** Repository and hub submodule `UnoMVVMExpress` exist at `1.0.0`.  
**Product:** MVVMExpress (Uno Platform family)  
**Package prefix:** `Plugin.Uno.MVVMExpress`  
**Catalog slug:** `plugin-uno-mvvmexpress`  
**Closest shipped reference:** WinUI family plan ([plugin-winui-mvvmexpress.md](plugin-winui-mvvmexpress.md)) for Frame / `ContentDialog` / `XamlRoot`, and [Plugin.Maui.MVVMExpress](https://github.com/nuvyntralabs/Plugin.Maui.MVVMExpress) 1.3 for multi-TFM hosting and Core.

This family is for **Uno Platform** apps that use the **WinUI** API surface (`Microsoft.UI.Xaml` via Uno.Sdk). It is **not** `Plugin.Maui.MVVMExpress` (MAUI XAML). It is **not** `Plugin.WinUI.MVVMExpress` (Windows App SDK only). Do **not** type-forward or PackageReference the WinUI family — Uno TFMs, `Uno.Sdk`, and Skia/WASM hosts are a different pack graph.

Usual alternatives: [CommunityToolkit.Mvvm](https://www.nuget.org/packages/CommunityToolkit.Mvvm), [Uno.Extensions.Navigation](https://platform.uno/docs/articles/external/uno.extensions/doc/Learn/Navigation/Overview.html), Prism.

---

## 1. Problem

Uno gives one WinUI XAML codebase across Windows App SDK, Skia desktop, Android, iOS, and WebAssembly. Apps still need:

- ViewModel lifecycle that works when the host is a `Page` inside a `Frame` on every head
- Typed navigation without `Frame.Navigate` in ViewModels
- Dialogs that use `ContentDialog` where it works and a safe fallback on heads that do not
- The same Core contract so a MAUI or WPF ViewModel ports with a namespace swap

Uno.Extensions.Navigation is a capable router. MVVMExpress must not wrap or fork it. The product is the same `INavigator` / `AsyncState` / `UseAuth<TChallenge>()` shell as the other families.

## 2. Principles

1. **Core is UI-framework-free.** `Plugin.Uno.MVVMExpress.Core` is `net10.0` only. No `Uno.WinUI`, no `Microsoft.WindowsAppSDK`, no MAUI.
2. **Independent family.** No `PackageReference` to `Plugin.Maui.MVVMExpress.*`, `Plugin.Wpf.MVVMExpress.*`, `Plugin.WinUI.MVVMExpress.*`, or `Plugin.Avalonia.MVVMExpress.*`.
3. **Do not share a nupkg with WinUI.** Copy WinUI host *patterns* after that family exists. Uno.Sdk multi-targeting cannot live inside `Plugin.WinUI.MVVMExpress`.
4. **ViewModels stay host-agnostic.** `INavigator`, `IDialogs`, `IMainThread` only.
5. **No MAUI Shell and no Uno.Extensions.Navigation dependency.** `Frame` + `SectionHostViewModel` are the 1.0 hosts.
6. **Toasts must not replace `Window.Content`.** `Popup` / overlay on `XamlRoot`. If a head has no `XamlRoot` yet, toast is a no-op.
7. **1.0 heads are explicit.** WinAppSDK + Skia desktop + one mobile head in the Playground. WASM is best-effort in 1.0, not a SemVer promise.
8. **Do not PackageReference Uno.Extensions, Prism, or CommunityToolkit** from library projects.
9. **Pipeline-only publish.** Never `dotnet nuget push` from this workspace.

## 3. Naming

| Role | Value |
| --- | --- |
| Product | MVVMExpress (Uno family) |
| NuGet / assembly prefix | `Plugin.Uno.MVVMExpress` |
| Root namespace | `Plugin.Uno.MVVMExpress` |
| Host registration | `UseUnoMvvmExpress` / `AddUnoMvvmExpress` |
| Navigation | `UseFrameNavigation` → `UnoFrameNavigator` |
| Dialogs | `UseDialogs` → `UnoDialogs` / `UnoNotifier` |
| Template | `dotnet new uno-mvvmexpress` |
| GitHub | `nuvyntralabs/Plugin.Uno.MVVMExpress` |
| Hub submodule folder | `UnoMVVMExpress` |

Collision-free Core names stay (`ObservableModel`, `INavigator`, `Outcome`).

## 4. Target frameworks

Uno Platform 6.4+ defaults new apps to .NET 10. Host / Navigation / Dialogs use Uno.Sdk multi-targeting:

| Head | TFM | 1.0 support |
| --- | --- | --- |
| Shared / tests / Core | `net10.0` | Required |
| Windows App SDK | `net10.0-windows10.0.19041.0` | Required |
| Skia desktop (Windows / macOS / Linux) | `net10.0-desktop` | Required |
| Android | `net10.0-android` | Required (Playground) |
| iOS | `net10.0-ios` | Required if CI has a Mac runner; otherwise documented manual |
| WebAssembly | `net10.0-browserwasm` | Best-effort — build in CI if cheap; no WASM-only bugs block 1.0 |

```xml
<TargetFrameworks>
  net10.0;
  net10.0-android;
  net10.0-ios;
  net10.0-windows10.0.19041.0;
  net10.0-desktop
</TargetFrameworks>
```

`net10.0` (no OS TFM) is the shared / test surface. Host APIs that need a window throw `FeatureNotSupportedException` there — same rule as MAUI.

Pin `Uno.Sdk` in `global.json` / the repo SDK. Do not also target UWP (`Uno.UI`). WinUI API only.

Core / Validation / Pagination / Testing stay **single** `net10.0` and pack on Linux.

## 5. Packages (1.0)

```
Plugin.Uno.MVVMExpress.Core              net10.0
    ▲
Plugin.Uno.MVVMExpress                   Host (Uno.Sdk TFMs)
    ▲
    ├── Navigation                       UnoFrameNavigator
    └── Dialogs                          ContentDialog + XamlRoot overlay

Plugin.Uno.MVVMExpress.Validation        net10.0
Plugin.Uno.MVVMExpress.Pagination        net10.0
Plugin.Uno.MVVMExpress.Testing           net10.0
Plugin.Uno.MVVMExpress.Templates         (Phase 3)
```

| Package | Role |
| --- | --- |
| `.Core` | Port of WPF / Maui Core |
| Host | `UseUnoMvvmExpress`, `UnoDispatcherMainThread`, `UnoWindowContext`, Loaded/Unloaded lifecycle |
| `.Navigation` | `UnoFrameNavigator.Map<TViewModel, TView>()` |
| `.Dialogs` | `UnoDialogs`, `UnoNotifier` |
| `.Validation` / `.Pagination` / `.Testing` | Port |
| `.Templates` | `uno-mvvmexpress` / `uno-mvvmexpress-page` on Uno.Sdk |

**Not in 1.0:** source generators, Reactive, CommunityToolkit compatibility, `UseDeepLinks` (abstraction may exist in Core; no Plugin.Maui.DeepLinks adapter), `UseSecureSessionAuth`, Uno.Extensions.Navigation interop package, Prism regions.

## 6. API parity — Maui 1.3 / WPF 1.0 / WinUI plan → Uno

| Surface | Status |
| --- | --- |
| Core ViewModel / commands / `AsyncState` / `Outcome` / messenger | Port |
| `INavigator` method surface | Port |
| `UseAuth<TChallenge>` / `GuardedNavigator` | Port |
| Validation / Pagination / Testing | Port |
| `UseWinUIMvvmExpress` | Adapt → `UseUnoMvvmExpress` |
| `DispatcherQueueMainThread` | Adapt → `UnoDispatcherMainThread` (`DispatcherQueue` on WinUI heads; Uno dispatcher on Skia/WASM) |
| Lifecycle | Adapt → `FrameworkElement.Loaded` / `Unloaded` (WinUI surface) |
| `WinUIFrameNavigator` | Adapt → `UnoFrameNavigator` (same `Microsoft.UI.Xaml.Controls.Frame` API) |
| Modal stack | Adapt → `ContentDialog` where supported; owned `Window` on desktop heads |
| Multi-window | Partial — first-class on WinAppSDK / Skia desktop; single-window on mobile / WASM |
| `ContentDialog` | Adapt — must set `XamlRoot`; fallback alert `Window` if `ContentDialog` is unsupported on a head |
| Toast overlay | Adapt → `Popup` + `InfoBar` on `XamlRoot` |
| `INotifyDataErrorInfo` forms | Adapt → `UnoFormViewModel` |
| `SectionHostViewModel` | Port — sample `NavigationView` |
| Shell / `UseShell` | Skip |
| Uno.Extensions.Navigation | Skip (do not wrap) |
| `UseDeepLinks` / SecureSession | Skip as host adapters (mobile deep links are a post-1.0 sample) |
| Source generators | Skip (1.0) |
| Templates / IDE extensions | Port in Phase 3 |

## 7. Host mapping

### 7.1 Registration

Uno apps use `App.xaml.cs` + Uno.Sdk. Register on the same generic host / `IServiceCollection` the app already builds:

```csharp
builder.Services.AddSingleton<IAuthState, DemoAuthState>();
builder.Services.UseUnoMvvmExpress(o => o
    .UseFrameNavigation((nav, _) => nav
        .Map<LoginViewModel, LoginPage>("login")
        .Map<HomeViewModel, HomePage>("home"))
    .UseDialogs()
    .UseAuth<LoginViewModel>());
```

`App.OnLaunched` / desktop lifetime shows `MainWindow` and sets `UnoWindowContext.Current`.

Do not require `Uno.Extensions.Hosting`. `Microsoft.Extensions.DependencyInjection` + `Microsoft.Extensions.Hosting` is enough (same as WPF).

### 7.2 Window contract

```xml
<Window …>
  <Grid>
    <Frame x:Name="NavigationHost" />
  </Grid>
</Window>
```

Same visual contract as the WinUI family. After sign-in, `ResetAsync<HomeViewModel>()` clears the journal.

### 7.3 Threading

- Capture a dispatcher at host start (`DispatcherQueue` on WinAppSDK; Uno’s UI dispatcher on other heads).
- Navigators hop to `IMainThread` **before** constructing a `Page`.
- Never call `ContentDialog.ShowAsync` off-thread.
- WASM: dispatcher hop is still required; do not block the UI thread with `.Result`.

### 7.4 Lifecycle

WinUI `Loaded` / `Unloaded` on the page:

```
Loaded → InitializeAsync (once) → OnNavigatedToAsync → OnAppearingAsync
Unloaded → OnDisappearingAsync → OnNavigatedFromAsync
```

Mobile may unload pages more aggressively than WinAppSDK. Page-scope dispose on pop remains the leak rule (same as MAUI).

### 7.5 Navigation

`UnoFrameNavigator` is the WinUI Frame navigator with Uno-safe construction:

| `INavigator` | Uno host |
| --- | --- |
| `NavigateToAsync<T>` | Resolve page from DI, set `DataContext`, `Frame.Navigate` |
| `GoBackAsync` / `ReplaceAsync` / `ResetAsync` / `PopToRootAsync` | Frame journal + Core `NavigationStack` |
| Modal | `ContentDialog` hosting a mapped view |

`Map<TViewModel, TView>()` requires `TView : Microsoft.UI.Xaml.FrameworkElement`.

If a head’s `Frame` journal is incomplete, Core `NavigationStack` is the source of truth (WPF lesson).

### 7.6 Dialogs and toasts

| Abstraction | Implementation | Head notes |
| --- | --- | --- |
| `AlertAsync` / `ConfirmAsync` | `ContentDialog` + `XamlRoot` | If `ContentDialog` fails on a head, fall back to a modal `Window` on desktop; on mobile throw `FeatureNotSupportedException` only after fallback is impossible — prefer a code-path that always shows *something* |
| `ErrorAsync` | Same | |
| `ToastAsync` | `Popup` + `InfoBar` | No-op if `XamlRoot` is null. Never replace `Window.Content` |

Do not use WPF `MessageBox` or Avalonia APIs.

### 7.7 Forms

`UnoFormViewModel` : `INotifyDataErrorInfo`. WinUI binding + `DataAnnotations` from the Validation package.

## 8. What stays in Core vs Uno

| Independent | Uno-specific |
| --- | --- |
| Observable model, commands, state, outcome | Loaded/Unloaded lifecycle |
| Messenger, busy, pipeline | `UnoDispatcherMainThread` |
| Forms / pagination / validation | `UnoFrameNavigator` |
| `InMemoryNavigator` / `GuardedNavigator` | `ContentDialog` / `Popup` |
| Testing fakes | `UnoWindowContext` |

Sibling MauiEssentials plugins (DeepLinks, SecureSession, NetworkMonitor) are **not** PackageReferences. A later sample may adapt them on Android/iOS only.

## 9. Phases

### Phase 0 — Design lock

- [ ] Prefix `Plugin.Uno.MVVMExpress` approved
- [ ] 1.0 heads approved (WinAppSDK + desktop + Android; iOS/WASM as above)
- [ ] WinUI family Phase 2 exists **or** this family accepts copying from the WinUI *plan* without waiting for its nupkg
- [x] Create `nuvyntralabs/Plugin.Uno.MVVMExpress` + hub submodule `UnoMVVMExpress`
- [ ] Pin Uno.Sdk version in the repo

**Recommendation:** start Uno Phase 1 (Core port) anytime. Start Uno Phase 2 (Frame host) after the WinUI navigator is sketched or merged — the code will look like `WinUIFrameNavigator` with Uno TFMs.

### Phase 1 — Core + Host (1.0.0)

Port Core. Implement `UseUnoMvvmExpress`, dispatcher, window context, lifecycle.

**Acceptance**

- Core tests pass on Linux
- Host builds at least `net10.0` + `net10.0-desktop` on Linux and `net10.0-windows10.0.19041.0` on Windows
- No Uno / WinUI reference on Core

### Phase 2 — Navigation + Dialogs (0.1.1-preview)

- `UnoFrameNavigator` + `UseAuth<TChallenge>()`
- Dialogs + overlay toast
- Playground: WinAppSDK **and** Skia desktop; Android if the CI image allows

**Acceptance**

- Login replace-root
- Toast does not replace `Window.Content`
- `ContentDialog` has `XamlRoot` on WinAppSDK
- Desktop Skia Playground navigates Home → Details with typed args
- View construction on `IMainThread`

### Phase 3 — Productization (1.0.0)

- [x] `dotnet new uno-mvvmexpress` (Uno.Sdk single-project)
- [x] IDE extensions that only call `dotnet new`
- [x] Docs, `llms.txt`, `AGENTS.md`, known-limitations (WASM, multi-window on mobile)
- [x] Hub catalog + skill catalog
- [x] CI:
  - Linux: test Core; pack Core/Validation/Pagination/Testing/Templates; build Host for `net10.0` + `net10.0-desktop`
  - Windows: pack Host/Navigation/Dialogs including `net10.0-windows10.0.19041.0`
  - Optional Mac: `net10.0-ios` build
- nuget.org secret `NUGET_KEY_UNO` scoped to `Plugin.Uno.*`

## 10. Repository layout

```
Plugin.Uno.MVVMExpress/
├── AGENTS.md
├── ARCHITECTURE.md
├── API-DESIGN.md
├── API-PARITY.md
├── CHANGELOG.md
├── README.md
├── llms.txt
├── global.json                 # Uno.Sdk pin
├── src/ …
├── tests/                      # net10.0 only
├── samples/Playground          # Uno.Sdk multi-head
├── templates/
├── extensions/
└── .github/workflows/ci.yml
```

Playground should be one Uno.Sdk project with heads enabled in the csproj, not four duplicate samples.

## 11. Playground (Phase 2)

Same functional script as WPF / WinUI:

- Demo credentials `demo@mvvmexpress.dev` / `secret`
- Login replace-root, list, form, toast
- Second window **only** on desktop heads (hide the button on Android / WASM)

Do not call `Frame.Navigate` or `ContentDialog.ShowAsync` from a ViewModel.

## 12. Risks

| Risk | Mitigation |
| --- | --- |
| “Just use the WinUI nupkg” | Different TFMs and Uno.Sdk; document in README |
| Uno.Extensions.Navigation collision | Different type names; no package ref; migration note only |
| `ContentDialog` / `XamlRoot` gaps on Skia or WASM | Fallback + known-limitations; tests per head where CI can run |
| MAUI users installing Uno packages | README: Uno XAML apps only |
| iOS CI cost | 1.0 may ship iOS TFM built on Mac only when a runner exists |
| Copy-paste drift from WinUI family | After both exist, a short `API-PARITY.md` row tracks host-only diffs |
| Taking `Uno.WinUI` from Core | Forbidden |
| Deep linking / push on mobile | Out of 1.0; compose later |

## 13. Decision log

| ID | Decision | Status |
| --- | --- | --- |
| U1 | Official prefix `Plugin.Uno.MVVMExpress` | Proposed |
| U2 | Independent family — no WinUI nupkg reference | Proposed |
| U3 | Uno.Sdk + WinUI API only (no UWP `Uno.UI`) | Proposed |
| U4 | 1.0 heads: WinAppSDK, `net10.0-desktop`, Android; iOS/WASM not SemVer-blocking | Proposed |
| U5 | Frame + `ContentDialog` + `XamlRoot` overlay | Proposed |
| U6 | No Uno.Extensions.Navigation / Prism PackageReference | Proposed |
| U7 | `NUGET_KEY_UNO` for nuget.org | Proposed |
| U8 | Implement host after WinUI host patterns exist; Core may start earlier | Proposed |

## 14. How to use this document

Seed the new repo’s architecture and design-plan files. Do not generate the full multi-head framework in one change. Phase 1 (Core + dispatcher) first. Publishing stays in GitHub Actions.
