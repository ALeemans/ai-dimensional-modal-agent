# Agent Instruction: 01 — Metadata Collection & Source Profiling

**Author:** Anne Leemans, in collaboration with Claude Opus 4.6

> This is a reusable instruction document. It describes how an AI agent should collect and catalog metadata from any data source as the first step toward building a dimensional model.

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

### CSV File Convention

All CSV output files must use:
- **Separator:** `;` (semicolon)
- **Encoding:** `utf-8-sig` (UTF-8 with BOM — ensures correct opening in Excel)

Each output document must begin with:

```markdown
**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6
**Date:** {date}
**Source:** {data source name}
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

---

## Applying This Instruction to DUO HBO Data

For the DUO pilot:
- Start at https://onderwijsdata.duo.nl/datasets/ and https://duo.nl/open_onderwijsdata/hoger-onderwijs/
- Filter to HBO datasets only
- Key dataset IDs: `p01hoinges`, `p03hoinschr`
- The API follows OData conventions — use `$metadata` endpoints where available
- Data is updated annually with a reference date of October 1st
- Last 5 academic years are typically available
