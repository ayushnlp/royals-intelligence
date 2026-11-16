# ROYALS INTELLIGENCE — ROUND 1 FINAL GIT STAGING PLAN (CORRECTED)

**Project:** ROYALS INTELLIGENCE  
**Scope:** SupeRR Selector Season 2 — Round 1  
**Milestone:** Pre-Commit Staging Audit & Controlled Release Plan (Corrected)  
**Date:** 2026-11-16  
**Auditor:** Senior Full-Stack Engineer, Software Architect, QA Lead & Technical Auditor  
**Controlling Git Branch:** `main`  
**Current HEAD Commit:** `6005022f780368d1ebd547c804b3318e9d8924fd`  
**Current Working Tree State:** Unstaged modifications and untracked submission assets present  
**Final Staging Verdict:** **READY FOR USER APPROVAL**

---

## 1. Executive Summary & Audit State

This document represents the **corrected final Git staging plan** incorporating strict review guidelines:
1. Inspection of all 11 deleted `.gitkeep` placeholders with explicit recommendations on restoration vs deletion.
2. Explicit scoping of roadmaps: `docs/REVISED_14_STAGE_ROADMAP.md` is classified as broader platform scope (Stages 6–13) and **excluded** from the Round 1 submission commit.
3. Rigorous classification of all audit reports into **FINAL / AUTHORITATIVE**, **SUPERSEDED**, **PRELIMINARY**, and **INTERNAL**, eliminating redundant root duplicates.
4. Strict enforcement of the raw data policy: all 7 source-pack files remain ignored by Git; zero 41 MB CSV blobs are staged.
5. Clean, granular three-commit architecture strictly separating Application Code, Official Submission Deliverables, and Authoritative Quality Audits.

---

## 2. Analysis of the 11 Deleted `.gitkeep` Placeholders

During previous working tree cleanup, 11 directory placeholder files were deleted. None of these 11 directories exist on disk today:

| Exact Path | Directory Purpose | Legacy Role | Official Round 1 Role | Auditor Recommendation |
|---|---|---|---|---|
| `data/external/venues/.gitkeep` | External venue data | Stage 4 Open-Meteo cache | Not used in R1 | **Restore** (`git checkout`) |
| `data/external/weather/.gitkeep` | External weather data | Stage 4 weather telemetry | Not used in R1 | **Restore** (`git checkout`) |
| `data/metadata/validation/.gitkeep` | Schema validation logs | Stage 2 metadata | Superseded by `data/validation/` | **Restore** (`git checkout`) |
| `data/raw/ball_by_ball/.gitkeep` | Legacy delivery feed | Stage 1 scraper output | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/domestic/.gitkeep` | Domestic match feed | Stage 3 match ingestion | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/fixtures/.gitkeep` | Fixture schedules | Stage 1 schedule feed | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/players/.gitkeep` | Player registry | Stage 1 player profile feed | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/scorecards/.gitkeep` | Official scorecards | Stage 1 scorecard feed | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/telemetry/.gitkeep` | Hawkeye/radar telemetry | Stage 1 telemetry feed | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/venues/.gitkeep` | Venue specifications | Stage 4 venue profiles | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |
| `data/raw/weather/.gitkeep` | Weather observations | Stage 4 hourly weather | Replaced by `data/raw/rajasthan_royals/` | **Restore** (`git checkout`) |

### Recommendation on Placeholders:
- **Recommended Action:** **RESTORE ALL 11 PLACEHOLDERS** using `git checkout -- data/external/... data/metadata/... data/raw/...`.
- **Reasoning:** Restoring these 0-byte placeholders costs zero repository overhead, maintains 100% structural compatibility with earlier Stage 1–4 ingestion modules (`backend/app/core/config.py`), and prevents unnecessary deletion noise in the submission commit diff.
- *Status:* In accordance with strict restrictions, **no files have been restored or deleted**.

---

## 3. Roadmap Scope & Policy

### Evaluation of `docs/REVISED_14_STAGE_ROADMAP.md`
- **Contents:** Details long-term architecture for Stages 6 through 13 (Player vs Player Matchups, Playing XI ILP Optimizer, Opposition Scouting, Auction Valuation, Markov Chain Simulation).
- **Round 1 Alignment:** The official Round 1 challenge is strictly confined to Top 10 Batters, Top 10 Bowlers, and dynamic pressure methodology. Stages 6–13 are explicitly out of scope for Round 1 submission.
- **Decision:** **EXCLUDE** `docs/REVISED_14_STAGE_ROADMAP.md` from the official Round 1 submission commit. The file is preserved locally on disk for subsequent competition stages.
- **Included Roadmap:** `docs/DEVELOPMENT_ROADMAP.md` (modified) is included because it accurately anchors completed Stages 0–4 and official Round 1 Pressure Analytics (`6005022`).

---

## 4. Audit Report Authority Classification

Every audit document and report in the repository has been evaluated and classified into one of four authority tiers:

### Tier 1: FINAL / AUTHORITATIVE DELIVERABLES (To Be Staged)
These documents represent authoritative, peer-reviewed, and verified submission deliverables:

1. **`ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` (Root):** Master Unstop competition deliverable (612 lines) detailing the five-stage methodology, Top 10 batters, Top 10 bowlers, and 20 candidate dossiers.
2. **`ROUND1_SUBMISSION_READINESS_AUDIT.md` (Root):** Final ST5-10 submission readiness audit certifying 303/303 passing tests, cryptographic artifact hashes, and deliverable completeness.
3. **`ST5_09_FINAL_BLOCKER_VERIFICATION.md` (Root):** Formal resolution of the Conservative PRI formula (`1.0 * SE`, not `1.96 * SE`) and raw storage idempotency verification.
4. **`ST5_09_FINAL_INDEPENDENT_ACCEPTANCE_AUDIT.md` (Root):** Comprehensive post-hotfix audit report verifying zero JSX errors, Next.js build success, and route availability.
5. **`ROUND1_GIT_STAGING_PLAN.md` (Root):** This controlled staging plan.
6. **`DATA_GOVERNANCE.md` (Root):** Official data pack governance policy, access boundaries, and lineage rules.
7. **`data/validation/DATA_QUALITY_AND_INTEGRITY_REPORT.md`:** Data profiling report validating 200,999 deliveries, 883 matches, 141 tournaments.
8. **`reports/DATASET_CRICKET_INTELLIGENCE_FINDINGS.md`:** Tactical findings and stroke/delivery variation analysis.
9. **`round1_pressure/reports/R1_SUBMISSION_02_BOWLING_RANKING_INTEGRITY_AUDIT.md`:** Mathematical proof of bowling sign convention and Jasprit Bumrah #1 ranking.
10. **`round1_pressure/reports/data_quality_report.md`**, **`pressure_detection_report.md`**, **`r1_05_2_validation_closure_report.md`:** Tracked reports reflecting test execution timestamps.

### Tier 2: REDUNDANT ROOT DUPLICATES (To Be EXCLUDED)
The following 9 untracked files in the repository root are **byte-for-byte identical duplicates** of files already tracked in `round1_pressure/reports/`:
- `r1_06_1_classification_audit.md` (Duplicate of `round1_pressure/reports/r1_06_1_classification_audit.md`)
- `r1_06_1_probability_audit.md` (Duplicate of `round1_pressure/reports/r1_06_1_probability_audit.md`)
- `r1_06_1_recommendations.md` (Duplicate of `round1_pressure/reports/r1_06_1_recommendations.md`)
- `r1_06_2_1_classification_consistency_audit.md` (Duplicate of `round1_pressure/reports/r1_06_2_1_...`)
- `r1_06_2_1_population_reconciliation.md` (Duplicate of `round1_pressure/reports/r1_06_2_1_...`)
- `r1_06_2_1_recommendations.md` (Duplicate of `round1_pressure/reports/r1_06_2_1_...`)
- `r1_06_2_2_remediation_report.md` (Duplicate of `round1_pressure/reports/r1_06_2_2_...`)
- `r1_06_2_3_reconciliation_report.md` (Duplicate of `round1_pressure/reports/r1_06_2_3_...`)
- `r1_06_2_remediation_report.md` (Duplicate of `round1_pressure/reports/r1_06_2_...`)
*Action:* **EXCLUDE from staging**. They remain safely tracked in `round1_pressure/reports/`.

### Tier 3: SUPERSEDED / INTERMEDIATE AUDITS (To Be EXCLUDED)
These documents represent intermediate milestones or preliminary findings superseded by later authoritative audits:
- `round1_pressure/reports/R1_SUBMISSION_READINESS_AUDIT.md`: Preliminary audit conducted before frontend integration; superseded by root `ROUND1_SUBMISSION_READINESS_AUDIT.md`.
- `FRONTEND_INTEGRATION_AUDIT.md`: Pre-integration frontend audit; superseded by ST5-09 and ST5-10 audits.
- `FRONTEND_IMPLEMENTATION_ROADMAP.md`: Preliminary UI roadmap; superseded by actual implementation.
- `PROJECT_STATUS_AND_PROGRESS_AUDIT.md`: Intermediate status audit; superseded by ST5-10 readiness audit.
- `ST5_07_API_INTEGRATION_MATRIX.md`, `ST5_07_FRONTEND_IMPLEMENTATION_REPORT.md`, `ST5_07_TEST_REPORT.md`: Intermediate ST5-07 records; superseded by ST5-09 and ST5-10.
*Action:* **EXCLUDE from staging**. Preserved locally on disk for historical audit trails.

### Tier 4: INTERNAL RESEARCH & ARCHIVES (To Be EXCLUDED)
- `round1_pressure/reports/reliability_framework_architecture_audit_pre_authorization.md`: Internal pre-auth research.
- `docs/DEVELOPMENT_ROADMAP_ARCHIVE_PRE_DATASET.md`: Pre-dataset historical archive.
- `docs/PRIORITIZED_IMPLEMENTATION_BACKLOG.md`: Internal sprint backlog.
- `docs/DATASET_FEATURE_COMPATIBILITY_MATRIX.md`, `docs/DATASET_INVENTORY_AND_PROFILING_REPORT.md`: Internal exploratory profiling.
*Action:* **EXCLUDE from staging**.

---

## 5. Raw Data Policy & Judge Reproduction Guidance

1. **Strict Git Exclusion of Raw Data:**
   - All 7 files in `data/raw/rajasthan_royals/round_1_data_pack/` (`ball_by_ball.csv` [41 MB], `matches.csv`, etc.) remain **strictly ignored** by `.gitignore` (`data/raw/**/*`).
   - Zero raw CSV files will be force-added to Git.
   - Only `data/raw/rajasthan_royals/.gitkeep` and `data/processed/rajasthan_royals/.gitkeep` are tracked to establish directory structure.
2. **Judge Placement Documentation:**
   - Section 1 of [DATA_GOVERNANCE.md](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/DATA_GOVERNANCE.md) and Section 10 of [ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md) provide explicit dataset placement instructions:
     - Place the seven official CSV files into `data/raw/rajasthan_royals/round_1_data_pack/`.
     - Verify SHA-256 hashes against the published cryptographic baseline table.
     - Execute `pytest backend/tests/` and `pytest round1_pressure/tests/` to reproduce all findings deterministically.

---

## 6. Corrected Three-Commit Staging Architecture

### Commit 1: Core Platform Integration & UI (Application Code)
*Focus: Production Next.js 15 frontend, FastAPI backend, analytics engines, tests, and configuration.*

**Exact Inclusion Paths (22 items):**
- `backend/app/acquisition/storage/raw_storage.py`
- `backend/app/analytics/__init__.py`
- `backend/app/analytics/dataset_cricket_intelligence.py`
- `backend/app/analytics/pressure_intelligence.py`
- `backend/app/api/v1/router.py`
- `backend/app/api/v1/endpoints/pressure.py`
- `backend/app/api/v1/endpoints/tactical.py`
- `backend/app/schemas/pressure.py`
- `backend/app/schemas/tactical.py`
- `backend/tests/test_dataset_cricket_intelligence.py`
- `backend/tests/test_pressure_api.py`
- `backend/tests/test_tactical_api.py`
- `frontend/src/app/layout.tsx`
- `frontend/src/app/page.tsx`
- `frontend/src/app/not-found.tsx`
- `frontend/src/app/pressure/`
- `frontend/src/app/tactical/`
- `frontend/src/components/layout/Header.tsx`
- `frontend/src/components/layout/Sidebar.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/types/index.ts`
- `.gitignore`

**Proposed Commit Message:**
```text
feat(platform): integrate Round 1 Pressure Analytics and Stage 5 Tactical Intelligence

- Implement read-only REST endpoints under /api/v1/analytics/pressure/ and /tactical/
- Deliver Next.js 15 dashboards for /pressure (Flagship Round 1) and /tactical
- Add Conservative PRI (1-SE lower bound) leaderboards and 20 candidate dossiers
- Resolve JSX LaTeX syntax errors on / and restore Tailwind layout styling
- Ensure raw storage content-based idempotency across timestamp boundaries
- Add 3 automated test suites covering pressure, tactical, and dataset analytics
```

---

### Commit 2: Official Submission Deliverables & Documentation
*Focus: Master Unstop submission report, data governance, and rebaselined architecture.*

**Exact Inclusion Paths (7 items):**
- `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md`
- `DATA_GOVERNANCE.md`
- `DEVELOPMENT_PRIORITIES.md`
- `PROJECT_ARCHITECTURE.md`
- `PROJECT_ROADMAP.md`
- `PROJECT_STATUS.md`
- `docs/DEVELOPMENT_ROADMAP.md`

**Proposed Commit Message:**
```text
docs(submission): add official Round 1 methodology report and data governance

- Add master Unstop competition report (ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md)
- Detail dynamic pressure detection, 12-cell baselines, and Empirical Bayes shrinkage
- Document Top 10 Batters, Top 10 Bowlers, and 20 candidate evidence profiles
- Establish official Data Governance policy and dataset baseline specification
- Rebaseline development roadmap against official Rajasthan Royals competition pack
```

---

### Commit 3: Final Authoritative Acceptance Audits & Project Hygiene
*Focus: Authoritative audit deliverables, blocker closure, directory keep files.*

**Exact Inclusion Paths (11 items):**
- `ROUND1_SUBMISSION_READINESS_AUDIT.md`
- `ROUND1_GIT_STAGING_PLAN.md`
- `ST5_09_FINAL_BLOCKER_VERIFICATION.md`
- `ST5_09_FINAL_INDEPENDENT_ACCEPTANCE_AUDIT.md`
- `data/validation/DATA_QUALITY_AND_INTEGRITY_REPORT.md`
- `reports/DATASET_CRICKET_INTELLIGENCE_FINDINGS.md`
- `round1_pressure/reports/R1_SUBMISSION_02_BOWLING_RANKING_INTEGRITY_AUDIT.md`
- `round1_pressure/reports/data_quality_report.md`
- `round1_pressure/reports/pressure_detection_report.md`
- `round1_pressure/reports/r1_05_2_validation_closure_report.md`
- `data/processed/rajasthan_royals/.gitkeep`
- `data/raw/rajasthan_royals/.gitkeep`
- *(Plus restoration of the 11 `.gitkeep` placeholders to resolve unstaged deletions cleanly)*

**Proposed Commit Message:**
```text
audit(r1-freeze): document independent acceptance, blocker closure, and project freeze

- Add ST5-09 independent acceptance audit and final blocker verification reports
- Confirm Conservative PRI formula consistency (1-SE lower bound, not 1.96 CI)
- Add ST5-10 final submission readiness audit and pre-commit staging plan
- Add bowling ranking integrity audit verifying Jasprit Bumrah #1 ranking
- Restore and retain directory placeholder .gitkeep files
```

---

## 7. Complete Exclusion List (Preserved Locally, Not Staged)

The following paths are **excluded** from all staging and commits:
1. `data/raw/rajasthan_royals/round_1_data_pack/` (7 raw CSV files, ~43 MB; kept ignored by `.gitignore`).
2. The 9 redundant duplicate `r1_06_*.md` files in root (authoritative tracked versions reside in `round1_pressure/reports/`).
3. `docs/REVISED_14_STAGE_ROADMAP.md` (broader Stages 6–13 scope; kept out of Round 1 submission).
4. `docs/DEVELOPMENT_ROADMAP_ARCHIVE_PRE_DATASET.md` (historical archive).
5. `docs/PRIORITIZED_IMPLEMENTATION_BACKLOG.md` (internal sprint backlog).
6. `docs/DATASET_FEATURE_COMPATIBILITY_MATRIX.md` (internal exploratory reference).
7. `docs/DATASET_INVENTORY_AND_PROFILING_REPORT.md` (internal exploratory reference).
8. `FRONTEND_INTEGRATION_AUDIT.md` (superseded preliminary audit).
9. `FRONTEND_IMPLEMENTATION_ROADMAP.md` (superseded preliminary roadmap).
10. `PROJECT_STATUS_AND_PROGRESS_AUDIT.md` (superseded intermediate audit).
11. `ST5_07_API_INTEGRATION_MATRIX.md` (superseded milestone record).
12. `ST5_07_FRONTEND_IMPLEMENTATION_REPORT.md` (superseded milestone record).
13. `ST5_07_TEST_REPORT.md` (superseded milestone record).
14. `round1_pressure/reports/R1_SUBMISSION_READINESS_AUDIT.md` (superseded preliminary audit).
15. `round1_pressure/reports/reliability_framework_architecture_audit_pre_authorization.md` (internal pre-auth audit).

---

## 8. Suggested Official Release Tag (Not Created)

- **Suggested Tag:** `v4.1.0-round1-submission`
- **Annotation:** `Official Rajasthan Royals SupeRR Selector Season 2 (Round 1) Submission Release`

---

## 9. Final Decision & Stop Condition

### **FINAL VERDICT: READY FOR USER APPROVAL**

The corrected staging plan:
- Resolves all 11 placeholder considerations.
- Protects the Round 1 scope boundary by excluding future-stage roadmaps.
- Filters out duplicate and superseded audit files, retaining only authoritative records.
- Keeps large raw data packs strictly ignored.
- Establishes clean, reviewable commit boundaries.

**STOP CONDITION:** Execution is stopped. Awaiting your explicit approval before performing any restoration, staging, or committing.
