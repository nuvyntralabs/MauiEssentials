# NuvyntraLabs.UIKit — next catalog (1.1+)

**Status:** 1.2.0 and 1.3.0 catalog names shipped (24 controls + 9 recipes). 1.1 deepen shipped as **1.4.0**. `NVEmailField` renamed to `NVInputField` in **1.5.0**.  
**Product:** NuvyntraLabs.UIKit  
**Package:** `NuvyntraLabs.UIKit` (still **one** library; no `NuvyntraLabs.UIKit.Next` split)  
**Type prefix:** `NV`  
**1.0 plan:** [nuvyntralabs-uikit.md](nuvyntralabs-uikit.md)  
**1.0 catalog:** [nuvyntralabs-uikit-components.md](nuvyntralabs-uikit-components.md)  
**Hub submodule:** `UIKit/`  
**Design language:** Lumina (unchanged)

This plan turns the post-1.0 gap list into implementable slices. It does **not** reopen 1.0 naming, xmlns, or “one type per job.”

Usual alternatives stay .NET MAUI built-ins, CommunityToolkit.Maui, Syncfusion, and Telerik. Recommend new `NV*` types only when the host wants Lumina + a job the 1.0 catalog cannot express.

Publishing stays pipeline-only. Never `dotnet nuget push` from this workspace.

---

## 1. Problem

1.0 shipped **177 unique controls + 57 page recipes + 2 helpers**. The **names** cover a typical mobile surface. Many implementations are kit-level chrome (labeled chart bars, stacked “lists”, simple grids). Hosts now ask for:

- Controls that feel like the catalog descriptions (virtualized lists, real series, sort/filter grid)
- Jobs 1.0 never named (command palette, coach marks, paywall, file drop)
- Page recipes that compose those jobs (invoice, compare, in-call)
- Optional chrome that *presents* sibling MauiEssentials plugins without taking a `PackageReference`

Those are still **UI library** problems. Runtime work stays in `Plugin.Maui.*`.

---

## 2. Principles (unchanged)

1. **Single assembly.** New types land in `NuvyntraLabs.UIKit`. Internal folders stay acyclic: Theming → Primitives → Actions / Inputs / Feedback → Layout → Data / Charts / Calendar / Media → Pages.
2. **Reuse before new XAML.** A page may only compose existing `NV*` types + tokens. New chrome goes into a control first.
3. **One type per job.** Do not add Snackbar, Shimmer, SideDrawer, SlideView, or `NVLineChart`. Those are aliases or series.
4. **Framework first.** Do not wrap `ScrollView`, `StackLayout`, `Grid`, `FlexLayout`, or `AbsoluteLayout`.
5. **Tokens own appearance.** No `#RRGGBB` or magic `Thickness` in control code-behind.
6. **No sibling PackageReference.** Hosts attach [VoipCore](https://www.nuget.org/packages/Plugin.Maui.VoipCore), [OfflineSync](https://www.nuget.org/packages/Plugin.Maui.OfflineSync), [SmartUpload](https://www.nuget.org/packages/Plugin.Maui.SmartUpload), [BluetoothManager](https://www.nuget.org/packages/Plugin.Maui.BluetoothManager), [Printing](https://www.nuget.org/packages/Plugin.Maui.Printing), [NfcPlus](https://www.nuget.org/packages/Plugin.Maui.NfcPlus), [AppReview](https://www.nuget.org/packages/Plugin.Maui.AppReview), [FormValidation](https://www.nuget.org/packages/Plugin.Maui.FormValidation), [KeyboardManager](https://www.nuget.org/packages/Plugin.Maui.KeyboardManager) themselves. Host-chrome types expose slots (`ICommand`, streams, bindable content) only.
7. **A control is done only with tests + gallery page.** Same bar as 1.0 §8.
8. **Pipeline-only publish.** Bump `Version` / `PackageVersion` in the UIKit csproj. CI pushes nuget.org (`NUGET_KEY_UIKIT`) and GitHub Packages.

---

## 3. Totals

| Layer | 1.0 | This plan | After (if all slices ship) |
| --- | ---: | ---: | ---: |
| Unique controls | 177 | **+24** | 201 |
| Page recipes | 57 | **+9** | 66 |
| Helpers | 2 | 0 | 2 |
| Foundation | 8 | 0 | 8 |

**33 new public types** (24 controls + 9 recipes). Deepening 1.0 types does **not** add names and is **not** in the +24.

Slash-pairs stay **two types** when the jobs differ (`NVPaywall` gate vs `NVSubscriptionCard` tile; `NVCallBar` overlay vs `NVInCallView` full chrome; `NVInvoiceView` vs `NVReceiptView`).

---

## 4. What 1.0 already covers — deepen first

Do **not** add a second list, grid, or chart type. 1.1 makes the existing names match [nuvyntralabs-uikit-components.md](nuvyntralabs-uikit-components.md).

| 1.0 type | 1.0 today (typical) | 1.4 “done” |
| --- | --- | --- |
| `NVCollectionView` | `VerticalStackLayout` of cards | MAUI virtualization; `LayoutMode`; swipe; select; group — **done** |
| `NVDataGrid` / `NVTreeDataGrid` | Simple `Grid` of labels | Sort cycle, filter, freeze, edit commit/cancel, page via `NVDataPager` — **done** |
| `NVChart` | Labeled `BoxView` bars | One `GraphicsView`; `NVChartSeriesKind` actually draws — **done** |
| `NVCalendar` / `NVScheduler` | Kit chrome | Month nav, multi-select, recurrence cap, agenda list — **done** |
| `NVPdfViewer` / `NVImageEditor` / `NVChat` | Title / caption / message list | Zoom/search, crop/annotate, streaming + attach slot — **done** |
| `NVBarcode` | Encoded `Label` text | Drawn Code128 / QR (still **generate-only**) — **done** |

Also continue Phase 7 from the 1.0 plan: RTL, contrast, font scale 80–200%, Windows keyboard, Mac Catalyst, 90% line coverage.

**Gate:** do not merge 1.2 catalog names until `NVCollectionView`, `NVDataGrid`, and `NVChart` have gallery pages that exercise the rows above.

---

## 5. Releases

| Release | Theme | Ships |
| --- | --- | --- |
| **1.1.0** → **1.4.0** | Deepen 1.0 (no new catalog names) | §4 types — **shipped** (Phase 7 RTL / contrast continues) |
| **1.2.0** | Unique everyday chrome | 8 controls + 6 recipes (priority cut) — **shipped** |
| **1.3.0** | Data / viz + remaining chrome | remaining 16 controls + remaining 3 recipes — **shipped** |
| **1.5.0** | Rename confusing field | `NVEmailField` → `NVInputField` — **shipped** |

Bump `Version` / `PackageVersion` in the UIKit project. Update hub counts in `UIKit/README.md`, `UIKit/UIKitLib.md`, `NVCatalog`, and [nuvyntralabs-uikit-components.md](nuvyntralabs-uikit-components.md) in the same release.

### 5.1 Priority cut (1.2.0)

| Kind | Types |
| --- | --- |
| Controls (8) | `NVCommandPalette`, `NVCoachMark`, `NVContextMenu`, `NVFileDrop`, `NVPaywall`, `NVWhatsNew`, `NVConsentBanner`, `NVHeatCalendar` |
| Recipes (6) | `NVInvoiceView`, `NVReceiptView`, `NVCompareView`, `NVStoreLocatorView`, `NVSubscriptionView`, `NVWhatsNewView` |

`NVHeatCalendar` is the one 1.2 viz type — it is not a `NVChart` series (day cells, not x/y).

---

## 6. New unique controls (24)

IDs are new bands so they do not collide with NV-FND … NV-MED / NV-PG-01…49.

### 6.1 App chrome — `NV-APP` (10)

| ID | Type | Role | Ships |
| --- | --- | --- | --- |
| NV-APP-01 | `NVCommandPalette` | ⌘K / spotlight; filter commands + recent | 1.2 |
| NV-APP-02 | `NVCoachMark` | Spotlight hole + title/body/next on a real control | 1.2 |
| NV-APP-03 | `NVContextMenu` | Long-press / right-click items (`NVMenu` stays a drop-down **button**) | 1.2 |
| NV-APP-04 | `NVSpeedDial` | FAB that fans out 2–5 actions | 1.3 |
| NV-APP-05 | `NVFileDrop` | Drop well + attach chips; host supplies pick/bytes | 1.2 |
| NV-APP-06 | `NVWhatsNew` | Version title + bullet list + dismiss | 1.2 |
| NV-APP-07 | `NVConsentBanner` | Privacy copy + accept / manage actions | 1.2 |
| NV-APP-08 | `NVPaywall` | Blocking / sheet gate; slots for plan tiles | 1.2 |
| NV-APP-09 | `NVSubscriptionCard` | One plan: name, price, feature bullets, CTA | 1.3 |
| NV-APP-10 | `NVEmojiPicker` | Searchable glyph grid for composer / chat | 1.3 |

Reuse: `OverlayHost` for palette, context menu, paywall, what’s new. `NVFloatingActionButton` for speed-dial. `NVBanner` chrome for consent (new type because actions + legal copy are the job). `NVPaywall` hosts `NVSubscriptionCard`; do not merge them.

### 6.2 Data plus — `NV-DAT` (3)

| ID | Type | Role | Ships |
| --- | --- | --- | --- |
| NV-DAT-08 | `NVPivotGrid` | Rows × columns aggregation (`NVDataGrid` stays flat) | 1.3 |
| NV-DAT-09 | `NVPropertyGrid` | Inspect key/value with `NV*` editors | 1.3 |
| NV-DAT-10 | `NVJsonTree` | Expandable JSON (`NVTreeView` is general hierarchy) | 1.3 |

Reuse: `NVTreeView` expand model, `NVDataForm` field factory, `FieldChrome`.

### 6.3 Viz / media plus (3)

| ID | Type | Role | Ships |
| --- | --- | --- | --- |
| NV-VIZ-08 | `NVHeatCalendar` | Contribution / habit day cells | 1.2 |
| NV-MED-11 | `NVDiffView` | Unified / side-by-side text | 1.3 |
| NV-MED-12 | `NVCodeEditor` | Editable code (`NVCodeBlock` stays display-only) | 1.3 |

Reuse: `NVCalendar` month math for the heatmap. Do **not** add `NVSankey` / `NVNetworkGraph` in this wave.

### 6.4 Host chrome — `NV-HST` (8)

UI only. No `Plugin.Maui.*` reference inside the library.

| ID | Type | Role | Host (app, not this nupkg) | Ships |
| --- | --- | --- | --- | --- |
| NV-HST-01 | `NVCallBar` | Compact in-call overlay (mute / end) | [VoipCore](https://www.nuget.org/packages/Plugin.Maui.VoipCore) | 1.3 |
| NV-HST-02 | `NVInCallView` | Full in-call chrome (avatar, timer, keypad slot) | VoipCore | 1.3 |
| NV-HST-03 | `NVSyncConflictCard` | Local vs remote + keep / take remote | [OfflineSync](https://www.nuget.org/packages/Plugin.Maui.OfflineSync) | 1.3 |
| NV-HST-04 | `NVUploadTile` | File name, bytes, retry | [SmartUpload](https://www.nuget.org/packages/Plugin.Maui.SmartUpload) | 1.3 |
| NV-HST-05 | `NVDeviceSheet` | Nearby device list + connect | [BluetoothManager](https://www.nuget.org/packages/Plugin.Maui.BluetoothManager) | 1.3 |
| NV-HST-06 | `NVPrintPreview` | Page image slot + print / share actions | [Printing](https://www.nuget.org/packages/Plugin.Maui.Printing), [SharePlus](https://www.nuget.org/packages/Plugin.Maui.SharePlus) | 1.3 |
| NV-HST-07 | `NVNfcPrompt` | Hold-near artwork + status | [NfcPlus](https://www.nuget.org/packages/Plugin.Maui.NfcPlus) | 1.3 |
| NV-HST-08 | `NVReviewPrompt` | Stars + “not now” / “review” | [AppReview](https://www.nuget.org/packages/Plugin.Maui.AppReview) | 1.3 |

Bindable surface is chrome + `ICommand`. Sample mocks the host; the library must compile without those packages.

---

## 7. New page recipes (9)

Each recipe is a `ContentView`. Tile vs list vs card stays `LayoutMode`.

| ID | Type | Built from | Ships |
| --- | --- | --- | --- |
| NV-PG-50 | `NVInvoiceView` | `NVCollectionView`, `NVCurrencyLabel`, `NVStickyBar` | 1.2 |
| NV-PG-51 | `NVReceiptView` | `NVTicket`, `NVCurrencyLabel`, `NVBarcode` | 1.2 |
| NV-PG-52 | `NVCompareView` | two `NVCard` columns + `NVCheckList` | 1.2 |
| NV-PG-53 | `NVStoreLocatorView` | `NVCollectionView` + `NVMap` slot | 1.2 |
| NV-PG-54 | `NVSubscriptionView` | `NVPaywall` or `NVSubscriptionCard` row | 1.2 |
| NV-PG-55 | `NVWhatsNewView` | `NVWhatsNew` | 1.2 |
| NV-PG-56 | `NVConflictResolveView` | `NVSyncConflictCard` | 1.3 |
| NV-PG-57 | `NVCallView` | `NVInCallView` | 1.3 |
| NV-PG-58 | `NVAddressFormView` | `NVDataForm`, `NVCountryPicker`, `NVPhoneField` | 1.3 |

If a recipe needs new chrome, **stop** and add the control first.

---

## 8. Out of scope (this wave and still)

| Item | Why |
| --- | --- |
| Snackbar, Shimmer, SideDrawer, SlideView, Rotator | Aliases of Toast, Skeleton, Drawer, Carousel |
| `NVLineChart`, `NVPieChart`, Sankey, network graph | Series or a later viz wave |
| `NVScrollView` / `NVStackLayout` / `NVGrid` | Framework first |
| PDF / Word / Excel / ZIP **engines** | Not UI |
| Camera barcode **scanner** | 1.0 exclusion; host camera / MediaPipeline |
| Paid map tiles, real Face ID, STT, video decode | Host plugins; keep slots |
| Vendor “AI AssistView” | `NVChat` + `NVAIPrompt` already exist |
| WPF / WinUI / Avalonia / Uno ports | MAUI only |
| Growing past ~190 **named** controls before 1.1 deepen ships | Names without behavior |

---

## 9. Shared building blocks (write once)

Do not fork 1.0 blocks. Extend them.

| Block | New consumers |
| --- | --- |
| `OverlayHost` | Command palette, context menu, paywall, what’s new, device sheet, review prompt |
| `NVFloatingActionButton` | Speed dial |
| `NVBanner` / `FieldChrome` | Consent, upload tile, conflict card |
| `NVTreeView` expand | JSON tree, property grid |
| `NVCalendar` month math | Heat calendar |
| `NVDataForm` field factory | Address recipe, property grid editors |
| `NVEmptyView` | Palette no-results, locator empty |
| `LayoutMode` | Compare / locator lists |

Optional later (not this wave): `NVDataForm.Map<T>()` source generator.

---

## 10. Catalog and sample updates (same PR as the types)

In `UIKit/`:

1. Append types to `NVCatalog.Controls` / `NVCatalog.Pages` (tests assert names).
2. Add a gallery section **Next** (or App / Data+ / Host) in `samples/NuvyntraLabs.UIKit.Sample`.
3. Document bindable names in `UIKit/UIKitLib.md`.
4. Recount README: “201 controls + 66 page recipes” only after **1.3.0**. After 1.2 write the actual shipped count.

In the hub (this repo), merge shipped IDs into [nuvyntralabs-uikit-components.md](nuvyntralabs-uikit-components.md) when the submodule pointer moves.

---

## 11. Tests

Same contract as 1.0 §8. Every new `NV*` view:

| ID | Case |
| --- | --- |
| T-COM-01…08 | Default ctor, bindable round-trip, disabled, theme, contrast, automation, `CanExecute`, no leak |
| T-APP-01 | Palette filter is case-insensitive; empty query shows recents |
| T-APP-02 | Coach mark `Next` advances; last step raises `Completed` |
| T-APP-03 | Context menu opens on command; item `Command` fires once |
| T-APP-04 | File drop ignores empty; chips bind `Name` / `Size` |
| T-APP-05 | Paywall `Dismiss` is a no-op when `IsBlocking` |
| T-APP-06 | Consent `Accept` sets a bindable `IsAccepted` |
| T-VIZ-08 | Heat calendar cells = days in `Month`; missing values draw empty |
| T-DAT-08 | Pivot empty source renders without throw |
| T-HST-01 | Host chrome types construct with null commands (sample mocks) |
| T-PG-50…58 | Each recipe instantiates with null `BindingContext` |

Coverage gate stays **≥ 90%** line on the library. Add `Tests/{Area}/{Control}Tests.cs` in the same PR as the control.

---

## 12. Suggested PR sequence

Work in the `UIKit/` submodule. One gallery page + tests per PR.

**1.1.0**

1. `NVCollectionView` virtualization + selection  
2. `NVDataGrid` sort / filter / page (tree-grid reuses columns)  
3. `NVChart` Skia surface + existing `NVChartSeriesKind`  
4. Calendar / scheduler + barcode draw  
5. Phase 7 RTL / contrast pass  

**1.2.0**

6. `OverlayHost` extensions → `NVCommandPalette`, `NVContextMenu`  
7. `NVCoachMark`, `NVWhatsNew`, `NVConsentBanner`  
8. `NVFileDrop`, `NVPaywall`  
9. `NVHeatCalendar`  
10. Recipes NV-PG-50…55  

**1.3.0**

11. `NVSpeedDial`, `NVSubscriptionCard`, `NVEmojiPicker`  
12. `NVPivotGrid`, `NVPropertyGrid`, `NVJsonTree`  
13. `NVDiffView`, `NVCodeEditor`  
14. Host chrome NV-HST-01…08 (mocked sample)  
15. Recipes NV-PG-56…58  
16. Hub pointer + catalog merge + version bump  

---

## 13. Success criteria

| Release | Done when |
| --- | --- |
| 1.1.0 → 1.4.0 | Gallery proves list / grid / chart rows in §4; no new `NVCatalog` names — **done** |
| 1.5.0 | `NVInputField` is the catalog name; no remaining `NVEmailField` type — **done** |
| 1.2.0 | All NV-APP 1.2 IDs + NV-VIZ-08 + NV-PG-50…55 construct from the sample; `UIKitLib.md` lists new bindables |
| 1.3.0 | All 24 + 9 IDs are in `NVCatalog`; README counts match; host types compile without `Plugin.Maui.*` — **done** |

Lumina light and dark stay original (not Syncfusion / Telerik). Single nupkg via CI.

---

## 14. Locked decisions

| Topic | Choice |
| --- | --- |
| Where types live | Same `NuvyntraLabs.UIKit` nupkg |
| How many new types | **33** (24 controls + 9 recipes) unless a later conversation cuts the list |
| 1.2 cut | **8 + 6** (§5.1) |
| Deepen vs names | 1.1 deepen **before** 1.2 names |
| Host plugins | Slots only; host PackageReference |
| Barcode scan / document engines | Still out of scope |

Niladri Padhy / Nuvyntra Labs. Hub: [MauiEssentials](https://github.com/nuvyntralabs/MauiEssentials). Package: [NuvyntraLabs.UIKit](https://www.nuget.org/packages/NuvyntraLabs.UIKit).
