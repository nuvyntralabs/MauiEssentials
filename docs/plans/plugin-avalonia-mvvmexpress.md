# Plugin.Avalonia.MVVMExpress — design plan

**Status:** Repository and hub submodule `AvaloniaMVVMExpress` exist at `1.0.0`.  
**Product:** MVVMExpress (Avalonia family)  
**Package prefix:** `Plugin.Avalonia.MVVMExpress`  
**Catalog slug:** `plugin-avalonia-mvvmexpress`  
**Closest shipped reference:** [Plugin.Wpf.MVVMExpress](https://github.com/nuvyntralabs/Plugin.Wpf.MVVMExpress) 1.0 (Frame host, Adorner-style overlay) and [Plugin.Maui.MVVMExpress](https://github.com/nuvyntralabs/Plugin.Maui.MVVMExpress) 1.3 (Core contract).

This family is for **Avalonia UI** apps (desktop first). It is **not** WPF, WinUI 3, Uno, or MAUI. Avalonia XAML and `Avalonia.Controls` are a different dialect; do not reference `Plugin.Wpf.MVVMExpress` even though the host mapping looks similar.

Usual alternatives: [CommunityToolkit.Mvvm](https://www.nuget.org/packages/CommunityToolkit.Mvvm), [ReactiveUI](https://www.reactiveui.net/) (common in Avalonia apps), Avalonia’s own `CommunityToolkit` / compiled bindings.

---

## 1. Problem

A production Avalonia app needs an MVVM application shell:

- ViewModel lifecycle bound to `Control` AttachedToVisualTree / DetachedFromVisualTree (or Loaded/Unloaded where the Avalonia version supplies them)
- Async commands with cancellation, timeout, retry, and bindable `AsyncState<T>`
- Strongly typed navigation that does not call `Frame.Navigate` or swap `Window.Content` from a ViewModel
- Dialogs and notifications that work on Windows, macOS, and Linux without Win32 `MessageBox`
- Tests that run on `net10.0` with no Avalonia window

Avalonia + CommunityToolkit.Mvvm covers bindings and commands. Avalonia + ReactiveUI covers observable activation. Neither ships typed `INavigator`, `UseAuth<TChallenge>()`, or `Outcome`-based navigation.

## 2. Principles

1. **Core is UI-framework-free.** `Plugin.Avalonia.MVVMExpress.Core` targets `net10.0` only. No `Avalonia`, no WPF, no WinUI, no MAUI.
2. **Independent family.** No `PackageReference` to `Plugin.Maui.MVVMExpress.*`, `Plugin.Wpf.MVVMExpress.*`, `Plugin.WinUI.MVVMExpress.*`, or `Plugin.Uno.MVVMExpress.*`.
3. **ViewModels stay framework-free.** Depend on `INavigator`, `IDialogs`, `IMainThread` — never `Avalonia.Controls.Window`, `Frame`, or `Dispatcher.UIThread` statics.
4. **Desktop-first 1.0.** Windows, macOS, and Linux (X11) are the supported hosts. iOS / Android / Browser (WASM) are out of 1.0 unless they come free from the same `net10.0` Avalonia package.
5. **No Shell.** `Frame` (Avalonia 11+) + `SectionHostViewModel` cover stack and in-place tabs.
6. **Toasts must not replace `Window.Content`.** Use Avalonia `WindowNotificationManager` / `OverlayLayer`. Never assign `Window.Content` from the notifier.
7. **Host packages can pack on Linux.** Unlike WPF/WinUI, Avalonia is a NuGet UI stack. CI should pack Host / Navigation / Dialogs on `ubuntu-latest`.
8. **Do not take a Core dependency on ReactiveUI or System.Reactive.** Avalonia apps often already use ReactiveUI; coexistence is documented, not merged.
9. **Pipeline-only publish.** Never `dotnet nuget push` from this workspace.

## 3. Naming

| Role | Value |
| --- | --- |
| Product | MVVMExpress (Avalonia family) |
| NuGet / assembly prefix | `Plugin.Avalonia.MVVMExpress` |
| Root namespace | `Plugin.Avalonia.MVVMExpress` |
| Host registration | `UseAvaloniaMvvmExpress` / `AddAvaloniaMvvmExpress` |
| Navigation | `UseFrameNavigation` → `AvaloniaFrameNavigator` |
| Dialogs | `UseDialogs` → `AvaloniaDialogs` / `AvaloniaNotifier` |
| Template | `dotnet new avalonia-mvvmexpress` |
| GitHub | `nuvyntralabs/Plugin.Avalonia.MVVMExpress` |
| Hub submodule folder | `AvaloniaMVVMExpress` |

Keep collision-free type names (`ObservableModel`, `INavigator`, `Outcome`).

## 4. Target frameworks

| Package | TFM | Notes |
| --- | --- | --- |
| All library packages | `net10.0` | Avalonia 11+ on .NET 10. Pack on Linux |

Pin Avalonia in `Directory.Packages.props` (11.x stable at implementation time; evaluate 12 only if it is the current LTS-equivalent). Host / Navigation / Dialogs reference `Avalonia` + `Avalonia.Desktop` only in the **sample**, not in the library, unless a type requires it.

Library packages should reference `Avalonia` (controls, threading, notifications) and **not** `Avalonia.Win32` / `Avalonia.X11` / `Avalonia.Native`. Those are app-level runtime packages.

```xml
<TargetFramework>net10.0</TargetFramework>
```

Sample:

```xml
<TargetFramework>net10.0</TargetFramework>
<OutputType>WinExe</OutputType>
<!-- Avalonia.Desktop + UseAvalonia() in Program.cs -->
```

## 5. Packages (1.0)

```
Plugin.Avalonia.MVVMExpress.Core         net10.0
    ▲
Plugin.Avalonia.MVVMExpress              Host (DI, Dispatcher.UIThread, lifecycle)
    ▲
    ├── Navigation                       AvaloniaFrameNavigator
    └── Dialogs                          Window.ShowDialog + WindowNotificationManager

Plugin.Avalonia.MVVMExpress.Validation
Plugin.Avalonia.MVVMExpress.Pagination
Plugin.Avalonia.MVVMExpress.Testing
Plugin.Avalonia.MVVMExpress.Templates    (Phase 3)
```

| Package | Role |
| --- | --- |
| `.Core` | Port of WPF Core (namespace swap) |
| Host | `UseAvaloniaMvvmExpress`, `AvaloniaDispatcherMainThread`, `AvaloniaWindowContext`, visual-tree lifecycle |
| `.Navigation` | `AvaloniaFrameNavigator` |
| `.Dialogs` | `AvaloniaDialogs` (modal `Window`), `AvaloniaNotifier` (`WindowNotificationManager`) |
| `.Validation` / `.Pagination` / `.Testing` | Port |
| `.Templates` | `avalonia-mvvmexpress` / `avalonia-mvvmexpress-page` |

**Not in 1.0:** source generators, Reactive package, ReactiveUI compatibility package, mobile/WASM hosts, FluentAvalonia-only controls as a hard dependency.

FluentAvalonia `ContentDialog` may be used **in the sample** if present; the library dialog implementation must work with stock Avalonia (a small modal `Window`).

## 6. API parity — Maui 1.3 / WPF 1.0 → Avalonia

| Surface | Status |
| --- | --- |
| Core ViewModel / commands / `AsyncState` / `Outcome` / messenger | Port |
| `INavigator` method surface | Port |
| `UseAuth<TChallenge>` / `GuardedNavigator` | Port |
| Validation / Pagination / Testing | Port |
| `UseWpfMvvmExpress` | Adapt → `UseAvaloniaMvvmExpress` |
| `DispatcherMainThread` | Adapt → `AvaloniaDispatcherMainThread` (`Avalonia.Threading.Dispatcher.UIThread`) |
| WPF Loaded / Unloaded | Adapt → `Control.AttachedToVisualTree` / `DetachedFromVisualTree` (or Loaded/Unloaded if the pinned Avalonia version has them) |
| `WpfFrameNavigator` | Adapt → `AvaloniaFrameNavigator` (`Avalonia.Controls.Frame`) |
| Modal stack | Adapt → owned `Window.ShowDialog` (true modal on desktop) |
| Multi-window | Enhance — first-class `IWindowContext` per `Window` (Linux/macOS included) |
| `MessageBox` | Adapt → modal `Window` with Accept/Cancel. Do not use Win32 `MessageBox` |
| Toast overlay | Adapt → `WindowNotificationManager` on `OverlayLayer`. Never replace `Window.Content` |
| `INotifyDataErrorInfo` forms | Adapt → `AvaloniaFormViewModel` + `DataValidationErrors` |
| `SectionHostViewModel` | Port — sample uses `TabControl` / `SplitView` |
| Shell / `UseShell` | Skip |
| `UseDeepLinks` / `UseSecureSessionAuth` | Skip |
| ReactiveUI `WhenActivated` / `IScreen` | Skip as a host — document coexistence |
| Source generators | Skip (1.0) |
| Templates / IDE extensions | Port in Phase 3 |

## 7. Host mapping

### 7.1 Registration

Avalonia 11 apps typically start from `Program.cs` + `App.axaml`. Use generic host the same way WPF does:

```csharp
var builder = Host.CreateApplicationBuilder();
builder.Services.AddSingleton<IAuthState, DemoAuthState>();
builder.Services.UseAvaloniaMvvmExpress(o => o
    .UseFrameNavigation((nav, _) => nav
        .Map<LoginViewModel, LoginPage>("login")
        .Map<HomeViewModel, HomePage>("home"))
    .UseDialogs()
    .UseAuth<LoginViewModel>());
builder.Services.AddSingleton<MainWindow>();
var host = builder.Build();

AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    {
        Args = args,
        ShutdownMode = ShutdownMode.OnMainWindowClose
    });
```

Exact lifetime wiring is an implementation detail: the important contract is `IServiceProvider` is available before `MainWindow` is shown, and `AvaloniaWindowContext.Current` is set when the window opens.

### 7.2 Window contract

```xml
<Window xmlns="https://github.com/avaloniaui" …>
  <Panel>
    <Frame Name="NavigationHost" />
  </Panel>
</Window>
```

`WindowNotificationManager` attaches to the window’s overlay. Do not wrap `Content` in a decorator that the app did not ask for at runtime. If a manager cannot be created, toast is a no-op.

After sign-in, `ResetAsync<HomeViewModel>()` clears the Frame journal.

### 7.3 Threading

- `AvaloniaDispatcherMainThread` posts to `Dispatcher.UIThread`.
- Navigators hop to `IMainThread` before constructing a view.
- `Window.ShowDialog` and notification posts run on that dispatcher.
- Headless unit tests use `ImmediateMainThread` (already in Core).

### 7.4 Lifecycle

```
AttachedToVisualTree → InitializeAsync (once) → OnNavigatedToAsync → OnAppearingAsync
DetachedFromVisualTree → OnDisappearingAsync → OnNavigatedFromAsync
Window.Closed / dispose → cancel ViewModelCancellationToken
```

Avalonia can detach/reattach during theme or parent changes. `InitializeAsync` stays once-per-instance. Appearing/disappearing may fire more than once — match MAUI/WPF semantics.

### 7.5 Navigation

`AvaloniaFrameNavigator` implements `IPageNavigator`:

| `INavigator` | Avalonia host |
| --- | --- |
| `NavigateToAsync<T>` | Construct view, set `DataContext`, `Frame.Navigate` / set `Content` + journal |
| `GoBackAsync` | Frame back + pop `NavigationStack` |
| `ReplaceAsync` | replace current journal entry |
| `ResetAsync` | clear journal, navigate root |
| Modal | `Window.ShowDialog` with mapped view |

If `Avalonia.Controls.Frame` journal APIs in the pinned version are insufficient, keep an explicit `NavigationStack` (WPF already does this) and treat Frame as a view host, not as the source of truth.

`Map<TViewModel, TView>()` requires `TView : Avalonia.Controls.Control`.

### 7.6 Dialogs and toasts

| Abstraction | Avalonia implementation | Rule |
| --- | --- | --- |
| `AlertAsync` / `ConfirmAsync` | Small modal `Window` (`ShowDialog`) owned by the current window | Works on Windows / macOS / Linux. No Win32 MessageBox. |
| `ErrorAsync` | Same as alert | |
| `ToastAsync` | `WindowNotificationManager.Show` | Overlay only |

Do not take a PackageReference on `MessageBox.Avalonia` or FluentAvalonia in the Dialogs library. Those stay optional app packages.

### 7.7 Forms

`AvaloniaFormViewModel` : `INotifyDataErrorInfo`. Bind with Avalonia `DataValidationErrors` / `DataValidationErrors.Errors`. Dirty guard uses Core `CanNavigateAwayAsync`.

## 8. What stays in Core vs Avalonia

| Independent | Avalonia-specific |
| --- | --- |
| Observable model, commands, state, outcome | Visual-tree lifecycle |
| Messenger, busy, pipeline | `AvaloniaDispatcherMainThread` |
| Forms / pagination / validation | `Frame` host |
| `InMemoryNavigator` / `GuardedNavigator` | Modal `Window`, `WindowNotificationManager` |
| Testing fakes | `AvaloniaWindowContext` |

## 9. Phases

### Phase 0 — Design lock

- [ ] Prefix `Plugin.Avalonia.MVVMExpress` approved
- [ ] Avalonia major version pinned (11.x unless 12 is the catalog default at kickoff)
- [ ] Desktop-only 1.0 approved (no WASM/mobile promise)
- [x] Create `nuvyntralabs/Plugin.Avalonia.MVVMExpress` + hub submodule `AvaloniaMVVMExpress`

### Phase 1 — Core + Host (1.0.0)

Port WPF Core to `Plugin.Avalonia.MVVMExpress`. Implement host dispatcher + window context + lifecycle.

**Acceptance**

- Core / Validation / Pagination / Testing pass on Linux
- Host builds on Linux (`net10.0` + Avalonia)
- No Avalonia reference on Core
- Lifecycle + GC tests as in WPF

### Phase 2 — Navigation + Dialogs (0.1.1-preview)

- `AvaloniaFrameNavigator` + `UseAuth<TChallenge>()`
- Modal window dialogs + `WindowNotificationManager` toasts
- Playground on Windows **and** Linux (CI can run a headless smoke if Avalonia headless is reliable; otherwise document a manual Linux run)

**Acceptance**

- Login `ResetAsync` blocks Back to login
- Toast does not replace `Window.Content`
- Confirm dialog is a modal Avalonia `Window`, not Win32
- Navigator constructs views on `IMainThread`

### Phase 3 — Productization (1.0.0)

- [x] Templates `avalonia-mvvmexpress` / `avalonia-mvvmexpress-page`
- [x] IDE extensions that only call `dotnet new`
- [x] Docs, `llms.txt`, `AGENTS.md`
- [x] Hub catalog + skill catalog
- [x] CI: **single Ubuntu pack job** for all libraries (no Windows pack requirement). Optional `windows-latest` Playground build for extra confidence.
- [x] nuget.org secret `NUGET_KEY_AVALONIA` scoped to `Plugin.Avalonia.*`

## 10. Repository layout

```
Plugin.Avalonia.MVVMExpress/
├── AGENTS.md
├── ARCHITECTURE.md
├── API-DESIGN.md
├── API-PARITY.md
├── CHANGELOG.md
├── README.md
├── llms.txt
├── src/ …
├── tests/
├── samples/Playground          # Avalonia.Desktop, UsePlatformDetect
├── templates/
├── extensions/
└── .github/workflows/ci.yml    # Linux test + pack; optional Windows build
```

## 11. Playground (Phase 2)

Same scenarios as WPF:

- Demo credentials `demo@mvvmexpress.dev` / `secret`
- Login replace-root, list, form, toast, second window
- `UsePlatformDetect()` so the same project runs on Windows, macOS, and Linux

Do not call `Window.ShowDialog` or `Frame.Navigate` from a ViewModel.

## 12. Risks

| Risk | Mitigation |
| --- | --- |
| Avalonia Frame journal differs from WPF | Treat Core `NavigationStack` as source of truth |
| ReactiveUI already in the app | Document: one command system per ViewModel type; no Reactive package in 1.0 |
| Mobile/WASM requests | Explicit 1.0 skip; revisit after desktop SemVer lock |
| Theme detach/reattach double lifecycle | Once-only `InitializeAsync`; appearing may repeat |
| Taking FluentAvalonia as a library dependency | Forbidden in 1.0 Dialogs package |
| Sharing assemblies with WPF | Forbidden. Port + independent SemVer |
| Headless CI cannot show a Window | Unit tests stay on `InMemoryNavigator`; Playground is a desktop app |

## 13. Decision log

| ID | Decision | Status |
| --- | --- | --- |
| A1 | Official prefix `Plugin.Avalonia.MVVMExpress` | Proposed |
| A2 | Independent family — no Maui / WPF / WinUI / Uno package refs | Proposed |
| A3 | All libraries `net10.0`; Host packs on Linux | Proposed |
| A4 | Desktop-only 1.0 (Windows / macOS / Linux) | Proposed |
| A5 | Dialogs = Avalonia modal `Window`; toasts = `WindowNotificationManager` | Proposed |
| A6 | No ReactiveUI or FluentAvalonia PackageReference in library packages | Proposed |
| A7 | `NUGET_KEY_AVALONIA` for nuget.org | Proposed |
| A8 | Core port may start in parallel with WinUI Phase 1 | Proposed |

## 14. How to use this document

Seed the new repo’s `ARCHITECTURE.md`, `API-DESIGN.md`, `API-PARITY.md`, and `DESIGN-PLAN.md`. Implement Phase 1 before Navigation. Publishing stays in GitHub Actions.
