# Fase 4: Ontwerp Dimensioneel Model — DUO HBO

**Auteur:** Anne Leemans, in samenwerking met Claude Sonnet 4.6
**Datum:** 2026-02-20
**Basis:** Metagegevenscatalogus (Fase 1), Bronanalyse (Fase 2), Ruwe data (Fase 3)

---

## Kernuitdaging

DUO levert **pre-geaggregeerde snapshots**, geen transactierecords. Elke dataset (p01–p04) heeft **drie bronbestanden** (a/b/c) die verschillende kruistabellaties zijn van dezelfde onderliggende data:

| Variant | Extra dimensie | Granulariteit op opleiding |
|---------|---------------|---------------------------|
| a (geslacht) | GESLACHT | Grof: ONDERDEEL + SUBONDERDEEL + TYPE_HOGER_ONDERWIJS |
| b (opleiding) | OPLEIDINGSCODE (CROHO) | Fijn: individuele opleiding |
| c (opleidingsvorm) | OPLEIDINGSVORM | Grof: ONDERDEEL + SUBONDERDEEL + TYPE_HOGER_ONDERWIJS |

Deze zijn **niet combineerbaar** — samenvoegen leidt tot dubbeltellingen.

---

## Ontwerpbeslissingen

### Beslissing 1: Drie feitentabelfamilies

Drie bedrijfsprocessen, elk met de b-variant als **primaire feitentabel** (fijnste korrel op opleidingsniveau):

| # | Feitentabel | Bron | Korrel (één rij = ...) | Meetwaarde |
|---|-------------|------|------------------------|------------|
| 1 | `feit_ingeschrevenen` | p01b | studiejaar × gemeente × instelling × opleiding(CROHO) | AANTAL_INGESCHREVENEN |
| 2 | `feit_eerstejaars` | p02b | studiejaar × gemeente × instelling × opleiding(CROHO) | AANTAL_EERSTEJAARS_INGESCHREVENEN |
| 3 | `feit_gediplomeerden` | p04b | diplomajaar × gemeente × instelling × opleiding(CROHO) × soort_diploma | AANTAL_GEDIPLOMEERDEN |

**Aanvullende feitentabellen** (bouwen indien nodig):

| # | Feitentabel | Bron | Extra dimensie t.o.v. primair |
|---|-------------|------|-------------------------------|
| 4 | `feit_ingeschrevenen_geslacht` | p01a | + GESLACHT (maar zonder CROHO-code) |
| 5 | `feit_ingeschrevenen_oplvorm` | p01c | + OPLEIDINGSVORM (maar zonder CROHO-code) |
| 6–7 | `feit_eerstejaars_geslacht/_oplvorm` | p02a/c | idem |
| 8–9 | `feit_gediplomeerden_geslacht/_oplvorm` | p04a/c | idem |

**Motivatie:** De b-variant biedt CROHO-code-niveau detail, wat de meest bruikbare analyse-as is (welke specifieke opleiding?). De a/c-varianten voegen geslacht resp. opleidingsvorm toe, maar op een grover opleidingsniveau (sector). Omdat de varianten niet combineerbaar zijn, worden ze als aparte feitentabellen gemodelleerd.

### Beslissing 2: p03 (inschrijvingen) wordt overgeslagen

p01 (ingeschrevenen = unieke personen) en p03 (inschrijvingen = inschrijvingsrecords) hebben bijna identieke structuur en aantallen (~15.900 rijen). Het verschil is semantisch (personen vs. inschrijvingen) maar voor deze proof of concept niet cruciaal. p01 is de primaire bron. p03 kan later als aparte feitentabelfamilie worden toegevoegd.

### Beslissing 3: Twee dimensieniveaus voor opleidingen

De a/c-varianten missen CROHO-code en werken op sector/subsector-niveau. Dit vereist **twee aparte dimensies**:
- `dim_opleiding` — CROHO-niveau (voor primaire feitentabellen)
- `dim_sector` — ONDERDEEL + SUBONDERDEEL + TYPE_HOGER_ONDERWIJS (voor aanvullende feitentabellen)

**Motivatie:** Een feitentabel kan niet verwijzen naar een dimensie op een fijner niveau dan de korrel van de data toelaat. De a/c-bestanden bevatten geen CROHO-code, dus ze kunnen niet joinen op `dim_opleiding`. Een apart `dim_sector` voorkomt NULL-sleutels in de feitentabel.

### Beslissing 4: Eén gedeelde tijddimensie

`dim_tijd` bevat alle jaren (2019–2024). Feitentabellen verwijzen met FK naar deze dimensie, ongeacht of het een STUDIEJAAR of DIPLOMAJAAR betreft. Het type jaar is impliciet in de feitentabel zelf.

**Motivatie:** Het jaarbereik overlapt (2019–2024). Een gedeelde dimensie maakt drill-across queries mogelijk (bijv. "vergelijk inschrijvingen en diploma's in hetzelfde jaar"). De semantiek van het jaar (peildatum vs. diplomajaar) wordt door de feitentabel bepaald, niet door de dimensie.

### Beslissing 5: SCD Type 1 (alleen huidige waarden)

DUO levert alleen `_ACTUEEL`-velden (huidige instellingscode/naam). Historische codes zijn niet beschikbaar. Daarom: **SCD Type 1** — overschrijf bij wijziging. Geen historische tracking mogelijk met deze brondata.

### Beslissing 6: Privacyonderdrukking als NULL

`AANTAL = -1` (DUO's AVG-filter voor waarden < 5) wordt bij laden omgezet naar `NULL`. Dit voorkomt dat -1 meetelt in SUM/AVG-berekeningen. Een vlag `is_onderdrukt` (boolean) wordt toegevoegd aan feitentabellen.

**Motivatie:** NULL wordt correct genegeerd door SQL-aggregatiefuncties. De boolean-vlag maakt het mogelijk om het percentage onderdrukte records te rapporteren.

---

## Sterrenmodel — Dimensietabellen

### `dim_tijd`

Kleine dimensie (6 rijen). Alle jaren uit het beschikbare bereik.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| tijd_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| jaar | INT (NK) | STUDIEJAAR / DIPLOMAJAAR | Natuurlijke sleutel (2019, 2020, ...) |
| academisch_jaar_label | TEXT | Afgeleid | "2020/2021" |
| decennium | INT | Afgeleid | 2020 |

### `dim_instelling`

~36 rijen (HBO-instellingen). Verrijkt met adresgegevens.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| instelling_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| brin_code | TEXT (NK) | INSTELLINGSCODE_ACTUEEL | Natuurlijke sleutel (4 chars) |
| instellingsnaam | TEXT | INSTELLINGSNAAM_ACTUEEL | Huidige naam |
| soort_instelling | TEXT | SOORT_INSTELLING | "reguliere inst." |
| denominatie | TEXT | adressen.DENOMINATIE | Religieuze/filosofische achtergrond |
| bevoegd_gezag_nummer | TEXT | adressen.BEVOEGD GEZAG NUMMER | FK naar dim_bestuur |
| straatnaam | TEXT | adressen.STRAATNAAM | Bezoekadres |
| postcode | TEXT | adressen.POSTCODE | Bezoekadres |
| plaatsnaam | TEXT | adressen.PLAATSNAAM | Bezoekadres |
| website | TEXT | adressen.INTERNETADRES | Website |

**Bronnen:** Primaire attributen uit p01–p04 statistische datasets. Verrijking (denominatie, adres, website) via LEFT JOIN op `adressen-hogescholen` op BRIN-code.

**Let op:** Adressen-bestand gebruikt `;`-separator en kolomnamen met spaties. Vereist transformatie bij laden.

### `dim_opleiding`

~247 rijen (unieke CROHO-codes in HBO-data). Verrijkt met RIO-registerdata.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| opleiding_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| croho_code | INT (NK) | OPLEIDINGSCODE_ACTUEEL | Natuurlijke sleutel |
| opleidingsnaam | TEXT | OPLEIDINGSNAAM_ACTUEEL | Huidige naam |
| type_hoger_onderwijs | TEXT | TYPE_HOGER_ONDERWIJS | bachelor / associate degree / master |
| onderdeel | TEXT | ONDERDEEL | ISCED-sector (TECHNIEK, ECONOMIE, ...) |
| subonderdeel | TEXT | SUBONDERDEEL | Subsector |
| graad | TEXT | ho_opleidingsoverzicht.GRAAD | BACHELOR / MASTER / ASSOCIATE_DEGREE |
| studielast_ects | INT | ho_opleidingsoverzicht.STUDIELAST | ECTS-punten |
| eqf_niveau | INT | ho_opleidingsoverzicht.EQF | EQF-niveau (5/6/7) |
| isced_code | INT | ho_opleidingsoverzicht.ISCED | ISCED-studierichting |
| nlqf_niveau | INT | ho_opleidingsoverzicht.NLQF | NLQF-niveau |
| voertaal | TEXT | ho_opleidingsoverzicht.VOERTAAL | NLD / ENG |

**Bronnen:** Basisattributen (CROHO, naam, sector) uit p01b–p04b. Verrijking (ECTS, EQF, ISCED, voertaal) via LEFT JOIN op `ho_opleidingsoverzicht` op CROHO-code (`OPLEIDINGSCODE_ACTUEEL` = `ERKENDEOPLEIDINGSCODE`).

**Let op:** ho_opleidingsoverzicht bevat meerdere rijen per CROHO-code (per locatie/vorm). Bij de join moet gededupliceerd worden op CROHO-code.

### `dim_sector`

~48 rijen (unieke combinaties). Gebruikt door aanvullende feitentabellen (a/c-varianten).

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| sector_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| onderdeel | TEXT (NK deel) | ONDERDEEL | ISCED-sector |
| subonderdeel | TEXT (NK deel) | SUBONDERDEEL | Subsector |
| type_hoger_onderwijs | TEXT (NK deel) | TYPE_HOGER_ONDERWIJS | bachelor / associate degree / master |

**Samengestelde natuurlijke sleutel:** (onderdeel, subonderdeel, type_hoger_onderwijs)

### `dim_geografie`

~52 rijen (unieke gemeenten in HBO-data). Verrijkt met regionale indelingen.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| geografie_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| gemeentenummer | TEXT (NK) | GEMEENTENUMMER | CBS-code met voorloopnullen |
| gemeentenaam | TEXT | GEMEENTENAAM | Genormaliseerd (mixed case) |
| provincienaam | TEXT | PROVINCIENAAM | Provincienaam |
| corop_code | TEXT | adressen.COROPGEBIED CODE | COROP-regiocode |
| corop_naam | TEXT | adressen.COROPGEBIED NAAM | COROP-regionaam |
| rpa_code | TEXT | adressen.RPA-GEBIED CODE | RPA-regiocode |
| rpa_naam | TEXT | adressen.RPA-GEBIED NAAM | RPA-regionaam |

**Bronnen:** Basisattributen (gemeentenummer, -naam, provincie) uit statistische datasets. Verrijking (COROP, RPA) via LEFT JOIN op `adressen-hogescholen` op gemeentenummer.

**Let op:** Gemeentenaam is mixed case in statistische datasets ("Leeuwarden") maar UPPER CASE in adressen ("LEEUWARDEN"). Normalisatie nodig.

**Hiërarchie:** Gemeente → Provincie (altijd beschikbaar). Gemeente → COROP → (landelijk) als alternatieve hiërarchie.

### `dim_geslacht`

2 rijen.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| geslacht_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| geslacht | TEXT (NK) | GESLACHT | MAN / VROUW |

### `dim_opleidingsvorm`

3 rijen.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| opleidingsvorm_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| opleidingsvorm_code | TEXT (NK) | OPLEIDINGSVORM | VT / DT / DU |
| opleidingsvorm_naam | TEXT | Afgeleid | Voltijd / Deeltijd / Duaal |

### `dim_bestuur`

~36 rijen (unieke bevoegde gezagen voor HBO).

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| bestuur_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| bevoegd_gezag_nummer | TEXT (NK) | BEVOEGD GEZAG NUMMER | Natuurlijke sleutel |
| bevoegd_gezag_naam | TEXT | BEVOEGD GEZAG NAAM | Naam |
| denominatie | TEXT | DENOMINATIE | Religieuze achtergrond |
| plaatsnaam | TEXT | PLAATSNAAM | Vestigingsplaats |
| kvk_nummer | TEXT | KVK-NUMMER | KvK-registratie |

**Bron:** adressen-besturen. Gekoppeld aan dim_instelling via bevoegd_gezag_nummer (outrigger-relatie).

### `dim_soort_diploma`

3 rijen. Alleen gebruikt door feit_gediplomeerden.

| Kolom | Type | Bron | Beschrijving |
|-------|------|------|-------------|
| soort_diploma_key | INT (SK) | Gegenereerd | Surrogaatsleutel |
| soort_diploma | TEXT (NK) | SOORT_DIPLOMA | hbo bachelor / hbo associate degree / hbo master |

---

## Sterrenmodel — Feitentabellen

### Primaire feitentabellen

#### `feit_ingeschrevenen`

| Kolom | Type | Beschrijving |
|-------|------|-------------|
| ingeschrevenen_key | INT (SK) | Surrogaatsleutel |
| tijd_key | INT (FK) | → dim_tijd (STUDIEJAAR) |
| instelling_key | INT (FK) | → dim_instelling |
| opleiding_key | INT (FK) | → dim_opleiding |
| geografie_key | INT (FK) | → dim_geografie |
| aantal_ingeschrevenen | INT | Meetwaarde (NULL indien onderdrukt) |
| is_onderdrukt | BOOLEAN | TRUE als originele waarde = -1 |

**Korrel:** Eén rij per studiejaar × gemeente × instelling × opleiding (CROHO)
**Bron:** p01b — `ingeschrevenenhbo.csv` (7.170 rijen)
**Type:** Periodieke snapshot feitentabel

#### `feit_eerstejaars`

Identieke structuur als `feit_ingeschrevenen`, met:
- Meetwaarde: `aantal_eerstejaars` i.p.v. `aantal_ingeschrevenen`

**Bron:** p02b — `eerstejaarsingeschrevenenhbo.csv` (5.834 rijen)

#### `feit_gediplomeerden`

| Kolom | Type | Beschrijving |
|-------|------|-------------|
| gediplomeerden_key | INT (SK) | Surrogaatsleutel |
| tijd_key | INT (FK) | → dim_tijd (DIPLOMAJAAR) |
| instelling_key | INT (FK) | → dim_instelling |
| opleiding_key | INT (FK) | → dim_opleiding |
| geografie_key | INT (FK) | → dim_geografie |
| soort_diploma_key | INT (FK) | → dim_soort_diploma |
| aantal_gediplomeerden | INT | Meetwaarde (NULL indien onderdrukt) |
| is_onderdrukt | BOOLEAN | TRUE als originele waarde = -1 |

**Korrel:** Eén rij per diplomajaar × gemeente × instelling × opleiding (CROHO) × soort_diploma
**Bron:** p04b — `gediplomeerdenhbo.csv` (6.813 rijen)

### Aanvullende feitentabellen (geslacht-varianten)

#### `feit_ingeschrevenen_geslacht`

| Kolom | Type | Beschrijving |
|-------|------|-------------|
| id | INT (SK) | Surrogaatsleutel |
| tijd_key | INT (FK) | → dim_tijd |
| instelling_key | INT (FK) | → dim_instelling |
| sector_key | INT (FK) | → dim_sector |
| geografie_key | INT (FK) | → dim_geografie |
| geslacht_key | INT (FK) | → dim_geslacht |
| aantal_ingeschrevenen | INT | Meetwaarde |
| is_onderdrukt | BOOLEAN | |

**Korrel:** studiejaar × gemeente × instelling × sector × niveau × geslacht
**Bron:** p01a — `ingeschrevenengeslhbo.csv` (4.833 rijen)

Dezelfde structuur geldt voor:
- `feit_eerstejaars_geslacht` (bron: p02a, 3.407 rijen)
- `feit_gediplomeerden_geslacht` (bron: p04a, 4.445 rijen — met `soort_diploma_key` i.p.v. `type_hoger_onderwijs` in dim_sector)

### Aanvullende feitentabellen (opleidingsvorm-varianten)

#### `feit_ingeschrevenen_oplvorm`

Zelfde structuur als geslacht-variant, maar met `opleidingsvorm_key` (FK → dim_opleidingsvorm) i.p.v. `geslacht_key`.

**Bron:** p01c — `ingeschrevenenoplvhbo.csv` (3.889 rijen)

Dezelfde structuur geldt voor:
- `feit_eerstejaars_oplvorm` (bron: p02c, 2.908 rijen)
- `feit_gediplomeerden_oplvorm` (bron: p04c, 3.591 rijen)

---

## Sterrenmodel — Visueel

### Primaire feitentabellen (b-varianten)

```
                          ┌──────────────┐
                          │  dim_tijd    │
                          │──────────────│
                          │ jaar         │
                          │ acad_jaar    │
                          └──────┬───────┘
                                 │
    ┌──────────────┐    ┌────────┴────────┐    ┌──────────────────┐
    │dim_instelling│    │                 │    │  dim_opleiding   │
    │──────────────│    │ FEIT_INGESCHR   │    │──────────────────│
    │ brin_code    │◄───│ EVENEN          │───►│ croho_code       │
    │ naam         │    │                 │    │ naam             │
    │ denominatie  │    │ aantal_ingeschr │    │ sector           │
    └──────┬───────┘    │ is_onderdrukt   │    │ ects, eqf, isced │
           │            │                 │    └──────────────────┘
    ┌──────┴───────┐    │                 │
    │ dim_bestuur  │    └────────┬────────┘
    │──────────────│             │
    │ bev_gezag_nr │    ┌────────┴────────┐
    │ naam         │    │ dim_geografie   │
    └──────────────┘    │─────────────────│
      (outrigger)       │ gemeentenr      │
                        │ gemeente        │
                        │ provincie       │
                        │ corop           │
                        └─────────────────┘

  Zelfde patroon voor:
  • feit_eerstejaars (zelfde dimensies)
  • feit_gediplomeerden (+dim_soort_diploma)
```

### Aanvullende feitentabellen (a/c-varianten)

```
    ┌──────────────┐    ┌─────────────────────────┐    ┌──────────────┐
    │  dim_sector  │    │ FEIT_INGESCHREVENEN      │    │ dim_geslacht │
    │──────────────│    │ _GESLACHT                │    │──────────────│
    │ onderdeel    │◄───│                          │───►│ geslacht     │
    │ subonderdeel │    │ FK: tijd, instelling,    │    └──────────────┘
    │ type_ho      │    │     sector, geografie,   │
    └──────────────┘    │     geslacht             │
                        │ aantal_ingeschrevenen    │
                        └─────────────────────────┘

    ┌──────────────┐    ┌─────────────────────────┐    ┌────────────────┐
    │  dim_sector  │    │ FEIT_INGESCHREVENEN      │    │dim_opleidings- │
    │──────────────│    │ _OPLVORM                 │    │ vorm           │
    │ onderdeel    │◄───│                          │───►│────────────────│
    │ subonderdeel │    │ FK: tijd, instelling,    │    │ code (VT/DT/DU)│
    │ type_ho      │    │     sector, geografie,   │    │ naam           │
    └──────────────┘    │     opleidingsvorm       │    └────────────────┘
                        │ aantal_ingeschrevenen    │
                        └─────────────────────────┘
```

---

## Dimensiehiërarchieën

| Dimensie | Hiërarchie | Niveaus |
|----------|-----------|---------|
| dim_geografie | Administratief | Gemeente → Provincie |
| dim_geografie | Regionaal | Gemeente → COROP → (landelijk) |
| dim_opleiding | Programma | Opleiding (CROHO) → Subsector → Sector |
| dim_opleiding | Niveau | Opleiding → Graad (AD/BA/MA) → EQF |
| dim_instelling | Bestuurlijk | Instelling → Bestuur (via dim_bestuur) |
| dim_tijd | Kalender | Jaar → Decennium |

---

## Conformiteit met Kimball-methodologie

| Principe | Toepassing |
|----------|-----------|
| Bus-architectuur | Conforme dimensies (dim_tijd, dim_instelling, dim_geografie) worden gedeeld door alle feitentabellen |
| Één feitentabel per korrel | Aparte feitentabellen voor de drie niet-combineerbare varianten (a/b/c) |
| Surrogaatsleutels | Alle dimensies hebben een gegenereerde surrogaatsleutel (niet afhankelijk van bronsleutels) |
| Geen sneeuwvlok | dim_bestuur is een outrigger (gedenormaliseerd in dim_instelling via bevoegd_gezag_nummer), geen FK in de feitentabel |
| Snapshot feitentabel | Alle feitentabellen zijn periodieke snapshots (jaarlijks), geen transactiefeitentabellen |
| SCD strategie | Type 1 (overschrijf) — afgedwongen door databeschikbaarheid, niet door keuze |
| Null-handling | Onbekende/onderdrukte meetwaarden als NULL + boolean vlag |

---

## Bekende beperkingen

1. **Geen student-niveau data** — alleen geaggregeerde aantallen. Geen cohortanalyse, geen doorstroomanalyse mogelijk.
2. **Geslacht, opleiding en opleidingsvorm niet combineerbaar** — drie aparte feitentabelfamilies door DUO's pre-aggregatie. De vraag "hoeveel vrouwen studeren B Elektrotechniek?" is niet beantwoordbaar.
3. **Alleen huidige codes** — `_ACTUEEL`-velden verbergen historische fusies/naamswijzigingen (bijv. NHL + Stenden → NHL Stenden). SCD Type 1 is de enige optie.
4. **Privacyonderdrukking** — 5-7% van meetwaarden is NULL (oorspronkelijk -1). Totalen berekend via SUM zullen iets te laag zijn.
5. **p01 vs p03 niet onderscheidbaar** — semantisch verschil (personen vs. inschrijvingen) niet verifieerbaar zonder DUO-documentatie. p03 is voorlopig uitgesloten.
6. **Geen locatiedimensie** — statistische datasets kennen alleen gemeente, geen campuslocatie. Locatiedata uit ho_opleidingsoverzicht/erkenningen past niet op de korrel van de feitentabellen.
