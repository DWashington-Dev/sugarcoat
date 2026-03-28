# SugarCoat Frontend Design Spec
**Date:** 2026-03-26
**Scope:** Single-file frontend (`index.html`) for the SugarCoat T1D glucose companion app
**Approach:** Option B — Single HTML file, JS-driven state management

---

## Overview

SugarCoat's frontend is a single `index.html` file served by Flask at `/`. All states — landing, dashboard, analysis — live in this one file. JavaScript controls which state is visible by hiding and showing sections based on API call results. No page reloads. No routing library needed.

---

## Color Palette & Branding

- **Primary blue:** `#186fcc`
- **Background:** Near-black (e.g. `#0a0a0f`)
- **Text:** White (`#ffffff`) and light gray (`#c8d0db`)
- **Accent / in-range:** Teal or soft green (e.g. `#2dd4bf`)
- **High / above range:** Amber or orange (e.g. `#f59e0b`)
- **Low / below range:** Red (e.g. `#ef4444`)
- **Logo / wordmark:** Plain text — `SugarCoat.` — capital C, period included. No icon.

---

## Tech Stack (all CDN, no installs)

- **Tailwind CSS** — utility styling
- **Chart.js** — interactive glucose line chart
- **marked.js** — renders Claude's markdown analysis output as HTML

No build step. No npm. Flask serves the single HTML file.

---

## State Machine

```
Landing State
    ↓ (user clicks "Connect with Dexcom")
/login → Dexcom OAuth → /callback
    ↓ (token stored in Flask session)
Dashboard State
    ↓ (user opens bubble picker, makes selections, clicks Analyze)
Processing State  ← /analyze POST running
    ↓ (response received)
Results State  (appended below dashboard, user can scroll)
```

JS determines initial state on page load by calling `/stats`. Success → show Dashboard. Failure (401 / empty) → show Landing.

---

## Section 1 — Landing State

### Layout
Full-screen dark section. Centered content vertically and horizontally.

### Content
- `SugarCoat.` wordmark top-left (text, not an image)
- Headline: short, direct — e.g. "Your glucose data, finally in plain English"
- 2–3 supporting lines explaining what SugarCoat does and who it's for (T1D users with Dexcom CGMs)
- Single CTA button: "Connect with Dexcom" → links to `/login`
- Placeholder slot reserved for future hero animation / video loop (Apple-style ambient video)

### Behavior
Hidden immediately when `/stats` returns successfully on page load.

---

## Section 2 — Dashboard State

### Top Stat Strip
Three stat cards in a row, full width, sequentially fade in one at a time on load:

| Position | Stat | Source |
|----------|------|--------|
| Left | Average Glucose (mg/dL) | `/stats` → `avg` |
| Center | Star Rating (★ 1–5) | Calculated client-side from A1C estimate |
| Right | Recommended Time in Range (%) | `/stats` → `rec_tir` |

**A1C estimate formula** (already in codebase): `((avg + 46.7) / 28.7)`
**Star rating logic** (already in codebase): based on A1C thresholds

Animation: each card fades in with a 200ms delay stagger (left → center → right).

### Main Body — Two-Column Grid

**Left / Main Column (≈65% width):**
1. Interactive glucose line chart (Chart.js)
2. Bubble picker trigger button ("Get My Analysis")
3. Processing state (shown during `/analyze` call)
4. Analysis results (Claude's response, rendered via marked.js)

**Right Sidebar (≈35% width):**
- **Highs panel:** Top 3 highest individual readings, timestamp, value, % time above range
- **Lows panel:** Bottom 3 lowest individual readings, timestamp, value, % time below range
- Data source: `/readings` — sorted and sliced client-side in JS. No new backend routes needed.

---

## Section 3 — Glucose Chart

### Library
Chart.js (CDN). Line chart type.

### Data Source
`/readings` — fetched on dashboard load, parsed into labels (timestamps) and values.

### Visual Encoding
- **In-range points** (70–160 mg/dL): Teal / accent color
- **Above-range points** (>160): Amber
- **Below-range points** (<70): Red
- Smooth curved line connecting all points

### Interactivity (built into Chart.js, no custom code needed)
- Hover over any point → tooltip shows exact glucose value and timestamp
- Point lifts / highlights on hover
- Smooth load animation

---

## Section 4 — Bubble Picker

### Concept
"Coca-Cola freestyle machine" interaction pattern. Four main category bubbles displayed in a panel. Tapping a category expands a ring of sub-option bubbles around it. Selecting a sub-option collapses the ring and marks the category as chosen. Once all four categories are selected, the "Analyze" button activates.

### Categories and Sub-options

**Food (maps to `diet` field in `/analyze`)**
- Low-carb / Keto
- Balanced / Moderate
- High-carb
- Processed / Fast food

**Activity (maps to `activity` field)**
- Sedentary
- Light (walks, daily movement)
- Moderate (gym, sports)
- Intense / Athletic

**CGM Engagement (maps to `cgm` field)**
- Checking constantly
- Checking a few times a day
- Rarely checking
- Just started using CGM

**Dosing (maps to `dosing` field)**
- Very consistent
- Sometimes miss doses
- Often adjusting / correcting
- Not on insulin

### Behavior
- Picker appears as an overlay panel (not a blocking modal — page is still visible behind it)
- Selected categories show a visual checkmark / filled state
- "Analyze" button is disabled until all 4 are selected
- Selections stored in a plain JS object: `{ diet: '', activity: '', cgm: '', dosing: '' }`

---

## Section 5 — Processing State

### Trigger
Shown immediately when user clicks "Analyze" and the `/analyze` POST is sent.

### Visual
VirusTotal-inspired: a pulsing status line cycling through on-brand copy:

```
Pulling your readings...
Running the numbers...
Sugar coating your results...
Almost there...
```

Each line fades in/out on a short interval. A subtle animated indicator (e.g. blinking dot or progress bar) accompanies the text.

### Behavior
Hidden as soon as `/analyze` returns a response (success or error).

---

## Section 6 — Analysis Results

### Source
`/analyze` POST returns `{ analysis: "<markdown string>" }`

### Rendering
marked.js parses the markdown string and inserts it as HTML into a styled results card. The card appears below the bubble picker section.

### Claude's output format (from existing system prompt)
- "Uncoated" summary paragraph
- Sugar Rushes section (causes of highs)
- Sugar Crashes section (causes of lows)
- Off the Charts section (outliers / unusual patterns)
- Next Steps (2–3 actionable suggestions)

---

## Future Enhancements (out of scope for this build)

- Hero animation / ambient video loop on landing page
- PDF upload via pdfplumber for users without active CGM
- Medical context / knowledge base injected into Claude system prompt
- Date range selector for the glucose chart
- Mobile-responsive layout pass

---

## Backend Changes Required

None. All data needs are covered by existing routes:
- `/stats` — stat strip (avg, rec_tir, A1C/stars)
- `/readings` — chart data + sidebar highs/lows (sorted client-side)
- `/analyze` — bubble picker POST
- `/login` — landing page CTA

---

## Files Affected

| File | Change |
|------|--------|
| `learninglabs/templates/index.html` | Full rewrite — this is the deliverable |
| `learninglabs/app.py` | No changes required |

