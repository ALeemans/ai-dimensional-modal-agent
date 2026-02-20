# AI Dimensional Modeling Agent — Project Memory

> This file is tracked in git and is the canonical memory for this project.
> It is available across machines. Always read this file at the start of a session.

## Language Rules

**Communication:** English — Claude and user discuss, plan, and review in English.

**Project content:** Use the project language for all artifacts and deliverables.
- Project language is determined per project based on the target audience.
- DUO HBO pilot: **Dutch** 🇳🇱 — all output files, metadata, documentation, and data in Dutch.

### File language reference (DUO HBO pilot)

| File / Type | Language | Reason |
|---|---|---|
| `agent/instructions/*.md` | English | Reusable process documentation |
| `.claude/memory/MEMORY.md` | English | Agent memory / communication |
| `README.md` | Dutch | Deliverable for Dutch stakeholders |
| `docs/PLAN.md` | Dutch | Project plan for Dutch stakeholders |
| `data/metadata/*.csv` | Dutch | Data artifacts |
| `data/metadata/*-metadata-catalog.md` | Dutch | Data artifacts |
| CSV column headers | Dutch | Data artifacts |
| Field descriptions, data quality notes | Dutch | Data artifacts |

---

## Project Overview

- **Goal:** Build an AI agent that generates dimensional models (star schemas) from source data
- **Pilot dataset:** DUO Open Onderwijsdata HBO
- **Method:** Kimball methodology
- **Repo:** `d:\HogeschoolUtrecht\GithubRepos\ai-dimensional-modal-agent`

## DUO Dataset Conventions

- CSV separator: `;` (semicolon)
- Encoding: `utf-8-sig` (UTF-8 with BOM — for Excel compatibility)
- Gender field: `MAN` / `VROUW` (text)
- Privacy suppression: `-1` for counts < 5 (not 4 as DUO documentation suggests)
- Municipality codes: stored as text with leading zeros (e.g. `"0106"`)

## Dutch Dimensional Modeling Terminology

| Dutch | English |
|---|---|
| sterrenmodel | star schema |
| feitentabel | fact table |
| dimensietabel | dimension table |
| meetwaarde | measure |
| granulariteit | grain |
| langzaam veranderende dimensie | slowly changing dimension |
| peildatum | reference date |
| academisch jaar | academic year |

## Phase Progress

- Fase 1.1 ✅ — Dataset inventory complete (8 datasets)
- Fase 1.2 ✅ — All 8 datasets profiled at field level
- Fase 1.3 ✅ — Metadata catalog complete (`duo-hbo-metadata-catalog.md` — 8 datasets, 16 relationships, 13 data quality notes)
- Fase 1.4 ✅ — Language rules documented in `agent/instructions/01-metadata-collection.md`
- **Fase 1 — COMPLETE ✅**
- Fase 2.1–2.4 ✅ — Business analysis complete (`docs/fase2-bronanalyse.md` — 10 entities, 3 fact candidates, 7 dimension candidates)
- Fase 2.5 ✅ — Instruction file written (`agent/instructions/02-source-analysis.md`)
- **Fase 2 — COMPLETE ✅**
- Fase 3.1–3.5 ✅ — Data extraction complete (16 files in `data/raw/`, manifest written)
- Fase 3.6 ✅ — Instruction file written (`agent/instructions/03-data-extraction.md`)
- **Fase 3 — COMPLETE ✅**
- Fase 4 → Next — Dimensional model design (star schema: fact tables + dimensions)
- Fase 5 → — Model validation
- Fase 6 → — Agent assembly
