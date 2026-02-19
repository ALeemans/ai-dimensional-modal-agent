# Metadata Catalog: DUO Open Onderwijsdata — HBO

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6
**Date:** 2026-02-19
**Source:** DUO Open Onderwijsdata (https://onderwijsdata.duo.nl)

---

## Dataset Inventory

| # | Dataset ID | Name | Description | Resources (HBO) | Row Count (HBO total) | Grain | Update Freq | History |
|---|-----------|------|-------------|-----------------|----------------------|-------|-------------|---------|
| 1 | p01hoinges | Ingeschrevenen HBO | Enrolled students in HBO, by geography, institution, program, and demographics | 3 CSVs (gender, level, education form) | ~15,892 | Students per institution/program/year | Annual (Oct 1) | Last 5 academic years |
| 2 | p02ho1ejrs | Eerstejaars ingeschrevenen HBO | First-year enrolled students in HBO | 3 CSVs (gender, level, education form) | ~12,149 | First-year students per institution/program/year | Annual (Oct 1) | Last 5 academic years |
| 3 | p03hoinschr | Inschrijvingen HBO | Enrollments (inscriptions) in HBO | 3 CSVs (gender, level, education form) | ~15,900 | Enrollments per institution/program/year | Annual (Oct 1) | Last 5 academic years |
| 4 | p04hogdipl | Gediplomeerden HBO | Graduates from HBO programs | 3 CSVs (gender, level, education form) | ~14,849 | Graduates per institution/program/year | Annual (Oct 1) | Last 5 academic years |
| 5 | ho_opleidingsoverzicht | HO Opleidingsoverzicht | Overview of all funded HO programs from RIO | 1 CSV | 7,090 | One row per program/location | Daily | Current |
| 6 | overzicht-erkenningen-ho | Overzicht Erkenningen HO | OCW-recognized HO institutions and programs | 1 CSV + PDF docs | 6,747 | One row per accreditation | Daily | Current |
| 7 | — | Adressen hogescholen en universiteiten | Addresses of HBO institutions and universities | 1 CSV + 1 XLSX | Small (~50) | One row per institution (main campus) | Monthly | Current |
| 8 | — | Adressen besturen | Addresses of governing boards | 1 CSV + 1 XLSX | Small (~50) | One row per governing board | Monthly | Current |

---

## Resource Detail: HBO-Specific Files

### p01hoinges — Ingeschrevenen HBO

| # | Resource | File | Records | Size | Description |
|---|----------|------|---------|------|-------------|
| 1a | HBO incl. geslacht | ingeschrevenengeslhbo.csv | 4,833 | 762 KB | Enrolled students by geography, institution, program, gender |
| 1b | HBO niveau opleiding | ingeschrevenenhbo.csv | 7,170 | 1.34 MB | Enrolled students by geography, institution, program level |
| 1c | HBO incl. opleidingsvorm | ingeschrevenenoplvhbo.csv | 3,889 | 601 KB | Enrolled students by geography, institution, education form (VT/DT/DU) |

### p02ho1ejrs — Eerstejaars Ingeschrevenen HBO

| # | Resource | File | Records | Size | Description |
|---|----------|------|---------|------|-------------|
| 2a | HBO incl. geslacht | 1ejrsingeschrevenengeslhbo.csv | 3,407 | 534 KB | First-year students by geography, institution, program, gender |
| 2b | HBO niveau opleiding | 1ejrsingeschrevenenhbo.csv | 5,834 | 1.08 MB | First-year students by geography, institution, program level |
| 2c | HBO incl. opleidingsvorm | 1ejrsingeschrevenenoplvhbo.csv | 2,908 | 448 KB | First-year students by geography, institution, education form |

### p03hoinschr — Inschrijvingen HBO

| # | Resource | File | Records | Size | Description |
|---|----------|------|---------|------|-------------|
| 3a | HBO incl. geslacht | inschrijvingengeslhbo.csv | 4,835 | ~762 KB | Enrollments by geography, institution, program, gender |
| 3b | HBO niveau opleiding | inschrijvingenhbo.csv | 7,174 | ~1.34 MB | Enrollments by geography, institution, program level |
| 3c | HBO incl. opleidingsvorm | inschrijvingenoplvhbo.csv | 3,891 | ~601 KB | Enrollments by geography, institution, education form |

### p04hogdipl — Gediplomeerden HBO

| # | Resource | File | Records | Size | Description |
|---|----------|------|---------|------|-------------|
| 4a | HBO incl. geslacht | gediplomeerdengeslhbo.csv | 4,445 | 716 KB | Graduates by geography, institution, program, gender |
| 4b | HBO niveau opleiding | gediplomeerdenhbo.csv | 6,813 | 1.3 MB | Graduates by geography, institution, program level |
| 4c | HBO incl. opleidingsvorm | gediplomeerdenoplvhbo.csv | 3,591 | 568 KB | Graduates by geography, institution, education form |

### Reference Datasets

| # | Resource | File | Records | Description |
|---|----------|------|---------|-------------|
| 5 | HO Opleidingsoverzicht | ho_opleidingsoverzicht.csv | 7,090 | All funded HO programs from RIO register |
| 6 | Erkenningen HO | ho_erkenningen_rio.csv | 6,747 | OCW-recognized HO accreditations |
| 7 | Adressen instellingen | Adressen hogescholen en universiteiten.csv | ~50 | Institution main campus addresses |
| 8 | Adressen besturen | Adressen besturen hogescholen en universiteiten.csv | ~50 | Governing board addresses |

---

## General Notes

- **License:** All datasets are CC-BY (Creative Commons Attribution)
- **Privacy filter:** Student counts < 5 are displayed as 4 (GDPR compliance)
- **Scope:** Datasets p01–p04 cover both HBO and WO; only HBO resources are in scope for this pilot
- **Reference date:** Student data is measured on October 1st of each academic year
- **Source system:** "Één Cijfer Hoger Onderwijs" (One Number Higher Education)
- **Contact:** informatieproducten@duo.nl / gegevensmagazijn@duo.nl
- **API portal:** https://onderwijsdata.duo.nl/datasets/

---

## Field Metadata

### Dataset: p01hoinges — Ingeschrevenen HBO

All 3 HBO resources share a **common core** of 10 fields plus one resource-specific field each. The measure field is always `AANTAL_INGESCHREVENEN`.

**Source data separator:** `,` (comma) — note: DUO uses comma-separated CSVs

#### Common Fields (all 3 resources)

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | STUDIEJAAR | numeric | Academic year (reference date Oct 1) | No | 2020, 2021, 2022, 2023, 2024 | 5 | 0% | Date/time dimension key |
| 2 | PROVINCIENAAM | text | Province name | No | Drenthe, Noord-Holland, Zuid-Holland, Utrecht | 12 | 0% | Geography dimension |
| 3 | GEMEENTENUMMER | text | Municipality code (CBS) | No | 0106, 0114, 0363, 0599 | 52 | 0% | Geography dimension key |
| 4 | GEMEENTENAAM | text | Municipality name | No | Assen, Amsterdam, Rotterdam, Utrecht | 52 | 0% | Geography dimension |
| 5 | SOORT_INSTELLING | text | Institution type | No | reguliere inst. | 1 | 0% | Institution dimension |
| 6 | TYPE_HOGER_ONDERWIJS | text | Higher education level | No | associate degree, bachelor, master | 3 | 0% | Program dimension |
| 7 | INSTELLINGSCODE_ACTUEEL | text | Current institution code (BRIN) | No | 25DW, 28DN, 22OJ, 30GB | 36 | 0% | Institution dimension key |
| 8 | INSTELLINGSNAAM_ACTUEEL | text | Current institution name | No | Hogeschool Utrecht, Hogeschool van Amsterdam | 36 | 0% | Institution dimension |
| 9 | ONDERDEEL | text | ISCED sector / domain | No | TECHNIEK, ECONOMIE, ONDERWIJS, GEZONDHEIDSZORG, GEDRAG_EN_MAATSCHAPPIJ, LANDBOUW_EN_NATUURLIJKE_OMGEVING, TAAL_EN_CULTUUR, SECTOROVERSTIJGEND | 8 | 0% | Program dimension |
| 10 | SUBONDERDEEL | text | Sub-sector / sub-domain | No | leraar basisonderwijs, n.v.t. (techniek), voortgezette kunstopleidingen | 16 | 0% | Program dimension |
| 11 | AANTAL_INGESCHREVENEN | numeric | Number of enrolled students | No | 5, 50, 163, 5247 (also -1 for suppressed) | Continuous | 0% | **Measure** |

#### Resource-Specific Fields

| Resource | Extra Field | Type | Description | Sample Values | Cardinality | Role Guess |
|----------|-----------|------|-------------|---------------|-------------|------------|
| 1a (geslacht) | GESLACHT | text | Gender | MAN, VROUW | 2 | Demographic dimension |
| 1b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO program code | 34267, 34808, 80009 | 247 | Program dimension key |
| 1b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Program name | B Elektrotechniek, M Smart Systems Engineering | 247 | Program dimension |
| 1c (oplvorm) | OPLEIDINGSVORM | text | Education delivery form | VT (full-time), DT (part-time), DU (dual) | 3 | Program dimension |

#### Resource Summary

| Resource | File | Records | Grain |
|----------|------|---------|-------|
| 1a | ingeschrevenengeslhbo.csv | 4,833 | Students per year × municipality × institution × sector × subsector × education level × gender |
| 1b | ingeschrevenenhbo.csv | 7,170 | Students per year × municipality × institution × program (CROHO) |
| 1c | ingeschrevenenoplvhbo.csv | 3,889 | Students per year × municipality × institution × sector × subsector × education level × education form |

#### Data Quality Notes (p01hoinges)

- [ ] **Privacy suppression:** `AANTAL_INGESCHREVENEN = -1` occurs in 273 of 4,833 records (5.7%) in resource 1a — these represent counts < 5 suppressed for GDPR compliance. Note: DUO documentation states counts < 5 are displayed as 4, but the actual data uses -1 for suppression. **Needs human verification.**
- [ ] `SOORT_INSTELLING` has cardinality 1 (always "reguliere inst.") — may be redundant for HBO-only scope, but could differ when combining with WO data
- [ ] `GEMEENTENUMMER` is stored as text (not integer) — padded with leading zeros (e.g. "0106")
- [ ] The 3 resources represent different cross-tabulations of the same base data — not independent observations. They cannot be simply joined or unioned
- [ ] `ONDERDEEL` and `SUBONDERDEEL` use a hierarchical classification; `SUBONDERDEEL` often contains "n.v.t. (sector)" meaning the sector has no further subdivision

## Relationships

> _To be completed in Step 3: Identify Relationships_

## Data Quality Notes

> _To be completed in Step 4: Document Data Quality Observations_
