# Overview Slide-Zoom (缩放总览) Design Reference Manual

Conditional design guidance for a deck whose first page is an archive-style overview hub: one-event content pages open from preview cards on the hub, and the presenter returns to the hub between parts. It reproduces the composition and reading logic of the original PowerPoint 缩放定位 (Slide Zoom) workflow inside this pipeline's editable-SVG → native-PPTX output.

**Trigger**: load only when the user explicitly requests this pattern — the literal phrases 「用缩放总览美化」「做成缩放总览」「用缩放总览来排」, or equivalent English intent such as "overview slide zoom", "zoom overview", or "an archive overview page that opens each story". Never activate it by default: ordinary generate and beautify keep their current behavior, and a deck that merely has many photos, a cover, or a contents page does not qualify. An explicit request also overrides a fidelity page-count invariant: inside Beautify or another fixed-page-count request the pattern still applies, and the hub page plus one-event pages may change the page count — state that change to the user before authoring (§2). A trigger without the user-supplied overview background and decoration assets does not activate it either — ask for them once (§1).

**Ownership**: a conditional Generate design reference, not a fifth route or profile. Default keeps Strategist, its two blocking confirmations, and the plan → lock → execute gates; Quick keeps its one-pass flow. Roster and §IX content stay Plan-only, navigation targets stay §IX `Hyperlinks` content, geometry stays Executor-only; this reference supplies craft and boundary, never a parallel procedure. When the user explicitly asks for it inside Beautify or another fixed-page-count request, apply it anyway: the explicit request overrides only the page-count/re-pagination invariant, not wording fidelity or the profile's other constraints, and the changed page count is stated to the user (§2). Without the explicit request, default Beautify keeps the original page count.

**Read it twice**: in planning before the three Stage-2 solutions and page roster (Default) or in the Quick planning pass, and again in the Executor read batch before P01.

---

## 1. Asset Gate

The user supplies the look of the hub. Do not synthesize, download, or approximate decorations.

| Asset | Required | Treatment |
|---|---|---|
| Overview background image | Yes | Prepared full-bleed derivative, slightly blurred and dimmed (§4) |
| Decoration layers — torn-paper texture, kraft envelope, stamps, tape, postmarks, wordmark stamps | Yes | User-supplied transparent PNGs; placed as image layers |
| Content photos | Yes | One photo per content page by default; white-border framing is SVG-owned |
| Hub title, subtitle, file/index label, credit decoration | Sentence-level text | Authored as editable text, not baked into images |

Ask once, at planning time, naming what is missing. If the user declines to supply the background or decorations, do not run this pattern — an ordinary deck or a plain hyperlinked contents page is the honest outcome (§9). Never invent a kraft envelope or a torn edge to imitate the reference.

Prepare the background before any SVG exists:

```bash
python3 ${SKILL_DIR}/scripts/image_treat.py <project_path> images/<background> \
  --output overview_background.png --blur 6 --brightness 0.78
```

`--blur` and `--brightness` are starting points judged on canvas: keep the background legible enough to read as a surface and quiet enough that cards win. Pixel blur and brightness are prepared derivatives under [`image-base.md`](./image-base.md) §2 — never bake the white photo border or card shadows into a derivative; those stay SVG-owned.

---

## 2. Roster Shape

- **P01 is the hub.** It is the overview page in the roster, counted in §I `Page Count` and present in §IX like any page; it is not a decorative background layer.
- **Pages 02..N are content pages.** Each one carries exactly one event, one story, or one evidence set. Several photos on one page are one event's evidence, not several events.
- **Optional last page** for closing credits only when the source material earns it; it is not part of the hub loop.
- The hub reads as a cover and as a navigation map at once: `page_rhythm` anchor, page job "orient the whole archive and open any part".
- No page-number chrome is required; the file/index label substitutes for it.

§IX records this shape with existing lines only:

- Hub page: `Composition` describes the collage and card placement; `Hyperlinks` lists every card target, e.g. `#slide-02, #slide-03, #slide-04, #slide-05`.
- Each content page: `Hyperlinks` lists its return target, `#slide-01`.

The final checker compares each page's anchors with its `Hyperlinks` line as a set, so the hub line must name every card and nothing else. Do not add new Design Spec field names for this pattern.

**Page-count policy — explicit request beats a fixed page count.** When the request starts as Beautify (or any run whose profile fixes the page split), an explicit 「缩放总览」 request still activates this pattern: add P01 as a new page and re-cut the content into one-event pages, which may split a crowded source page or merge fragments of the same event. Keep all wording verbatim (Beautify's fidelity constraint stays), update §I `Page Count` and the §IX roster to the new count, and state the old → new page count to the user in the confirmation or plan message before any SVG is authored. Do not silently keep the source page split and then claim the pattern; do not slide the hub into the existing page count by dropping a source event. Without the explicit request, default Beautify keeps the original page count unchanged.

---

## 3. Content Page Craft

One-event pages share one template so the deck reads as a file, not a slide sampler.

| Element | Craft |
|---|---|
| Surface | Aged-paper or theme texture surface (§III), or an intentionally darker aged-map surface on selected pages; decorations small and consistent — stamp, small logo, credit script |
| Composition | Text column left, photo right on the same row (the source deck's working layout); the left column stacks kicker → title → body; a centered kicker above the title is the minimal variant |
| Year / date kicker | Short, bold, accent color (the source deck used red), above the title; ~22–26 px at 1280-wide |
| Title | 44–54 px, heavy weight, white text on a near-black highlight band sized to the text (two lines allowed in the source); the band is a highlight, never a full-width strip |
| Body | 18–20 px, at most three short lines, dark neutral on the paper surface; on a dark surface switch body to white and keep the title white-on-black too — a dark-gray body left on a dark surface is the failure the source deck corrected |
| Photo | The largest object, vertical composition in the right column; thick white border (8–12 px at 1280-wide, one width deck-wide) and one soft shadow; slight rotation `-3°..-6°` is allowed page by page |
| Hierarchy | Year small → title huge → body small → photo dominant; the dark band is the only high-contrast text surface |

A white-bordered photo is a framed picture: SVG draws the white frame, the shadow, and the placement; the bitmap supplies only the photograph. The frame keeps the page editable and lets the same framing scale down cleanly into hub cards.

Keep title and body inside the planned content area. If a title needs two lines, shorten the wording or reduce the type size; never let the band become a paragraph block. Body copy states the event, not the narration — the narration stays in notes.

---

## 4. Overview Page Craft

Build the hub as one full-bleed composition, back to front:

1. **Background** — the prepared derivative at full bleed (`x=0 y=0 width=canvas width height=canvas height`, or a `preserveAspectRatio="xMidYMid slice"` image covering the canvas). No white page edge may show. The source deck used a full-page cover picture with an artistic blur plus brightness about `-19%`; bake blur and dimming into one derivative with `image_treat.py` (for example `--blur 6 --brightness 0.81`) instead of authoring a picture effect the exporter cannot carry.
2. **Decoration layers** — user PNGs in depth order: torn paper, envelope as centerpiece, stamps, tape, wordmark. Keep their transparency; never flatten them into a re-drawn vector.
3. **Preview cards** — the navigation objects (§4.1), placed on and around the envelope.
4. **Hub title block** — display wordmark or two-line title, small subtitle, file/index label, and a credit decoration. Typed as editable text; place it in the quietest region, not on top of a card.

### 4.1 Preview cards (the zoom stand-ins)

Each card is an authored miniature of one target page, not a live thumbnail:

- Composition: white-framed photo (the target page's own photo, same crop) with a caption line under it — `MONTH DAY, YEAR · short event title`, 11–13 px, one line. When the page's title band is the identifying feature, include a slim dark band with the shortened title instead of duplicating body text.
- Size and placement: 13–19% of canvas width (170–245 px at 1280); 4–8 cards; stagger positions along the envelope and decorations rather than a neat grid; rotations `-6°..-12°` relative to the hub, with the top row following the envelope's edge instead of a level line; cards may overlap decoration edges but never overlap each other's clickable area.
- Background: no white page rectangle behind a card — the aged-paper surface or transparency shows through, equivalent to turning off 缩放定位背景 in PowerPoint.
- Shadow: shape-level external-offset shadow on the floating cards only; decoration layers stay flat; 2–3 elevation levels at most.
- Clickability: wrap the whole card group in one anchor, and give the card one contiguous hit area. Decorations in front of a card must stay behind it in z-order, or move aside.
- Consistency: card framing and border width follow §3; caption style is identical across cards.

The card is a designed object. It must stay legible at final size — if the replica would shrink text below readability, keep photo + year + short title and drop the rest.

---

## 5. Navigation Contract

| Page | Anchor target | Carrier |
|---|---|---|
| Hub | `#slide-N` (N = that card's content page) | Whole preview-card group |
| Hub | — | Decorations and title block carry no anchor |
| Content page | `#slide-01` (return to hub) | Whole return chip or one small decoration; never a text run hidden in body copy |

- Use ordinary objects; do not put navigation on a `trigger_shape` animation group (links are rejected there).
- The exported PPTX contains native slide-jump click actions; in slide-show view a card click jumps to its page and the return chip jumps back to the hub. Presenting is "click the part you want to talk about, return, choose the next part" — the video's 哪里想讲点哪里, 讲完返回总览, 再继续下一步 logic.
- A jump is a slide change, not a zoom animation. Leave the deck's normal page transitions subtle (fade or a short push) so a jump does not read as a glitch; do not claim a zoom transition.
- Targets are absolute 1-based page numbers. Any roster change shifts them; the revision round in [`generate-pptx.md`](../workflows/generate-pptx.md) already sweeps hyperlink targets.
- Anchor syntax, validation, and export lowering live in [`native-hyperlinks.md`](./native-hyperlinks.md); do not restate them here.

---

## 6. Executor Authoring Contract

- Read this reference and [`native-hyperlinks.md`](./native-hyperlinks.md) before P01 when §IX plans the pattern. Link lowering needs no export flag.
- Author content pages first, then the hub, so each card matches its final page. Keep numeric filenames in roster order; the hub may be drawn last even though it is `P01`.
- Frame, border, shadow, and rotation are SVG-owned; reuse one canonical soft shadow from [`executor-base.md`](./executor-base.md) §4 rather than inventing per-card values.
- Place the background derivative as the bottom image and confirm no white edge survives at any zoom level. Decorations are images with alpha; keep their natural edges.
- Every card's anchor and every return chip must correspond to the §IX `Hyperlinks` line. The final checker reports both sides, so fix plan or anchors before export rather than whiting out a chip.
- Keep the hub within a normal single-page SVG. No page contains another page's full content as a picture; that is the fake zoom this reference forbids.

---

## 7. Capability Boundary — native PowerPoint Slide Zoom

This pipeline does **not** generate PowerPoint Slide Zoom or Summary Zoom objects (`p:zoom`), and makes no attempt to synthesize their XML. The exported file is ordinary slides with native click hyperlinks.

| PowerPoint feature | In the exported PPTX |
|---|---|
| Slide-jump click navigation | Works — native `ppaction://hlinksldjump` actions on any card or chip |
| 缩放定位背景 (hide a zoom frame's white page background) | Not present; the authored cards simply have no white backdrop |
| 返回到缩放定位 (Return to Zoom, automatic return) | Not present; the authored return chip performs the same jump manually |
| Thumbnail refresh after editing a content page | Not present; authored previews are static by design — update the card when that page's identifying photo/title changes |
| Zoom-in / zoom-out motion during the jump | Not present; a jump is a slide change |

Never tell the user that Slide Zoom was generated, that thumbnails stay in sync, or that a checkbox exists in the delivered file. Report what is real: "overview card navigation is exported as native hyperlinks; native Slide Zoom can be added in PowerPoint in a few steps".

### 7.1 Manual upgrade path

Offer this as optional post-delivery manual work, not as part of the export:

1. Open the PPTX in desktop Microsoft PowerPoint.
2. In the slide thumbnail pane, Ctrl+click the content slides to select them together.
3. 插入 (Insert) → 缩放 (Zoom) → 幻灯片缩放 (Slide Zoom).
4. Drag the generated zoom frames over the authored preview cards and match size, rotation, and stacking.
5. In 缩放工具 (Zoom Tools), clear 缩放定位背景 for each frame to drop the white page backdrop; tick 返回到缩放定位 on frames that must return to the hub.
6. Multi-select the frames and add one shadow; delete or hide the authored cards beneath them if they show through.
7. Present: the frames are clickable in slide-show view, and editing a content page updates its thumbnail after reopening the file.

Menu paths and labels differ by PowerPoint version and platform; 缩放定位 may be missing in non-Microsoft or older editors such as WPS. State that caveat instead of promising parity. On PowerPoint for macOS the same controls appear as 插入 → 缩放定位 → 幻灯片缩放 and 缩放工具 exposes 返回到缩放定位, 缩放定位背景, and 持续时间 (the source demo used 01.00 s); duration changes only the zoom speed.

---

## 8. Degradation Modes

Choose the first mode the material supports and say which one was used:

1. **Full authored pattern** — user background and decorations present: hub + preview cards + hyperlink jumps, with the manual Slide Zoom upgrade offered separately (§7).
2. **Plain hub** — background supplied, decorations not: a clean full-bleed hub with typed cards on the theme surface; no fabricated textures, no fake envelope.
3. **Contents-page navigation** — no hub visual assets at all: an ordinary contents page whose rows carry the same jumps (see [`native-hyperlinks.md`](./native-hyperlinks.md)); explicitly not the 缩放总览 look.
4. **Original manual workflow** — the user wants only the original PowerPoint 缩放定位 workflow, or declines the hub assets: keep the deck as delivered (or as an ordinary Beautify result, preserving its page count) and offer the manual route (§7.1). A fidelity or fixed-page-count request is not a decline reason by itself; an explicit 「缩放总览」 request keeps the pattern and applies the §2 page-count policy.

Never degrade into a fake: one slide containing all pages as pictures, a static collage whose cards only look clickable, or a claimed zoom interaction that the file does not have.

---

## 9. Quick Generate Addendum

In Quick, this reference loads in the planning pass (it replaces nothing) and again before P01. There is no Design Spec, so the §IX plan-equality check is absent: keep the card-to-page map in the transient plan summary, verify every anchor still points inside the final roster, and report the mapping in the carrier receipt. Export uses the normal lockless final checker and `svg_to_pptx.py` flags; no extra flag exists for navigation.

---

## 10. Acceptance Checklist

- [ ] Hub is page 01, content pages each cover one event, roster matches §I/§IX (or the Quick transient roster).
- [ ] When the request began as Beautify or another fixed-page-count run, the old → new page count was stated to the user before authoring, and wording stayed verbatim.
- [ ] Hub background derivative is full-bleed, blurred and dimmed; no white page edge.
- [ ] User-supplied decorations only; no invented textures or envelopes.
- [ ] Photos and cards share one white-border width; cards are rotated, staggered, shadowed, and legible.
- [ ] Every card jumps to its page; every content page returns to `#slide-01`; no anchor on a trigger group.
- [ ] §IX `Hyperlinks` lines complete and equal to the anchors; final checker and export postflight pass.
- [ ] Delivered message states the capability boundary and the optional manual Slide Zoom upgrade.

---

## 11. Boundaries and Owners

- This reference owns the hub composition, card craft, navigation contract, and capability boundary. It does not own roster-contract confirmation (Strategist), anchor grammar (native-hyperlinks.md), image treatment (image-base.md), shadow values (executor-base.md), transitions (animations.md), or export commands (generate-pptx.md Step 7).
- Do not add a lock field, a schema field, a confirmation question, or a route/profile for this pattern. A user who asks for it in a fidelity or fixed-page-count context still gets the pattern under the §2 page-count policy, with the new count stated before authoring — not a silent, unchanged deck; only an asset refusal, a manual-only preference, or missing event material changes the outcome.
