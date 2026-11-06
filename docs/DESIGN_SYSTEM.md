# ROYALS INTELLIGENCE — DESIGN SYSTEM & VISUAL IDENTITY
**Design Standard:** Professional Elite Sports Analytics  
**Version:** 1.0.0 (Stage 0 Baseline)  

---

## 1. Brand Color Palette

The visual identity is anchored directly to the prestigious colors of the Rajasthan Royals franchise:

| Token Name | Hex Code | RGB | Role / Usage | Contrast Ratio (vs White) |
| :--- | :--- | :--- | :--- | :--- |
| **Royal Navy** | `#101C37` | `rgb(16, 28, 55)` | Primary background (dark), sidebar, headers, authoritative text. | 14.8:1 (AAA) |
| **Royals Pink** | `#E91E8F` | `rgb(233, 30, 143)` | Primary accent, call-to-actions, active indicators, highlights. | 4.6:1 (AA) |
| **Royals Gold** | `#D6B56D` | `rgb(214, 181, 109)` | Auxiliary accent, trophy/auction highlights, premium badges. | 1.8:1 (Used on Navy: 7.9:1 AAA) |
| **Light Grey** | `#F4F6FA` | `rgb(244, 246, 250)` | Canvas background (light mode), card borders, neutral fills. | 1.1:1 (Background) |
| **Pure White** | `#FFFFFF` | `rgb(255, 255, 255)` | Card backgrounds, high-contrast text on dark surfaces. | 1.0:1 |
| **Slate Dark** | `#0B1220` | `rgb(11, 18, 32)` | Deep dark mode background canvas. | 17.2:1 (AAA) |
| **Status Green** | `#10B981` | `rgb(16, 185, 129)` | System healthy, positive delta, high sample confidence. | 3.1:1 |
| **Status Amber** | `#F59E0B` | `rgb(245, 158, 11)` | Pending integration, moderate sample, cautionary warning. | 2.1:1 |
| **Status Red** | `#EF4444` | `rgb(239, 68, 68)` | System error, high risk, negative delta. | 4.0:1 |

---

## 2. Typography Hierarchy

* **Primary Font Family:** Inter / System UI Sans-serif (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).
* **Monospace Font Family:** JetBrains Mono / SFMono / Fira Code (Used for sample sizes, timestamps, IDs, code, and financial valuations).

### Scale:
- **Display 1:** `32px / 2.0rem`, Bold (700) — Platform title, major module headers.
- **Heading 1:** `24px / 1.5rem`, Semi-bold (600) — Section titles, modal titles.
- **Heading 2:** `18px / 1.125rem`, Medium (500) — Card titles, table headers.
- **Body Large:** `16px / 1.0rem`, Regular (400) — Primary narrative and briefing copy.
- **Body Regular:** `14px / 0.875rem`, Regular (400) — Table cells, standard form inputs.
- **Caption / Meta:** `12px / 0.75rem`, Medium (500) — Timestamp, sample size badges, data confidence indicators.

---

## 3. UI Component Architecture

1. **Application Shell:**
   - **Fixed Sidebar:** Deep Royal Navy (`#101C37`) background with glowing Royals Pink (`#E91E8F`) active route pills and muted gold accents.
   - **Header Bar:** Crisp border-b divider with breadcrumb navigation, live API health pill, environment indicator, and quick actions.
   - **Main Content Viewport:** Fluid, responsive grid container with comfortable padding (`px-6 py-6`).
2. **Card Containers:**
   - Rounded borders (`rounded-xl` / `12px`).
   - Subtle border color (`border border-slate-200 dark:border-slate-800`).
   - Elevated cards carry faint navy shadows.
3. **Empty States & Data Pending Patterns:**
   - Under Stage 0 and throughout early development, modules lacking ingestion pipelines MUST display honest empty states.
   - Banner pattern: Pulsing amber indicator, "Stage 0 Initialized — Data Integration Pending", accompanied by an architectural blueprint summary of what will populate the view in future stages.

---

## 4. Accessibility & Contrast Guidelines

- All text on dark navy surfaces must achieve at least WCAG 2.1 AA (4.5:1) for normal text and AAA (7:1) for prominent headings.
- Interactive buttons and links must provide visible focus rings (`focus:ring-2 focus:ring-[#E91E8F]`).
- Screen reader ARIA tags must be present on sidebar collapse controls, navigation items, and health status indicators.
