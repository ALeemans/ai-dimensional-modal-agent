# Agent Instruction: 04 — Dimensional Model Design

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6

> This is a reusable instruction document. It describes how an AI agent should design a dimensional model (star schema) from analyzed source data — transforming the business understanding from Phase 2 into a concrete Kimball-style data warehouse design.

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Use the project language for all outputs (e.g. Dutch for DUO HBO projects)

---

## Purpose

Phase 2 (Source Analysis) identified business entities, processes, granularity, and relationships. This phase transforms that understanding into a **dimensional model** — a star schema with fact tables and dimension tables following the Kimball methodology.

---

## Prerequisites

Before starting this phase, you must have:

- [ ] A completed **metadata catalog** (Phase 1) with field profiles
- [ ] A completed **source analysis** (Phase 2) with:
  - Identified business entities
  - Documented granularity per dataset
  - Identified business processes
  - Mapped relationships between entities
- [ ] Access to **raw data** (Phase 3) for validation of assumptions

---

## Step 4.1 — Identify Fact Table Candidates

### Method

For each business process identified in Phase 2, determine if it produces a **fact table**:

1. **Is there a measurable event or snapshot?** If the data records a count, amount, or measurement — it's a fact candidate.
2. **What type of fact table?**
   - **Transaction fact:** One row per event (e.g., one sale, one click)
   - **Periodic snapshot:** One row per time period per entity (e.g., monthly balance)
   - **Accumulating snapshot:** One row per process instance, updated as milestones occur
   - **Aggregated fact:** Pre-aggregated data where the source already contains summarized counts

3. **Determine the grain** — what does one row represent? This is the most critical decision.

### Decision Framework: Pre-aggregated Data

When source data is **already aggregated** (common in government/statistical data):

- The fact table grain equals the source grain — you cannot go finer
- Multiple aggregation variants of the same data require **separate fact tables** (not combinable)
- Document what analysis questions become unanswerable due to aggregation

### Output

A table per candidate:

| Attribute | Value |
|-----------|-------|
| Fact table name | `feit_xxx` |
| Business process | ... |
| Fact table type | Transaction / Periodic snapshot / Aggregated |
| Grain | One row per ... × ... × ... |
| Measure(s) | field_name (SUM/COUNT/AVG) |
| Source file | ... |
| Row count | ... |

---

## Step 4.2 — Identify Dimension Table Candidates

### Method

For each fact table, list the **descriptive context** fields. These become dimensions:

1. **Who?** — People, organizations, accounts
2. **What?** — Products, services, programs
3. **When?** — Time periods, dates
4. **Where?** — Geographic locations
5. **How?** — Methods, forms, categories

### Rules

- Each dimension should have a **surrogate key** (auto-increment integer) and a **natural key** (business identifier)
- Prefer **wide, denormalized dimensions** (no snowflaking) — add descriptive attributes directly to the dimension
- Small categorical fields (< 5 values) can be **separate mini-dimensions** or **degenerate dimensions** (stored directly in the fact table)
- If a field appears in the fact source but doesn't fit any dimension, consider making it a **degenerate dimension** (stored in the fact table without a foreign key)

### Enrichment

Dimensions can be **enriched** from reference datasets that weren't used for fact tables:

- JOIN reference data to dimension tables on shared natural keys
- Document any type mismatches (e.g., numeric vs text keys) that need CAST operations
- When reference data has multiple rows per natural key (e.g., multiple locations per program), decide on deduplication strategy

### Output

A table per dimension:

| Attribute | Value |
|-----------|-------|
| Dimension name | `dim_xxx` |
| Natural key | field_name |
| Approximate row count | ... |
| Primary source | ... |
| Enrichment sources | ... (via JOIN on ...) |
| Key attributes | ... |

---

## Step 4.3 — Define Granularity

### Method

For each fact table, explicitly state the grain as a **composite natural key**:

```
Grain: one row per [time_period] × [entity_1] × [entity_2] × ... × [entity_n]
```

### Validation

- Count distinct combinations of grain fields in source data — should match total row count
- If row count > distinct combinations → duplicates exist (data quality issue)
- If row count < distinct combinations → some combinations are missing (sparse data, which is normal)

---

## Step 4.4 — Map Measures

### Method

For each fact table, document the measures:

| Measure | Source field | Type | Aggregation | Null handling |
|---------|-------------|------|-------------|---------------|
| ... | ... | Additive / Semi-additive / Non-additive | SUM / AVG / COUNT | NULL = unknown / 0 / suppressed |

### Special Cases

- **Privacy-suppressed values** (e.g., -1 for counts < 5): Convert to NULL, add boolean flag `is_suppressed`
- **Derived measures**: Document calculation formula
- **Semi-additive measures** (e.g., balances): Note which dimensions they can be summed across

---

## Step 4.5 — Define Dimension Hierarchies

### Method

For each dimension, identify drill-down paths:

```
Level 1 (coarsest) → Level 2 → Level 3 (finest)
```

Examples:
- Geography: Country → Province → Municipality
- Time: Decade → Year → Quarter → Month
- Product: Category → Subcategory → Product

### Rules

- All hierarchy levels should be attributes within the same dimension table (no snowflaking)
- Document **ragged hierarchies** (not all branches have the same depth)
- Document **alternative hierarchies** (multiple drill paths from the same dimension)

---

## Step 4.6 — Determine SCD Strategy

### Method

For each dimension, determine the Slowly Changing Dimension strategy:

| Strategy | When to use |
|----------|-------------|
| **Type 1** (overwrite) | Only current values matter; no historical tracking needed; or source doesn't provide history |
| **Type 2** (add row) | Historical changes must be tracked; source provides both old and new values |
| **Type 3** (add column) | Only the most recent change needs tracking (current + previous value) |

### Practical Guidance

- If the source only provides current/actual values (e.g., `_ACTUEEL` fields), Type 1 is the only viable option
- If the source provides effective dates (begin/end), Type 2 is possible
- Document what historical analysis is lost due to Type 1

---

## Step 4.7 — Draw the Star Schema

### Method

Create a visual representation showing:
- Fact tables in the center
- Dimension tables around them
- Foreign key relationships as lines
- Outrigger relationships (dimension-to-dimension) clearly marked

Use ASCII art for text-based output:

```
    ┌─────────┐    ┌──────────┐    ┌─────────┐
    │ dim_who │◄───│ FACT_xxx │───►│ dim_what│
    └─────────┘    │          │    └─────────┘
                   │ measure  │
    ┌─────────┐    │          │    ┌─────────┐
    │dim_when │◄───│          │───►│dim_where│
    └─────────┘    └──────────┘    └─────────┘
```

---

## Step 4.8 — Document Known Limitations

Every dimensional model has limitations. Explicitly document:

1. **What questions cannot be answered** due to grain, aggregation, or missing dimensions
2. **Data quality issues** that affect measure accuracy (suppression, missing values)
3. **Historical gaps** due to SCD strategy or source limitations
4. **Conformity issues** between dimensions shared across fact tables

---

## Step 4.9 — Write the Design Document

### Output File

Create `docs/fase4-dimensioneel-ontwerp.md` (or equivalent in project language) containing:

1. **Core challenge** — What makes this data source unique/difficult
2. **Design decisions** — Each major decision with motivation
3. **Dimension tables** — Full column listing with types, sources, descriptions
4. **Fact tables** — Full column listing with grain, source, row count
5. **Visual schema** — ASCII star schema diagram
6. **Hierarchies** — All drill paths per dimension
7. **Kimball conformity** — How the design follows Kimball principles
8. **Known limitations** — What can't be done with this model

---

## Checklist

Before moving to Phase 5 (Validation), verify:

- [ ] Every business process from Phase 2 has a corresponding fact table (or documented reason for exclusion)
- [ ] Every fact table has an explicitly stated grain
- [ ] Every dimension has a surrogate key and natural key
- [ ] No snowflake joins — all hierarchy levels are within dimension tables
- [ ] Shared dimensions (time, geography, organization) are conformed across fact tables
- [ ] NULL handling is documented for all measures
- [ ] SCD strategy is documented for all dimensions
- [ ] Known limitations are documented
- [ ] The design document is complete and reviewable
