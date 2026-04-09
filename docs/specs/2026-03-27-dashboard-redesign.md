# SugarCoat Dashboard Redesign
**Date:** 2026-03-27

## Overview
Full rebuild of `learninglabs/templates/index.html`. Same Flask backend, same JS logic — new layout, color system, and interaction patterns.

## Layout — 3-Zone Structure
- **Left zone:** Invisible hover trigger strip. On cursor enter → peek panel slides in with: Logout, Reset Data, New Analysis. Slides back out on cursor leave.
- **Center:** Main dashboard content (stat strip + charts + analysis flow). Max-width expanded to fill 4K properly.
- **Right zone:** Persistent sidebar, always visible, styled like an app panel. Contains time-of-day highs pattern card + time-of-day lows pattern card.

## Color System
| Token | Value | Use |
|---|---|---|
| `--bg` | `#ffffff` | Page background |
| `--surface` | `rgba(255,255,255,0.65)` | Frosted glass cards |
| `--blue` | `#0ea5e9` | Primary accent, charts, buttons |
| `--blue-dark` | `#0284c7` | Hover states |
| `--blue-light` | `#e0f2fe` | Tints, selected states |
| `--high` | `#f43f5e` | Above-range readings (replaces red) |
| `--high-light` | `#fff1f2` | High card backgrounds |
| `--low` | `#8b5cf6` | Below-range readings (replaces orange) |
| `--low-light` | `#f5f3ff` | Low card backgrounds |
| `--inrange` | `#10b981` | In-range / TIR good |
| `--text` | `#0f172a` | Primary text |
| `--text-secondary` | `#64748b` | Labels, subtitles |

## Right Sidebar — Pattern Cards
Replace the current "top 3 readings" list with time-of-day pattern analysis computed from the readings array:
- Group readings by hour bucket (e.g. 6am–9am, 9am–12pm, etc.)
- **Highs card:** Show the 2–3 time windows with the highest avg glucose. Label: "Your spikes tend to happen around [time]."
- **Lows card:** Show the 2–3 time windows with lowest avg glucose. Label: "Watch out around [time] — consider eating before."
- Keep rose/violet color coding consistent with the main palette.

## Left Peek Panel
- Fixed left edge, full height, ~16px wide invisible trigger zone
- On hover: panel slides in (200ms ease), width ~220px, frosted glass surface
- Contents: sugarCoat. wordmark at top, then action buttons: New Analysis, Reset Data, Logout
- On mouse leave: slides back out

## Charts
- Keep all 3 Chart.js charts (overview + high days + low days)
- Update colors: overview line → `#0ea5e9`, high days → `#f43f5e`, low days → `#8b5cf6`
- **Tooltip upgrade:** Custom HTML tooltip (not Chart.js default) with frosted glass style, fade-in animation (~150ms), shows glucose value + formatted timestamp together
- Remove point markers (keep `pointRadius: 0`)

## Stat Strip
3 cards across the top: Avg Glucose, Your Score (A1C + stars), Time in Range. Keep the same data, update to new color tokens and white background.

## Aesthetic
- White background, no warm tones
- `backdrop-filter: blur(12px)` on all cards
- Subtle borders: `1px solid rgba(148,163,184,0.15)`
- Shadows: very light, `0 1px 3px rgba(15,23,42,0.06)`
- Fonts: Anonymous Pro (wordmark), Outfit (everything else) — unchanged
