# NuvyntraLabs.UIKit — unique component catalog

**Status:** Implemented at `1.5.0` (201 controls + 66 recipes; `NVEmailField` renamed to `NVInputField`)  
**Product:** NuvyntraLabs.UIKit  
**Package:** `NuvyntraLabs.UIKit` (single library)  
**Type prefix:** `NV` (`NVCheckBox`, `NVRadioButton`)  
**XAML xmlns:** `http://nuvyntralabs.com/uikit` → `nv`  
**Hub submodule:** `UIKit/` (separate git repository)  
**Design language:** **Lumina** (original; not a Syncfusion or Telerik theme)

This document is the **capability inventory**. Vendor sites were used only to find unique jobs. Class names are Nuvyntra Labs originals.

Capability references only:

- [Essential UI Kit for .NET MAUI](https://www.syncfusion.com/essential-maui-ui-kit) — page patterns
- [Telerik UI for .NET MAUI](https://www.telerik.com/maui-ui#all-components) — control surface
- [Syncfusion .NET MAUI Controls](https://www.syncfusion.com/maui-controls) and [Syncfusion Toolkit](https://github.com/syncfusion/maui-toolkit) — control surface

Implementation order, reuse layers, tests, and the sample gallery live in [nuvyntralabs-uikit.md](nuvyntralabs-uikit.md). Post-1.0 names and the 1.4 deepen notes live in [nuvyntralabs-uikit-next.md](nuvyntralabs-uikit-next.md).

---

## Naming

| Rule | Example |
| --- | --- |
| Prefix | `NV` + familiar control name, PascalCase |
| Views | `NVCheckBox`, `NVRadioButton`, `NVDataGrid` |
| Helpers | `NVTheme`, `NVTokens`, `NVRadioGroup` |
| Pages | `NVSignInView`, `NVCartView` — recipes, not extra chrome |
| IDs | `NV-FND-01`, `NV-ACT-05`, … |

Never `Sf*`, `Rad*`, or `Lk*`.

---

## 1. How uniqueness was decided

Vendor catalogs overlap heavily. This kit ships **one** type per problem.

| Rule | Meaning |
| --- | --- |
| One type per job | `NVButton`, not three branded buttons. Variants are bindable properties / styles. |
| Merge aliases | SideDrawer = NavigationDrawer. Carousel = SlideView = Rotator. Skeleton = Shimmer. Chat = Conversational UI = AI AssistView (same shell, different message kinds). |
| Chart is one engine | Line, bar, pie, candle, funnel, polar, sunburst, spark are **series**, not separate packages. |
| Pages are compositions | Login, Cart, Dashboard are **recipes** over primitives. |
| Framework first | Do not wrap a MAUI control unless Lumina styling or missing behavior is the product. |
| Out of scope | Document **processing** libraries (PDF/Word/Excel/ZIP engines). PDF **viewing** is in. |

---

## 2. Unique controls

**Total unique controls: 201** (plus 2 helper types: `NVRadioGroup`, `NVFormField`)  
**Total unique page recipes: 66**

Vendor-shaped 1.0 (96) plus the everyday mobile surface (basics → advanced) so one kit can compose a typical app.

### 2.1 Foundation (8)

| ID | Type | Role |
| --- | --- | --- |
| NV-FND-01 | `NVTheme` | Light / dark + runtime brand swap |
| NV-FND-02 | `NVTokens` | Color, space, radius, elevation, duration |
| NV-FND-03 | `NVTypography` | Display / title / body / label / mono |
| NV-FND-04 | `NVIcons` | Stroke icon font |
| NV-FND-05 | `NVMotion` | Easing, duration, reduced-motion |
| NV-FND-06 | `NVDensity` | Compact / comfortable / spacious |
| NV-FND-07 | `NVVisualState` | Rest / hover / press / focus / disabled / error |
| NV-FND-08 | `NVAccessibility` | Focus ring, live region, contrast helpers |

### 2.2 Primitives (12)

| ID | Type | Notes |
| --- | --- | --- |
| NV-PRI-01 | `NVSurface` | Themed paper fill |
| NV-PRI-02 | `NVDivider` | Horizontal / vertical hairline |
| NV-PRI-03 | `NVIcon` | Size, tone, spin |
| NV-PRI-04 | `NVAvatar` | Initials, image, status pip |
| NV-PRI-05 | `NVBadge` | Count, dot, tone |
| NV-PRI-06 | `NVSkeleton` | Wave / pulse placeholders |
| NV-PRI-07 | `NVEffects` | Press ripple, highlight |
| NV-PRI-08 | `NVElevation` | 0–5 shadow steps |
| NV-PRI-09 | `NVOverlay` | Scrim for sheets and dialogs |
| NV-PRI-10 | `NVInteractiveViewer` | Zoom, pan, reset |
| NV-PRI-11 | `NVSpacer` | Token-sized gap |
| NV-PRI-12 | `NVHighlight` | Search / mention highlight span |

### 2.3 Actions (10 + `NVRadioGroup`)

| ID | Type | Variants |
| --- | --- | --- |
| NV-ACT-01 | `NVButton` | Filled, tonal, outline, ghost, danger |
| NV-ACT-02 | `NVIconButton` | Square / circular |
| NV-ACT-03 | `NVToggleButton` | On / off with icon |
| NV-ACT-04 | `NVDropDownButton` | Menu flyout |
| NV-ACT-05 | `NVCheckBox` | Checked / unchecked / indeterminate |
| NV-ACT-06 | `NVRadioButton` | Group via `NVRadioGroup` |
| NV-ACT-07 | `NVSwitch` | On / off + label |
| NV-ACT-08 | `NVChip` | Filter, input, assist, choice |
| NV-ACT-09 | `NVSegmentedControl` | Equal / wrap, icons |
| NV-ACT-10 | `NVSpeechToTextButton` | Host supplies recognizer |

### 2.4 Inputs (22)

| ID | Type | Notes |
| --- | --- | --- |
| NV-INP-01 | `NVTextField` | Floating label, helper, error, leading / trailing |
| NV-INP-02 | `NVEditor` | Multi-line, counter |
| NV-INP-03 | `NVSearchBar` | Debounce, clear, suggestions slot |
| NV-INP-04 | `NVMaskedEntry` | Pattern mask |
| NV-INP-05 | `NVNumericEntry` | Culture, format |
| NV-INP-06 | `NVNumericUpDown` | Inc / dec |
| NV-INP-07 | `NVOtpInput` | Length, mask, paste |
| NV-INP-08 | `NVAutoComplete` | Filter, async source |
| NV-INP-09 | `NVComboBox` | Editable / closed |
| NV-INP-10 | `NVPicker` | Single / multi |
| NV-INP-11 | `NVDatePicker` | Calendar popover |
| NV-INP-12 | `NVTimePicker` | 12 / 24 h |
| NV-INP-13 | `NVDateTimePicker` | Combined |
| NV-INP-14 | `NVTimeSpanPicker` | Duration |
| NV-INP-15 | `NVTemplatedPicker` | Host item template |
| NV-INP-16 | `NVColorPicker` | Palette + custom |
| NV-INP-17 | `NVSlider` | Discrete ticks |
| NV-INP-18 | `NVRangeSlider` | Dual thumb |
| NV-INP-19 | `NVCircularSlider` | Angular value |
| NV-INP-20 | `NVRangeSelector` | Chart-linked or standalone |
| NV-INP-21 | `NVSignaturePad` | Stroke export |
| NV-INP-22 | `NVRating` | Stars / custom glyph |

`NVPromptInput` (NV-MED-10) is `NVEditor` + send / stop / attach slots, not a third text box. `NVDataForm` hosts these fields.

### 2.5 Feedback (10)

| ID | Type | Notes |
| --- | --- | --- |
| NV-FBK-01 | `NVProgressBar` | Linear; determinate / indeterminate |
| NV-FBK-02 | `NVCircularProgressBar` | Circular; determinate / indeterminate |
| NV-FBK-03 | `NVStepProgressBar` | Horizontal steps |
| NV-FBK-04 | `NVBusyIndicator` | Overlay + label |
| NV-FBK-05 | `NVPullToRefresh` | Composes MAUI `RefreshView` chrome |
| NV-FBK-06 | `NVPopup` | Modal / anchored |
| NV-FBK-07 | `NVToast` | Timed, swipe dismiss |
| NV-FBK-08 | `NVBanner` | Inline alert |
| NV-FBK-09 | `NVEmptyView` | Icon, title, action |
| NV-FBK-10 | `NVTooltip` | Hover / long-press |

### 2.6 Layout and navigation (16)

| ID | Type | Notes |
| --- | --- | --- |
| NV-LAY-01 | `NVCard` | Media, actions, dismiss |
| NV-LAY-02 | `NVAccordion` | One-open or multi |
| NV-LAY-03 | `NVExpander` | Single panel |
| NV-LAY-04 | `NVTabView` | Top / bottom, scrollable |
| NV-LAY-05 | `NVBottomSheet` | Detents, scrim |
| NV-LAY-06 | `NVNavigationDrawer` | Any edge |
| NV-LAY-07 | `NVNavigationView` | Adaptive: hamburger → rail → expanded |
| NV-LAY-08 | `NVDockLayout` | LTRB + fill |
| NV-LAY-09 | `NVWrapLayout` | Flow wrap |
| NV-LAY-10 | `NVGridSplitter` | Resize panes |
| NV-LAY-11 | `NVToolbar` | Title, actions, overflow |
| NV-LAY-12 | `NVBackdrop` | Revealed back layer |
| NV-LAY-13 | `NVCarousel` | Peek, indicators |
| NV-LAY-14 | `NVParallaxView` | Header shift |
| NV-LAY-15 | `NVBottomNavigation` | 3–5 destinations |
| NV-LAY-16 | `NVRadialMenu` | Deferred if usage is low |

### 2.7 Data (7)

| ID | Type | Notes |
| --- | --- | --- |
| NV-DAT-01 | `NVCollectionView` | Virtualized list / grid / horizontal. Group, swipe, select |
| NV-DAT-02 | `NVDataGrid` | Sort, filter, group, edit, freeze, page |
| NV-DAT-03 | `NVTreeDataGrid` | Hierarchical rows; reuses `NVDataGrid` columns |
| NV-DAT-04 | `NVTreeView` | Expand, check, lazy |
| NV-DAT-05 | `NVDataForm` | Auto fields from `NV*` inputs; host may attach FormValidation |
| NV-DAT-06 | `NVDataPager` | Shared by grid and list |
| NV-DAT-07 | `NVKanban` | Columns + `NVCard` |

### 2.8 Visualization (7)

| ID | Type | Notes |
| --- | --- | --- |
| NV-VIZ-01 | `NVChart` | One Skia surface. Series: line, spline, area, bar, column, pie, donut, scatter, bubble, candle, OHLC, funnel, pyramid, polar, radar, sunburst, spark |
| NV-VIZ-02 | `NVRadialGauge` | Arcs, needles |
| NV-VIZ-03 | `NVLinearGauge` | Horizontal / vertical |
| NV-VIZ-04 | `NVDigitalGauge` | Segment digits |
| NV-VIZ-05 | `NVMap` | Tiles + shapes; host supplies tile source |
| NV-VIZ-06 | `NVBarcode` | 1D / 2D **generation** (not camera scan) |
| NV-VIZ-07 | `NVTreeMap` | Nested rectangles |

### 2.9 Calendar and scheduling (2)

| ID | Type | Notes |
| --- | --- | --- |
| NV-CAL-01 | `NVCalendar` | Month / year / decade; multi-select |
| NV-CAL-02 | `NVScheduler` | Day / week / month; recurrence |

### 2.10 Media, documents, conversation, AI (10)

| ID | Type | Notes |
| --- | --- | --- |
| NV-MED-01 | `NVImageEditor` | Crop, rotate, annotate |
| NV-MED-02 | `NVRichTextEditor` | Bold / lists / link; not a Word engine |
| NV-MED-03 | `NVMarkdownViewer` | Render + optional edit |
| NV-MED-04 | `NVPdfViewer` | Open file / stream; zoom, search |
| NV-MED-05 | `NVChat` | Message list, composer, typing, attachments |
| NV-MED-06 | `NVAIPrompt` | Suggestion chips + submit |
| NV-MED-07 | `NVSmartPasteButton` | Host maps clipboard → fields |
| NV-MED-08 | `NVDocxViewer` | Phase 6 — view / light edit |
| NV-MED-09 | `NVSpreadsheet` | Phase 6 — grid of cells, not an Excel engine |
| NV-MED-10 | `NVPromptInput` | Text area + send / stop / attach slots |

### 2.11 Basics → advanced (complete mobile surface)

These close the gap between a control catalog and “design any mobile app.”

| Band | Types |
| --- | --- |
| Type and chrome | `NVHeading`, `NVBodyText`, `NVCaptionText`, `NVImage`, `NVSafeArea`, `NVSectionHeader`, `NVFormSection`, `NVAppScaffold`, `NVFloatingActionButton`, `NVDotIndicator` |
| Rows | `NVListTile`, `NVSettingsTile`, `NVChipGroup`, `NVCheckList`, `NVGroupedList`, `NVIndexBar`, `NVSwipeTile`, `NVSelectionBar`, `NVSkeletonList`, `NVInfiniteFooter` |
| Overlays | `NVDialog`, `NVActionSheet`, `NVMenu` |
| Fields | `NVInputField`, `NVPhoneField`, `NVPasswordField`, `NVPasswordStrength`, `NVQuantityStepper`, `NVDateRangePicker`, `NVMonthYearPicker`, `NVFilterBar`, `NVTagInput`, `NVPinPad`, `NVCopyable`, `NVLink`, `NVCountryPicker`, `NVLanguagePicker`, `NVThemePicker` |
| Patterns | `NVCurrencyLabel`, `NVCountdown`, `NVQuote`, `NVCodeBlock`, `NVBulletList`, `NVStatCard`, `NVTimeline`, `NVWizard`, `NVStickyBar`, `NVCartBar`, `NVPriceTag`, `NVVariantPicker`, `NVCouponField`, `NVTicket`, `NVTimeSlotPicker`, `NVSeatPicker` |
| Social | `NVProfileHeader`, `NVFeedCard`, `NVComposer`, `NVBubble`, `NVTypingIndicator`, `NVStoryRing`, `NVReactionBar`, `NVNotificationRow`, `NVContactTile` |
| Media+ | `NVImageGallery`, `NVLightbox`, `NVVideoPlayer`, `NVAudioPlayer`, `NVWebView`, `NVVoiceNote`, `NVWaveform`, `NVBeforeAfter` |
| Advanced | `NVMasterDetail`, `NVRetryView`, `NVOfflineBanner`, `NVPermissionCard`, `NVForceUpdate`, `NVLockPad`, `NVBiometricGate`, `NVDashboardGrid`, `NVGantt`, `NVOrgChart` |

Extra recipes: `NVPinLockView`, `NVForceUpdateView`, `NVSearchResultsView`, `NVFilterSheetView`, `NVMediaPlayerView`, `NVSplitInboxView`, `NVOnboardingPermissionsView`, `NVOrderSummaryView`.

### 2.12 App chrome and heat calendar (1.2)

| ID | Type | Role |
| --- | --- | --- |
| NV-APP-01 | `NVCommandPalette` | ⌘K / spotlight; filter commands + recent |
| NV-APP-02 | `NVCoachMark` | Spotlight hole + title/body/next on a real control |
| NV-APP-03 | `NVContextMenu` | Long-press / right-click items (`NVMenu` stays a drop-down **button**) |
| NV-APP-05 | `NVFileDrop` | Drop well + attach chips; host supplies pick/bytes |
| NV-APP-06 | `NVWhatsNew` | Version title + bullet list + dismiss |
| NV-APP-07 | `NVConsentBanner` | Privacy copy + accept / manage actions |
| NV-APP-08 | `NVPaywall` | Blocking / sheet gate; slots for plan tiles |
| NV-VIZ-08 | `NVHeatCalendar` | Contribution / habit day cells |
| NV-APP-04 | `NVSpeedDial` | FAB that fans out 2–5 actions |
| NV-APP-09 | `NVSubscriptionCard` | One plan: name, price, feature bullets, CTA |
| NV-APP-10 | `NVEmojiPicker` | Searchable glyph grid |

### 2.13 Data, media, and host chrome (1.3)

| ID | Type | Role |
| --- | --- | --- |
| NV-DAT-08 | `NVPivotGrid` | Rows × columns aggregation |
| NV-DAT-09 | `NVPropertyGrid` | Inspect key/value with `NV*` editors |
| NV-DAT-10 | `NVJsonTree` | Expandable JSON |
| NV-MED-11 | `NVDiffView` | Unified / side-by-side text |
| NV-MED-12 | `NVCodeEditor` | Editable code |
| NV-HST-01 | `NVCallBar` | Compact in-call overlay |
| NV-HST-02 | `NVInCallView` | Full in-call chrome |
| NV-HST-03 | `NVSyncConflictCard` | Local vs remote |
| NV-HST-04 | `NVUploadTile` | File name, bytes, retry |
| NV-HST-05 | `NVDeviceSheet` | Nearby device list |
| NV-HST-06 | `NVPrintPreview` | Page image slot |
| NV-HST-07 | `NVNfcPrompt` | Hold-near artwork |
| NV-HST-08 | `NVReviewPrompt` | Stars + not now / review |

---

## 3. Unique page recipes (compositions)

Each recipe is a `ContentView`. Tile vs list vs card is `LayoutMode`, not a new type.

### 3.1 Auth and onboarding (8)

| ID | Type | Built from |
| --- | --- | --- |
| NV-PG-01 | `NVSignInView` | `NVTextField`, `NVButton`, `NVIconButton` |
| NV-PG-02 | `NVSignUpView` | `NVDataForm` |
| NV-PG-03 | `NVForgotPasswordView` | `NVTextField`, `NVButton`, `NVEmptyView` |
| NV-PG-04 | `NVResetPasswordView` | `NVOtpInput`, `NVTextField` |
| NV-PG-05 | `NVSocialSignInView` | `NVSignInView` + `NVIconButton` row |
| NV-PG-06 | `NVTabbedAuthView` | `NVTabView` + sign-in / sign-up |
| NV-PG-07 | `NVProfileSetupView` | `NVAvatar`, `NVDataForm` |
| NV-PG-08 | `NVWalkthroughView` | `NVCarousel`, `NVButton` |

### 3.2 Commerce (12)

| ID | Type |
| --- | --- |
| NV-PG-09 | `NVCategoryView` |
| NV-PG-10 | `NVCatalogView` |
| NV-PG-11 | `NVProductHomeView` |
| NV-PG-12 | `NVProductDetailView` |
| NV-PG-13 | `NVCartView` |
| NV-PG-14 | `NVWishlistView` |
| NV-PG-15 | `NVCheckoutView` |
| NV-PG-16 | `NVCardPaymentView` |
| NV-PG-17 | `NVSavedCardsView` |
| NV-PG-18 | `NVPaymentResultView` |
| NV-PG-19 | `NVOrdersView` |
| NV-PG-20 | `NVOrderHistoryView` |

### 3.3 Content and about (8)

| ID | Type |
| --- | --- |
| NV-PG-21 | `NVArticleFeedView` |
| NV-PG-22 | `NVArticleDetailView` |
| NV-PG-23 | `NVMyArticlesView` |
| NV-PG-24 | `NVReviewView` |
| NV-PG-25 | `NVContactView` |
| NV-PG-26 | `NVAboutView` |
| NV-PG-27 | `NVFaqView` |
| NV-PG-28 | `NVBookmarksView` |

### 3.4 Chat, social, profile (7)

| ID | Type |
| --- | --- |
| NV-PG-29 | `NVInboxView` |
| NV-PG-30 | `NVConversationView` |
| NV-PG-31 | `NVSocialProfileView` |
| NV-PG-32 | `NVPeopleListView` |
| NV-PG-33 | `NVAuthorProfileView` |
| NV-PG-34 | `NVHealthProfileView` |
| NV-PG-35 | `NVChatProfileView` |

### 3.5 Lists, files, media (6)

| ID | Type |
| --- | --- |
| NV-PG-36 | `NVNavigationHubView` |
| NV-PG-37 | `NVMediaLibraryView` |
| NV-PG-38 | `NVPlaylistView` |
| NV-PG-39 | `NVFileExplorerView` |
| NV-PG-40 | `NVDocumentsView` |
| NV-PG-41 | `NVSuggestionsView` |

### 3.6 Empty, error, settings (8)

| ID | Type |
| --- | --- |
| NV-PG-42 | `NVStatusView` | Empty / error via reason enum |
| NV-PG-43 | `NVSettingsView` |
| NV-PG-44 | `NVHelpView` |
| NV-PG-45 | `NVNotificationsView` |
| NV-PG-46 | `NVDeliveryTrackView` |
| NV-PG-47 | `NVAddressBookView` |
| NV-PG-48 | `NVBookingView` |
| NV-PG-49 | `NVDashboardView` | One layout; sample ships seven data presets |

### 3.7 Next (1.2)

| ID | Type | Built from |
| --- | --- | --- |
| NV-PG-50 | `NVInvoiceView` | `NVCollectionView`, `NVCurrencyLabel`, `NVStickyBar` |
| NV-PG-51 | `NVReceiptView` | `NVTicket`, `NVCurrencyLabel`, `NVBarcode` |
| NV-PG-52 | `NVCompareView` | two `NVCard` columns + `NVCheckList` |
| NV-PG-53 | `NVStoreLocatorView` | `NVCollectionView` + `NVMap` slot |
| NV-PG-54 | `NVSubscriptionView` | `NVPaywall` |
| NV-PG-55 | `NVWhatsNewView` | `NVWhatsNew` |
| NV-PG-56 | `NVConflictResolveView` | `NVSyncConflictCard` |
| NV-PG-57 | `NVCallView` | `NVInCallView` |
| NV-PG-58 | `NVAddressFormView` | `NVDataForm`, `NVCountryPicker`, `NVPhoneField` |

---

## 4. Excluded

| Item | Why |
| --- | --- |
| PDF / Word / Excel / ZIP **engines** | Not UI |
| Vendor “smart” AI wrappers | Host AI; we ship `NVAIPrompt` + `NVChat` |
| Camera barcode **scanner** | Generation only (`NVBarcode`) |
| Paid map tile keys | Host injects a tile provider |
| Pixel-identical Essential UI Kit screens | Lumina recipes, not clones |

---

## 5. MauiEssentials composition (host, not PackageReference)

| Need | Niladri / Nuvyntra package |
| --- | --- |
| Field rules on `NVDataForm` | [Plugin.Maui.FormValidation](https://www.nuget.org/packages/Plugin.Maui.FormValidation) |
| Keyboard avoid on auth / checkout | [Plugin.Maui.KeyboardManager](https://www.nuget.org/packages/Plugin.Maui.KeyboardManager) |
| Sample navigation | [Plugin.Maui.MVVMExpress](https://www.nuget.org/packages/Plugin.Maui.MVVMExpress.Core) |
| Print / share a PDF | [Plugin.Maui.Printing](https://www.nuget.org/packages/Plugin.Maui.Printing), [Plugin.Maui.SharePlus](https://www.nuget.org/packages/Plugin.Maui.SharePlus) |
| Image capture into editor | [Plugin.Maui.MediaPipeline](https://www.nuget.org/packages/Plugin.Maui.MediaPipeline) |

Usual alternatives: .NET MAUI built-ins, CommunityToolkit.Maui, Syncfusion, Telerik.
