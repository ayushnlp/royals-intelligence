# ROYALS INTELLIGENCE — ST5-07 API INTEGRATION MATRIX
**Tactical Analytics REST API Endpoints vs Frontend UI Components**

---

## 1. Overview

This matrix establishes the comprehensive binding between the backend REST API endpoints exposed under `/api/v1/analytics/tactical/` and the frontend presentation components implemented in `frontend/src/app/tactical/page.tsx` and `frontend/src/lib/api.ts`.

All data displayed in the Tactical Intelligence dashboard is derived exclusively from the official Rajasthan Royals Round 1 data pack.

---

## 2. API Endpoint to Frontend Component Matrix

| # | Endpoint URL | Method | Query Parameters | Response Model | Frontend API Client Method | Frontend UI Target (Module) | Fallback / Error Handling |
| :-: | :--- | :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | `/api/v1/analytics/tactical/summary` | `GET` | *None* | `TacticalDatasetSummaryResponse` | `fetchTacticalSummary()` | **Module A:** Top Telemetry Ribbon (Total balls, legal balls, matches, runs off bat, wickets, speed records) | Returns `null`, UI renders verified empirical fallback constants (200,999 balls, 867 matches) |
| **2** | `/api/v1/analytics/tactical/phases` | `GET` | `striker_id?: int`<br>`bowler_id?: int`<br>`phase?: str` | `TacticalPhaseResponse` | `fetchTacticalPhases(params)` | **Module B:** Match Phase Architecture Cards (Powerplay, Middle, Death splits, SR, Economy, Dot %, Boundary %, Balls/Wkt) | Displays tournament baseline phase figures if player ID is unspecified or offline |
| **3** | `/api/v1/analytics/tactical/strokes` | `GET` | `striker_id?: int`<br>`stroke?: str`<br>`min_balls: int` (default 50) | `TacticalStrokesResponse` | `fetchTacticalStrokes(params)` | **Module C:** 30 Batting Strokes Efficiency Table, Runs/Shot, Dismissal Risk %, Boundary %, Profile Badging | Empty array returned; table shows empty state with filter reset prompt |
| **4** | `/api/v1/analytics/tactical/handedness` | `GET` | `batting_type?: str`<br>`pace_or_spin?: str`<br>`striker_id?: int`<br>`bowler_id?: int` | `HandednessMatrixResponse` | `fetchTacticalHandedness(params)` | **Module D:** 4-Way Cross-Split Matrix Cards (RHB/LHB vs Pace/Spin) | Returns `null`; matrix displays default 4-cell layout |
| **5** | `/api/v1/analytics/tactical/variations` | `GET` | `bowler_id?: int`<br>`delivery_style?: str`<br>`min_balls: int` (default 50) | `DeliveryStylesResponse` | `fetchTacticalVariations(params)` | **Module E:** 34 Bowling Variations Table, Economy Rate, Bowling Avg, Dot Ball %, Discipline Badges | Displays empty table if threshold exceeds sample size |
| **6** | `/api/v1/analytics/tactical/speed-profiles` | `GET` | `bowler_id?: int`<br>`min_balls: int` (default 30)<br>`top_n: int` (default 10) | `SpeedProfileResponse` | `fetchTacticalSpeedProfiles(params)` | **Module F:** Speed Telemetry Distribution Brackets, Top 10 Fastest Bowlers, Sensor Quality Notice | Renders 4 speed brackets and sensor safeguard disclaimer card |
| **7** | `/api/v1/analytics/tactical/players/{player_id}` | `GET` | `player_id: int` (Path parameter) | `PlayerTacticalProfileResponse` | `fetchPlayerTacticalProfile(playerId)` | **Module G:** Multi-Dimensional Player Tactical Dossier (Batting phase splits, top strokes, bowling variations, speed) | 404 handled gracefully; dossier retains previously loaded player or displays selection guide |
| **8** | `/api/v1/analytics/tactical/death-overs` | `GET` | `discipline: str` (`all`, `batting`, `bowling`)<br>`min_balls: int` (default 100)<br>`limit: int` (default 10) | `DeathOversRankingResponse` | `fetchTacticalDeathOvers(params)` | **Module H:** Death Overs (16–20) Dual Leaderboards (Finishers by SR & Containment Bowlers by Economy) | Displays dual or single leaderboard depending on discipline filter |
| **9** | `/api/v1/analytics/tactical/matchups` | `GET` | `striker_id: int` (Required)<br>`bowler_id: int` (Required) | `HeadToHeadMatchupResponse` | `fetchTacticalMatchup(strikerId, bowlerId)` | **Module I:** Direct Head-to-Head Micro-Battle Card (Runs, Balls, Dismissals, SR, Dots, Automated Verdict) | Returns valid 0-ball response object with "Zero Direct Deliveries Recorded" verdict |
| **10** | `/api/v1/analytics/tactical/players` | `GET` | `query: str` (Search substring)<br>`limit: int` (default 25) | `List[PlayerLookupItem]` | `fetchTacticalPlayers(query, limit)` | **Modules G & I:** Interactive Player Search Autocomplete Dropdown & Quick Select Pills | Returns empty list `[]` if query is empty or no match is found |

---

## 3. Data Contracts & Schema Details

### 3.1. `TacticalDatasetSummaryResponse`
```typescript
export interface TacticalDatasetSummaryResponse {
  total_deliveries: number;              // 200,999
  legal_deliveries: number;              // 192,709
  total_matches_with_deliveries: number; // 867
  total_unique_strikers: number;         // 618
  total_unique_bowlers: number;          // 460
  total_runs_off_bat: number;            // 260,209
  total_wickets_fallen: number;          // 11,460
  total_bowler_wickets: number;          // 10,489
  overall_run_rate_per_6_balls: number;  // 8.10
  valid_radar_speed_records: number;     // 123,113
  data_provenance: string;               // "Official Rajasthan Royals Round 1 Data Pack"
  generated_at: string;
}
```

### 3.2. `TacticalPhaseResponse` & `TacticalPhaseSplitItem`
```typescript
export interface TacticalPhaseSplitItem {
  phase: string;                         // "Powerplay" | "Middle" | "Death"
  total_balls: number;
  legal_balls: number;
  runs: number;
  wickets: number;
  strike_rate?: number | null;
  economy_rate?: number | null;
  average?: number | null;
  dot_ball_percentage: number;
  boundary_percentage: number;
  balls_per_wicket?: number | null;
}
```

### 3.3. `SpeedProfileResponse` & Sensor Safeguard
```typescript
export interface SpeedProfileResponse {
  bowler_id?: number | null;
  bowler_name?: string | null;
  total_deliveries?: number | null;
  overall_valid_speed_deliveries?: number | null; // 123,113
  valid_speed_deliveries?: number | null;
  speed_coverage_pct: number;                    // 61.3%
  mean_speed_kmh?: number | null;
  median_speed_kmh?: number | null;
  min_speed_kmh?: number | null;
  max_speed_kmh?: number | null;
  std_speed_kmh?: number | null;
  speed_brackets?: SpeedBrackets | null;         // slow, medium, fast_medium, express
  top_fastest_bowlers?: FastestBowlerItem[] | null;
  sensor_safeguards_applied: boolean;            // true
  data_quality_note: string;
  data_provenance: string;
}
```

### 3.4. `HeadToHeadMatchupResponse`
```typescript
export interface HeadToHeadMatchupResponse {
  striker_id: number;
  striker_name: string;
  bowler_id: number;
  bowler_name: string;
  balls_faced: number;
  legal_balls: number;
  runs_scored: number;
  dismissals: number;
  fours: number;
  sixes: number;
  dot_balls: number;
  strike_rate: number;
  dot_ball_pct: number;
  boundary_pct: number;
  data_provenance: string;
}
```

---

## 4. Client Request Strategy & Caching Policy

1. **No-Store Dynamic Fetch:**  
   Every client fetch call in `frontend/src/lib/api.ts` specifies `{ cache: "no-store" }` to ensure fresh tactical analysis when toggling filters, sliders, or searching players.
2. **Parallel Promise Resolution:**  
   On initial mount of the `/tactical` page, the aggregate summary, phase baseline, stroke rankings, handedness matrix, variations, speed profiles, and death overs leaderboards are requested concurrently via `Promise.all`:
   ```typescript
   const [sumRes, phaseRes, strokeRes, handRes, varRes, spdRes, deathRes] = await Promise.all([
     fetchTacticalSummary(),
     fetchTacticalPhases(),
     fetchTacticalStrokes({ min_balls: strokeMinBalls }),
     fetchTacticalHandedness(),
     fetchTacticalVariations({ min_balls: variationMinBalls }),
     fetchTacticalSpeedProfiles({ min_balls: 30, top_n: 10 }),
     fetchTacticalDeathOvers({ discipline: deathDiscipline, min_balls: deathMinBalls, limit: 10 }),
   ]);
   ```
3. **Targeted Sub-query Debouncing / Selective Re-fetch:**  
   - Modifying `strokeMinBalls` triggers only `fetchTacticalStrokes()`.
   - Modifying `variationMinBalls` triggers only `fetchTacticalVariations()`.
   - Modifying `deathDiscipline` or `deathMinBalls` triggers only `fetchTacticalDeathOvers()`.
   - Selecting a preset matchup or typing player names triggers targeted single-player / pair queries.

---

## 5. Verification & Compliance Confirmation

- All 10 REST endpoints were confirmed operational and verified against FastAPI OpenAPI schema definitions.
- All response structures deserialize cleanly into TypeScript interfaces without any type coercion or missing field warnings.
