# MauiDev — design plan

**Status:** Repository and hub submodule `MauiDev` exist at `1.0.1`.  
**Product:** MauiDev — developer productivity toolkit for .NET MAUI  
**Package:** `Plugin.Maui.MauiDev.Cli` (`PackAsTool`, command `maui-dev`). nuget.org reserved `MauiDev.Cli`.  
**Extension:** `nuvyntralabs.maui-dev`  
**Closest shipped reference:** [Plugin.Maui.Performance.Cli](../../Performance/src/Plugin.Maui.Performance.Cli/Plugin.Maui.Performance.Cli.csproj)

This is a machine + project toolchain, not a runtime `Plugin.Maui.*` library. `maui-perf`, LeakAnalyser, AppHealth, and Diagnostics stay the runtime/profiling products.

Usual alternatives: maui-check, `dotnet workload`, Visual Studio MAUI installer, Microsoft `maui` CLI.

## Decisions

- GitHub: `nuvyntralabs/MauiDev`
- Hub folder: `MauiDev`
- `MauiDev.Core` is internal (`IsPackable=false`)
- Analyze v1 is heuristic, not Roslyn
- Pipeline-only publish (NuGet + optional Marketplace / Open VSX)
- `doctor --fix` allow-list: duplicate MAUI resource items, missing `UseMaui`

## 1.0 commands

`doctor`, `analyze`, `resources`, `clean`, `package`

Global: `--path`, `--format human|json|sarif`, `--ci`, `--fix`, `--dry-run`, `--warn-as-error`

## Release

CI on the plugin repo: version align (CLI + extension `package.json`), NuGet key check, unit tests, Linux pack, nuget.org + GitHub Packages, `vsce package`. Marketplace/Open VSX when `VSCE_PAT` / `OVSX_PAT` exist.

Never `dotnet nuget push` or `vsce publish` from a local clone.

Next slice: [maudev-next.md](maudev-next.md) (1.1 / 1.2). Implemented at `1.2.0`.
