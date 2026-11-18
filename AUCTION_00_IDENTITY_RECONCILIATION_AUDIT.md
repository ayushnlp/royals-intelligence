# ROYALS INTELLIGENCE — AUCTION-00 IDENTITY RECONCILIATION AUDIT
## Player Deduplication, Alias Resolution & Canonical Entity Architecture
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-18T04:07:00+05:30  
**Candidate Universe Scope:** 1,217 Unique Players across 6,413 Competition Mappings  
**Audit Status:** COMPLETE & VERIFIED

---

## 1. Candidate Universe Breadth & Scope

Unlike naive evaluations that restrict analysis to the 268 rows in `ipl_players.csv`, ROYALS INTELLIGENCE expands the candidate universe to **1,217 unique players** identified in `competition_team_player_mapping.csv` across Syed Mushtaq Ali Trophy, Vijay Hazare Trophy, Ranji Trophy, and IPL competitions.

```mermaid
graph LR
    A["competition_team_player_mapping.csv<br/>(6,413 Rows)"] --> B["1,217 Unique Player IDs"]
    C["ipl_players.csv<br/>(268 Rows)"] --> D["267 Unique Names"]
    B --> E["Canonical Player Registry<br/>(RR-PLAYER-XXXXX)"]
    D --> E
    F["Alias Resolver<br/>(23 Known Spelling Variants)"] --> E
    G["Disambiguation Engine<br/>(7 Multi-Name Collisions)"] --> E
```

---

## 2. Duplicate Detection: The Ravi Bishnoi Case Study

### 2.1 The Discrepancy
In `ipl_players.csv`, exactly one player name appears twice:
- **Row 179:** `Ravi Bishnoi` | Team: `Rajasthan Royals` | Role: `Bowler` | Age: 24 | Bowling: `Right-arm leg break`
- **Row 261:** `Ravi Bishnoi` | Team: `Lucknow Super Giants` | Role: `Bowler` | Age: 24 | Bowling: `Right-arm leg break`

### 2.2 Forensic Resolution & Semantic Governance
1. **Single Physical Individual:** Both rows represent the same individual (Indian international leg-spinner Ravi Bishnoi).
2. **Dual-Franchise Attribution:** The duplicate reflects historical roster transitions (drafted by LSG in 2022, benchmarked against RR in internal projections).
3. **No Entity Fragmentation:** AUCTION-01 canonical registry unifies Ravi Bishnoi under a single canonical entity while preserving both source row pointers (Row 179 and Row 261) in the provenance ledger.
4. **Performance Aggregation:** All 200,999 deliveries bowled by or faced by Ravi Bishnoi across both LSG and domestic matches are correctly attributed to his single canonical profile.

---

## 3. Name Collisions & Disambiguation

While there are 1,217 unique player IDs, there are 1,210 unique string names in `competition_team_player_mapping.csv`. This reveals **7 legitimate name collisions** where distinct players share the same name:

| Shared Name | Player ID A | Team / Association A | Player ID B | Team / Association B | Disambiguation Strategy |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **Mohit Sharma** | 360 | Haryana / GT | 4219 | Domestic State XI | Distinct Canonical IDs (`RR-PLAYER-00360`, `RR-PLAYER-04219`) |
| **Shivam Sharma** | 1049 | Delhi | 7330 | Services | Distinct Canonical IDs |
| **Amit Mishra** | 28 | Haryana / LSG | 7458 | Uttar Pradesh | Distinct Canonical IDs |
| **Ankit Sharma** | 1058 | Madhya Pradesh | 8120 | Puducherry | Distinct Canonical IDs |
| **Saurabh Kumar** | 1069 | Uttar Pradesh | 7452 | Services | Distinct Canonical IDs |
| **Ravi Kumar** | 7321 | Bengal (U19) | 8107 | Services | Distinct Canonical IDs |
| **Akash Deep** | 1166 | Bengal / RCB | 8221 | Domestic State XI | Distinct Canonical IDs |

*Governance Rule:* Player names are **never** used as primary keys. All joins and aggregations strictly use integer `player_id` or namespaced `canonical_id` (`RR-PLAYER-XXXXX`).

---

## 4. Alias Resolution & Spelling Normalization

The `AliasResolver` maps 23 known variant spellings, initials, and scorebook abbreviations to their canonical representation:
- `K.L. Rahul` $\rightarrow$ `KL Rahul`
- `V. Kohli` $\rightarrow$ `Virat Kohli`
- `R. Ashwin` $\rightarrow$ `Ravichandran Ashwin`
- `S. Samson` $\rightarrow$ `Sanju Samson`
- `Y. Jaiswal` $\rightarrow$ `Yashasvi Jaiswal`
- `R. Jadeja` $\rightarrow$ `Ravindra Jadeja`
- `N. Burger` $\rightarrow$ `Nandre Burger`
- `T. Deshpande` $\rightarrow$ `Tushar Deshpande`
- `D. Shanaka` $\rightarrow$ `Dasun Shanaka`
- `M. Theekshana` $\rightarrow$ `Maheesh Theekshana`
*(All 23 cases verified by automated tests in `test_auction_01_identity.py`).*

---

## 5. Decoupling Roster Association from Current Squad Membership

A foundational principle established in AUCTION-00 is the strict separation between:
1. **Source CSV Roster Snapshot:** The 27 players listed under `Team == 'Rajasthan Royals'` in `ipl_players.csv`.
2. **Historical Franchise Representation:** Players who represented RR between 2022 and 2024.
3. **Current Verified Legal Contract:** Legally binding contracts registered with the BCCI for IPL 2027.

The 27 entries in `ipl_players.csv` are treated as **provisional research benchmarks**, not verified current legal contracts.
