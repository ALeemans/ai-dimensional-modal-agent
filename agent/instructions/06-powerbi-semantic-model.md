# Agent Instruction: 06 — Power BI Semantic Model (TMDL)

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6

> This is a reusable instruction document. It describes how an AI agent should generate a Power BI semantic model in TMDL format from a set of processed Parquet files, based on the dimensional model designed in Phase 4 and built in Phase 5.

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Use the project language for all outputs. TMDL display names (tables, columns, measures) and DAX expressions use the project language (e.g. Dutch for DUO HBO).

---

## Purpose

This phase creates a Power BI semantic model that reads the processed Parquet files as tables, defines column types and display names, sets up all relationships between fact and dimension tables, and adds basic DAX measures.

Output:
- `powerbi/<model-name>.SemanticModel/definition/tables/*.tmdl` — one TMDL file per table
- `powerbi/<model-name>.SemanticModel/definition/relationships.tmdl` — all FK relationships
- `scripts/generate_powerbi_tmdl.py` — the generation script (idempotent, re-runnable)

---

## Prerequisites

- Phase 5 complete: all Parquet files present in `data/processed/`
- A Power BI PBIP project already scaffolded (`.pbip` file + `.SemanticModel` folder with `definition/model.tmdl` and `definition/database.tmdl`)
- Python 3.10+ with `pyarrow` installed (already required for Phase 5)
- Dimensional model design documented (grain, FK columns, measure columns, display names)

---

## How to Scaffold a New PBIP Project

If the `.pbip` file does not yet exist, create it in Power BI Desktop:

1. Open Power BI Desktop
2. File → Save As → choose **Power BI Project (.pbip)** format
3. Save in `powerbi/<model-name>.pbip`
4. Close Power BI Desktop

This produces:
```
powerbi/
  <model-name>.pbip
  <model-name>.Report/
  <model-name>.SemanticModel/
    definition/
      model.tmdl        ← model-level settings
      database.tmdl     ← compatibility level
    definition.pbism
    .platform
```

The `tables/` subdirectory and `relationships.tmdl` do not exist yet — the generation script creates them.

---

## Script Architecture

A single script generates all TMDL output:

```
scripts/
  generate_powerbi_tmdl.py    # Reads parquet schemas → writes TMDL files
```

**Why a generation script instead of hand-written TMDL:**
- Column types are read from the actual Parquet schemas — no guessing or manual sync needed
- UUIDs (`lineageTag`) are generated programmatically — no copy-paste errors
- Re-runnable: regenerates all files cleanly if the schema or display names change
- Idempotent: safe to run multiple times

---

## TMDL Format Reference

Power BI uses **TMDL (Tabular Model Definition Language)** — a text-based format for the Analysis Services tabular model that Power BI is built on. In PBIP Developer Mode, the model is serialised as a folder of `.tmdl` files.

### File responsibilities

| File | Contains |
|------|----------|
| `definition/model.tmdl` | Model-level settings (culture, data access). **Do not add relationships here.** |
| `definition/database.tmdl` | Compatibility level. Do not modify. |
| `definition/relationships.tmdl` | All relationship definitions. |
| `definition/tables/<Name>.tmdl` | One file per table (columns, measures, data source). |

### Table file syntax

```tmdl
table 'Display Name'
	lineageTag: <uuid>

	column 'Column Display Name'
		dataType: int64
		lineageTag: <uuid>
		isHidden
		summarizeBy: none
		sourceColumn: source_col_name    ← only when display name ≠ source name

	column AnotherColumn
		dataType: string
		lineageTag: <uuid>
		summarizeBy: none
		sourceColumn: another_col

	measure 'Measure Name' = DAX_expression
		formatString: "#,0"
		lineageTag: <uuid>

	partition 'Partition Name' = m
		mode: import
		source = ```
			let
			    Source = Parquet.Document(File.Contents("D:/path/to/file.parquet"))
			in
			    Source
		```
```

**Indentation:** tabs only (never spaces). Top-level keywords (`table`, `relationship`) at column 0; their children indented one tab; grandchildren two tabs.

**Quoting:** names containing spaces use single quotes (`'Academisch Jaar'`). Single-word names need no quotes (`Jaar`).

**dataType values:** `int64`, `double`, `string`, `boolean`, `dateTime`

**summarizeBy:** use `sum` only for additive numeric measures (`aantal_*`). Use `none` for everything else (keys, codes, text, booleans).

**isHidden:** bare keyword (no `= true`), written on its own line inside the column block. Use for all surrogate and foreign key columns.

**sourceColumn:** required when the TMDL display name differs from the Parquet column name. Omit when they match exactly.

### relationships.tmdl syntax

```tmdl
relationship <uuid>
	fromColumn: 'Fact Table'.FK Column Display Name
	toColumn: DimTable.PK Column Display Name

relationship <uuid>
	fromColumn: 'Another Fact'.'Soort Diploma Key'
	toColumn: 'Soort Diploma'.'Soort Diploma Key'
```

- One `relationship` block per FK, no wrapping object
- Table names: **always single-quoted**, regardless of whether they contain spaces
- Column names after the dot: **single-quoted when they contain spaces**, unquoted otherwise
- All relationships are many-to-one (fact/child → dimension/parent) by default
- Dimension-to-dimension relationships (outriggers) use the same syntax

---

## Script Configuration Sections

The script has five configuration blocks that must be updated for each new project. Everything else (type mapping, TMDL rendering, file I/O) is generic and does not need to change.

### 1. `TABLE_NAMES` — internal parquet stem → display name

```python
TABLE_NAMES: dict[str, str] = {
    "dim_tijd":            "Tijd",
    "feit_ingeschrevenen": "Ingeschrevenen",
    ...
}
```

One entry per Parquet file in `data/processed/`. The display name is what Power BI users see.

### 2. `COLUMN_NAMES` — source column → display name

```python
COLUMN_NAMES: dict[str, str] = {
    "tijd_key":              "Tijd Key",
    "academisch_jaar_label": "Academisch Jaar",
    "aantal_ingeschrevenen": "Aantal Ingeschrevenen",
    ...
}
```

Only columns whose display name differs from the source name need an entry — but it is safe (and recommended) to include all columns for clarity.

### 3. `HIDDEN_COLS` — surrogate and foreign key column names to hide

```python
HIDDEN_COLS: set[str] = {
    "tijd_key", "instelling_key", "opleiding_key", ...,
    "ingeschrevenen_key", "id",
}
```

These columns appear in the TMDL with `isHidden` set. Users see only business-meaningful columns in the Power BI field list.

### 4. `MEASURES` — DAX measures per fact table

```python
MEASURES: dict[str, list[tuple[str, str, str]]] = {
    "feit_ingeschrevenen": [
        ("Totaal Ingeschrevenen",
         "SUM('Ingeschrevenen'[Aantal Ingeschrevenen])",
         "#,0"),
        ("% Privacy Onderdrukt",
         "DIVIDE(COUNTROWS(FILTER('Ingeschrevenen', 'Ingeschrevenen'[Privacy Onderdrukt])), COUNTROWS('Ingeschrevenen'))",
         "0.00%"),
    ],
    ...
}
```

Tuple structure: `(display_name, dax_expression, format_string)`. Use the table's **display name** (from `TABLE_NAMES`) inside the DAX expression. Dimension tables typically have no measures.

### 5. `RELATIONSHIPS` — FK tuples

```python
RELATIONSHIPS: list[tuple[str, str, str, str]] = [
    # (from_table_key, from_column_source, to_table_key, to_column_source)
    ("feit_ingeschrevenen", "tijd_key",      "dim_tijd",      "tijd_key"),
    ("feit_ingeschrevenen", "instelling_key","dim_instelling","instelling_key"),
    ...
]
```

Use the **internal table key** (Parquet stem) and the **source column name** (not display name). The script resolves display names automatically. List every FK in every fact table.

---

## Running the Script

```bash
python scripts/generate_powerbi_tmdl.py
```

The script:
1. Reads each Parquet file's schema via `pyarrow` (no data loaded into memory)
2. Generates one `.tmdl` file per table in `definition/tables/`
3. Writes `definition/relationships.tmdl` with all FK relationships
4. Leaves `definition/model.tmdl` untouched

Re-run freely: all output files are overwritten on each run.

---

## Opening the Model in Power BI Desktop

1. Double-click `powerbi/<model-name>.pbip`
2. Power BI Desktop opens and detects the TMDL files
3. Click **Refresh** to load data from the Parquet files
4. The model diagram should show all tables and relationships

If Power BI shows errors on open, common causes:

| Error | Likely cause |
|-------|--------------|
| Table not found | TMDL file missing from `tables/` — check that the script ran without errors |
| Column not found | `sourceColumn` in TMDL does not match the actual Parquet column name (case-sensitive) |
| Relationship error | `fromColumn` or `toColumn` table/column name in `relationships.tmdl` does not match the display name in the table TMDL |
| File not found | Absolute path in the M expression does not match the actual file location — update `PROCESSED` path and re-run |

---

## Adapting to a New Dataset

When applying this to a different project:

1. **Scaffold a PBIP project** (see above) — one `.pbip` file per semantic model
2. **Copy `generate_powerbi_tmdl.py`** into the new project's `scripts/` folder
3. **Update the five configuration blocks** (`TABLE_NAMES`, `COLUMN_NAMES`, `HIDDEN_COLS`, `MEASURES`, `RELATIONSHIPS`) to match the new dimensional model
4. **Update the path constants** at the top of the script (`PROCESSED`, `DEFINITION`) if the folder structure differs
5. **Run the script** and open the `.pbip` in Power BI Desktop
6. **Verify** the model diagram matches the expected star schema

**Do not modify** the helper functions (`gen_uuid`, `q`, `pa_to_tmdl_type`, `summarize_by`, `generate_table_tmdl`, `build_relationships_tmdl`) — these are generic and project-independent.
