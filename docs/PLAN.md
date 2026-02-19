# Project Plan: AI Dimensional Modeling Agent

**Author:** Anne Leemans, in collaboration with Claude Opus 4.6

## Goal

Create an AI agent that can build a complete dimensional model (star schema) from scratch, given only access to a data source (API, database, flat files). The agent should work on **any** data source that meets basic prerequisites — not just DUO data.

### Three deliverables

1. **A dimensional model** of DUO HBO data (proof of concept)
2. **An AI-powered workflow** that generates dimensional models from source data
3. **Agent instruction documents** that allow the agent to be reused on any future data source

---

## Step-by-Step Plan

### Phase 1: Metadata Collection & Source Profiling

> _"You can't model what you don't understand."_

**Objective:** Collect as much accurate metadata as possible from the DUO HBO data sources.

**Steps:**

1.1. **Inventory all HBO datasets** from DUO Open Onderwijsdata
   - Studenten HBO (students)
   - Inschrijvingen HBO (enrollments)
   - Studenten eerstejaars HBO (first-year students)
   - Inschrijvingen eerstejaars HBO (first-year enrollments)
   - Afgestudeerden HBO (graduates)
   - Adressen hogescholen en universiteiten (institution addresses)
   - Adressen besturen (governing board addresses)

1.2. **Explore each API endpoint** and document:
   - Available fields (column names, data types)
   - Sample data (first rows)
   - Cardinality of each field
   - Null/empty rates
   - Value distributions for categorical fields
   - Relationships between datasets (shared keys)
   - Update frequency and historical depth

1.3. **Create a metadata catalog** with structured output per dataset

1.4. **Write Agent Instruction:** `01-metadata-collection.md` — How to profile any data source

---

### Phase 2: Source Analysis & Business Understanding

**Objective:** Understand what the data represents in business terms.

**Steps:**

2.1. **Identify business entities** (student, institution, program, enrollment, graduation)

2.2. **Map grain** for each dataset — what does one row represent?

2.3. **Identify business processes** (enrollment, graduation, etc.)

2.4. **Document relationships** between entities

2.5. **Write Agent Instruction:** `02-source-analysis.md` — How to derive business meaning from metadata

---

### Phase 3: Dimensional Model Design

**Objective:** Design the star schema — identify facts and dimensions.

**Steps:**

3.1. **Identify fact candidates** — What are the measurable events/transactions?
   - Enrollments (inschrijvingen)
   - Graduations (afgestudeerden)
   - Student counts (aggregated facts)

3.2. **Identify dimension candidates** — What are the descriptive attributes?
   - Student demographics (gender, nationality, age)
   - Institution (name, address, type, board)
   - Program/Study (CROHO code, field of study, level)
   - Time (academic year, reference date)
   - Geography (province, municipality)

3.3. **Define grain** for each fact table

3.4. **Map measures** (counts, sums, derived metrics)

3.5. **Define dimension hierarchies** and slowly changing dimension strategies

3.6. **Draw the star schema**

3.7. **Write Agent Instruction:** `03-dimensional-design.md` — How to design facts and dimensions from analyzed sources

---

### Phase 4: Model Validation

**Objective:** Validate the generated model against best practices and data reality.

**Steps:**

4.1. **Check conformance** to Kimball methodology

4.2. **Validate referential integrity** — Do all FK relationships hold?

4.3. **Test with sample queries** — Can the model answer typical business questions?

4.4. **Compare against manual design** — Would a human DWH architect make the same choices?

4.5. **Write Agent Instruction:** `04-model-validation.md` — How to validate a generated dimensional model

---

### Phase 5: Agent Assembly

**Objective:** Package all instructions into a coherent, reusable agent.

**Steps:**

5.1. **Compile all instruction documents** into a complete agent workflow

5.2. **Define prerequisites** — What does a data source need to be suitable?

5.3. **Create templates** for metadata catalogs, model definitions, validation checklists

5.4. **Test the agent** on a second data source (if time permits)

5.5. **Write Agent Instruction:** `05-agent-workflow.md` — The master orchestration document

---

## DUO HBO Data Sources

| Dataset | Description | Updated | Scope |
|---------|-------------|---------|-------|
| Studenten HBO | Student counts per reference date Oct 1 | Mar 2025 | Last 5 years |
| Inschrijvingen HBO | Enrollment records | Mar 2025 | Last 5 years |
| Studenten eerstejaars HBO | First-year student counts | Mar 2025 | Last 5 years |
| Inschrijvingen eerstejaars HBO | First-year enrollment records | Mar 2025 | Last 5 years |
| Afgestudeerden HBO | Graduate records | Mar 2025 | Last 5 years |
| Adressen hogescholen/universiteiten | Institution addresses | Feb 2026 | Current |
| Adressen besturen | Governing board addresses | Feb 2026 | Current |

**API Portal:** https://onderwijsdata.duo.nl/datasets/

**Key dataset IDs:**
- `p01hoinges` — Ingeschrevenen hoger onderwijs
- `p03hoinschr` — Inschrijvingen hoger onderwijs

---

## Prerequisites for Future Data Sources

For the agent to work on a new data source, it should have:

- [ ] Accessible data (API, database, or structured files)
- [ ] Machine-readable metadata (field names, types) or documentation
- [ ] Sufficient data volume to distinguish facts from dimensions
- [ ] Identifiable business process(es) the data describes
- [ ] At least one measurable event or transaction

---

## Success Criteria

- The generated DUO HBO dimensional model is valid and usable
- The agent instructions are clear enough to produce a model on a new data source without project-specific knowledge
- The workflow is repeatable and produces consistent results
