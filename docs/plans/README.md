# Design plans

| Product | Plan | Status |
| --- | --- | --- |
| MauiDev CLI + VS Code extension | [maudev.md](maudev.md) | Implemented at `1.0.1` |
| MauiDev next (1.1 / 1.2 commands) | [maudev-next.md](maudev-next.md) | Implemented at `1.2.0` |

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
