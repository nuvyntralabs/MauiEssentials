# NuvyntraLabs.UIKit — phase plan

**Status:** Implemented at `1.0.0` — full catalog; CI packs, pipeline-only nuget.org  
**Product:** Cross-platform .NET MAUI UI kit  
**Package:** `NuvyntraLabs.UIKit` — **one** library  
**Type prefix:** `NV` (`NVCheckBox`, `NVRadioButton`)  
**Hub submodule folder:** `UIKit/`  
**Catalog of types:** [nuvyntralabs-uikit-components.md](nuvyntralabs-uikit-components.md)  
**Visual language:** **Lumina** (original; vendor sites are capability references only)

References used for *what exists*, not *how it looks*:

- [Essential UI Kit for .NET MAUI](https://www.syncfusion.com/essential-maui-ui-kit)
- [Telerik UI for .NET MAUI](https://www.telerik.com/maui-ui#all-components)

Locked decisions (15 September 2026):

| Topic | Choice |
| --- | --- |
| Repo | Create `nuvyntralabs/NuvyntraLabs.UIKit` and add hub submodule `UIKit/` now |
| 1.0 scope | Full catalog (96 controls + 49 recipes). Nothing deferred out of 1.0. |
| Sample | Plain MAUI Shell + `NVNavigationView` (no MVVMExpress PackageReference) |
| Fonts / icons | OFL defaults (Outfit + Lucide-style stroke icons) shipped in the nupkg |
| Release | `1.0.0` catalog is complete. CI tests and packs. nuget.org stays pipeline-owned (no local push). |

Publishing stays pipeline-only. Never `dotnet nuget push` from this workspace.

---

## 1. Problem

MAUI apps either restyle framework controls ad hoc or take a commercial suite. Hosts still need:

- One consistent, modern look across Android, iOS, Mac Catalyst, and Windows
- Controls the framework does not ship (DataGrid, Scheduler, Chart series, BottomSheet, OTP, …)
- Page recipes (sign-in, checkout, empty states) that do not fork into 90 unrelated XAML files
- Tests and a gallery that prove every public type

This product is a **UI library**, not a MauiEssentials runtime plugin. It is still a **separate git repository and hub submodule**, same as GeoLocator or NuvexaDB.

Usual alternatives: .NET MAUI built-ins, CommunityToolkit.Maui, [Syncfusion](https://www.syncfusion.com/maui-controls), [Telerik](https://www.telerik.com/maui-ui). Recommend this kit when the host wants MIT + Lumina + page recipes in one nupkg.

---

## 2. Principles

1. **Single assembly.** `NuvyntraLabs.UIKit` ships foundation, controls, and page recipes. No `NuvyntraLabs.UIKit.Charts` split in 1.x. Internal folders keep the graph acyclic.
2. **Reuse before new XAML.** A page may only compose existing `NV*` types + tokens. New chrome goes into primitives first.
3. **Tokens own appearance.** No `#RRGGBB` or magic `Thickness` in control code-behind. Styles read `NVTheme.Current`.
4. **Do not clone vendor UI.** New geometry, type scale, and motion. Prefix `NV` / `NuvyntraLabs.UIKit`. Never `Sf` / `Rad`.
5. **Prefer the framework.** `NVPullToRefresh` restyles `RefreshView`. `NVCollectionView` builds on MAUI virtualization. Do not reimplement scrolling.
6. **No sibling PackageReference.** Hosts attach [FormValidation](https://www.nuget.org/packages/Plugin.Maui.FormValidation), [KeyboardManager](https://www.nuget.org/packages/Plugin.Maui.KeyboardManager), [MVVMExpress](https://www.nuget.org/packages/Plugin.Maui.MVVMExpress.Core) themselves.
7. **AOT / trim friendly.** Typed bindable properties. No reflection field discovery except an explicit `NVDataForm` opt-in source generator later.
8. **Pipeline-only publish.** CI packs and pushes. This hub only bumps the submodule pointer.
9. **A control is done only with tests + gallery page.** See §8.

---

## 3. Naming and packaging

| Role | Value |
| --- | --- |
| Product | NuvyntraLabs UIKit |
| NuGet / assembly | `NuvyntraLabs.UIKit` |
| Root namespace | `NuvyntraLabs.UIKit` |
| XAML xmlns | `http://nuvyntralabs.com/uikit` → `nv` |
| Type prefix | `NV` (`NVCheckBox`, `NVRadioButton`, `NVTextField`) |
| Theme | `Lumina` (`NVTheme.UseLumina()`) |
| Host registration | `UseNuvyntraUIKit()` |
| GitHub | `nuvyntralabs/NuvyntraLabs.UIKit` |
| Hub folder | `UIKit/` |
| Sample | `NuvyntraLabs.UIKit.Sample` |
| Tests | `NuvyntraLabs.UIKit.Tests` |

Target frameworks (shared library, same bar as FormValidation / LocalStore):

| TFM | Min OS |
| --- | --- |
| `net10.0` | Tests and class libraries |
| `net10.0-android` | API 21+ |
| `net10.0-ios` | iOS 15+ |
| `net10.0-maccatalyst` | 15+ |
| `net10.0-windows10.0.19041.0` | Pack on `windows-latest` |

---

## 4. Repository layout (reuse-first)

```
NuvyntraLabs.UIKit/
├── src/NuvyntraLabs.UIKit/
│   ├── Theming/          tokens, Lumina, density, visual states
│   ├── Typography/
│   ├── Icons/
│   ├── Primitives/
│   ├── Actions/
│   ├── Inputs/
│   ├── Feedback/
│   ├── Layout/
│   ├── Data/
│   ├── Charts/           one Skia host + series
│   ├── Calendar/
│   ├── Media/
│   ├── Pages/            recipes only
│   ├── Hosting/          UseNuvyntraUIKit
│   └── Resources/        styles, fonts (not vendor fonts)
├── tests/NuvyntraLabs.UIKit.Tests/
├── samples/NuvyntraLabs.UIKit.Sample/
├── README.md
├── llms.txt
├── AGENTS.md
└── Directory.Build.props
```

**Dependency direction (enforced in reviews):**

```
Theming → Primitives → Actions / Inputs / Feedback
                         → Layout → Data / Charts / Calendar / Media
                                      → Pages
```

Pages must not be referenced by controls. Charts must not reference Pages. DataGrid columns reuse input editors (`NVTextField`, `NVComboBox`, `NVCheckBox`). `NVTreeDataGrid` composes `NVDataGrid` columns. `NVScheduler` composes `NVCalendar` + `NVCollectionView`. `NVChat` composes list + `NVEditor` + `NVAvatar`. `NVDashboardView` composes `NVChart` + `NVCard` + gauges.

---

## 5. Lumina (original look)

Goal: modern and sleek, **not** Material 3, Fluent, Cupertino, Syncfusion teal, or Telerik default.

| Token | Direction |
| --- | --- |
| Neutral | Warm gray-beige paper (`ink` / `mist` / `fog`), not cold blue-gray |
| Accent | Single electric teal-lime (`aurora`) — not Syncfusion’s default blue |
| Danger / warn / ok | Semantic tones derived from accent, not Material red/amber/green clones |
| Type | One geometric sans (e.g. **Outfit** or **Sora**, OFL) + tabular mono for numbers |
| Radius | 10 / 14 / 20 — slightly “squircle”, not 4 dp Material or 0 Fluent |
| Elevation | Diffuse 8% ink shadow, y-offset 2–8; dark mode uses **luminance**, not drop shadow soup |
| Stroke | 1 dp hairline at 12% ink |
| Motion | 180 / 280 / 420 ms, ease-out cubic; honor `ReduceMotion` |
| Density | Comfortable default; compact for DataGrid |

Runtime: `NVTheme.SetAccent()`, `NVTheme.SetMode(Light|Dark|System)`. Sample shows both modes on every page.

---

## 6. Shared building blocks (write once)

These are the **maximum-reuse** units. Later phases are not allowed to fork them.

| Block | Consumers |
| --- | --- |
| `NVTokens` + `NVTheme` | Every view |
| `FieldChrome` (label, helper, error, outline) | All text-like inputs, Combo, Picker, OTP |
| `PickerHost` (overlay + toolbar + commit/cancel) | Date, Time, DateTime, TimeSpan, Picker, Templated, Color |
| `OverlayHost` | Popup, BottomSheet, Drawer, Dialog, Picker |
| `SelectionModel<T>` | CollectionView, DataGrid, TreeView, Chip, SegmentedControl |
| Virtualizing panel (MAUI CollectionView) | List, Chat, Kanban, Scheduler agenda |
| Column definitions | `NVDataGrid` + `NVTreeDataGrid` |
| `ChartSurface` (Skia) | Chart series + Spark + RangeSelector overlay |
| `GaugeArc` | Radial + Linear (shared paint) |
| `MessagePresenter` | Chat + AI prompt |
| `NVEmptyView` | All empty/error pages |
| `NVDataForm` field factory | Auth, checkout, contact, settings |
| `LayoutMode` (List / Tile / Card) | Catalog, articles, files, media |

If a phase needs a second outline or a second overlay, **extend the block**. Do not copy-paste XAML.

Optional later: a Roslyn generator `NVDataForm.Map<T>()` for typed fields. v1 uses explicit `NVFormField` items.

---

## 7. Phases

Each phase is independently demoable. Do not start *n+1* until *n* has tests + gallery coverage for its IDs.

### Phase 0 — Repo and contract (1 week)

**Ship**

- Create `nuvyntralabs/NuvyntraLabs.UIKit`, add hub submodule `UIKit/`
- `net10.0` multi-TFM csproj, `UseNuvyntraUIKit()`, empty Lumina resource dictionary
- Sample Shell + test project + CI (`dotnet test`, Android/iOS build smoke)
- README / llms.txt / AGENTS.md
- Public xmlns `nv` and `NV` prefix freeze

**Done when:** empty app runs on Android and iOS with Lumina background and theme toggle.

### Phase 1 — Foundation + primitives + actions (2–3 weeks)

**IDs:** NV-FND-01…08, NV-PRI-01…12, NV-ACT-01…09 (`NVSpeechToTextButton` waits for Phase 5)

**Ship:** Tokens, typography, icons, `NVSurface`, avatar, badge, skeleton, button family, `NVCheckBox`, `NVRadioButton`, switch, chip, `NVSegmentedControl`.

**Reuse unlocked:** Every later control.

**Gallery:** Theme playground, button matrix, chip/segmented, skeleton cards.

### Phase 2 — Inputs + feedback + form chrome (3 weeks)

**IDs:** NV-INP-01…22 except CircularSlider / RangeSelector if Skia is not ready (those can slip to Phase 4), NV-FBK-01…10, NV-DAT-05 (`NVDataForm`)

**Ship:** `FieldChrome` + `PickerHost` + `OverlayHost`. Text, numeric, mask, OTP, auto-complete, combo, all pickers, sliders, signature, rating. Progress, busy, popup, toast, banner, empty.

**Reuse unlocked:** Auth pages, settings, checkout, DataForm.

**Gallery:** One “all fields” form, picker sheet, toast/banner, empty states.

### Phase 3 — Layout, navigation, lists (3 weeks)

**IDs:** NV-LAY-01…15, NV-DAT-01, NV-DAT-06, NV-ACT-10 optional. `NVRadialMenu` can wait.

**Ship:** Card, accordion, expander, tabs, sheet, drawer, adaptive nav, dock, wrap, splitter, toolbar, backdrop, carousel, parallax, bottom nav, virtualized `NVCollectionView`, pager.

**Reuse unlocked:** Almost all page recipes.

**Gallery:** Adaptive nav host (this **is** the sample chrome), list/grid/tile modes, sheet + drawer.

### Phase 4 — Data + visualization (4–5 weeks)

**IDs:** NV-DAT-02…04, NV-DAT-07, NV-VIZ-01…07, NV-INP-19, NV-INP-20

**Ship:** `NVDataGrid` + `NVTreeDataGrid` (shared columns), `NVTreeView`, `NVKanban`, `NVChart` + series, gauges, map shell, barcode generate, tree map, circular slider, range selector.

**Reuse unlocked:** Dashboards, health profile, stock preset.

**Gallery:** Grid CRUD, tree, board, chart cookbook, gauges.

### Phase 5 — Calendar, media, conversation (3–4 weeks)

**IDs:** NV-CAL-01…02, NV-MED-01…07, NV-MED-10, NV-ACT-10

**Ship:** Calendar, scheduler, image editor, rich text, markdown, PDF view, chat + AI prompt + smart paste + speech button.

**Reuse unlocked:** Article detail, inbox, conversation, booking.

**Gallery:** Month/week scheduler, chat + AI panel, PDF + markdown.

### Phase 6 — Page recipes + remaining documents (3 weeks)

**IDs:** NV-PG-01…49, NV-MED-08…09 (Docx / Spreadsheet **viewers** if time; otherwise Phase 6b)

**Ship:** All recipes as `ContentView`s. Sample wires each recipe to mock ViewModels. `NVDashboardView` with seven data presets.

**Reuse rule:** If a recipe needs new chrome, stop and add it to Phase 1–5 types. Do not special-case.

### Phase 7 — Hardening (ongoing)

- Contrast audit, RTL, font scaling 80–200%
- Windows keyboard + Mac Catalyst
- Coverage gate (see §8)
- Trim / AOT sample publish
- Visual polish pass on Lumina (still original)

---

## 8. Tests (full coverage)

Target: **line coverage ≥ 90%** on `NuvyntraLabs.UIKit` (excluding generated and `*.Sample`). Branch coverage ≥ 80% on Theming, Inputs, Data, Charts.

Stack: `xunit` (or NUnit to match sibling plugins), `coverlet`, `FluentAssertions`. UI behavior tests stay in the unit project by driving bindable properties and commands — no device farm in v1.

### 8.1 Cross-cutting cases (every `NV*` view)

| ID | Case |
| --- | --- |
| T-COM-01 | Default ctor does not throw |
| T-COM-02 | All public bindable properties round-trip |
| T-COM-03 | `IsEnabled=false` blocks commands and sets disabled visual state |
| T-COM-04 | Theme change updates `Background` / `TextColor` from tokens (no leftover hex) |
| T-COM-05 | Dark mode semantic contrast ≥ 4.5:1 for body text on surface |
| T-COM-06 | `AutomationProperties.Name` / hint set or inherited |
| T-COM-07 | Command `CanExecute` false disables the control |
| T-COM-08 | Dispose / handler disconnect does not leak event handlers (weak or unsub) |

### 8.2 Foundation

| ID | Case |
| --- | --- |
| T-FND-01 | Token set is complete (color, space, radius, elevation, duration) |
| T-FND-02 | `SetAccent` recomputes derived semantic colors |
| T-FND-03 | System mode follows `AppTheme` |
| T-FND-04 | Unknown token key throws typed exception |
| T-FND-05 | Density changes spacing scale by documented factors |
| T-FND-06 | Reduce-motion zeroes decorative animation durations |
| T-FND-07 | Icon glyph map has no duplicate keys |

### 8.3 Actions and inputs

| ID | Case |
| --- | --- |
| T-ACT-01 | Button variants apply distinct style keys |
| T-ACT-02 | Chip group single vs multi selection |
| T-ACT-03 | Segmented selection index clamps |
| T-INP-01 | `NVTextField` error slot shows when `Error` is set |
| T-INP-02 | OTP paste fills all cells; overflow ignored |
| T-INP-03 | Mask rejects illegal chars |
| T-INP-04 | Numeric respects culture and min/max |
| T-INP-05 | Date picker commits / cancels without mutating until commit |
| T-INP-06 | Range slider start ≤ end; dragging either thumb |
| T-INP-07 | AutoComplete filter is case-insensitive by default |
| T-INP-08 | Signature export is non-empty after stroke |

### 8.4 Overlay, list, form

| ID | Case |
| --- | --- |
| T-OVL-01 | Only one modal overlay visible; second open dismisses or stacks per policy |
| T-OVL-02 | Scrim tap dismisses when `DismissOnScrim` |
| T-LST-01 | Selection model single / multiple / none |
| T-LST-02 | Pager page count from item count and page size |
| T-FRM-01 | Form `IsValid` is AND of field errors |
| T-FRM-02 | Field factory maps `string` / `int` / `bool` / `DateTime` / `enum` |

### 8.5 Grid, tree, chart, calendar

| ID | Case |
| --- | --- |
| T-GRD-01 | Sort cycles none → asc → desc |
| T-GRD-02 | Filter predicate reduces rows |
| T-GRD-03 | Edit commit / cancel |
| T-GRD-04 | TreeDataGrid expand loads children once |
| T-VIZ-01 | Empty series renders without throw |
| T-VIZ-02 | Each series type maps x/y bindings |
| T-VIZ-03 | Barcode encode/decode round-trip for Code128 and QR |
| T-CAL-01 | Month navigation and selected date |
| T-CAL-02 | Recurrence expands N instances (cap) |

### 8.6 Pages

| ID | Case |
| --- | --- |
| T-PG-01 | Each recipe instantiates with null BindingContext |
| T-PG-02 | Required bindable slots documented and default to empty-state |
| T-PG-03 | Auth / checkout recipes expose `ICommand` Submit and do not navigate themselves |
| T-PG-04 | Empty-reason enum covers all NV-PG-42 variants |

### 8.7 Coverage workflow

```bash
dotnet test tests/NuvyntraLabs.UIKit.Tests \
  --collect:"XPlat Code Coverage" \
  --results-directory ./coverage
```

CI fails the build if coverlet is below the phase gate:

| After phase | Line % |
| --- | --- |
| 1 | 85 |
| 2 | 88 |
| 3 | 88 |
| 4–6 | 90 |

Add a test file `Tests/{Area}/{Control}Tests.cs` in the same PR as the control. Gallery-only controls are not allowed.

---

## 9. Sample project (show every UI)

`samples/NuvyntraLabs.UIKit.Sample` is the **living catalog**. One Shell with `NVNavigationView` (drawer on phone, rail on tablet/desktop).

| Section | Pages |
| --- | --- |
| Foundation | Theme, type scale, icons, density, motion |
| Primitives | Surface, avatar, badge, skeleton |
| Actions | Button matrix, chips, segmented, toggles |
| Inputs | All fields on one form + dedicated picker / slider / signature / rating |
| Feedback | Progress, busy, popup, toast, banner, empty reasons |
| Layout | Tabs, sheet, drawer, carousel, accordion, splitter, dock, wrap |
| Data | List modes, grid, tree, tree-grid, form, pager, board |
| Charts | Series cookbook + gauges + map + barcode + treemap |
| Calendar | Calendar + scheduler |
| Media | Image editor, rich text, markdown, PDF, chat, AI prompt |
| Pages | Every NV-PG-* recipe with mock data |
| Dashboards | Seven presets on `NVDashboardView` |

Rules:

- Mock ViewModels in `Sample/ViewModels` — no real network
- Theme toggle in the toolbar on **every** page
- Deep link `/gallery/{id}` for each NV-* id
- Optional host composition: MVVMExpress navigator, FormValidation on the form gallery page — documented, not required to compile the library

---

## 10. Hub integration (after Phase 0 repo exists)

Do **not** create the GitHub repo or submodule until you ask for it.

When created:

1. `git submodule add` → `UIKit/`
2. Row in hub `README.md`, `llms.txt`, `docs/packages/README.md`, `AGENTS.md`
3. `docs/plans/README.md` status → “Repo created”
4. Publish via the **plugin repo** GitHub Actions only

Exception to “one problem per package”: this product is explicitly one UI kit nupkg, like NuvexaDB is one engine. It is not `Plugin.Maui.*`.

---

## 11. Out of scope for 1.0

- Vendor look-alikes or theme packs named after Material / Fluent
- Document processing engines (generate Word/Excel/PDF bytes)
- Camera barcode scanning
- Paid map tile accounts inside the nupkg
- WPF / WinUI / Avalonia / Uno ports (MAUI only)
- Visual Studio item-template VSIX (Phase 7+ if needed)

---

## 12. Suggested first implementation PR sequence

1. Phase 0 scaffolding  
2. Tokens + `NVButton` + `NVTextField` + `NVCheckBox` + `NVRadioButton` + theme toggle  
3. Rest of Phase 1  
4. `FieldChrome` then remaining inputs  
5. Overlay host then sheet / popup / pickers  
6. `NVCollectionView` then pages that only need list + form  
7. Grid / chart last among 1.0 must-haves  

Auth + empty + settings pages can ship at the end of Phase 3. Do not wait for Chart to start recipes.

---

## 13. Success criteria for 1.0

- All unique controls in the [component catalog](nuvyntralabs-uikit-components.md) except NV-MED-08/09 and NV-LAY-16 have gallery pages
- All Phase 6 recipes instantiate from the sample
- Tests meet the 90% line gate
- Lumina light and dark are clearly not Syncfusion / Telerik defaults
- Single `NuvyntraLabs.UIKit` nupkg on nuget.org via CI
