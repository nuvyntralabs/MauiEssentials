# Nuvyn — design plan

**Status:** Implemented at `0.2.0` (hub folder `Nuvyn/`; CI in `Nuvyn/.github/workflows/ci.yml`; nuget.org publish still pipeline-only via `NUGET_KEY_NUVYN`)  
**Product:** Nuvyn — Spec-driven CLI for building .NET MAUI apps (Android, iOS, Windows, Mac Catalyst) on the Nuvyntra stack. Domain-agnostic: the user's requirements define the product.  
**Package:** `NuvyntraLabs.Nuvyn.Cli` (`PackAsTool`, command `nuvyn`)  
**Hub folder (proposed):** `Nuvyn/`  
**GitHub (proposed):** `nuvyntralabs/Nuvyn`  
**Closest shipped references:** [MauiDev](maudev.md) (`maui-dev`) for `dotnet tool` packaging; [Plugin.Maui.MVVMExpress.Templates](https://www.nuget.org/packages/Plugin.Maui.MVVMExpress.Templates) for the host scaffold. [GitHub Spec Kit](https://github.com/github/spec-kit) is a usual any-stack alternative, not a parent product.

This is a **developer product**, not a runtime `Plugin.Maui.*` library and not a MauiEssentials catalog skill pack. Users install the tool, `init` an app, then drive a coding agent through Nuvyntra-locked phases. Walkthrough: [Nuvyn/USER-GUIDE.md](../../Nuvyn/USER-GUIDE.md).

Nuvyn is its own product — not a Spec Kit clone or preset. Usual alternative for any stack: GitHub Spec Kit (`specify init`) plus a hand-picked MAUI stack.

## What it is (and is not)

| | Spec Kit | Nuvyn |
| --- | --- | --- |
| User installs | `specify-cli` (PyPI / uv) | `NuvyntraLabs.Nuvyn.Cli` (`dotnet tool`) |
| First command | `specify init Taskify --integration cursor-agent` | `nuvyn init ClinicApp --agent cursor` |
| `init` creates | `.specify/` + agent command files | A **runnable MAUI host** + `.nuvyn/` + agent files |
| Plan phase | Any stack the user types | MVVMExpress + UIKit + smallest Plugin.Maui.* |
| Doctor | — | Can call `maui-dev` after scaffold |

Not MauiDev. `maui-dev` diagnoses an existing MAUI tree. Nuvyn **creates** the tree and the spec workflow. They compose: `nuvyn init` then `maui-dev doctor`.

Not a Spec Kit preset or clone. A preset would still require Python/`specify` and would not copy the embedded MVVMExpress + UIKit host.

Command bodies and `.nuvyn/` templates live in `Nuvyn/payload/`. `nuvyn init` copies them into the **user's app**, not into this catalog hub.

## User journey

```bash
dotnet tool install -g NuvyntraLabs.Nuvyn.Cli --source https://api.nuget.org/v3/index.json
nuvyn init ClinicApp --agent cursor
cd ClinicApp
# optional: open in Cursor / VS / VS Code
```

`init` must leave a host that `dotnet build` can compile (workloads permitting):

```
ClinicApp/
├── ClinicApp.sln
├── ClinicApp/                    # MAUI host, Lumina NV* pages
│   ├── MauiProgram.cs            # UseMvvmExpress + UseNuvyntraUIKit
│   └── Pages/MainPage            # Nuvyntra logo + counter
├── ClinicApp.Core/
├── .nuvyn/
│   ├── constitution.md           # pre-filled Nuvyntra principles
│   ├── feature.json              # created on first /nuvyn-specify
│   ├── templates/                # spec, stack, screens, tasks
│   └── reference/                # constraints, stack-map, recipes
├── .cursor/skills/nuvyn-*/       # when --agent cursor
├── specs/                        # empty until specify
└── README.md                     # how to run the slash chain
```

Then in the coding agent:

```
/nuvyn.constitution
/nuvyn.specify        <the user's product — any domain>
/nuvyn.clarify
/nuvyn.plan
/nuvyn.analysis
/nuvyn.task
/nuvyn.implement
```

## CLI (1.0)

| Command | Purpose |
| --- | --- |
| `nuvyn init <name>` | New directory only: MAUI host + `.nuvyn/` + agent files. Refuses if the folder already exists. |
| `nuvyn version` | Tool version |
| `nuvyn update` | Refresh `.nuvyn/templates`, `reference`, and agent skills; do not overwrite host code or `specs/` |
| `nuvyn agent add <id>` | Write a second integration (1.1) |

Flags:

| Flag | Default | Notes |
| --- | --- | --- |
| `--agent` | prompted | Spec Kit coding-agent keys (`cursor`, `copilot`, `claude`, `gemini`, `codex`, `cursor-agent`, …). Searchable picker when omitted. |
| `--skip-workload-check` | off | Do not fail if MAUI workloads are missing |

Out of 0.2: `--vertical market|clinic|field|bank|civic` (LuminaPlayground seed), GitHub issue export, `nuvyn update`.

## Locked stack (written into constitution + host csproj)

- Default host from `nuvyn init`: MVVMExpress, UIKit, HttpForge, FormValidation, KeyboardManager. Extra packages only when the user asks.
- TFMs: `net10.0-android`, `net10.0-ios`
- Extra plugins added later by `/nuvyn.plan` + `/nuvyn.implement`. **Catalog first** (MauiEssentials docs / README / `src/` / NuGet); outside libraries only when the catalog has no fit
- Do not dump the full catalog into the csproj
- Fail-closed DeepLinks / PushRouter / SmartUpload / FeatureFlags when those packages are added
- Never `dotnet nuget push` from the generated app

## Agent payload

Nuvyn phases, with Nuvyntra-locked **plan** (packages + Lumina screens):

`constitution` → `specify` → `clarify` → `plan` → `analysis` → `task` → `implement`

0.2 writes files for the Spec Kit coding-agent set (Cursor, Copilot, Claude Code, Gemini CLI, Codex, Windsurf, and the rest). Destinations follow each agent's usual project folder.

## Repo layout (proposed)

```
Nuvyn/
├── src/NuvyntraLabs.Nuvyn.Cli/     # PackAsTool, command nuvyn
├── payload/
│   ├── nuvyn/                      # templates + reference + constitution
│   └── agents/cursor/skills/       # SKILL.md files
├── tests/
├── README.md
├── llms.txt
└── AGENTS.md
```

`init` copies `payload/` into the target. Do not generate skill markdown at runtime.

Hub module: `Nuvyn/` is a **standalone** product (same model as MauiDev / UIKit). No `ProjectReference` to sibling submodules. `init` uses nuget.org package IDs only. When extracted, GitHub is `nuvyntralabs/Nuvyn` and the hub holds only a submodule pointer. Publishing is pipeline-only (`NUGET_KEY` or a dedicated key — decide at first CI).

## Implementation order

1. New `nuvyntralabs/Nuvyn` repo + `PackAsTool` CLI with `version` and `init <name>`
2. Keep payloads in `Nuvyn/payload/` only
3. `init` copies `payload/host` (MVVMExpress + Lumina `NV*` pages), adds UIKit, writes constitution and README
4. Tests: init into a temp dir; assert csproj, `MauiProgram`, `.nuvyn/constitution.md`, skill files exist
5. Hub submodule + catalog row (related product, not `Plugin.Maui.*`)
6. Later: `nuvyn update`, optional `--vertical`

## Coding agents

Shipped (`--agent`): Spec Kit keys plus `cursor` (alias `cursor-agent`), `iflow`, `roo`, and `windsurf`. Generic writes `.agents/commands/`.

## Decisions still open

- Exact NuGet id if `NuvyntraLabs.Nuvyn.Cli` is taken
- Whether `init` requires the MVVMExpress template package to be installed globally, or embeds a minimal host
- nuget.org key (reuse UIKit vs new)
