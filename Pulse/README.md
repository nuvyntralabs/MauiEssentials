# maui-pulse

[![NuGet](https://img.shields.io/nuget/v/Plugin.Maui.Pulse.Cli.svg?label=NuGet)](https://www.nuget.org/packages/Plugin.Maui.Pulse.Cli)

Live session CLI for **Nuvyntra `Plugin.Maui.*` data only**. It does not scrape logcat, Charles, Firebase, Sentry, or MAUI framework APIs.

```bash
dotnet tool install -g Plugin.Maui.Pulse.Cli --source https://api.nuget.org/v3/index.json
maui-pulse listen --port 7878
```

**GitHub:** https://github.com/nuvyntralabs/MauiPulse  
**NuGet:** https://www.nuget.org/packages/Plugin.Maui.Pulse.Cli  
**Docs:** https://nuvyntralabs.github.io/toolkits/maui-pulse/  
**Catalog:** https://github.com/nuvyntralabs/MauiEssentials  
**Author:** [Niladri Prasad Padhy](https://github.com/NiladriPadhy)  
**License:** MIT  
**Version:** 1.0.0

It does **not** replace [MauiDev](https://github.com/nuvyntralabs/MauiDev) (`maui-dev doctor`) or [maui-perf](https://www.nuget.org/packages/Plugin.Maui.Performance.Cli). Those are before-the-run and profile-take tools. Pulse is the during-the-session viewer.

Publishing is pipeline-only — never `dotnet nuget push` from a local clone.

## Install

```bash
dotnet tool install -g Plugin.Maui.Pulse.Cli --source https://api.nuget.org/v3/index.json
maui-pulse version
```

Requires the .NET 10 SDK. Do not `dotnet add package Plugin.Maui.Pulse.Cli` into an app.

On an interactive terminal `maui-pulse` asks every 4 hours whether to update from nuget.org (`[y/N]`, default no). Skip with `--no-update-check` or `NUVYNTRA_NO_UPDATE_CHECK=1`. Cache: `~/.nuvyntra/cli-updates.json`. The CLI does not phone home.

## Allow-list

| Lane | Source | Signal |
| --- | --- | --- |
| NETWORK | [Plugin.Maui.NetworkMonitor](https://www.nuget.org/packages/Plugin.Maui.NetworkMonitor) | `StatusChanged` / current status |
| API | [Plugin.Maui.NetworkDiagnostics](https://www.nuget.org/packages/Plugin.Maui.NetworkDiagnostics) | On-demand `RunAsync()` report |
| QUEUE | [Plugin.Maui.JobQueue](https://www.nuget.org/packages/Plugin.Maui.JobQueue) + [Plugin.Maui.RetryQueue](https://www.nuget.org/packages/Plugin.Maui.RetryQueue) | Events + `*.db3` |
| SYNC | [Plugin.Maui.OfflineSync](https://www.nuget.org/packages/Plugin.Maui.OfflineSync) | Conflicts, pending, `offlinesync.db3` |
| PERMS | [Plugin.Maui.PermissionFlow](https://www.nuget.org/packages/Plugin.Maui.PermissionFlow) | `FlowCompleted` / `PermissionChanged` |
| HEALTH | [Plugin.Maui.AppHealth](https://www.nuget.org/packages/Plugin.Maui.AppHealth) | `HealthChanged` |
| LEAK | [Plugin.Maui.LeakAnalyser](https://www.nuget.org/packages/Plugin.Maui.LeakAnalyser) | `OnLeaked` (Debug) |
| CRASH | [Plugin.Maui.Diagnostics](https://www.nuget.org/packages/Plugin.Maui.Diagnostics) | Timeline / ANR / crash files |
| SESSION | [Plugin.Maui.DeviceSession](https://www.nuget.org/packages/Plugin.Maui.DeviceSession) | Install / session id |

A lane that is not installed prints `— not installed` and is skipped. Pulse does not invent a substitute.

[Plugin.Maui.Observability](https://www.nuget.org/packages/Plugin.Maui.Observability) may carry bytes (`HttpEndpoint` → `maui-pulse listen`). Pulse still only **renders** allow-listed sources. Observability domains such as SmartUpload are dropped.

## Commands

| Command | Purpose |
| --- | --- |
| `listen` | HTTP sink on `--port` (default 7878) or `--stdin` JSON |
| `attach` | Same sink plus a nine-lane table; `--from` seeds file lanes |
| `pull` | Copy known plugin files from `--from` |
| `queues` | Inspect `plugin.maui.jobqueue.db3` and `plugin.maui.retryqueue.db3` |
| `sync` | Inspect `offlinesync.db3` |
| `incident` | Zip allow-listed files + `manifest.json` |
| `version` | Print `1.0.0` |

```bash
maui-pulse listen --stdin --once --format json
maui-pulse attach --from ./pulled --once --format json
maui-pulse pull --from ./device-files --out ./pulled
maui-pulse queues --from ./pulled
maui-pulse sync --db ./pulled/offlinesync.db3
maui-pulse incident --from ./pulled --out incident.zip
```

`--format human|json`. JSON skips the nuget.org update prompt.

Exit codes: `0` success (including skipped lanes), `1` no allow-listed evidence / no files to copy, `2` usage.

## Listen JSON

POST `http://127.0.0.1:7878/` with:

```json
{
  "source": "Plugin.Maui.NetworkMonitor",
  "lane": "network",
  "signal": "StatusChanged",
  "summary": "captive portal"
}
```

Or an Observability batch. Only mapped domains (`Network`, `Health`, `Sync` / `OfflineSync`, `Session` / `Identity`) are accepted.

Presence (Debug hook / host):

```json
{
  "plugins": [
    { "id": "Plugin.Maui.NetworkMonitor", "lane": "network", "state": "running" },
    { "id": "Plugin.Maui.OfflineSync", "lane": "sync", "state": "not_installed" }
  ]
}
```

Unknown `source` / `id` values are dropped.

## Files Pulse may read

- `plugin.maui.jobqueue.db3`
- `plugin.maui.retryqueue.db3`
- `offlinesync.db3`
- `maui-diagnostics/`

Copy those off a debug device, then `--from`. `pull --adb` only prints how to copy; it does not scrape logcat.

## What it is not

- Not Nuvyn (new-app scaffold)
- Not maui-dev (static project doctor)
- Not maui-perf (EventPipe profile)
- Not Observability (in-app exporter). Observability can push; Pulse listens.
