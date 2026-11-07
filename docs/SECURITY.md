# ROYALS INTELLIGENCE — SECURITY & DATA PROTECTION POLICY
**Classification:** Confidential / Rajasthan Royals Technical Security Standard  
**Document Version:** 1.0.0 (Stage 0 Baseline)  

---

## 1. Core Principles

1. **Confidentiality of Competitive Intelligence:** Strategic scout notes, psychological ratings, and auction bid limits represent core sporting IP. A breach gives opposing franchises an asymmetric advantage.
2. **Zero Hardcoded Secrets:** Credentials, private keys, API secrets, and connection URIs must never exist in plaintext within the repository.
3. **Partitioned Data Domains:** Strict isolation between open-source cricket records and Rajasthan Royals proprietary intelligence.

---

## 2. Secrets Management & Git Policy

- **Ignored Artifacts:** The `.gitignore` at the repository root strictly excludes:
  - All `.env`, `.env.local`, `.env.*` configuration files.
  - SSH/TLS certificates (`*.pem`, `*.key`).
  - Cache databases and temporary test runs.
- **Environment Templates:** All required configuration variables must be documented in `.env.example` templates with non-functional dummy defaults.
- **Pre-Commit Auditing:** Before any commit or push, staged files must be inspected for accidental secret exposure.

---

## 3. Data Protection & Storage Boundaries

### 3.1. Public vs. Proprietary Data Boundary
```
[PUBLIC / UNRESTRICTED]
- Historical match scorecards
- Public ball-by-ball delivery feeds (Cricsheet)
- Player career basic aggregates
- Tournament schedules & venue locations
      |
      | (Physical Directory & Access Barrier)
      v
[PROPRIETARY / RESTRICTED (Rajasthan Royals Internal Only)]
- Scout qualitative evaluation logs
- Medical and biomechanical screening dossiers
- Replacement simulator WAR calculations
- IPL 2027 Auction purse allocation models and max bid ceilings
- Tactical opposition weakness dossiers
```

### 3.2. Proprietary Data Handling Rules
1. Proprietary files reside exclusively in `data/proprietary/` which is ignored by Git.
2. Stored records must be encrypted at rest in production environments (AES-256).
3. Database backups containing proprietary tables must be encrypted using franchise-managed KMS keys.

---

## 4. API & Network Security

- **CORS Protection:** Backend API strictly allows configured origins (e.g., `http://localhost:3000` in local dev). Wildcard `*` origins are prohibited.
- **Health Probes:** `/health` and `/api/v1/health` endpoints expose only operational status, latency, and component health. Database connection strings, passwords, and host IP addresses are never leaked in response payloads.
- **Error Sanitization:** Centralized exception handlers catch database and server exceptions and return sanitized RFC-7807 problem details without internal stack traces in non-debug mode.


---

## 4. Stage 2 Data Classification & Access Boundary Enforcement

### 4.1. Dataset Classification Levels
1. **`PUBLIC`**: Standard scorecards and aggregated metrics. Freely exposed to all API callers.
2. **`INTERNAL_SCOUTING`**: Roster priority tiers, player archetypes, and calculated age metrics. Visible within platform interface.
3. **`RR_PROPRIETARY_CONFIDENTIAL`**: Qualitative scout evaluations, confidential notes, strategic bid ceilings, and trialist evaluations.

### 4.2. Automated Access Masking Engine
The system enforces automatic role-based data masking via `RRDataPackService.mask_confidential_data()`:
- Public / standard users receive masked strings:
  - `confidential_notes`: `"[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"`
  - `proprietary_notes`: `"[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"`
  - `scout_identifier`: `"[ANONYMIZED_RR_SCOUT]"`
  - `scouting_tier`: `"INTERNAL"`
- Full evaluation fidelity is unlocked exclusively for authenticated requests carrying authorized headers (`x-user-role: rr_scout_admin` or `rr_lead_analyst`).
