# Agent Instruction: 05 — ETL Build (Dimension & Fact Tables)

**Author:** Anne Leemans, in collaboration with Claude Opus 4.6

> This is a reusable instruction document. It describes how an AI agent should build an ETL pipeline that transforms raw source data into a dimensional model (Parquet files), based on the design produced in Phase 4.

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Use the project language for all outputs. Script comments and print statements may be in the project language (e.g. Dutch for DUO HBO).

---

## Purpose

This phase transforms raw source data (CSV files in `data/raw/`) into a set of dimension and fact tables (Parquet files in `data/processed/`), implementing the star schema designed in Phase 4.

Output:
- One Parquet file per dimension table (`dim_*.parquet`)
- One Parquet file per fact table (`feit_*.parquet`)
- A shared utilities module (`etl_utils.py`)
- An orchestration script (`build_all.py`) that runs the full pipeline in dependency order

---

## Prerequisites

- Phase 3 complete: raw source data present in `data/raw/`
- Phase 4 complete: dimensional model design documented in `docs/fase4-*.md`
- Python 3.10+ with `pandas` and `pyarrow` installed
- Design document specifying: grain, surrogate keys, natural keys, measure columns, FK relationships, and privacy suppression rules

---

## Script Architecture

### One script per table

Each dimension and fact table gets its own standalone Python script:

```
scripts/
  etl_utils.py                          # Shared helpers (paths, CSV readers, write_parquet)
  build_dim_tijd.py                     # → data/processed/dim_tijd.parquet
  build_dim_geslacht.py                 # → data/processed/dim_geslacht.parquet
  ...
  build_feit_ingeschrevenen.py          # → data/processed/feit_ingeschrevenen.parquet
  ...
  build_all.py                          # Orchestrator — runs all scripts in order
```

**Why one script per table:**
- Easy to re-run a single table during debugging
- Clear dependency visibility (each script lists its requirements in the docstring)
- No shared state — each script is idempotent (overwrites existing Parquet on re-run)

### Shared utilities (`etl_utils.py`)

Three functions only:
- `read_stat_csv(path)` — reads statistical source CSVs (comma-separated, UTF-8-BOM, all columns as `str`)
- `read_adres_csv(path)` — reads address source CSVs (semicolon-separated, cp1252 encoding)
- `write_parquet(df, name)` — writes `data/processed/{name}.parquet`, prints confirmation

### Orchestrator (`build_all.py`)

Uses `subprocess.run` to execute each script in a new Python process. This avoids module caching issues when scripts share names. Prints per-step timing and collects errors. Exits with code 1 if any step fails.

---

## Build Order (Dependency-Driven)

Scripts must run in this sequence:

```
1. Trivial dimensions (no source data dependencies)
   dim_tijd, dim_geslacht, dim_opleidingsvorm, dim_soort_diploma

2. Sector dimension (reads a/c-variant source files)
   dim_sector

3. Enriched dimensions (read raw data + cross-references)
   dim_geografie, dim_bestuur, dim_instelling, dim_opleiding

4. Primary fact tables (b-variants — CROHO grain)
   feit_ingeschrevenen, feit_inschrijvingen, feit_eerstejaars, feit_gediplomeerden

5. Supplementary fact tables — geslacht variants (a-variants — sector grain)
   feit_*_geslacht (× 4)

6. Supplementary fact tables — opleidingsvorm variants (c-variants — sector grain)
   feit_*_oplvorm (× 4)
```

---

## Standard Script Patterns

### Dimension script pattern

```python
"""
build_dim_<naam>.py
<Beschrijving van de dimensie en bron>
Output: data/processed/dim_<naam>.parquet

Vereisten: <welke scripts eerst moeten draaien, of 'geen'>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, PROCESSED, read_stat_csv, write_parquet

print("Bouwen dim_<naam>...")

# 1. Load source data
df = read_stat_csv(RAW / "...")

# 2. Extract unique combinations, drop nulls
df = df[COLS].drop_duplicates().dropna(subset=[NK_COL])

# 3. Rename to Dutch snake_case output column names
df.rename(columns={...}, inplace=True)

# 4. Sort for deterministic key assignment
df = df.sort_values(NK_COL).reset_index(drop=True)

# 5. Add surrogate key (starts at 1)
df.insert(0, "<naam>_key", range(1, len(df) + 1))

write_parquet(df, "dim_<naam>")
```

### Fact table script pattern

```python
"""
build_feit_<naam>.py
<Korrel, meetwaarde, bron>
Privacyonderdrukking: -1 → NULL + is_onderdrukt = True

Vereisten (run eerst): <lijst van dim scripts>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, PROCESSED, read_stat_csv, write_parquet

print("Bouwen feit_<naam>...")

# 1. Load source
df = read_stat_csv(RAW / "...")

# 2. Load only needed columns from each dimension
dim_tijd = pd.read_parquet(PROCESSED / "dim_tijd.parquet")[["tijd_key", "jaar"]]
# ... other dimensions

# 3. Cast join keys to matching types
df["_jaar"] = pd.to_numeric(df["STUDIEJAAR"], errors="coerce").astype("Int64")
dim_tijd["jaar"] = dim_tijd["jaar"].astype("Int64")

# 4. Left-join all dimensions (LEFT = keep all source rows, expose unmatched as NULL)
df = df.merge(dim_tijd, left_on="_jaar", right_on="jaar", how="left")
# ... other merges

# 5. Handle privacy suppression (-1 → NULL)
aantallen = pd.to_numeric(df["AANTAL_..."], errors="coerce")
df["is_onderdrukt"]  = aantallen == -1
df["aantal_..."]     = aantallen.where(aantallen != -1).astype("Int64")

# 6. Select FK columns + measures only (drop all source columns)
df_feit = df[["tijd_key", ..., "aantal_...", "is_onderdrukt"]].copy()
df_feit.insert(0, "<naam>_key", range(1, len(df_feit) + 1))

write_parquet(df_feit, "feit_<naam>")
```

---

## Source File Quirks (DUO HBO)

### Column naming inconsistencies across datasets

| Dataset | Time column | Education key | Type column |
|---------|-------------|---------------|-------------|
| p01b, p02b, p03b | `STUDIEJAAR` | `OPLEIDINGSCODE_ACTUEEL` | `TYPE_HOGER_ONDERWIJS` |
| p04b | `DIPLOMAJAAR` | `OPLEIDINGSCODE_ACTUEEL` | `SOORT_DIPLOMA` (not TYPE_HOGER_ONDERWIJS) |
| p01a/c, p02a/c, p03a/c | `STUDIEJAAR` | *(absent — sector grain)* | `TYPE_HOGER_ONDERWIJS` |
| p04a/c | `DIPLOMAJAAR` | *(absent — sector grain)* | `SOORT_DIPLOMA` |

**p04 fix:** Derive `TYPE_HOGER_ONDERWIJS` by stripping the `"hbo "` prefix from `SOORT_DIPLOMA`:
```python
df["TYPE_HOGER_ONDERWIJS"] = df["SOORT_DIPLOMA"].str.replace("hbo ", "", regex=False)
```

Values: `"hbo bachelor"` → `"bachelor"`, `"hbo associate degree"` → `"associate degree"`, `"hbo master"` → `"master"`

### CSV encoding

| File group | Separator | Encoding |
|------------|-----------|----------|
| Statistical datasets (p01–p04, ho_opleidingsoverzicht) | `,` (comma, quoted) | `utf-8-sig` |
| Address files (instellingen, besturen) | `;` (semicolon) | `cp1252` |

### CROHO codes (dim_opleiding)

- Stored as string `"34267"` in source → cast to `Int64` in dimension
- Cast also required before dim_opleiding join in fact scripts

### Municipality codes (dim_geografie)

- Always read as `str` (dtype=str) to preserve leading zeros (`"0106"`)
- Join on string equality — no numeric casting

### Privacy suppression

- Source value `-1` = DUO AVG-filter (count < 5)
- Always convert to `NULL` (`pd.NA`) before storing as measure
- Add boolean `is_onderdrukt` column alongside every measure column

### ho_opleidingsoverzicht deduplication

This file contains multiple rows per CROHO code (one per location/form/provider). Before joining to dim_opleiding, deduplicate on `ERKENDEOPLEIDINGSCODE` to keep one row per code:
```python
rio = rio.drop_duplicates(subset=["ERKENDEOPLEIDINGSCODE"])
```

---

## Validation Checklist

After running `build_all.py`, verify:

| Check | How |
|-------|-----|
| Row counts match design expectations | Compare Parquet row counts to design doc estimates |
| Zero NULL foreign keys | For each FK column in fact tables: `df[fk].isna().sum() == 0` |
| Privacy suppression rate | `is_onderdrukt.sum() / len(df)` — expect 1–6% for primary facts |
| Surrogate keys start at 1, no gaps | `df[sk].min() == 1`, `df[sk].max() == len(df)` |
| Dim natural keys are unique | `df[nk].nunique() == len(df)` |

---

## Adapting to a New Dataset

When applying this pattern to a different source dataset:

1. **Inventory the source files** — identify separators, encodings, column naming conventions
2. **Check for column inconsistencies** — does every source file have the same columns? (DUO: p04 lacks TYPE_HOGER_ONDERWIJS)
3. **Identify the grain per fact table** — what combination of columns uniquely identifies a row?
4. **Identify privacy/suppression conventions** — DUO uses `-1`; other sources may use `"*"`, `"x"`, or empty string
5. **Map natural keys to dimension tables** — every FK in a fact table must resolve to exactly one dimension row
6. **Test with LEFT JOIN** — a LEFT JOIN with zero NULLs in the FK column confirms complete dimension coverage
