# Agent Instruction: 01 — Metadata Collection & Source Profiling

**Author:** Anne Leemans, in collaboration with Claude Opus 4.6

> This is a reusable instruction document. It describes how an AI agent should collect and catalog metadata from any data source as the first step toward building a dimensional model.

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Dutch (all outputs, metadata, documentation, and data intended for use by Dutch stakeholders)

For DUO HBO projects:
- Dataset names, descriptions → Dutch
- Field names, metadata, data dictionaries → Dutch
- README, PLAN, project documentation → Dutch
- CSV headers and data → Dutch
- Agent outputs and catalogs → Dutch

**Rationale:** All content that will be reviewed, used, or delivered to Dutch education institutions must be in Dutch. Instructions about *how* the process works can be in English for international reusability.

---

## Collaboration Model

This project is a human–AI collaboration:

- **AI agent (Claude):** performs data discovery, profiling, documentation, and draft output
- **Human (Anne Leemans):** reviews outputs, runs tests, validates results, and approves each phase before the next begins

The agent must produce clear, reviewable output at each step so the human can verify correctness before proceeding.

## Purpose

Before any dimensional modeling can begin, the agent must thoroughly understand the source data. This phase produces a **metadata catalog** — a structured description of every dataset, field, and relationship available.

## Prerequisites

The data source must provide at least one of:
- An API with discoverable endpoints (REST, OData, GraphQL)
- A database with queryable schema information
- Structured files (CSV, Parquet, JSON) with headers or schema files
- Documentation describing the data structure

## Instructions for the Agent

### Step 1: Discover Available Datasets

**Goal:** Produce a complete inventory of all datasets/tables/files in scope.

**Actions:**
1. Query the API catalog, database information_schema, or file listing
2. For each dataset, record:
   - **Name** (technical identifier)
   - **Display name** (human-readable)
   - **Description** (what it contains)
   - **Source URL or location**
   - **Update frequency**
   - **Historical depth** (how far back does data go?)
   - **Scope/filter** (e.g., "only HBO" or "all education levels")

**Output:** A dataset inventory table (see template below)

---

### Step 1.5: Fetch Official Source Documentation

**Goal:** Collect and preserve the official, authoritative definitions and selection criteria for every dataset — before profiling the data itself.

**Why this matters:** Field names and sample values alone cannot tell you:
- What is *included* vs *excluded* from a count
- What a metric *actually measures* (e.g. persons vs. records)
- What privacy or filtering rules affect the data
- Official definitions of domain-specific terms

These definitions are **critical for correct dimensional modeling** and must be documented verbatim to avoid misinterpretation later.

**Actions:**
1. For every dataset found in Step 1, retrieve the **official dataset description** from its source:
   - For CKAN APIs (e.g. DUO): `GET /api/3/action/package_show?id={dataset_id}` — extract the `notes` field
   - For REST APIs: look for `/docs`, `/swagger`, or `/metadata` endpoints
   - For databases: query `information_schema.columns.column_comment` or equivalent
   - For file-based sources: look for README, data dictionaries, codebooks, or accompanying PDF documentation

2. For each dataset, extract and record:
   - **Selection criteria** — exactly what records are included and excluded
   - **Counting unit** — is this counting persons, events, records, amounts?
   - **Reference date / peildatum** — when is the data measured?
   - **Time scope** — which periods are covered?
   - **Privacy / suppression rules** — are small counts suppressed, rounded, or replaced?
   - **Known exclusions** — what categories are deliberately left out?
   - **Source system** — what upstream system generates this data?

3. Quote the relevant text **verbatim** in the metadata catalog — do not paraphrase definitions that affect analytical meaning. This prevents future misinterpretation and provides an audit trail.

4. Immediately compare documentation against the actual data:
   - Does the claimed suppression rule match what you see in the data? (e.g. documentation says "shown as 4" but data contains -1)
   - Does the claimed grain match the actual row count and distinct key combinations?
   - Are stated exclusions visible in the data (i.e., missing expected categories)?

5. Build a **begrippenoverzicht** (glossary) of all domain-specific terms with official definitions. Include at minimum:
   - Every measure (what exactly is being counted)
   - Every key domain concept (e.g. "ingeschrevene", "hoofdinschrijving", "peildatum")
   - All coded values (e.g. VT/DT/DU, M/V, MAN/VROUW)
   - Any terms whose meaning differs from everyday usage

**Output:** A section titled "Officiële Brondocumentatie en Definities" in the metadata catalog, containing:
- Verbatim selection criteria per dataset
- A begrippenoverzicht (glossary table) with: Term | Definition | Dataset(s)
- Any discrepancies found between documentation and actual data

**⚠️ Do not skip this step even if the data source seems self-explanatory.** Subtle definitional differences (e.g. persons vs. enrollments, main vs. secondary registrations) directly determine how many fact tables are needed and whether analytical results will be correct.

---

### Step 2: Profile Each Dataset

**Goal:** For every dataset, collect detailed field-level metadata.

**Actions per dataset:**
1. Retrieve the schema or first N rows
2. For each field/column, record:
   - **Field name**
   - **Data type** (string, integer, date, decimal, etc.)
   - **Description** (if available from API metadata or documentation)
   - **Nullable** (yes/no)
   - **Sample values** (3-5 representative values)
   - **Cardinality** (approximate number of distinct values)
   - **Null rate** (percentage of null/empty values)
   - **Potential role** (identifier, attribute, measure, date, foreign key — initial guess)

3. Record the **row count** of the dataset
4. Record the **grain** — what does one row represent? (initial assessment)

**Output:** A field-level metadata table per dataset

---

### Step 3: Identify Relationships

**Goal:** Find connections between datasets through shared fields.

**Actions:**
1. Compare field names across datasets — look for exact matches and semantic matches
2. For each potential relationship, record:
   - **Source dataset.field** → **Target dataset.field**
   - **Relationship type** (1:1, 1:N, N:M)
   - **Confidence** (high/medium/low — based on name match, value overlap, documentation)
3. Validate relationships by checking value overlap between fields

**Output:** A relationship map

---

### Step 4: Document Data Quality Observations

**Goal:** Flag anything that may affect modeling decisions.

**Actions:**
1. Note fields with high null rates (>20%)
2. Note fields with suspicious cardinality (e.g., an ID field with low cardinality)
3. Note inconsistent formatting or encoding
4. Note fields that appear duplicated across datasets
5. Note any aggregated vs. transactional data patterns

**Output:** A data quality notes section in the metadata catalog

---

## Output Template

The metadata catalog should be saved as: `data/metadata/{source-name}-metadata-catalog.md`

### Language in Output
**For Dutch projects (DUO HBO):** All output content must be in Dutch
- Dataset names and descriptions → Dutch
- Field names and descriptions → Dutch
- Column headers in CSV files → Dutch
- Data quality notes → Dutch
- All narrative text → Dutch

**Exception:** The metadata catalog structure/headings can follow English patterns, but all content within must be Dutch.

### CSV File Convention

All CSV output files must use:
- **Separator:** `;` (semicolon)
- **Encoding:** `utf-8-sig` (UTF-8 with BOM — ensures correct opening in Excel)
- **Language:** All headers and content in Dutch (for Dutch projects)

Each output document must begin with:

```markdown
**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6
**Date:** {date}
**Source:** {data source name}
```

### Official Documentation (per dataset)

```markdown
## Officiële Brondocumentatie en Definities

> Bron: {API endpoint / document name}, opgehaald {date}. Tekst letterlijk overgenomen.

### {Dataset name} — Selectiecriteria

**Selectie:** *"{verbatim selection criteria from official documentation}"*

**Kernbegrip:** {one-sentence plain-language summary of what is counted}

**AVG/privacy-filter:** *"{verbatim suppression rule}"*

> **Let op:** {any discrepancy between documentation and actual data}

### Begrippenoverzicht

| Begrip | Definitie | Dataset(s) |
|--------|-----------|------------|
| **{Term}** | {Official definition} | {Which datasets use it} |
```

### Dataset Inventory

```markdown
| # | Dataset ID | Name | Description | Row Count | Grain | Update Freq | History |
|---|-----------|------|-------------|-----------|-------|-------------|---------|
| 1 | ...       | ...  | ...         | ...       | ...   | ...         | ...     |
```

### Field Metadata (per dataset)

```markdown
## Dataset: {dataset_name}

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | ...   | ...  | ...         | ...      | ...           | ...         | ...    | ...        |

**Grain:** {what one row represents}
**Row count:** {total rows}
```

### Relationships

```markdown
| Source | Target | Type | Confidence | Notes |
|--------|--------|------|------------|-------|
| dataset_a.field_x | dataset_b.field_y | 1:N | High | Exact name match, 98% value overlap |
```

### Data Quality Notes

```markdown
- [ ] {observation}
```

---

## Tips for the Agent

- **Be thorough over fast.** Missing a field or relationship now creates problems later.
- **Don't assume.** If the role of a field is unclear, mark it as "unknown" with notes.
- **Record everything.** Even fields that seem irrelevant may become useful dimensions.
- **Use the data, not just the schema.** Sample values reveal more than data types alone.
- **Ask about scope early.** If only a subset of data is in scope (e.g., HBO only), filter early.
- **Always fetch official documentation first (Step 1.5).** Two datasets can have nearly identical structure, row counts, and field names yet measure completely different things (e.g. "persons" vs "enrollments"). You cannot discover this from the data alone — only official definitions reveal it.
- **Quote verbatim, don't paraphrase.** Selection criteria and exclusions must be exact. A paraphrase may lose the precise boundary condition that determines whether your fact tables are correct.
- **Verify documentation against data.** Discrepancies between official documentation and actual data values (e.g. suppression value "-1" vs "4") are important findings that affect downstream modeling.
- **Build the glossary early.** Domain terms that look similar but mean different things (like "ingeschrevene" vs "inschrijving") will cause modeling errors if left undefined.

---

## Applying This Instruction to DUO HBO Data

For the DUO pilot:
- Start at https://onderwijsdata.duo.nl/datasets/ and https://duo.nl/open_onderwijsdata/hoger-onderwijs/
- Filter to HBO datasets only
- Key dataset IDs: `p01hoinges`, `p03hoinschr`
- The API follows OData conventions — use `$metadata` endpoints where available
- Data is updated annually with a reference date of October 1st
- Last 5 academic years are typically available

### Dutch Language Requirements for DUO Projects

**All outputs must be in Dutch:**
- Dataset inventory → translate to Dutch
- Field metadata tables → all headers and content in Dutch
- Relationship descriptions → Dutch
- Data quality notes → Dutch
- All narrative documentation → Dutch
- Example headers: `Datasetnaam`, `Veldenmaatschappij`, `Beschrijving`, `Null mogelijk`, `Voorbeeldwaarden`, `Kardinaliteit`

DUO data stakeholders and the target audience (HBO institutions) are Dutch-speaking. All deliverables must be accessible in Dutch.
