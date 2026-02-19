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

---

## Field Metadata

### Dataset: p02ho1ejrs — Eerstejaars Ingeschrevenen HBO

Identical structure to p01hoinges. Key difference: measure field is `AANTAL_EERSTEJAARS_INGESCHREVENEN`.

#### Common Fields (all 3 resources)

Same 10 common fields as p01hoinges (STUDIEJAAR, PROVINCIENAAM, GEMEENTENUMMER, GEMEENTENAAM, SOORT_INSTELLING, TYPE_HOGER_ONDERWIJS, INSTELLINGSCODE_ACTUEEL, INSTELLINGSNAAM_ACTUEEL, ONDERDEEL, SUBONDERDEEL) plus:

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 11 | AANTAL_EERSTEJAARS_INGESCHREVENEN | numeric | Number of first-year enrolled students | No | 8, 14, 36, 67, -1 | Continuous | 0% | **Measure** |

#### Resource-Specific Fields

| Resource | Extra Field | Type | Description | Sample Values | Cardinality | Role Guess |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 2a (geslacht) | GESLACHT | text | Gender | MAN, VROUW | 2 | Demographic dimension |
| 2b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO program code | 34808, 80009, 80040 | ~247 | Program dimension key |
| 2b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Program name | B Opleiding tot leraar Basisonderwijs, Ad Hotel Management | ~247 | Program dimension |
| 2c (oplvorm) | OPLEIDINGSVORM | text | Education delivery form | VT (full-time), DT (part-time), DU (dual) | 3 | Program dimension |

#### Resource Summary

| Resource | File | Records | Grain |
|----------|------|---------|-------|
| 2a | eerstejaarsingeschrevenengeslhbo.csv | 3,407 | First-year students per year × municipality × institution × sector × subsector × education level × gender |
| 2b | eerstejaarsingeschrevenenhbo.csv | 5,834 | First-year students per year × municipality × institution × program (CROHO) |
| 2c | eerstejaarsingeschrevenenoplvhbo.csv | 2,908 | First-year students per year × municipality × institution × sector × subsector × education level × education form |

#### Data Quality Notes (p02ho1ejrs)

- [ ] Privacy suppression: `AANTAL_EERSTEJAARS_INGESCHREVENEN = -1` occurs in resource 2a (exact rate not yet measured) — same GDPR mechanism as p01hoinges
- [ ] Structure is identical to p01hoinges. First-year students are a subset of all enrolled students — the two datasets should not be simply unioned

---

### Dataset: p03hoinschr — Inschrijvingen HBO

Almost identical structure to p01hoinges. Key difference: measure field is `AANTAL_INSCHRIJVINGEN`. The distinction between p01 ("Ingeschrevenen" = enrolled persons) and p03 ("Inschrijvingen" = enrollments) may reflect a subtle conceptual difference or a different extraction from the source system. Row counts are nearly identical (p01: 15,892 vs p03: 15,900 total).

#### Common Fields (all 3 resources)

Same 10 common fields as p01hoinges plus:

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 11 | AANTAL_INSCHRIJVINGEN | numeric | Number of enrollments | No | 5, 23, 53, 57, 111, -1 | Continuous | 0% | **Measure** |

#### Resource-Specific Fields

| Resource | Extra Field | Type | Description | Sample Values | Cardinality | Role Guess |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 3a (geslacht) | GESLACHT | text | Gender | MAN, VROUW | 2 | Demographic dimension |
| 3b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO program code | 34267, 34808, 80009, 80040 | ~247 | Program dimension key |
| 3b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Program name | B Elektrotechniek, Ad Tourism Management | ~247 | Program dimension |
| 3c (oplvorm) | OPLEIDINGSVORM | text | Education delivery form | VT, DT, DU | 3 | Program dimension |

#### Resource Summary

| Resource | File | Records | Grain |
|----------|------|---------|-------|
| 3a | inschrijvingengeslhbo.csv | 4,835 | Enrollments per year × municipality × institution × sector × subsector × education level × gender |
| 3b | inschrijvingenhbo.csv | 7,174 | Enrollments per year × municipality × institution × program (CROHO) |
| 3c | inschrijvingenoplvhbo.csv | 3,891 | Enrollments per year × municipality × institution × sector × subsector × education level × education form |

#### Data Quality Notes (p03hoinschr)

- [ ] Semantic relationship with p01hoinges unclear — structure and row counts nearly identical. Needs verification with DUO documentation whether these represent the same or different underlying counts
- [ ] Privacy suppression: `AANTAL_INSCHRIJVINGEN = -1` occurs in resources (exact rate not yet measured)

---

### Dataset: p04hogdipl — Gediplomeerden HBO

Differs structurally from p01–p03:
- Year dimension: `DIPLOMAJAAR` (diploma award year), not `STUDIEJAAR` (enrollment year Oct 1)
- `TYPE_HOGER_ONDERWIJS` is absent — replaced by `SOORT_DIPLOMA`
- Measure: `AANTAL_GEDIPLOMEERDEN`

#### Common Fields (all 3 resources)

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | DIPLOMAJAAR | numeric | Year diploma was awarded | No | 2019, 2020, 2021, 2022, 2023 | 5 | 0% | Date dimension key |
| 2 | PROVINCIENAAM | text | Province name | No | Drenthe, Gelderland, Noord-Holland | 12 | 0% | Geography dimension |
| 3 | GEMEENTENUMMER | text | Municipality code (CBS) | No | 0106, 0114, 0228 | 52 | 0% | Geography dimension key |
| 4 | GEMEENTENAAM | text | Municipality name | No | Assen, Emmen, Ede | 52 | 0% | Geography dimension |
| 5 | SOORT_INSTELLING | text | Institution type | No | reguliere inst. | 1 | 0% | Institution dimension |
| 6 | INSTELLINGSCODE_ACTUEEL | text | Current institution code (BRIN) | No | 25BE, 31FR | 36 | 0% | Institution dimension key |
| 7 | INSTELLINGSNAAM_ACTUEEL | text | Current institution name | No | Hanzehogeschool Groningen, NHL Stenden Hogeschool | 36 | 0% | Institution dimension |
| 8 | ONDERDEEL | text | ISCED sector / domain | No | TECHNIEK, ONDERWIJS, ECONOMIE | 8 | 0% | Program dimension |
| 9 | SUBONDERDEEL | text | Sub-sector / sub-domain | No | n.v.t. (techniek), leraar basisonderwijs | 16 | 0% | Program dimension |
| 10 | SOORT_DIPLOMA | text | Type of diploma awarded | No | hbo bachelor, hbo associate degree | 3 | 0% | Program dimension |
| 11 | AANTAL_GEDIPLOMEERDEN | numeric | Number of graduates | No | 9, 23, 42, -1 | Continuous | 0% | **Measure** |

#### Resource-Specific Fields

| Resource | Extra Field | Type | Description | Sample Values | Cardinality | Role Guess |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 4a (geslacht) | GESLACHT | text | Gender | MAN, VROUW | 2 | Demographic dimension |
| 4b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO program code | 34267, 34808, 35520 | ~200 | Program dimension key |
| 4b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Program name | B Elektrotechniek, B International Business | ~200 | Program dimension |
| 4c (oplvorm) | OPLEIDINGSVORM | text | Education delivery form | VT, DT, DU | 3 | Program dimension |

#### Resource Summary

| Resource | File | Records | Grain |
|----------|------|---------|-------|
| 4a | gediplomeerdengeslhbo.csv | 4,445 | Graduates per diploma year × municipality × institution × sector × diploma type × gender |
| 4b | gediplomeerdenhbo.csv | 6,813 | Graduates per diploma year × municipality × institution × program (CROHO) × diploma type |
| 4c | gediplomeerdenoplvhbo.csv | 3,591 | Graduates per diploma year × municipality × institution × sector × diploma type × education form |

#### Data Quality Notes (p04hogdipl)

- [ ] `DIPLOMAJAAR` earliest value in samples is 2019 (vs 2020 for p01–p03 `STUDIEJAAR`) — verify full year range
- [ ] `SOORT_DIPLOMA` expected values: "hbo bachelor", "hbo associate degree", "hbo master" — only first two seen in HBO resources
- [ ] Privacy suppression: `AANTAL_GEDIPLOMEERDEN = -1` observed in samples (exact rate not measured)
- [ ] `SOORT_DIPLOMA` serves the same role as `TYPE_HOGER_ONDERWIJS` in p01–p03 but uses different vocabulary ("hbo bachelor" vs "bachelor")

---

### Dataset: ho_opleidingsoverzicht — HO Opleidingsoverzicht

Reference dataset from RIO. All currently funded HO programs (both HBO and WO). Master program catalog.

**Row count:** 7,090 | **Grain:** One row per offered program variant (program × form × location) | **Scope:** All HO — filter NIVEAU for HBO

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | ONDERWIJSBESTUURID | text | Education authority ID (RIO) | No | 100B349 | ~90 | 0% | Institution dimension key (RIO) |
| 2 | ONDERWIJSBESTUUR_NAAM | text | Education authority name | No | Stichting HZ University of Appl. Scienc. | ~90 | 0% | Institution dimension |
| 3 | ONDERWIJSAANBIEDERID | text | Provider ID (may differ from authority) | Yes | — | ~90 | Unknown | Institution dimension key |
| 4 | ONDERWIJSAANBIEDER_NAAM | text | Provider name | Yes | — | ~90 | Unknown | Institution dimension |
| 5 | ONDERWIJSLOCATIECODE | text | Teaching location code | Yes | — | ~300 | Unknown | Location dimension key |
| 6 | ONDERWIJSLOCATIESTRAAT | text | Teaching location street | Yes | — | ~300 | Unknown | Location dimension |
| 7 | ONDERWIJSLOCATIEPLAATS | text | Teaching location city | Yes | — | ~100 | Unknown | Location dimension |
| 8 | SOORT | text | Always "OPLEIDING" | No | OPLEIDING | 1 | 0% | Redundant |
| 9 | OPLEIDINGSEENHEIDCODE | text | Program unit code (RIO) | No | 1001O2869, 1001O3168 | ~700 | 0% | Program dimension key (RIO) |
| 10 | ERKENDEOPLEIDINGSCODE | numeric | CROHO program code | No | 34074, 34279, 49506 | ~700 | 0% | Program dimension key (CROHO) |
| 11 | AANGEBODEN_OPLEIDINGCODE | text | Offered program code | Yes | — | ~700 | Unknown | Program dimension key |
| 12 | EIGEN_AANGEBODEN_OPLEIDINGSLEUTEL | text | Institution's own program key | Yes | — | ~700 | Unknown | Institution-internal |
| 13 | NAAM_LANG | text | Full program name (Dutch) | No | Watermanagement, Civiele Techniek | ~700 | 0% | Program dimension |
| 14 | INTERNATIONALE_NAAM | text | International program name | Yes | Water Management, Civil Engineering | ~700 | Unknown | Program dimension |
| 15 | EIGENNAAM | text | Institution's proprietary name | Yes | — | ~700 | High | Program dimension |
| 16 | EIGENNAAM_DUITS | text | German proprietary name | Yes | — | ~700 | Very high | Rarely used |
| 17 | EIGENNAAM_ENGELS | text | English proprietary name | Yes | — | ~700 | High | Program dimension |
| 18 | VARIANT_VAN | text | Reference to variant-of program code | Yes | — | ~700 | Unknown | Relationship field |
| 19 | ERKENNER | text | Accreditation body | No | NVAO | 1–2 | 0% | Dimension |
| 20 | NIVEAU | text | Education level | No | HBO-BA, HBO-MA, HBO-AD, WO-BA, WO-MA | 5 | 0% | Program dimension — **use as scope filter** |
| 21 | GRAAD | text | Degree type | No | BACHELOR, MASTER, ASSOCIATE_DEGREE | 3 | 0% | Program dimension |
| 22 | STUDIELAST | numeric | ECTS credits | No | 60, 120, 180, 240 | ~10 | 0% | Program attribute |
| 23 | EQF | numeric | European Qualifications Framework level | No | 5, 6, 7 | 3 | 0% | Program dimension |
| 24 | ISCED | numeric | ISCED field of study code | No | — | ~50 | 0% | Program dimension |
| 25 | NLQF | numeric | Dutch Qualifications Framework level | No | 5, 6, 7 | 3 | 0% | Program dimension |
| 26 | WAARDEDOCUMENTSOORT | text | Certificate type | No | GETUIGSCHRIFT | 1–2 | 0% | Dimension |
| 27 | VORM | text | Education delivery form | Yes | VOLTIJD, DEELTIJD | 2–3 | Unknown | Program dimension |
| 28 | VOERTAAL | text | Language of instruction | Yes | NLD, ENG | 2–3 | Unknown | Program dimension |
| 29 | BEGINDATUM | timestamp | Program accreditation start date | No | 2002-09-01, 2015-09-01 | — | 0% | Slowly changing dimension |
| 30 | EINDDATUM | timestamp | Program accreditation end date | Yes | — | — | High | Slowly changing dimension |
| 31 | AANGEBODEN_OPLEIDING_BEGINDATUM | timestamp | Offered program start date | Yes | — | — | Unknown | Offering timeline |
| 32 | AANGEBODEN_OPLEIDING_EINDDATUM | timestamp | Offered program end date | Yes | — | — | Unknown | Offering timeline |
| 33 | EERSTE_INSTROOMDATUM | timestamp | First enrollment open date | Yes | — | — | Unknown | Offering timeline |
| 34 | LAATSTE_INSTROOMDATUM | timestamp | Last enrollment close date | Yes | — | — | Unknown | Offering timeline |
| 35 | DEFICIENTIE | text | Deficiency/prerequisite requirements | Yes | — | — | High | Program requirement |
| 36 | EISEN_WERKZAAMHEDEN | text | Work experience requirements | Yes | — | — | High | Program requirement |
| 37 | PROPEDEUTISCHE_FASE | text | Propaedeutic phase indicator | Yes | — | Low | Unknown | Program attribute |
| 38 | STUDIEKEUZECHECK | text | Study choice check indicator | Yes | — | Low | Unknown | Program attribute |
| 39 | VERSNELD_TRAJECT | text | Accelerated track indicator | Yes | — | Low | Unknown | Program attribute |
| 40 | PENVOERDER | text | Lead institution for joint programs | Yes | — | ~90 | High | Relationship field |
| 41 | SAMENWERKEND_MET | text | Cooperating institutions | Yes | — | — | Very high | Relationship field |
| 42 | BUITENLANDSEPARTNER | text | International partners | Yes | — | — | Very high | Rarely populated |
| 43 | WEBSITE | text | Program website URL | Yes | — | ~700 | Unknown | Informational |
| 44 | OMSCHRIJVING | text | Program description (free text) | Yes | — | — | Unknown | Informational |
| 45 | _id | int | CKAN internal row ID | No | 1–7090 | 7090 | 0% | System field |

#### Data Quality Notes (ho_opleidingsoverzicht)

- [ ] Dataset covers all HO (HBO + WO) — must filter `NIVEAU IN ('HBO-BA','HBO-MA','HBO-AD')` for HBO scope
- [ ] `SOORT` = "OPLEIDING" for all records — redundant field in this dataset
- [ ] Many nullable fields have unknown null rates — especially location fields (ONDERWIJSLOCATIECODE etc.), name variants, and timeline fields
- [ ] `EINDDATUM` null for active programs — treat null as "currently active"

---

### Dataset: overzicht-erkenningen-ho — Overzicht Erkenningen HO

Reference dataset of OCW-recognized HO programs and their accreditation status from the RIO register. Covers both HBO and WO.

**Row count:** 6,747 | **Grain:** One row per program recognition per institution branch | **Scope:** All HO — filter NIVEAU for HBO

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | BEVOEGD_GEZAG_CODE | text | Governing board code | No | 20045, 24832 | ~90 | 0% | Institution dimension key |
| 2 | BEVOEGD_GEZAG_NAAM | text | Governing board name | No | Protestantse Theologische Universiteit | ~90 | 0% | Institution dimension |
| 3 | INSTELLINGSCODE | text | Institution code (BRIN) | No | 00DV, 00IC | ~200 | 0% | Institution dimension key (BRIN) |
| 4 | INSTELLINGSNAAM | text | Institution name | No | Protestantse Theologische Universiteit | ~200 | 0% | Institution dimension |
| 5 | VESTIGINGSCODE | text | Branch/campus code | No | 00DV01, 00IC01 | ~500 | 0% | Location dimension key |
| 6 | VESTIGINGSNAAM | text | Branch/campus name | No | Protestantse Theologische Universiteit; Utrecht | ~500 | 0% | Location dimension |
| 7 | GEMEENTENAAM | text | Municipality name | No | Utrecht, Amsterdam | ~100 | 0% | Geography dimension |
| 8 | PLAATSNAAM | text | City name (uppercase) | No | UTRECHT, AMSTERDAM | ~100 | 0% | Geography dimension |
| 9 | ERKENDEOPLEIDINGSCODE | text | CROHO program code | No | 56109, 60254 | ~700 | 0% | Program dimension key (CROHO) |
| 10 | INSTROOM_EINDDATUM | timestamp | Last enrollment date (null = active) | Yes | null, 2025-08-31 | — | High | Program timeline |
| 11 | OPLEIDINGSEENHEIDCODE | text | Program unit code (RIO) | No | 1016O1755, 1001O6573 | ~700 | 0% | Program dimension key (RIO) |
| 12 | EIGEN_OPLEIDINGSEENHEIDSLEUTEL | text | Institution's own program key | Yes | — | ~700 | Unknown | Institution-internal |
| 13 | OPLEIDINGSEENHEID_NAAM | text | Program name (Dutch) | No | Theologie | ~700 | 0% | Program dimension |
| 14 | OPLEIDINGSEENHEID_INTERNATIONALE_NAAM | text | Program name (English) | Yes | Theology | ~700 | Unknown | Program dimension |
| 15 | OPLEIDINGSEENHEID_SOORT | text | Program type | No | — | ~5 | 0% | Program dimension |
| 16 | STUDIELAST | numeric | ECTS credits | No | 180, 60 | ~10 | 0% | Program attribute |
| 17 | STUDIELASTEENHEID | text | Credits unit | No | ECTS | 1 | 0% | Informational |
| 18 | NIVEAU | text | Education level | No | WO-BA, WO-MA, HBO-BA | 5 | 0% | Program dimension — **use as scope filter** |
| 19 | GRAAD | text | Degree type | No | BACHELOR, MASTER | 3 | 0% | Program dimension |
| 20 | GRAADTOEVOEGING | text | Degree suffix (e.g. of Science) | Yes | — | ~5 | Unknown | Program dimension |
| 21 | ISCED | numeric | ISCED field of study code | No | — | ~50 | 0% | Program dimension |
| 22 | NLQF | numeric | Dutch Qualifications Framework level | No | — | 3 | 0% | Program dimension |
| 23 | EQF | numeric | European Qualifications Framework level | No | — | 3 | 0% | Program dimension |
| 24 | VORM | text | Education delivery form | No | VOLTIJD, DEELTIJD | 3 | 0% | Program dimension |
| 25 | ONDERDEEL | text | ISCED sector / domain | No | TAAL_EN_CULTUUR, ONDERWIJS | 8 | 0% | Program dimension |
| 26 | SUBONDERDEEL | text | Sub-sector / sub-domain | No | — | ~16 | 0% | Program dimension |
| 27 | BEKOSTIGINGSNIVEAU | text | Funding level | No | LAAG | ~3 | 0% | Funding dimension |
| 28 | GRONDSLAG_STUDIELAST | text | Basis for study load determination | Yes | — | ~5 | Unknown | Program attribute |
| 29 | BEROEPSEISEN | text | Professional requirements | Yes | — | ~5 | Unknown | Program attribute |
| 30 | OPLEIDINGSERKENNINGSKADER | text | Recognition framework | Yes | — | ~5 | Unknown | Regulatory |
| 31 | INTENSIEFPROGRAMMA | text | Intensive program indicator | Yes | — | 2 | Unknown | Program attribute |
| 32 | BEKOSTIGINGSCODE | text | Funding type | No | BEKOSTIGD | 2 | 0% | Funding dimension |
| 33 | AANVULLENDE_EISEN | text | Additional admission requirements | Yes | — | ~5 | Unknown | Program attribute |
| 34 | BEKOSTIGINGSDUUR | numeric | Funded duration (years) | No | — | ~5 | 0% | Program attribute |
| 35 | VESTIGINGSLICENTIE_BEGINDATUM | timestamp | Branch license start date | No | — | — | 0% | Program timeline |
| 36 | VESTIGINGSLICENTIE_EINDDATUM | timestamp | Branch license end date (null = active) | Yes | — | — | High | Program timeline |
| 37 | ACCREDITATIE_BESLUITDATUM | timestamp | Accreditation decision date | No | — | — | 0% | Accreditation timeline |
| 38 | ACCREDITATIE_BEGINDATUM | timestamp | Accreditation start date | No | 2025-09-01, 2020-04-06 | — | 0% | Accreditation timeline |
| 39 | ACCREDITATIE_VERVALDATUM | timestamp | Accreditation expiry date | Yes | — | — | Unknown | Accreditation timeline |
| 40 | ACCREDITATIE_AFBOUWDATUM | timestamp | Phase-out date | Yes | — | — | High | Accreditation timeline |
| 41 | ACCREDITATIE_INLEVERDATUM | timestamp | Submission deadline date | Yes | — | — | High | Accreditation timeline |
| 42 | ACCREDITATIE_VOORWAARDENDATUM | timestamp | Conditional accreditation date | Yes | — | — | High | Accreditation timeline |
| 43 | ACCREDITATIE_INTREKKINGSDATUM | text | Accreditation revocation date | Yes | — | — | High | Accreditation timeline |
| 44 | ACCREDITATIE_UITSTELDATUM | timestamp | Accreditation postponement date | Yes | — | — | High | Accreditation timeline |
| 45 | ACCREDITATIE_UITSTELREDEN | text | Reason for postponement | Yes | — | — | High | Accreditation metadata |
| 46 | SAMENWERKENDEINSTELLINGEN | text | Cooperating institutions | Yes | — | — | High | Relationship field |
| 47 | _id | int | CKAN internal row ID | No | 1–6747 | 6747 | 0% | System field |

#### Data Quality Notes (overzicht-erkenningen-ho)

- [ ] Dataset covers all HO (HBO + WO) — filter `NIVEAU` for HBO scope
- [ ] `ERKENDEOPLEIDINGSCODE` stored as text here vs numeric in ho_opleidingsoverzicht — type mismatch requires cast when joining on CROHO code
- [ ] Many accreditation date fields expected to be mostly null (only populated when the specific event occurred)
- [ ] `INSTROOM_EINDDATUM` null indicates program is currently accepting enrollments

---

### Dataset: Adressen hogescholen en universiteiten

Reference dataset with visiting and mailing addresses for all HBO and WO institutions. One row per institution (primary campus only).

**Row count:** ~50 | **Grain:** One row per institution | **Scope:** All HO — filter `SOORT HO` = 'hbo' for HBO
**Source:** RIO | **Update frequency:** Monthly

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | SOORT HO | text | Education type (lowercase) | No | hbo, wo | 2 | 0% | Scope filter |
| 2 | PROVINCIE | text | Province | No | Friesland, Gelderland | 12 | 0% | Geography dimension |
| 3 | BEVOEGD GEZAG NUMMER | text | Governing board number | No | 30156, 40235 | ~50 | 0% | Institution dimension key |
| 4 | INSTELLINGSCODE | text | Institution code (BRIN) | No | 31FR, 25BA | ~50 | 0% | Institution dimension key (BRIN) |
| 5 | INSTELLINGSNAAM | text | Institution name | No | NHL Stenden Hogeschool, CHE | ~50 | 0% | Institution dimension |
| 6 | STRAATNAAM | text | Street name (visiting address) | No | Rengerslaan, Oude Kerkweg | ~50 | 0% | Address attribute |
| 7 | HUISNUMMER-TOEVOEGING | text | House number + suffix | No | 10, 100 | ~50 | 0% | Address attribute |
| 8 | POSTCODE | text | Postal code (visiting) | No | 8917 DD, 6717 JS | ~50 | 0% | Address attribute |
| 9 | PLAATSNAAM | text | City (visiting address, uppercase) | No | LEEUWARDEN, EDE | ~50 | 0% | Geography dimension |
| 10 | GEMEENTENUMMER | text | Municipality code (CBS) | No | 0080, 0228 | ~50 | 0% | Geography dimension key |
| 11 | GEMEENTENAAM | text | Municipality name (uppercase) | No | LEEUWARDEN, EDE | ~50 | 0% | Geography dimension |
| 12 | DENOMINATIE | text | Religious/philosophical affiliation | No | Overige, Protestants-Christelijk | ~5 | 0% | Institution attribute |
| 13 | TELEFOONNUMMER | text | Phone number | Yes | 0582512345 | ~50 | Unknown | Contact info |
| 14 | INTERNETADRES | text | Website URL | Yes | www.nhl.nl | ~50 | Unknown | Contact info |
| 15 | STRAATNAAM CORRESPONDENTIEADRES | text | Street name (mailing address) | Yes | Postbus | ~50 | Unknown | Address attribute |
| 16 | HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES | text | House number (mailing) | Yes | 1080 | ~50 | Unknown | Address attribute |
| 17 | POSTCODE CORRESPONDENTIEADRES | text | Postal code (mailing) | Yes | 8900 CB | ~50 | Unknown | Address attribute |
| 18 | PLAATSNAAM CORRESPONDENTIEADRES | text | City (mailing address) | Yes | LEEUWARDEN | ~50 | Unknown | Address attribute |
| 19 | NODAAL GEBIED CODE | text | Nodal region code | No | 10, 29 | ~40 | 0% | Geography dimension |
| 20 | NODAAL GEBIED NAAM | text | Nodal region name | No | Leeuwarden, Ede | ~40 | 0% | Geography dimension |
| 21 | RPA-GEBIED CODE | text | RPA region code | No | 04, 10 | ~30 | 0% | Geography dimension |
| 22 | RPA-GEBIED NAAM | text | RPA region name | No | Fryslân, De Vallei | ~30 | 0% | Geography dimension |
| 23 | WGR-GEBIED CODE | text | WGR region code | No | 04, 16 | ~30 | 0% | Geography dimension |
| 24 | WGR-GEBIED NAAM | text | WGR region name | No | Friesland-Noord, Eem en Vallei | ~30 | 0% | Geography dimension |
| 25 | COROPGEBIED CODE | text | COROP region code | No | 04, 13 | ~40 | 0% | Geography dimension |
| 26 | COROPGEBIED NAAM | text | COROP region name | No | Noord-Friesland, Veluwe | ~40 | 0% | Geography dimension |
| 27 | ONDERWIJSGEBIED CODE | text | Education region code | No | 03, 09 | ~12 | 0% | Geography dimension |
| 28 | ONDERWIJSGEBIED NAAM | text | Education region name | No | Friesland, Arnhem en omstreken | ~12 | 0% | Geography dimension |
| 29 | RMC-REGIO CODE | text | RMC region code | No | 04, 16 | ~39 | 0% | Geography dimension |
| 30 | RMC-REGIO NAAM | text | RMC region name | No | Friesland Noord, Eem en Vallei | ~39 | 0% | Geography dimension |

#### Data Quality Notes (Adressen hogescholen)

- [ ] Column names contain spaces — requires transformation (quoting or renaming) before loading
- [ ] `SOORT HO` is lowercase ("hbo", "wo") — inconsistent with uppercase convention in statistical datasets
- [ ] Only primary campus address per institution — institutions with multiple locations have one row
- [ ] `GEMEENTENAAM` and `PLAATSNAAM` are uppercase — same field, different casing vs statistical datasets
- [ ] Six regional classification systems present (Nodaal, RPA, WGR, COROP, Onderwijsgebied, RMC) — alternative geography hierarchies; most can be collapsed into one dim_geography

---

### Dataset: Adressen besturen hogescholen en universiteiten

Reference dataset with addresses for governing boards (bevoegde gezagen) of all HBO and WO institutions.

**Row count:** ~50 | **Grain:** One row per governing board | **Scope:** All HO — filter `SOORT HO` = 'hbo' for HBO
**Update frequency:** Monthly

| # | Field | Type | Description | Nullable | Sample Values | Cardinality | Null % | Role Guess |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | SOORT HO | text | Education type (lowercase) | No | hbo, wo | 2 | 0% | Scope filter |
| 2 | BEVOEGD GEZAG NUMMER | text | Governing board number | No | 24832, 28901, 29615 | ~50 | 0% | **Governing board key** |
| 3 | BEVOEGD GEZAG NAAM | text | Governing board name | No | Stichting Codarts, Stichting HKU | ~50 | 0% | Governing board dimension |
| 4 | STRAATNAAM | text | Street name (visiting address) | No | Kruisplein, Nieuwekade | ~50 | 0% | Address attribute |
| 5 | HUISNUMMER-TOEVOEGING | text | House number + suffix | No | 26, 1 | ~50 | 0% | Address attribute |
| 6 | POSTCODE | text | Postal code (visiting) | No | 3012 CC, 3511 RV | ~50 | 0% | Address attribute |
| 7 | PLAATSNAAM | text | City (visiting address, uppercase) | No | ROTTERDAM, UTRECHT | ~50 | 0% | Geography dimension |
| 8 | GEMEENTENUMMER | text | Municipality code (CBS) | No | 0599, 0344 | ~50 | 0% | Geography dimension key |
| 9 | GEMEENTENAAM | text | Municipality name (uppercase) | No | ROTTERDAM, UTRECHT | ~50 | 0% | Geography dimension |
| 10 | DENOMINATIE | text | Religious/philosophical affiliation | No | Algemeen bijzonder, Openbaar | ~5 | 0% | Institution attribute |
| 11 | TELEFOONNUMMER | text | Phone number | Yes | 0102171100 | ~50 | Unknown | Contact info |
| 12 | INTERNETADRES | text | Website URL | Yes | www.codarts.nl | ~50 | Unknown | Contact info |
| 13 | STRAATNAAM CORRESPONDENTIEADRES | text | Street name (mailing address) | Yes | Kruisplein, Postbus | ~50 | Unknown | Address attribute |
| 14 | HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES | text | House number (mailing) | Yes | 26, 1520 | ~50 | Unknown | Address attribute |
| 15 | POSTCODE CORRESPONDENTIEADRES | text | Postal code (mailing) | Yes | 3012 CC, 3500 BM | ~50 | Unknown | Address attribute |
| 16 | PLAATSNAAM CORRESPONDENTIEADRES | text | City (mailing address) | Yes | ROTTERDAM, UTRECHT | ~50 | Unknown | Address attribute |
| 17 | ADMINISTRATIEKANTOORNUMMER | text | Administrative office number | Yes | 164, 639 | ~50 | Unknown | Cross-reference |
| 18 | KVK-NUMMER | text | Chamber of Commerce number | Yes | 41126801, 41178974 | ~50 | Unknown | Legal identifier |

#### Data Quality Notes (Adressen besturen)

- [ ] Column names contain spaces — same transformation needed as Adressen hogescholen
- [ ] `BEVOEGD GEZAG NUMMER` values differ in format from `BEVOEGD_GEZAG_CODE` in overzicht-erkenningen-ho (e.g. "24832" vs "20045") — verify if same namespace before joining

---

## Relationships

| Source | Target | Relationship | Confidence | Notes |
|--------|--------|--------------|------------|-------|
| p01hoinges.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | High | Both are BRIN codes; statistical datasets join to address lookup |
| p01hoinges.INSTELLINGSCODE_ACTUEEL | overzicht-erkenningen-ho.INSTELLINGSCODE | N:1 | High | BRIN code: multiple programs per institution |
| p02ho1ejrs.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | High | Same as p01 |
| p03hoinschr.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | High | Same as p01 |
| p04hogdipl.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | High | Same as p01 |
| p01b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | High | CROHO code joins statistical data to program master (both numeric) |
| p02b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | High | Same as p01b |
| p03b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | High | Same as p01b |
| p04b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | High | Same as p01b |
| ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | overzicht-erkenningen-ho.ERKENDEOPLEIDINGSCODE | 1:N | High | **Type mismatch**: numeric vs text — needs CAST when joining on CROHO code |
| ho_opleidingsoverzicht.OPLEIDINGSEENHEIDCODE | overzicht-erkenningen-ho.OPLEIDINGSEENHEIDCODE | 1:N | High | RIO program unit code — consistent text type |
| adressen-hogescholen.INSTELLINGSCODE | overzicht-erkenningen-ho.INSTELLINGSCODE | 1:N | High | BRIN code: one institution address → many program accreditations |
| adressen-hogescholen.BEVOEGD GEZAG NUMMER | adressen-besturen.BEVOEGD GEZAG NUMMER | N:1 | High | Governing board number: institution → board address |
| adressen-hogescholen.BEVOEGD GEZAG NUMMER | overzicht-erkenningen-ho.BEVOEGD_GEZAG_CODE | N:1 | Medium | Same governing board concept; **verify value overlap** — naming/format differ |
| p01–p04.ONDERDEEL | overzicht-erkenningen-ho.ONDERDEEL | N:N | High | Shared vocabulary (TECHNIEK, ECONOMIE, etc.) — same classification system |
| p01–p04.SUBONDERDEEL | overzicht-erkenningen-ho.SUBONDERDEEL | N:N | High | Shared vocabulary |

---

## Data Quality Notes

- [ ] **Privacy suppression (all p01–p04):** Measure fields use `-1` for counts < 5 (GDPR). DUO documentation states values < 5 are displayed as 4, but actual data uses -1. Rate in p01 resource 1a: 5.7% (273/4,833 records). Rates for p02–p04 not yet measured.
- [ ] **p01 vs p03 semantic overlap:** "Ingeschrevenen" (enrolled persons) vs "Inschrijvingen" (enrollments) — almost identical structure and similar row counts (15,892 vs 15,900 total). Exact semantic difference needs verification with DUO documentation.
- [ ] **Year field naming inconsistency:** p01–p03 use `STUDIEJAAR`, p04 uses `DIPLOMAJAAR`. Both are integers representing academic/calendar year but describe different events.
- [ ] **SOORT_INSTELLING always = "reguliere inst."** in all p01–p04 datasets — zero analytical value for HBO-only scope. May differ when combining with WO data.
- [ ] **TYPE_HOGER_ONDERWIJS absent from p04hogdipl** — replaced by `SOORT_DIPLOMA`. Same concept, different vocabulary: "bachelor" (p01–p03) vs "hbo bachelor" (p04).
- [ ] **Column naming convention mismatch:** p01–p04 use UPPER_SNAKE_CASE. Address datasets use "UPPER CASE WITH SPACES". Needs normalization during loading.
- [ ] **CROHO code type mismatch:** `ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE` is numeric; `overzicht-erkenningen-ho.ERKENDEOPLEIDINGSCODE` is text. Values are equivalent — requires CAST when joining.
- [ ] **Reference datasets cover all HO (HBO + WO):** Filter ho_opleidingsoverzicht and overzicht-erkenningen-ho by `NIVEAU IN ('HBO-BA','HBO-MA','HBO-AD')` to scope to HBO.
- [ ] **GEMEENTENUMMER stored as text** (leading zeros, e.g. "0106") across all datasets — consistent, but must not be cast to integer.
- [ ] **Three resource splits per dataset (p01–p04):** Each statistical dataset has 3 resources representing different cross-tabulations (gender, program code, education form). These are NOT independent — they represent different aggregations of the same underlying data. Cannot be simply unioned or joined without double-counting.
- [ ] **Null rates for reference dataset nullable fields unknown** — especially EINDDATUM (null for active programs), location fields in ho_opleidingsoverzicht, and accreditation date fields in overzicht-erkenningen-ho.
- [ ] **DIPLOMAJAAR historical window may differ** — samples show 2019 as earliest value for p04hogdipl vs 2020 for p01–p03. Verify full available year range.
- [ ] **GEMEENTENAAM casing inconsistency:** Uppercase in address datasets ("LEEUWARDEN"), mixed case in statistical datasets ("Leeuwarden"). Needs normalization for joining.
