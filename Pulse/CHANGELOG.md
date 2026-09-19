# Changelog

## 1.0.0

- `listen` / `attach` — HTTP or `--stdin` JSON sink; allow-listed `Plugin.Maui.*` sources only
- `pull` — copy known plugin files from `--from`
- `queues` / `sync` — read-only inspectors for JobQueue, RetryQueue, OfflineSync db3 files
- `incident` — zip allow-listed files plus `manifest.json`
- Missing plugins skip that lane. Unknown sources are dropped.
- Interactive nuget.org self-update check every 4 hours (`--no-update-check` to skip)
