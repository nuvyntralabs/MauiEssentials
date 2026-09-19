# maui-pulse

A [dotnet tool](https://learn.microsoft.com/dotnet/core/tools/global-tools) that listens **only** to Nuvyntra `Plugin.Maui.*` session data.

```bash
dotnet tool install -g Plugin.Maui.Pulse.Cli --source https://api.nuget.org/v3/index.json
maui-pulse listen --port 7878
maui-pulse attach --from ./pulled --format json
maui-pulse queues --from ./pulled
maui-pulse sync --from ./pulled
maui-pulse incident --from ./pulled --out incident.zip
```

Unknown sources (logcat, Firebase, Sentry, MAUI `Connectivity`) are dropped. A missing plugin skips that lane.

Docs: https://nuvyntralabs.github.io/toolkits/maui-pulse/
