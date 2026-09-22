# NuvLoc — design plan

**Status:** Implemented at `1.1.2` (hub submodule `NuvLoc/`; GitHub `nuvyntralabs/NuvLoc`).  
**Product:** NuvLoc — agent-driven localization CLI (sibling `.resx`: MAUI, WPF, WinUI, Avalonia, Uno)  
**Package:** `NuvyntraLabs.NuvLoc.Cli` (`PackAsTool`, command `nuvloc`)  
**Catalog slug:** `nuvloc`  
**Hub folder:** `NuvLoc/`  
**GitHub:** `nuvyntralabs/NuvLoc`  
**Closest shipped reference:** [Nuvyn](nuvyn.md) (`nuvyn init --agent` → slash chain). MauiDev is the report / `dotnet tool` cousin, not the AI path.

This is a **developer product**, not a runtime `Plugin.Maui.*` library and not an OpenAI/Azure wrapper. The CLI validates `i18n.json`, diffs resource files, and installs coding-agent skills. **The agent already in the IDE translates.** Same door as Nuvyn: `--agent cursor` writes `/nuvloc.translate` and `/nuvloc.status`; Cursor’s model does the wording. There is no `provider` field and no API key.

**NuvLoc does not guarantee translation quality.** Machine / agent wording can be wrong, tone-deaf, or culturally off. A native speaker of each target language should review the culture files before you ship. Placeholder and coverage checks only prove the files are complete and tokens survived — not that the text is correct.

Usual alternatives: Visual Studio Multilingual App Toolkit, [ResXResourceManager](https://github.com/dotnet/ResXResourceManager), Crowdin / Phrase, or a vendor-key CLI.

---

## 1. Name

**Use `NuvLoc` / `nuvloc`.** The user named the product. Keep it. Do not ship `Plugin.Maui.I18n.Cli` or `maui-i18n`.

| Role | Value |
| --- | --- |
| Product | NuvLoc |
| NuGet | `NuvyntraLabs.NuvLoc.Cli` |
| Command | `nuvloc` (lowercase, same as `nuvyn`) |
| Slash commands | `/nuvloc.translate` and `/nuvloc.status` (both 1.0) |
| Config file | `i18n.json` (default name, project root) |
| GitHub | `nuvyntralabs/NuvLoc` |
| Hub submodule | `NuvLoc/` |

`NuvLoc` is the display name. The executable and slash prefix are `nuvloc`, matching `nuvyn` / `/nuvyn.specify`. Do not register `/NuvLoc.translate` as a second spelling.

This is a Labs CLI (Nuvyn family), not a `Plugin.Maui.*` runtime package. Later platforms stay on the same command.

---

## 2. Problem

A MAUI host has an English `.resx` and a list of cultures. It needs those culture files kept in lockstep when English keys are added or edited — without a second vendor account, and without pasting strings into a chat.

Nuvyn already solved “CLI wires the agent; the agent does the skilled work.” NuvLoc is that pattern for localization.

One problem: **from `i18n.json` (source file + language list), produce and maintain the culture files, using the coding agent as the translator.**

---

## 3. Principles

1. **Nuvyn flow, not a translation SaaS.** `init --agent` installs skills. `/nuvloc.translate` and `/nuvloc.status` run in the agent. The CLI does not call OpenAI, Azure, Anthropic, or any HTTP model API.
2. **No API keys.** `i18n.json` has no `provider`, `model`, or `apiKey`. Do not add them later as a “fallback.”
3. **CLI owns facts; agent owns wording.** The CLI validates config, diffs keys, and checks coverage. The agent writes translations. The agent must not invent keys or freestyle the whole `.resx` without a worklist.
4. **`init` attaches to an existing tree.** It is `nuvyn adopt`, not `nuvyn init`. It does not scaffold a MAUI host.
5. **English is the source of truth.** Never translate into English. Never invent keys that are not in the source file.
6. **Incremental by default.** Translate missing and stale keys only. Do not overwrite a human target value unless the user says so in the slash turn.
7. **Placeholders are a contract.** `{0}`, `{name}`, `{{literal}}`, `%s` / `%d` must survive. `nuvloc check` fails the key if they do not.
8. **Review is required.** Completeness ≠ correctness. Every README, skill, `init` success line, and human `status` / `check` report must say that NuvLoc does not give a 100% guarantee on translated text and that a native-language expert should review before ship. Do not bury this in a footnote.
9. **Resource files only.** NuvLoc writes culture `.resx` files. It does not bind UI. XAML `x:Static`, a markup extension, or code is the host’s choice. No `UseI18n`.
10. **One CLI, adapters later.** v1 adapter = MAUI `.resx`. `platform` in `i18n.json` selects the adapter.
11. **Pipeline-only publish.** `NUGET_KEY_NUVLOC` only. Never `dotnet nuget push` from this workspace.
12. **No CLI telemetry.** 4-hour nuget.org self-update prompt is allowed (`--no-update-check` / `NUVYNTRA_NO_UPDATE_CHECK=1`). Cache: `~/.nuvyntra/cli-updates.json`.

---

## 4. What it is (and is not)

| | Nuvyn | NuvLoc |
| --- | --- | --- |
| Install | `NuvyntraLabs.Nuvyn.Cli` → `nuvyn` | `NuvyntraLabs.NuvLoc.Cli` → `nuvloc` |
| `init` | **New folder** + MAUI host | **Existing project:** check `i18n.json` + write agent files |
| Agent work | `/nuvyn.specify` … `/nuvyn.implement` | `/nuvloc.translate` and `/nuvloc.status` |
| Who translates | — | The coding agent (Cursor, Copilot, …) |
| CI | `nuvyn check` | `nuvloc check` (coverage only; no agent in CI) |

Not MauiDev. Not a runtime plugin. Not Nuvyn — do not fold this into `nuvyn init`. An existing app installs NuvLoc the same way it would run `nuvyn adopt`: attach a workflow, do not rewrite the stack.

---

## 5. User journey

Host already exists. Author writes `i18n.json` at the project root:

```json
{
  "platform": "maui",
  "source": "Resources/Strings/AppResources.resx",
  "languages": ["es", "fr"]
}
```

```bash
dotnet tool install -g NuvyntraLabs.NuvLoc.Cli --source https://api.nuget.org/v3/index.json
cd ClinicApp
nuvloc init --configfile i18n.json --agent cursor
```

Local pack (from `NuvLoc/`) when nuget.org is not the source:

```bash
dotnet pack src/NuvyntraLabs.NuvLoc.Cli/NuvyntraLabs.NuvLoc.Cli.csproj -c Release -o artifacts
dotnet tool install -g NuvyntraLabs.NuvLoc.Cli \
  --add-source ./artifacts \
  --configfile ./nuget.config \
  --ignore-failed-sources \
  --version 1.1.2
```

`--configfile ./nuget.config` plus `--ignore-failed-sources` avoids a 401 from an extra machine-wide feed. Uninstall: `dotnet tool uninstall -g NuvyntraLabs.NuvLoc.Cli`.

`init` **checks** `i18n.json` (see §7), then copies the agent payload. It does not translate.

In Cursor:

```
/nuvloc.status
/nuvloc.translate
```

`/nuvloc.status` runs `nuvloc status` and explains coverage. `/nuvloc.translate` fills gaps (see §9). Both skills end with the native-review disclaimer.

```
ClinicApp/
├── i18n.json
├── Resources/Strings/
│   ├── AppResources.resx
│   ├── AppResources.es.resx
│   └── AppResources.fr.resx
├── .nuvloc/
│   ├── rules.md                 # placeholders, incremental, no invented keys, review required
│   └── reference/               # sibling .resx notes (dotnet-resx.md)
└── .cursor/skills/              # when --agent cursor
    ├── nuvloc-translate/SKILL.md
    └── nuvloc-status/SKILL.md
```

Command bodies live in `NuvLoc/payload/`. `init` copies them into the **user’s app**. Do not generate skill markdown at runtime.

---

## 6. `i18n.json` contract (1.1)

Default file name: `i18n.json`. `--configfile` overrides the path (relative to cwd or absolute).

```json
{
  "platform": "maui",
  "source": "Resources/Strings/AppResources.resx",
  "languages": ["es", "fr"]
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `platform` | **yes** | `maui`, `wpf`, `winui`, `avalonia`, or `uno` (sibling `.resx`). Unknown id → exit 2. WinUI / Uno PRI `.resw` folders are out of scope. |
| `source` | **yes** | Path to the English resource file, relative to the config file. Must exist. |
| `languages` | **yes** | Non-empty [BCP-47](https://www.rfc-editor.org/rfc/rfc5646.html) list. Tested popular codes: `es`, `fr`, `de`, `it`, `nl`, `ja`, `ko`, `zh-Hans`, `pt-BR`, `ar`, `hi`, `ru`. Other BCP-47 codes also work; if one fails, open a NuvLoc issue. Reject `en` / `en-US` / `en-GB` and non-BCP-47 tags (`foo`, `english`, `es_MX`): print the error and reason, skip that culture `.resx`. Canonicalize (`PT-br` → `pt-BR`). Table: [NuvLoc README](../../NuvLoc/README.md#valid-bcp-47-cultures). |

**Not in the file:** `provider`, `model`, `apiKey`, output pattern. Target path is derived: `AppResources.resx` → `AppResources.{lang}.resx` beside the source.

Optional later (still no provider): `context`, `glossary`. The agent can also read tone from `.nuvloc/rules.md`. Keep 1.1 to the three fields above.

---

## 7. `nuvloc init`

```bash
nuvloc init --configfile i18n.json --agent cursor
```

| Flag | Default | Notes |
| --- | --- | --- |
| `--configfile` | `i18n.json` | Path to check. Same meaning if omitted. |
| `--agent` | prompted | Spec Kit keys (`cursor`, `copilot`, `claude`, `gemini`, `codex`, …). Searchable picker when omitted. |
| `--path` | cwd | Search / project root |
| `--force` | off | Overwrite agent skill files. Never overwrite culture `.resx`. |
| `--no-update-check` | off | Skip the 4-hour nuget.org prompt |

`init` **checks** the config file. It does not create a host. Fail (exit 2) if any of these are true:

1. `--configfile` is missing
2. JSON is invalid
3. `platform` / `source` / `languages` missing or wrong type
4. `source` file does not exist (resolved relative to the config file)
5. `source` extension is not a 1.0 adapter (`.resx` for `maui`)
6. `languages` is empty, contains the source culture, or a code that is not a predefined BCP-47 culture

On success:

1. Write `.nuvloc/rules.md` + `reference/` (skip existing rules unless `--force`)
2. Write agent files for `--agent` (Cursor → `.cursor/skills/nuvloc-translate/` and `.cursor/skills/nuvloc-status/`, plus the command mapping Nuvyn uses)
3. Print the next steps: `/nuvloc.status` then `/nuvloc.translate` — and the native-review disclaimer

If `i18n.json` is missing, **do not invent one and continue.** Print a stub example and exit 2. The user owns the config (they already named the file). A later `nuvloc init --write-stub` is optional; not 1.0.

`nuvloc update` refreshes `.nuvloc/reference` and agent skills. It does not overwrite `i18n.json`, `.nuvloc/rules.md`, or any `.resx`.

`nuvloc agent add <id>` writes a second integration (same as Nuvyn 1.1).

---

## 8. CLI vs slash

| Surface | Purpose | Calls a model? |
| --- | --- | --- |
| `nuvloc init` | Check `i18n.json` + install skills | No |
| `nuvloc update` | Refresh skills / reference | No |
| `nuvloc plan` | JSON worklist: missing / stale / extra per language | No |
| `nuvloc status` | Human or JSON coverage table | No |
| `nuvloc check` | CI: exit 1 if missing or stale | No |
| `nuvloc version` | Tool version | No |
| **`/nuvloc.status`** | Agent runs `nuvloc status` and explains the table | No model needed for facts; agent only narrates |
| **`/nuvloc.translate`** | Agent translates the worklist and writes culture files | **Yes — the IDE agent** |

There is **no** `nuvloc translate` CLI command in 1.0. That would pull the design back to a provider key. Both slash commands ship in 1.0.

`--format human|json` on `plan` / `status` / `check`. `--ci` on `check` (no prompts). `--lang` restricts cultures; unknown or invalid codes exit 2. Exit codes: `0` pass, `1` failed check, `2` usage / bad config.

CI runs `nuvloc check`. It does not run an agent. Gaps fail the build; a developer (or a Cursor cloud job) runs `/nuvloc.translate` to fill them.

---

## 9. How `/nuvloc.translate` works

The skill is locked. The agent does not “localize the app” from vibes.

```
/nuvloc.translate
    ↓
Read i18n.json (and .nuvloc/rules.md)
    ↓
nuvloc plan --configfile i18n.json --format json
    ↓
For each language in the plan
    For each missing / stale key
        Translate English value → target language
        Keep key, comment, placeholders
    Write sibling .resx (create if needed)
    ↓
nuvloc check --configfile i18n.json
```

`plan` output (shape):

```json
{
  "source": "Resources/Strings/AppResources.resx",
  "languages": {
    "es": {
      "missing": [{ "key": "ItemsLeft", "value": "You have {0} items", "comment": "" }],
      "stale":   [{ "key": "Save", "value": "Save", "previousSource": "Store" }],
      "extra":   ["OldKey"],
      "current": 40
    }
  }
}
```

**Stale** = English *value* hash changed since the last successful write recorded in `.nuvloc/cache.json` (written by `check` / a post-step, or by the agent after a clean check). A human edit of the Spanish value is not stale and is not in the worklist.

**Extra** = in the culture file, not in English. Report only. Do not delete in 1.0.

The skill must say:

- Translate values only. Do not rename keys.
- Do not add keys that are not in the worklist.
- Preserve `{0}`, `{name}`, and `%s` / `%d` exactly.
- Do not overwrite `current` keys.
- Do not call a third-party translation HTTP API.
- After writes, run `nuvloc check`. If check fails, fix placeholders and stop.
- End the turn with the fixed disclaimer (see §9b). Do not claim the text is ship-ready.

`--dry-run` on `plan` is unnecessary; `plan` never writes. The agent can be asked “report only” in the same slash turn.

---

## 9b. How `/nuvloc.status` works

Facts come from the CLI. The agent does not recount keys from memory.

```
/nuvloc.status
    ↓
nuvloc status --configfile i18n.json --format json
    ↓
Present coverage per language:
    total / current / missing / stale / extra
    ↓
If missing or stale: suggest /nuvloc.translate
If check-clean: say files are complete, not that wording is correct
    ↓
Print the native-review disclaimer
```

The skill must not translate, edit `.resx`, or invent counts. `--lang` in the user turn may be forwarded to `nuvloc status --lang`.

---

## 9c. Required disclaimer (verbatim)

Use this wording in README, `.nuvloc/rules.md`, both skills, `init` success output, and the human footer of `status` / `check`:

> NuvLoc does not give a 100% guarantee on translated text. Agent wording can be inaccurate or culturally off. Review every culture file with a native speaker of that language before you ship. Coverage and placeholder checks only prove completeness, not correctness.

---

## 10. Sibling `.resx` adapter (1.1)

- Read/write `.resx` XML only (`maui`, `wpf`, `winui`, `avalonia`, `uno`).
- Preserve `resheader`, schema, comments, `xml:space`.
- Copy `name` + optional `<comment>` from source. Translate `<value>` only.
- Do not edit the source `.resx`, the `.csproj`, or `NeutralResourcesLanguage`.
- `net10.0` tool. No MAUI workload required to run the CLI. Sample host is not in `NuvLoc.slnx`.

Unsupported: PRI `.resw` under `Strings/{lang}/`, `.xlf`, JSON maps, Android XML, iOS strings.

---

## 11. Repo layout

```
NuvLoc/
├── src/NuvyntraLabs.NuvLoc.Cli/    # PackAsTool, command nuvloc
├── src/NuvLoc.Core/                # IsPackable=false — config, resx, diff, reports
├── payload/
│   ├── commands/{status,translate}.md
│   └── nuvloc/
│       ├── rules.md
│       └── reference/dotnet-resx.md
├── samples/NuvLocSample/           # MAUI host; AppResources.resx; not in slnx
├── tests/
├── nuget.config                    # nuget.org only (local tool install)
├── README.md
├── llms.txt
└── AGENTS.md
```

`NuvLoc.Core` has no MAUI package reference. Agent destinations follow the same Spec Kit set Nuvyn already writes (Cursor skills, Copilot, Claude, Gemini, Codex, Windsurf, generic `.agents/commands/`).

---

## 12. Implementation order

Shipped at 1.1.0:

1. `nuvyntralabs/NuvLoc` + `PackAsTool` CLI with `version` and `init --configfile --agent`
2. `i18n.json` validate + `ResxAdapter` (sibling `.resx` for `maui` / `wpf` / `winui` / `avalonia` / `uno`)
3. `plan` / `status` / `check` on fixtures (no agent)
4. Payload: `rules.md` + `/nuvloc.translate` + `/nuvloc.status`. Both include the disclaimer.
5. Tests + `samples/NuvLocSample` (`AppResources.resx`; not in `NuvLoc.slnx`)
6. Hub submodule + catalog row (Labs developer tool, next to Nuvyn)
7. CI: same fail-fast order as Nuvyn / MauiDev / Pulse — version alignment → `NUGET_KEY_NUVLOC` + unpublished version → tests → pack → nuget.org + GitHub Packages. No live model calls.

---

## 13. Later platforms

1.1 already accepts `maui`, `wpf`, `winui`, `avalonia`, and `uno` for sibling `.resx`. Same CLI. Do not add `Plugin.Wpf.NuvLoc`.

Still later: WinUI / Uno PRI `.resw` under `Strings/{lang}/` (new adapter). Optional `i18n.json` fields: `context`, `glossary` (agent hints only). Still no provider.

Nuvyn may later mention NuvLoc in the generated README. That is a Nuvyn change, not a NuvLoc requirement.

---

## 14. Decisions

Settled:

- Both `/nuvloc.translate` and `/nuvloc.status` ship in 1.0; 1.1 adds sibling `.resx` platforms.
- Translation quality is not guaranteed; native review is required (verbatim disclaimer).
- Resource files only — NuvLoc does not bind UI.
- GitHub `nuvyntralabs/NuvLoc` + MauiEssentials submodule `NuvLoc/`.
- `--agent` uses the same Spec Kit set as Nuvyn.
- `.nuvloc/cache.json` is written only by `nuvloc check --write-cache` (after `/nuvloc.translate`). CI `check` does not write the cache.
- Cursor destination: `.cursor/skills/nuvloc-translate/SKILL.md` and `.cursor/skills/nuvloc-status/SKILL.md` (Nuvyn Skill format).
- Local install: `--configfile ./nuget.config --ignore-failed-sources` so a 401 extra feed does not abort.
- CI uses `NUGET_KEY_NUVLOC` only.
