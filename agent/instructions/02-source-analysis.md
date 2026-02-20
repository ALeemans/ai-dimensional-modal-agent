# Agent Instruction: 02 — Source Analysis & Business Understanding

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6

> This is a reusable instruction document. It describes how an AI agent should analyze source data to derive business meaning — the essential step between metadata collection (Phase 1) and dimensional model design (Phase 3).

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Use the project language for all outputs (e.g. Dutch for DUO HBO projects)

---

## Purpose

Raw metadata (field names, types, cardinality) does not tell you *what the data means*. This phase bridges that gap by answering:

- What real-world things does this data describe? (entities)
- What real-world events does this data record? (business processes)
- What is the finest level of detail available? (grain)
- How do the datasets connect? (relationships)

The output of this phase directly drives Phase 3 (dimensional model design).

---

## Prerequisites

- Completed metadata catalog from Phase 1, including:
  - Field-level profiles for all datasets
  - **Official source documentation** (Step 1.5) — verbatim selection criteria and glossary per dataset
- If Step 1.5 was skipped or incomplete: fetch the official dataset descriptions now before proceeding. Business meaning cannot be reliably derived from field names and sample values alone.

---

## Instructions for the Agent

### Step 1: Identify Business Entities

**Goal:** Name the real-world things the data describes.

**Actions:**
1. Read through all field names and sample values in the metadata catalog
2. For each distinct concept found, define an entity:
   - **Name** — what is this thing called in the business domain?
   - **Description** — what does it represent?
   - **Primary key** — which field(s) uniquely identify it?
   - **Source dataset(s)** — where does it appear?
3. Note entities that appear in multiple datasets under different field names (synonyms)
4. Note entities that are implicit (e.g. a "date" dimension implied by a year field)

**Key questions:**
- What are the nouns in the business domain this data describes?
- Are there people, organizations, products, locations, or time periods?
- Are there reference/lookup tables that describe master data?

**Output:** Entity list with descriptions and source mappings

---

### Step 2: Determine Grain per Dataset

**Goal:** Precisely define what one row in each dataset represents.

**Actions:**
1. For each dataset, identify the combination of fields that makes a row unique
2. Express the grain as: *"One row = [count/event/entity] per [dimension1] × [dimension2] × ..."*
3. Classify the dataset type:
   - **Transactional fact** — one row per individual event (order, enrollment, payment)
   - **Periodic snapshot** — one row per entity per time period (balance, headcount on a date)
   - **Accumulating snapshot** — one row per process instance tracking milestones
   - **Dimension/reference** — descriptive master data (no measure)

**Key questions:**
- What combination of fields makes a row unique?
- Is this pre-aggregated data or individual-level data?
- What time period does each row represent?

**Watch out for:**
- Multiple resources/files per dataset that are alternative aggregations of the same base data — they are NOT independent rows and cannot be stacked
- Pre-aggregated data posing as transactional data (common in government open data)

**Output:** Grain statement per dataset, dataset type classification

---

### Step 3: Identify Business Processes

**Goal:** Name the real-world events or processes that generate the measurements in the data.

**Actions:**
1. For each dataset with measures (numeric fields that count or sum something), identify:
   - **Process name** — what event is being counted/measured?
   - **Trigger** — what causes a row to be created?
   - **Frequency** — how often is data captured (daily, annually, on event)?
   - **Measures available** — what can be counted or summed?
2. Group datasets that describe the same process (possibly at different granularities)
3. Identify supporting processes captured in reference datasets

**Key questions:**
- What business activity produces each measurement?
- Is this a count of events, a count of people, a monetary amount, or something else?
- Are there multiple datasets describing the same process from different angles?

**Output:** Business process list with associated datasets and measures

---

### Step 4: Document Entity Relationships

**Goal:** Map how the business entities connect to each other.

**Actions:**
1. For each pair of datasets with shared fields, verify the relationship:
   - Identify the join key(s)
   - Determine the relationship type (1:1, 1:N, N:M)
   - Check for data type mismatches (e.g. numeric ID in one table, text in another)
   - Note any naming discrepancies (same concept, different column names)
2. Draw or describe the entity relationship model
3. Flag relationships that require transformation before joining (CAST, TRIM, normalization)

**Key questions:**
- Which field in dataset A corresponds to which field in dataset B?
- Are the join key values in the same format and data type?
- Are there orphaned records (keys in one dataset with no match in another)?

**Output:** Relationship map with join keys, types, and data quality notes

---

## Output Template

Save the business analysis as: `docs/fase2-bronanalyse.md` (or language-appropriate equivalent)

### Entity List

```markdown
| # | Entity | Description | Primary Key | Source(s) |
|---|--------|-------------|-------------|-----------|
| 1 | ...    | ...         | ...         | ...       |
```

### Grain per Dataset

```markdown
| Dataset | Grain (one row = ...) | Type |
|---------|-----------------------|------|
| ...     | ...                   | Periodic snapshot / Transactional / Dimension |
```

### Business Processes

```markdown
| Process | Description | Type | Source Data | Measures | Frequency |
|---------|-------------|------|-------------|----------|-----------|
| ...     | ...         | Snapshot | ...     | ...      | Annual    |
```

### Relationship Map

```markdown
| From | To | Type | Join Key | Notes |
|------|----|------|----------|-------|
| dataset_a.field | dataset_b.field | N:1 | ... | Type mismatch: cast needed |
```

### Summary: Dimensional Model Candidates

```markdown
**Candidate fact tables:**
- fact_[process] — [grain] — measures: [list]

**Candidate dimension tables:**
- dim_[entity] — key: [field] — source: [dataset]
```

---

## Tips for the Agent

- **Don't guess business meaning from field names alone.** Check sample values, cardinality, and relationships to confirm your interpretation.
- **Always use official documentation (from Step 1.5) before drawing conclusions.** Two datasets with nearly identical structure, row counts, and field names may measure fundamentally different things. This is only discoverable from official selection criteria — not from the data itself. Example: "ingeschrevenen" (unique persons, main enrollment only) vs. "inschrijvingen" (all enrollment records including secondary) look identical in the CSV but require separate fact tables.
- **Selection criteria determine fact table count.** Each dataset with a different counting unit or inclusion rule typically becomes a separate fact table, not just a different measure in the same table.
- **Verify official exclusions.** Official documentation often lists what is *excluded* (e.g. "propedeuse diplomas are not counted", "aangewezen instellingen are excluded"). These exclusions define the analytical scope and must be documented as model limitations.
- **Pre-aggregated data is common in government open data.** Always determine whether data is transactional or already summarized — this defines whether your fact table will be transactional or a periodic snapshot.
- **Multiple files covering the same process** (e.g. one split by gender, one by program code) are typically alternative cross-tabulations of the same underlying fact. Model them as one fact table with nullable dimension keys, or as separate fact tables depending on analytical needs.
- **Privacy constraints** may mean individual-level data is unavailable. Pre-aggregated counts are the finest grain possible — design the model accordingly.
- **Time dimensions may differ** across processes (e.g. enrollment year vs. graduation year). These are separate time dimensions, not interchangeable.
- **Reference datasets are future dimension tables.** Identify them early — they provide the descriptive attributes for your fact table's foreign keys.
