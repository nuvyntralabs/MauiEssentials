# Design plans

| Product | Plan | Status |
| --- | --- | --- |
| MauiDev CLI + VS Code extension | [maudev.md](maudev.md) | Implemented at `1.0.1` |
| MauiDev next (1.1 / 1.2 commands) | [maudev-next.md](maudev-next.md) | Implemented at `1.2.3` (1.2 commands plus 4-hour nuget.org update check; TFM union + workload host skip) |
| Next-wave runtime plugins (9 packages; no barcode) | [next-wave-plugins.md](next-wave-plugins.md) | 1.0.2 published; Geofence / AppReview / VideoPipeline 1.1 deepen implemented |
| NuvexaDB embedded `.nvx` document database | Hub module `NuvexaDB/` (`Nuventra.NuvexaDB`) | Implemented at `1.0.0` (related product; not `Plugin.Maui.*`) |
| NuvyntraLabs.UIKit (MAUI controls + page recipes, `NV*` types) | [nuvyntralabs-uikit.md](nuvyntralabs-uikit.md) · [components](nuvyntralabs-uikit-components.md) | Implemented at `1.6.0` (201 controls + 66 recipes; Lumina visual refresh; `NVInputField` replaces `NVEmailField`; related product; not `Plugin.Maui.*`; CI publishes nuget.org + GitHub Packages) |
| NuvyntraLabs.UIKit next (1.1 deepen + 1.2 / 1.3 names) | [nuvyntralabs-uikit-next.md](nuvyntralabs-uikit-next.md) | 1.2 / 1.3 catalog + 1.4 deepen + 1.5 `NVInputField` rename shipped |
| Nuvyn (Spec-driven CLI for Nuvyntra MAUI apps) | [nuvyn.md](nuvyn.md) | Implemented at `1.2.0` — `NuvyntraLabs.Nuvyn.Cli`, command `nuvyn`; `init` + `adopt` (existing MAUI, no stack rewrite) + `update` + host proof + 4-hour update check + optional `maui-dev doctor`; Spec Kit coding-agent set; CI packs and publishes from `Nuvyn/.github/workflows/ci.yml` |
| NuvLoc (agent-driven localization CLI; `i18n.json`) | [nuvloc.md](nuvloc.md) | Implemented at `1.1.1` — `NuvyntraLabs.NuvLoc.Cli`, command `nuvloc`; `init --agent` + `/nuvloc.status` + `/nuvloc.translate`; sibling `.resx` (`maui` / `wpf` / `winui` / `avalonia` / `uno`); no provider / API key; resource files only |

## MVVMExpress platform family plans

Planning documents for the desktop MVVMExpress families. Repositories and hub submodules exist at `1.0.0`. Each family is an independent git repository and NuGet prefix — the same model as `Plugin.Wpf.MVVMExpress`.

| Family | Plan | Closest shipped reference |
| --- | --- | --- |
| WinUI 3 / Windows App SDK | [plugin-winui-mvvmexpress.md](plugin-winui-mvvmexpress.md) | WPF Frame host |
| Avalonia UI | [plugin-avalonia-mvvmexpress.md](plugin-avalonia-mvvmexpress.md) | WPF Frame host + Linux-packable UI |
| Uno Platform | [plugin-uno-mvvmexpress.md](plugin-uno-mvvmexpress.md) | WinUI Frame + MAUI multi-TFM CI |

## Shared contract

Taken from [Plugin.Wpf.MVVMExpress](https://github.com/nuvyntralabs/Plugin.Wpf.MVVMExpress) and [Plugin.Maui.MVVMExpress](https://github.com/nuvyntralabs/Plugin.Maui.MVVMExpress) 1.3:

1. Core stays UI-framework-free (`net10.0`). No WinUI, Avalonia, Uno, WPF, or MAUI references.
2. No `PackageReference` to `Plugin.Maui.MVVMExpress.*` or `Plugin.Wpf.MVVMExpress.*`. Core is a **port** (namespace swap), not a type-forward.
3. ViewModels depend on `INavigator`, `IDialogs`, `IMainThread` — never `Frame.Navigate`, `ContentDialog`, `MessageBox`, or `Window.ShowDialog`.
4. Navigators hop to `IMainThread` **before** constructing a view.
5. Toasts overlay the tree. They must not replace `Window.Content`.
6. Publishing is pipeline-only. Do not run `dotnet nuget push` from a local clone.

## Recommended implementation order

1. **WinUI 3** — single OS, Frame + `ContentDialog` map cleanly from WPF.
2. **Avalonia** — Core can start in parallel with WinUI; the host is a different XAML dialect but packs on Linux.
3. **Uno** — reuse WinUI host patterns after they exist; do **not** share a nupkg with WinUI (Uno.Sdk TFMs differ).

`Plugin.Maui.MVVMExpress` already covers MAUI-on-Windows (WinUI under MAUI). These three families are for apps that are **not** MAUI.

## Next-wave runtime plugins

Planning document for nine new `Plugin.Maui.*` repositories. Barcode / QR scanning is out of this wave.

| Wave | Packages |
| --- | --- |
| 1 — thin native gates | Biometric, KeepAwake, ScreenGuard, AppReview |
| 2 — field loop | LocalNotifications, Geofence |
| 3 — hardware / media / TLS | BluetoothSerial, VideoPipeline, TlsPin |

Catalog contract (one problem per package, `UseX`, no sibling `PackageReference`, pipeline-only publish) is in [next-wave-plugins.md](next-wave-plugins.md). All nine nupkgs shipped at `1.0.2`. Geofence, AppReview, and VideoPipeline 1.1 deepen OS geofences, Play Core review, and thumbnail / transcode.
