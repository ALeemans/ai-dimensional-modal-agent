# Metagegevenscatalogus: DUO Open Onderwijsdata — HBO

**Auteur:** Anne Leemans, in samenwerking met Claude Sonnet 4.6
**Datum:** 2026-02-19
**Bron:** DUO Open Onderwijsdata (https://onderwijsdata.duo.nl)

---

## Datasetinventarisatie

| # | Dataset-ID | Naam | Beschrijving | Bronbestanden (HBO) | Aantal rijen (HBO totaal) | Granulariteit | Updatefrequentie | Historische diepte |
|---|-----------|------|-------------|-----------------|----------------------|-------|-------------|---------|
| 1 | p01hoinges | Ingeschrevenen HBO | Ingeschrevenen in HBO, naar geografie, instelling, opleiding en demografische kenmerken | 3 CSV's (geslacht, niveau, opleidingsvorm) | ~15.892 | Studenten per instelling/opleiding/jaar | Jaarlijks (1 oktober) | Laatste 5 academische jaren |
| 2 | p02ho1ejrs | Eerstejaars ingeschrevenen HBO | Eerstejaars ingeschrevenen in HBO | 3 CSV's (geslacht, niveau, opleidingsvorm) | ~12.149 | Eerstejaars per instelling/opleiding/jaar | Jaarlijks (1 oktober) | Laatste 5 academische jaren |
| 3 | p03hoinschr | Inschrijvingen HBO | Inschrijvingen in HBO | 3 CSV's (geslacht, niveau, opleidingsvorm) | ~15.900 | Inschrijvingen per instelling/opleiding/jaar | Jaarlijks (1 oktober) | Laatste 5 academische jaren |
| 4 | p04hogdipl | Gediplomeerden HBO | Gediplomeerden van HBO-programma's | 3 CSV's (geslacht, niveau, opleidingsvorm) | ~14.849 | Gediplomeerden per instelling/opleiding/jaar | Jaarlijks (1 oktober) | Laatste 5 academische jaren |
| 5 | ho_opleidingsoverzicht | HO Opleidingsoverzicht | Overzicht van alle bekostigde HO-programma's uit RIO | 1 CSV | 7.090 | Een rij per opleiding/locatie | Dagelijks | Huidig |
| 6 | overzicht-erkenningen-ho | Overzicht Erkenningen HO | Door OCW erkende HO-instellingen en -programma's | 1 CSV + PDF-documenten | 6.747 | Een rij per erkenning | Dagelijks | Huidig |
| 7 | — | Adressen hogescholen en universiteiten | Adressen van HBO-instellingen en universiteiten | 1 CSV + 1 XLSX | Klein (~50) | Een rij per instelling (hoofdvestiging) | Maandelijks | Huidig |
| 8 | — | Adressen besturen | Adressen van bevoegde gezagen | 1 CSV + 1 XLSX | Klein (~50) | Een rij per bevoegd gezag | Maandelijks | Huidig |

---

## Officiële DUO-definities en selectiecriteria

> Bron: DUO CKAN API-documentatie (veld `notes`), opgehaald 2026-02-20. Tekst letterlijk overgenomen uit de officiële datasetbeschrijvingen.

### Bronsysteem

Alle statistische datasets (p01–p04) zijn afkomstig uit het bronsysteem **"Één Cijfer Hoger Onderwijs"** met peildatum 1 oktober, aangevuld met de **Basis Registratie Instellingen (BRIN)**. De werkgroep Één Cijfer Hoger Onderwijs bestaat uit leden van het CBS, DUO, VSNU, Vereniging Hogescholen, Inspectie van het Onderwijs en de directie hoger onderwijs van OCW.

### p01hoinges — Ingeschrevenen

**Selectie:** *"Van alle inschrijvingen op de peildatum 1 oktober worden de hoofdinschrijvingen bepaald en geteld als ingeschrevenen (natuurlijke personen). Het aantal ingeschrevenen binnen het domein hoger onderwijs wordt bepaald door de inschrijvingen in het hbo en het wo gezamenlijk te bekijken. Bij het domein hoger onderwijs is het uitgangspunt dat de natuurlijke personen binnen het gehele hoger onderwijs slechts één keer worden geteld. Een ingeschrevene met een hoofdinschrijving in het hbo kan dus geen hoofdinschrijving in het wo hebben of andersom. De inschrijvingen behorende bij opleidingen aan aangewezen instellingen worden niet meegeteld."*

**Kernbegrip:** Eén persoon = maximaal één telling, ongeacht het aantal inschrijvingen. Alleen hoofdinschrijvingen tellen mee.

**AVG-filter:** *"Oorspronkelijke aantallen kleiner dan 5 (1,2,3,4) allemaal worden weergegeven door 4."*

> **Let op:** De documentatie stelt dat waarden < 5 als **4** worden weergegeven. In de werkelijke CSV-bestanden komen echter waarden van **-1** voor. Dit verschil is nog niet opgehelderd met DUO.

### p02ho1ejrs — Eerstejaars ingeschrevenen

**Selectie:** *"Alleen de inschrijvingen op de peildatum 1 oktober die voor het eerst in het domein hoger onderwijs voorkomen worden meegenomen. Van deze inschrijvingen worden de hoofdinschrijvingen bepaald en geteld als eerstejaars ingeschrevenen. Het aantal eerstejaars ingeschrevenen binnen het domein hoger onderwijs wordt bepaald door de inschrijvingen in het hbo en het wo gezamenlijk te bekijken. Bij het domein hoger onderwijs is het uitgangspunt dat de natuurlijke personen binnen het gehele hoger onderwijs slechts één keer worden geteld. De inschrijvingen behorende bij opleidingen aan aangewezen instellingen worden niet meegeteld. De master inschrijvingen in het hoger beroepsonderwijs zijn eveneens buiten beschouwing gelaten."*

**Kernbegrip:** Deelverzameling van p01 — alleen personen die voor het **eerst** in het hoger onderwijs voorkomen. HBO-masterinschrijvingen zijn **uitgesloten**.

**AVG-filter:** Identiek aan p01.

### p03hoinschr — Inschrijvingen

**Selectie:** *"Voor de inschrijvingen op de peildatum 1 oktober worden zowel de hoofd- als de echte neveninschrijvingen meegeteld. De inschrijvingen behorende bij opleidingen aan aangewezen instellingen worden niet meegeteld."*

**Kernbegrip:** Telt **inschrijvingsrecords**, niet personen. Een student met twee studies telt als twee inschrijvingen. Zowel hoofd- als neveninschrijvingen worden meegeteld.

**AVG-filter:** Identiek aan p01.

### p04hogdipl — Gediplomeerden

**Selectie:** *"Het aantal gediplomeerden wordt geteld door te selecteren op hoofd-associate degree-diploma (hbo), hoofd-bachelor-diploma (hbo of wo), hoofd-master-diploma (hbo of wo), hoofd-doctoraal-diploma (wo) en hoofddiploma beroepsfase/postmaster (wo) op de peildatum 1 oktober. De propedeuse diploma's, postinitiële diploma's en diploma's behaald door uitwisselingsstudenten worden buiten beschouwing gelaten."*

**Kernbegrip:** Telt **hoofddiploma's**. Propedeuse, postinitieel en uitwisselingsdiploma's zijn uitgesloten. Peildatum is 1 oktober (niet de werkelijke diplomadatum).

**AVG-filter:** Identiek aan p01.

### ho_opleidingsoverzicht — HO Opleidingsoverzicht

**Selectie:** *"Het ho opleidingsoverzicht bevat informatie over bekostigde, actuele en toekomstige opleidingen in het hoger onderwijs."*

**Bron:** Registratie Instellingen en Opleidingen (RIO). Gegevens worden vastgelegd door onderwijsinstellingen zelf; kwaliteitsborging van opleidingserkenningen en opleidingseenheden ligt bij RIO.

**Periode:** Dagelijks geactualiseerd.

### overzicht-erkenningen-ho — Overzicht Erkenningen HO

**Selectie:** *"In het Overzicht Erkenningen ho staan de actuele gegevens van de OCW erkende instellingen en opleidingen in het hoger onderwijs."*

**Bron:** RIO. Nieuwe OCW-erkende opleidingen, wijzigingen en beëindigingen worden geregistreerd via het Loket Erkenningen Onderwijs ho (LEO ho, voorheen aCROHO).

**Periode:** Dagelijks geactualiseerd.

### adressen_ho — Adressen hogescholen en universiteiten / besturen

**Selectie:** *"Door OCW bekostigde Nederlandse HO-instellingen die actief zijn op het moment van aanmaak van de adreslevering en de bijbehorende besturen."*

**Bron:** Basis Registratie Instellingen (BRIN). Actuele stand op moment van aanmaak.

### Begrippenoverzicht

| Begrip | Definitie | Dataset(s) |
|--------|-----------|------------|
| **Ingeschrevene** | Een natuurlijke persoon met een hoofdinschrijving in het HO op peildatum 1 oktober. Per persoon maximaal één telling in het gehele HO. | p01 |
| **Inschrijving** | Een inschrijvingsrecord (hoofd- of neveninschrijving) op peildatum 1 oktober. Eén persoon kan meerdere inschrijvingen hebben. | p03 |
| **Eerstejaars ingeschrevene** | Een ingeschrevene die voor het eerst in het domein HO voorkomt op peildatum 1 oktober. HBO-masterinschrijvingen uitgesloten. | p02 |
| **Gediplomeerde** | Een persoon met een hoofd-AD-, bachelor-, master- of doctoraal-diploma. Propedeuse, postinitieel en uitwisselingsdiploma's uitgesloten. | p04 |
| **Hoofdinschrijving** | De primaire inschrijving van een persoon in het HO op peildatum. Bepaalt in welk type HO (hbo/wo) de persoon wordt geteld. | p01, p02 |
| **Neveninschrijving** | Een aanvullende (niet-primaire) inschrijving naast de hoofdinschrijving. Alleen meegeteld in p03 (inschrijvingen), niet in p01 (ingeschrevenen). | p03 |
| **Peildatum** | 1 oktober van het betreffende studiejaar. Het meetmoment waarop alle tellingen worden bepaald. | p01–p04 |
| **Studiejaar** | Het academisch jaar waarvoor de peildatum geldt (bijv. 2024 = studiejaar 2024/2025, peildatum 1 oktober 2024). | p01–p03 |
| **Diplomajaar** | Het kalenderjaar waarin het diploma is verleend (niet per se gelijk aan het studiejaar). | p04 |
| **BRIN-code** | Vier-letterige code uit de Basis Registratie Instellingen, uniek per instelling. | Alle |
| **CROHO-code** | Centraal Register Opleidingen Hoger Onderwijs — numerieke code die een opleiding uniek identificeert. | p01b–p04b, ho_opleidingsoverzicht, erkenningen |
| **Aangewezen instelling** | Een niet door OCW bekostigde HO-instelling. Inschrijvingen aan aangewezen instellingen zijn **uitgesloten** uit alle p01–p04 datasets. | p01–p04 |
| **AVG-filter** | Privacybescherming: aantallen < 5 worden aangepast. Documentatie zegt "weergegeven door 4"; CSV-bestanden bevatten -1. | p01–p04 |
| **RIO** | Registratie Instellingen en Opleidingen — het landelijke register van onderwijsinstellingen en -programma's. | ho_opleidingsoverzicht, erkenningen |
| **NVAO** | Nederlands-Vlaamse Accreditatieorganisatie — verantwoordelijk voor accreditatie van HO-opleidingen. | erkenningen |
| **Opleidingsvorm** | Wijze van onderwijs: VT = voltijd, DT = deeltijd, DU = duaal. | p01c–p04c |

---

## Resourcedetails: HBO-specifieke bestanden

### p01hoinges — Ingeschrevenen HBO

| # | Resource | Bestand | Records | Grootte | Beschrijving |
|---|----------|------|---------|------|-------------|
| 1a | HBO incl. geslacht | ingeschrevenengeslhbo.csv | 4.833 | 762 KB | Ingeschrevenen naar geografie, instelling, opleiding, geslacht |
| 1b | HBO niveau opleiding | ingeschrevenenhbo.csv | 7.170 | 1,34 MB | Ingeschrevenen naar geografie, instelling, opleidingsniveau |
| 1c | HBO incl. opleidingsvorm | ingeschrevenenoplvhbo.csv | 3.889 | 601 KB | Ingeschrevenen naar geografie, instelling, opleidingsvorm (VT/DT/DU) |

### p02ho1ejrs — Eerstejaars Ingeschrevenen HBO

| # | Resource | Bestand | Records | Grootte | Beschrijving |
|---|----------|------|---------|------|-------------|
| 2a | HBO incl. geslacht | 1ejrsingeschrevenengeslhbo.csv | 3.407 | 534 KB | Eerstejaars naar geografie, instelling, opleiding, geslacht |
| 2b | HBO niveau opleiding | 1ejrsingeschrevenenhbo.csv | 5.834 | 1,08 MB | Eerstejaars naar geografie, instelling, opleidingsniveau |
| 2c | HBO incl. opleidingsvorm | 1ejrsingeschrevenenoplvhbo.csv | 2.908 | 448 KB | Eerstejaars naar geografie, instelling, opleidingsvorm |

### p03hoinschr — Inschrijvingen HBO

| # | Resource | Bestand | Records | Grootte | Beschrijving |
|---|----------|------|---------|------|-------------|
| 3a | HBO incl. geslacht | inschrijvingengeslhbo.csv | 4.835 | ~762 KB | Inschrijvingen naar geografie, instelling, opleiding, geslacht |
| 3b | HBO niveau opleiding | inschrijvingenhbo.csv | 7.174 | ~1,34 MB | Inschrijvingen naar geografie, instelling, opleidingsniveau |
| 3c | HBO incl. opleidingsvorm | inschrijvingenoplvhbo.csv | 3.891 | ~601 KB | Inschrijvingen naar geografie, instelling, opleidingsvorm |

### p04hogdipl — Gediplomeerden HBO

| # | Resource | Bestand | Records | Grootte | Beschrijving |
|---|----------|------|---------|------|-------------|
| 4a | HBO incl. geslacht | gediplomeerdengeslhbo.csv | 4.445 | 716 KB | Gediplomeerden naar geografie, instelling, opleiding, geslacht |
| 4b | HBO niveau opleiding | gediplomeerdenhbo.csv | 6.813 | 1,3 MB | Gediplomeerden naar geografie, instelling, opleidingsniveau |
| 4c | HBO incl. opleidingsvorm | gediplomeerdenoplvhbo.csv | 3.591 | 568 KB | Gediplomeerden naar geografie, instelling, opleidingsvorm |

### Referentiedatasets

| # | Resource | Bestand | Records | Beschrijving |
|---|----------|------|---------|-------------|
| 5 | HO Opleidingsoverzicht | ho_opleidingsoverzicht.csv | 7.090 | Alle bekostigde HO-programma's uit RIO-register |
| 6 | Erkenningen HO | ho_erkenningen_rio.csv | 6.747 | Door OCW erkende HO-erkenningen |
| 7 | Adressen instellingen | Adressen hogescholen en universiteiten.csv | ~50 | Adressen hoofdvestiging instellingen |
| 8 | Adressen besturen | Adressen besturen hogescholen en universiteiten.csv | ~50 | Adressen bevoegde gezagen |

---

## Algemene opmerkingen

- **Licentie:** Alle datasets zijn CC-BY (Creative Commons Naamsvermelding)
- **Privacyfilter (AVG):** Officiële documentatie stelt dat aantallen < 5 worden weergegeven als **4**. In de werkelijke CSV-bestanden komen echter waarden van **-1** voor. Dit verschil is niet opgehelderd met DUO. Zie sectie "Officiële DUO-definities" voor details.
- **Bereik:** Datasets p01–p04 omvatten zowel HBO als WO; alleen HBO-bronbestanden zijn in scope voor deze pilot
- **Peildatum:** Studentengegevens worden gemeten op 1 oktober van elk academisch jaar
- **Bronsysteem:** "Één Cijfer Hoger Onderwijs"
- **Contact:** informatieproducten@duo.nl / gegevensmagazijn@duo.nl
- **API-portaal:** https://onderwijsdata.duo.nl/datasets/

---

## Veldmetadata

### Dataset: p01hoinges — Ingeschrevenen HBO

Alle 3 HBO-bronbestanden delen een **gemeenschappelijke kern** van 10 velden plus één bronbestand-specifiek veld elk. Het meetveld is altijd `AANTAL_INGESCHREVENEN`.

**Brondatascheidingsteken:** `,` (komma) — opmerking: DUO gebruikt komma-gescheiden CSV's

#### Gemeenschappelijke velden (alle 3 bronbestanden)

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | STUDIEJAAR | numeric | Academisch jaar (peildatum 1 oktober) | Nee | 2020, 2021, 2022, 2023, 2024 | 5 | 0% | Tijddimensiesleutel |
| 2 | PROVINCIENAAM | text | Provincienaam | Nee | Drenthe, Noord-Holland, Zuid-Holland, Utrecht | 12 | 0% | Geografiedimensie |
| 3 | GEMEENTENUMMER | text | Gemeentecode (CBS) | Nee | 0106, 0114, 0363, 0599 | 52 | 0% | Geografiedimensiesleutel |
| 4 | GEMEENTENAAM | text | Gemeentenaam | Nee | Assen, Amsterdam, Rotterdam, Utrecht | 52 | 0% | Geografiedimensie |
| 5 | SOORT_INSTELLING | text | Type instelling | Nee | reguliere inst. | 1 | 0% | Instellingsdimensie |
| 6 | TYPE_HOGER_ONDERWIJS | text | Hoger onderwijsniveau | Nee | associate degree, bachelor, master | 3 | 0% | Opleidingsdimensie |
| 7 | INSTELLINGSCODE_ACTUEEL | text | Huidige instellingscode (BRIN) | Nee | 25DW, 28DN, 22OJ, 30GB | 36 | 0% | Instellingsdimensiesleutel |
| 8 | INSTELLINGSNAAM_ACTUEEL | text | Huidige instellingsnaam | Nee | Hogeschool Utrecht, Hogeschool van Amsterdam | 36 | 0% | Instellingsdimensie |
| 9 | ONDERDEEL | text | ISCED-sector / domein | Nee | TECHNIEK, ECONOMIE, ONDERWIJS, GEZONDHEIDSZORG, GEDRAG_EN_MAATSCHAPPIJ, LANDBOUW_EN_NATUURLIJKE_OMGEVING, TAAL_EN_CULTUUR, SECTOROVERSTIJGEND | 8 | 0% | Opleidingsdimensie |
| 10 | SUBONDERDEEL | text | Subsector / subdomein | Nee | leraar basisonderwijs, n.v.t. (techniek), voortgezette kunstopleidingen | 16 | 0% | Opleidingsdimensie |
| 11 | AANTAL_INGESCHREVENEN | numeric | Aantal ingeschrevenen | Nee | 5, 50, 163, 5247 (ook -1 voor onderdrukt) | Continu | 0% | **Meetwaarde** |

#### Bronbestand-specifieke velden

| Bronbestand | Extra veld | Type | Beschrijving | Voorbeeldwaarden | Kardinaliteit | Verwachte rol |
|----------|-----------|------|-------------|---------------|-------------|------------|
| 1a (geslacht) | GESLACHT | text | Geslacht | MAN, VROUW | 2 | Demografiedimensie |
| 1b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO-opleidingscode | 34267, 34808, 80009 | 247 | Opleidingsdimensiesleutel |
| 1b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Opleidingsnaam | B Elektrotechniek, M Smart Systems Engineering | 247 | Opleidingsdimensie |
| 1c (oplvorm) | OPLEIDINGSVORM | text | Vorm van onderwijs | VT (fulltime), DT (deeltijd), DU (duaal) | 3 | Opleidingsdimensie |

#### Bronbestandoverzicht

| Bronbestand | Bestand | Records | Granulariteit |
|----------|------|---------|-------|
| 1a | ingeschrevenengeslhbo.csv | 4.833 | Studenten per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × geslacht |
| 1b | ingeschrevenenhbo.csv | 7.170 | Studenten per jaar × gemeente × instelling × opleiding (CROHO) |
| 1c | ingeschrevenenoplvhbo.csv | 3.889 | Studenten per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × opleidingsvorm |

#### Datakwaliteitsopmerkingen (p01hoinges)

- [ ] **Privacyonderdrukking:** `AANTAL_INGESCHREVENEN = -1` komt voor in 273 van 4.833 records (5,7%) in bronbestand 1a — deze vertegenwoordigen aantallen < 5 onderdrukt voor AVG-naleving. Opmerking: DUO-documentatie stelt dat aantallen < 5 als 4 worden weergegeven, maar de werkelijke gegevens gebruiken -1 voor onderdrukking. **Behoeft mensenhandmatige verificatie.**
- [ ] `SOORT_INSTELLING` heeft kardinaliteit 1 (altijd "reguliere inst.") — mogelijk overbodig voor HBO-bereik, maar kan verschillen bij combinatie met WO-gegevens
- [ ] `GEMEENTENUMMER` wordt als tekst opgeslagen (niet als geheel getal) — aangevuld met voorloopnullen (bijv. "0106")
- [ ] De 3 bronbestanden vertegenwoordigen verschillende kruistabellaties van dezelfde basisgegevens — geen onafhankelijke waarnemingen. Ze kunnen niet eenvoudig worden samengevoegd of gecombineerd
- [ ] `ONDERDEEL` en `SUBONDERDEEL` gebruiken een hiërarchische indeling; `SUBONDERDEEL` bevat vaak "n.v.t. (sector)" wat betekent dat de sector geen verdere onderverdeling heeft

---

## Veldmetadata

### Dataset: p02ho1ejrs — Eerstejaars Ingeschrevenen HBO

Identieke structuur als p01hoinges. Belangrijk verschil: meetveld is `AANTAL_EERSTEJAARS_INGESCHREVENEN`.

#### Gemeenschappelijke velden (alle 3 bronbestanden)

Dezelfde 10 gemeenschappelijke velden als p01hoinges (STUDIEJAAR, PROVINCIENAAM, GEMEENTENUMMER, GEMEENTENAAM, SOORT_INSTELLING, TYPE_HOGER_ONDERWIJS, INSTELLINGSCODE_ACTUEEL, INSTELLINGSNAAM_ACTUEEL, ONDERDEEL, SUBONDERDEEL) plus:

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 11 | AANTAL_EERSTEJAARS_INGESCHREVENEN | numeric | Aantal eerstejaars ingeschrevenen | Nee | 8, 14, 36, 67, -1 | Continu | 0% | **Meetwaarde** |

#### Bronbestand-specifieke velden

| Bronbestand | Extra veld | Type | Beschrijving | Voorbeeldwaarden | Kardinaliteit | Verwachte rol |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 2a (geslacht) | GESLACHT | text | Geslacht | MAN, VROUW | 2 | Demografiedimensie |
| 2b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO-opleidingscode | 34808, 80009, 80040 | ~247 | Opleidingsdimensiesleutel |
| 2b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Opleidingsnaam | B Opleiding tot leraar Basisonderwijs, Ad Hotel Management | ~247 | Opleidingsdimensie |
| 2c (oplvorm) | OPLEIDINGSVORM | text | Vorm van onderwijs | VT (fulltime), DT (deeltijd), DU (duaal) | 3 | Opleidingsdimensie |

#### Bronbestandoverzicht

| Bronbestand | Bestand | Records | Granulariteit |
|----------|------|---------|-------|
| 2a | eerstejaarsingeschrevenengeslhbo.csv | 3.407 | Eerstejaars per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × geslacht |
| 2b | eerstejaarsingeschrevenenhbo.csv | 5.834 | Eerstejaars per jaar × gemeente × instelling × opleiding (CROHO) |
| 2c | eerstejaarsingeschrevenenoplvhbo.csv | 2.908 | Eerstejaars per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × opleidingsvorm |

#### Datakwaliteitsopmerkingen (p02ho1ejrs)

- [ ] Privacyonderdrukking: `AANTAL_EERSTEJAARS_INGESCHREVENEN = -1` komt voor in bronbestand 2a (precieze frequentie nog niet gemeten) — hetzelfde AVG-mechanisme als p01hoinges
- [ ] Structuur is identiek aan p01hoinges. Eerstejaars zijn een deelverzameling van alle ingeschrevenen — de twee datasets moeten niet eenvoudig worden gecombineerd

---

### Dataset: p03hoinschr — Inschrijvingen HBO

Bijna identieke structuur als p01hoinges. Belangrijk verschil: meetveld is `AANTAL_INSCHRIJVINGEN`. Het onderscheid tussen p01 ("Ingeschrevenen" = ingeschrevenen personen) en p03 ("Inschrijvingen" = inschrijvingen) kan een subtiel conceptueel verschil weerspiegelen of een andere extractie uit het bronsysteem. Aantallen rijen zijn bijna identiek (p01: 15.892 vs p03: 15.900 totaal).

#### Gemeenschappelijke velden (alle 3 bronbestanden)

Dezelfde 10 gemeenschappelijke velden als p01hoinges plus:

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 11 | AANTAL_INSCHRIJVINGEN | numeric | Aantal inschrijvingen | Nee | 5, 23, 53, 57, 111, -1 | Continu | 0% | **Meetwaarde** |

#### Bronbestand-specifieke velden

| Bronbestand | Extra veld | Type | Beschrijving | Voorbeeldwaarden | Kardinaliteit | Verwachte rol |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 3a (geslacht) | GESLACHT | text | Geslacht | MAN, VROUW | 2 | Demografiedimensie |
| 3b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO-opleidingscode | 34267, 34808, 80009, 80040 | ~247 | Opleidingsdimensiesleutel |
| 3b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Opleidingsnaam | B Elektrotechniek, Ad Tourism Management | ~247 | Opleidingsdimensie |
| 3c (oplvorm) | OPLEIDINGSVORM | text | Vorm van onderwijs | VT, DT, DU | 3 | Opleidingsdimensie |

#### Bronbestandoverzicht

| Bronbestand | Bestand | Records | Granulariteit |
|----------|------|---------|-------|
| 3a | inschrijvingengeslhbo.csv | 4.835 | Inschrijvingen per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × geslacht |
| 3b | inschrijvingenhbo.csv | 7.174 | Inschrijvingen per jaar × gemeente × instelling × opleiding (CROHO) |
| 3c | inschrijvingenoplvhbo.csv | 3.891 | Inschrijvingen per jaar × gemeente × instelling × sector × subsector × onderwijsniveau × opleidingsvorm |

#### Datakwaliteitsopmerkingen (p03hoinschr)

- [ ] Semantische relatie met p01hoinges onduidelijk — structuur en aantallen rijen bijna identiek. Verificatie met DUO-documentatie nodig of deze dezelfde of verschillende onderliggende aantallen vertegenwoordigen
- [ ] Privacyonderdrukking: `AANTAL_INSCHRIJVINGEN = -1` komt voor in bronbestanden (precieze frequentie nog niet gemeten)

---

### Dataset: p04hogdipl — Gediplomeerden HBO

Structureel verschillend van p01–p03:
- Jaardimensie: `DIPLOMAJAAR` (diplomaverleningsjaar), niet `STUDIEJAAR` (inschrijvingsjaar 1 oktober)
- `TYPE_HOGER_ONDERWIJS` ontbreekt — vervangen door `SOORT_DIPLOMA`
- Meetwaarde: `AANTAL_GEDIPLOMEERDEN`

#### Gemeenschappelijke velden (alle 3 bronbestanden)

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | DIPLOMAJAAR | numeric | Jaar diploma werd verleend | Nee | 2019, 2020, 2021, 2022, 2023 | 5 | 0% | Tijddimensiesleutel |
| 2 | PROVINCIENAAM | text | Provincienaam | Nee | Drenthe, Gelderland, Noord-Holland | 12 | 0% | Geografiedimensie |
| 3 | GEMEENTENUMMER | text | Gemeentecode (CBS) | Nee | 0106, 0114, 0228 | 52 | 0% | Geografiedimensiesleutel |
| 4 | GEMEENTENAAM | text | Gemeentenaam | Nee | Assen, Emmen, Ede | 52 | 0% | Geografiedimensie |
| 5 | SOORT_INSTELLING | text | Type instelling | Nee | reguliere inst. | 1 | 0% | Instellingsdimensie |
| 6 | INSTELLINGSCODE_ACTUEEL | text | Huidige instellingscode (BRIN) | Nee | 25BE, 31FR | 36 | 0% | Instellingsdimensiesleutel |
| 7 | INSTELLINGSNAAM_ACTUEEL | text | Huidige instellingsnaam | Nee | Hanzehogeschool Groningen, NHL Stenden Hogeschool | 36 | 0% | Instellingsdimensie |
| 8 | ONDERDEEL | text | ISCED-sector / domein | Nee | TECHNIEK, ONDERWIJS, ECONOMIE | 8 | 0% | Opleidingsdimensie |
| 9 | SUBONDERDEEL | text | Subsector / subdomein | Nee | n.v.t. (techniek), leraar basisonderwijs | 16 | 0% | Opleidingsdimensie |
| 10 | SOORT_DIPLOMA | text | Type verleend diploma | Nee | hbo bachelor, hbo associate degree | 3 | 0% | Opleidingsdimensie |
| 11 | AANTAL_GEDIPLOMEERDEN | numeric | Aantal gediplomeerden | Nee | 9, 23, 42, -1 | Continu | 0% | **Meetwaarde** |

#### Bronbestand-specifieke velden

| Bronbestand | Extra veld | Type | Beschrijving | Voorbeeldwaarden | Kardinaliteit | Verwachte rol |
|----------|-------------|------|-------------|---------------|-------------|------------|
| 4a (geslacht) | GESLACHT | text | Geslacht | MAN, VROUW | 2 | Demografiedimensie |
| 4b (niveau) | OPLEIDINGSCODE_ACTUEEL | numeric | CROHO-opleidingscode | 34267, 34808, 35520 | ~200 | Opleidingsdimensiesleutel |
| 4b (niveau) | OPLEIDINGSNAAM_ACTUEEL | text | Opleidingsnaam | B Elektrotechniek, B International Business | ~200 | Opleidingsdimensie |
| 4c (oplvorm) | OPLEIDINGSVORM | text | Vorm van onderwijs | VT, DT, DU | 3 | Opleidingsdimensie |

#### Bronbestandoverzicht

| Bronbestand | Bestand | Records | Granulariteit |
|----------|------|---------|-------|
| 4a | gediplomeerdengeslhbo.csv | 4.445 | Gediplomeerden per diplomajaar × gemeente × instelling × sector × diplomatype × geslacht |
| 4b | gediplomeerdenhbo.csv | 6.813 | Gediplomeerden per diplomajaar × gemeente × instelling × opleiding (CROHO) × diplomatype |
| 4c | gediplomeerdenoplvhbo.csv | 3.591 | Gediplomeerden per diplomajaar × gemeente × instelling × sector × diplomatype × opleidingsvorm |

#### Datakwaliteitsopmerkingen (p04hogdipl)

- [ ] `DIPLOMAJAAR` vroegste waarde in samples is 2019 (vs 2020 voor p01–p03 `STUDIEJAAR`) — volledig jaarbereik verifiëren
- [ ] `SOORT_DIPLOMA` verwachte waarden: "hbo bachelor", "hbo associate degree", "hbo master" — alleen eerste twee gezien in HBO-bronbestanden
- [ ] Privacyonderdrukking: `AANTAL_GEDIPLOMEERDEN = -1` waargenomen in samples (precieze frequentie niet gemeten)
- [ ] `SOORT_DIPLOMA` vervult dezelfde rol als `TYPE_HOGER_ONDERWIJS` in p01–p03 maar gebruikt ander vocabulaire ("hbo bachelor" vs "bachelor")

---

### Dataset: ho_opleidingsoverzicht — HO Opleidingsoverzicht

Referentiedataset uit RIO. Alle momenteel bekostigde HO-programma's (zowel HBO als WO). Hoofdcatalogus van opleidingen.

**Aantal rijen:** 7.090 | **Granulariteit:** Een rij per aangeboden programmavariant (programma × vorm × locatie) | **Bereik:** Alle HO — filter NIVEAU voor HBO

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | ONDERWIJSBESTUURID | text | ID onderwijsbestuur (RIO) | Nee | 100B349 | ~90 | 0% | Instellingsdimensiesleutel (RIO) |
| 2 | ONDERWIJSBESTUUR_NAAM | text | Naam onderwijsbestuur | Nee | Stichting HZ University of Appl. Scienc. | ~90 | 0% | Instellingsdimensie |
| 3 | ONDERWIJSAANBIEDERID | text | ID onderwijsaanbieder (kan verschillen van bestuur) | Ja | — | ~90 | Onbekend | Instellingsdimensiesleutel |
| 4 | ONDERWIJSAANBIEDER_NAAM | text | Naam onderwijsaanbieder | Ja | — | ~90 | Onbekend | Instellingsdimensie |
| 5 | ONDERWIJSLOCATIECODE | text | Code onderwijslocatie | Ja | — | ~300 | Onbekend | Locatiedimensiesleutel |
| 6 | ONDERWIJSLOCATIESTRAAT | text | Straat onderwijslocatie | Ja | — | ~300 | Onbekend | Locatiedimensie |
| 7 | ONDERWIJSLOCATIEPLAATS | text | Plaats onderwijslocatie | Ja | — | ~100 | Onbekend | Locatiedimensie |
| 8 | SOORT | text | Altijd "OPLEIDING" | Nee | OPLEIDING | 1 | 0% | Overbodig |
| 9 | OPLEIDINGSEENHEIDCODE | text | Code opleidingseenheid (RIO) | Nee | 1001O2869, 1001O3168 | ~700 | 0% | Opleidingsdimensiesleutel (RIO) |
| 10 | ERKENDEOPLEIDINGSCODE | numeric | CROHO-opleidingscode | Nee | 34074, 34279, 49506 | ~700 | 0% | Opleidingsdimensiesleutel (CROHO) |
| 11 | AANGEBODEN_OPLEIDINGCODE | text | Code aangeboden opleiding | Ja | — | ~700 | Onbekend | Opleidingsdimensiesleutel |
| 12 | EIGEN_AANGEBODEN_OPLEIDINGSLEUTEL | text | Eigen programmasleutel instelling | Ja | — | ~700 | Onbekend | Instellingsintern |
| 13 | NAAM_LANG | text | Volledige programmanaam (Nederlands) | Nee | Watermanagement, Civiele Techniek | ~700 | 0% | Opleidingsdimensie |
| 14 | INTERNATIONALE_NAAM | text | Internationale programmanaam | Ja | Water Management, Civil Engineering | ~700 | Onbekend | Opleidingsdimensie |
| 15 | EIGENNAAM | text | Eigen naam instelling | Ja | — | ~700 | Hoog | Opleidingsdimensie |
| 16 | EIGENNAAM_DUITS | text | Duitse eigen naam | Ja | — | ~700 | Zeer hoog | Zelden gebruikt |
| 17 | EIGENNAAM_ENGELS | text | Engelse eigen naam | Ja | — | ~700 | Hoog | Opleidingsdimensie |
| 18 | VARIANT_VAN | text | Verwijzing naar variantopleiding | Ja | — | ~700 | Onbekend | Relatieveld |
| 19 | ERKENNER | text | Accreditatieorgaan | Nee | NVAO | 1–2 | 0% | Dimensie |
| 20 | NIVEAU | text | Onderwijsniveau | Nee | HBO-BA, HBO-MA, HBO-AD, WO-BA, WO-MA | 5 | 0% | Opleidingsdimensie — **gebruik als bereikfilter** |
| 21 | GRAAD | text | Type graad | Nee | BACHELOR, MASTER, ASSOCIATE_DEGREE | 3 | 0% | Opleidingsdimensie |
| 22 | STUDIELAST | numeric | ECTS-punten | Nee | 60, 120, 180, 240 | ~10 | 0% | Opleidingskenmerk |
| 23 | EQF | numeric | Europees Kwalificatieraamwerk-niveau | Nee | 5, 6, 7 | 3 | 0% | Opleidingsdimensie |
| 24 | ISCED | numeric | ISCED-code studierichting | Nee | — | ~50 | 0% | Opleidingsdimensie |
| 25 | NLQF | numeric | Nederlands Kwalificatieraamwerk-niveau | Nee | 5, 6, 7 | 3 | 0% | Opleidingsdimensie |
| 26 | WAARDEDOCUMENTSOORT | text | Type certificaat | Nee | GETUIGSCHRIFT | 1–2 | 0% | Dimensie |
| 27 | VORM | text | Vorm van onderwijs | Ja | VOLTIJD, DEELTIJD | 2–3 | Onbekend | Opleidingsdimensie |
| 28 | VOERTAAL | text | Voertaal | Ja | NLD, ENG | 2–3 | Onbekend | Opleidingsdimensie |
| 29 | BEGINDATUM | timestamp | Begindatum accreditatie programma | Nee | 2002-09-01, 2015-09-01 | — | 0% | Langzaam veranderende dimensie |
| 30 | EINDDATUM | timestamp | Einddatum accreditatie programma | Ja | — | — | Hoog | Langzaam veranderende dimensie |
| 31 | AANGEBODEN_OPLEIDING_BEGINDATUM | timestamp | Begindatum aangeboden opleiding | Ja | — | — | Onbekend | Aanbodtijdlijn |
| 32 | AANGEBODEN_OPLEIDING_EINDDATUM | timestamp | Einddatum aangeboden opleiding | Ja | — | — | Onbekend | Aanbodtijdlijn |
| 33 | EERSTE_INSTROOMDATUM | timestamp | Begindatum instroom openen | Ja | — | — | Onbekend | Aanbodtijdlijn |
| 34 | LAATSTE_INSTROOMDATUM | timestamp | Einddatum instroom sluiten | Ja | — | — | Onbekend | Aanbodtijdlijn |
| 35 | DEFICIENTIE | text | Deficiëntie/voorvereisteneisen | Ja | — | — | Hoog | Programmavereiste |
| 36 | EISEN_WERKZAAMHEDEN | text | Eisen werkervaring | Ja | — | — | Hoog | Programmavereiste |
| 37 | PROPEDEUTISCHE_FASE | text | Indicator propedeusefase | Ja | — | Laag | Onbekend | Programmakenmerk |
| 38 | STUDIEKEUZECHECK | text | Indicator studiekeuzecheck | Ja | — | Laag | Onbekend | Programmakenmerk |
| 39 | VERSNELD_TRAJECT | text | Indicator versneld traject | Ja | — | Laag | Onbekend | Programmakenmerk |
| 40 | PENVOERDER | text | Leidende instelling voor samenwerkingsprogramma's | Ja | — | ~90 | Hoog | Relatieveld |
| 41 | SAMENWERKEND_MET | text | Samenwerkende instellingen | Ja | — | — | Zeer hoog | Relatieveld |
| 42 | BUITENLANDSEPARTNER | text | Internationale partners | Ja | — | — | Zeer hoog | Zelden ingevuld |
| 43 | WEBSITE | text | Website programma | Ja | — | ~700 | Onbekend | Informatief |
| 44 | OMSCHRIJVING | text | Programmaomschrijving (vrije tekst) | Ja | — | — | Onbekend | Informatief |
| 45 | _id | int | CKAN interne rij-ID | Nee | 1–7090 | 7090 | 0% | Systeemveld |

#### Datakwaliteitsopmerkingen (ho_opleidingsoverzicht)

- [ ] Dataset omvat alle HO (HBO + WO) — moet `NIVEAU IN ('HBO-BA','HBO-MA','HBO-AD')` filteren voor HBO-bereik
- [ ] `SOORT` = "OPLEIDING" voor alle records — overbodig veld in deze dataset
- [ ] Veel velden kunnen null zijn met onbekende frequentie — vooral locatievelden (ONDERWIJSLOCATIECODE etc.), naamvarianten en tijdlijnvelden
- [ ] `EINDDATUM` null voor actieve programma's — null behandelen als "momenteel actief"

---

### Dataset: overzicht-erkenningen-ho — Overzicht Erkenningen HO

Referentiedataset van door OCW erkende HO-programma's en hun accreditatiestatus uit het RIO-register. Omvat zowel HBO als WO.

**Aantal rijen:** 6.747 | **Granulariteit:** Een rij per programmaerkenning per vestiging | **Bereik:** Alle HO — filter NIVEAU voor HBO

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | BEVOEGD_GEZAG_CODE | text | Code bevoegd gezag | Nee | 20045, 24832 | ~90 | 0% | Instellingsdimensiesleutel |
| 2 | BEVOEGD_GEZAG_NAAM | text | Naam bevoegd gezag | Nee | Protestantse Theologische Universiteit | ~90 | 0% | Instellingsdimensie |
| 3 | INSTELLINGSCODE | text | Instellingscode (BRIN) | Nee | 00DV, 00IC | ~200 | 0% | Instellingsdimensiesleutel (BRIN) |
| 4 | INSTELLINGSNAAM | text | Instellingsnaam | Nee | Protestantse Theologische Universiteit | ~200 | 0% | Instellingsdimensie |
| 5 | VESTIGINGSCODE | text | Code vestiging/campus | Nee | 00DV01, 00IC01 | ~500 | 0% | Locatiedimensiesleutel |
| 6 | VESTIGINGSNAAM | text | Naam vestiging/campus | Nee | Protestantse Theologische Universiteit; Utrecht | ~500 | 0% | Locatiedimensie |
| 7 | GEMEENTENAAM | text | Gemeentenaam | Nee | Utrecht, Amsterdam | ~100 | 0% | Geografiedimensie |
| 8 | PLAATSNAAM | text | Plaatsnaam (hoofdletters) | Nee | UTRECHT, AMSTERDAM | ~100 | 0% | Geografiedimensie |
| 9 | ERKENDEOPLEIDINGSCODE | text | CROHO-opleidingscode | Nee | 56109, 60254 | ~700 | 0% | Opleidingsdimensiesleutel (CROHO) |
| 10 | INSTROOM_EINDDATUM | timestamp | Laatste inschrijvingsdatum (null = actief) | Ja | null, 2025-08-31 | — | Hoog | Programmatijdlijn |
| 11 | OPLEIDINGSEENHEIDCODE | text | Code opleidingseenheid (RIO) | Nee | 1016O1755, 1001O6573 | ~700 | 0% | Opleidingsdimensiesleutel (RIO) |
| 12 | EIGEN_OPLEIDINGSEENHEIDSLEUTEL | text | Eigen programmasleutel instelling | Ja | — | ~700 | Onbekend | Instellingsintern |
| 13 | OPLEIDINGSEENHEID_NAAM | text | Programmanaam (Nederlands) | Nee | Theologie | ~700 | 0% | Opleidingsdimensie |
| 14 | OPLEIDINGSEENHEID_INTERNATIONALE_NAAM | text | Programmanaam (Engels) | Ja | Theology | ~700 | Onbekend | Opleidingsdimensie |
| 15 | OPLEIDINGSEENHEID_SOORT | text | Type programma | Nee | — | ~5 | 0% | Opleidingsdimensie |
| 16 | STUDIELAST | numeric | ECTS-punten | Nee | 180, 60 | ~10 | 0% | Programmakenmerk |
| 17 | STUDIELASTEENHEID | text | Eenheid punten | Nee | ECTS | 1 | 0% | Informatief |
| 18 | NIVEAU | text | Onderwijsniveau | Nee | WO-BA, WO-MA, HBO-BA | 5 | 0% | Opleidingsdimensie — **gebruik als bereikfilter** |
| 19 | GRAAD | text | Type graad | Nee | BACHELOR, MASTER | 3 | 0% | Opleidingsdimensie |
| 20 | GRAADTOEVOEGING | text | Graadtoevoeging (bijv. of Science) | Ja | — | ~5 | Onbekend | Opleidingsdimensie |
| 21 | ISCED | numeric | ISCED-code studierichting | Nee | — | ~50 | 0% | Opleidingsdimensie |
| 22 | NLQF | numeric | Nederlands Kwalificatieraamwerk-niveau | Nee | — | 3 | 0% | Opleidingsdimensie |
| 23 | EQF | numeric | Europees Kwalificatieraamwerk-niveau | Nee | — | 3 | 0% | Opleidingsdimensie |
| 24 | VORM | text | Vorm van onderwijs | Nee | VOLTIJD, DEELTIJD | 3 | 0% | Opleidingsdimensie |
| 25 | ONDERDEEL | text | ISCED-sector / domein | Nee | TAAL_EN_CULTUUR, ONDERWIJS | 8 | 0% | Opleidingsdimensie |
| 26 | SUBONDERDEEL | text | Subsector / subdomein | Nee | — | ~16 | 0% | Opleidingsdimensie |
| 27 | BEKOSTIGINGSNIVEAU | text | Bekostigingsniveau | Nee | LAAG | ~3 | 0% | Bekostigingsdimensie |
| 28 | GRONDSLAG_STUDIELAST | text | Grondslag bepaling studiebelas­ting | Ja | — | ~5 | Onbekend | Programmakenmerk |
| 29 | BEROEPSEISEN | text | Beroepsvereisten | Ja | — | ~5 | Onbekend | Programmakenmerk |
| 30 | OPLEIDINGSERKENNINGSKADER | text | Erkennngskader | Ja | — | ~5 | Onbekend | Regelgeving |
| 31 | INTENSIEFPROGRAMMA | text | Indicator intensief programma | Ja | — | 2 | Onbekend | Programmakenmerk |
| 32 | BEKOSTIGINGSCODE | text | Type bekostiging | Nee | BEKOSTIGD | 2 | 0% | Bekostigingsdimensie |
| 33 | AANVULLENDE_EISEN | text | Aanvullende toelatingsvoorwaarden | Ja | — | ~5 | Onbekend | Programmakenmerk |
| 34 | BEKOSTIGINGSDUUR | numeric | Bekostigde duur (jaren) | Nee | — | ~5 | 0% | Programmakenmerk |
| 35 | VESTIGINGSLICENTIE_BEGINDATUM | timestamp | Begindatum vestigingslicentie | Nee | — | — | 0% | Programmatijdlijn |
| 36 | VESTIGINGSLICENTIE_EINDDATUM | timestamp | Einddatum vestigingslicentie (null = actief) | Ja | — | — | Hoog | Programmatijdlijn |
| 37 | ACCREDITATIE_BESLUITDATUM | timestamp | Accreditatiebesluitdatum | Nee | — | — | 0% | Accrediteringstijdlijn |
| 38 | ACCREDITATIE_BEGINDATUM | timestamp | Begindatum accreditatie | Nee | 2025-09-01, 2020-04-06 | — | 0% | Accrediteringstijdlijn |
| 39 | ACCREDITATIE_VERVALDATUM | timestamp | Vervaldatum accreditatie | Ja | — | — | Onbekend | Accrediteringstijdlijn |
| 40 | ACCREDITATIE_AFBOUWDATUM | timestamp | Afbouwdatum | Ja | — | — | Hoog | Accrediteringstijdlijn |
| 41 | ACCREDITATIE_INLEVERDATUM | timestamp | Inleverdatum | Ja | — | — | Hoog | Accrediteringstijdlijn |
| 42 | ACCREDITATIE_VOORWAARDENDATUM | timestamp | Datum voorwaardelijke accreditatie | Ja | — | — | Hoog | Accrediteringstijdlijn |
| 43 | ACCREDITATIE_INTREKKINGSDATUM | text | Intrekkingsdatum accreditatie | Ja | — | — | Hoog | Accrediteringstijdlijn |
| 44 | ACCREDITATIE_UITSTELDATUM | timestamp | Uitsteldatum accreditatie | Ja | — | — | Hoog | Accrediteringstijdlijn |
| 45 | ACCREDITATIE_UITSTELREDEN | text | Reden uitstel | Ja | — | — | Hoog | Accrediteringsmetadata |
| 46 | SAMENWERKENDEINSTELLINGEN | text | Samenwerkende instellingen | Ja | — | — | Hoog | Relatieveld |
| 47 | _id | int | CKAN interne rij-ID | Nee | 1–6747 | 6747 | 0% | Systeemveld |

#### Datakwaliteitsopmerkingen (overzicht-erkenningen-ho)

- [ ] Dataset omvat alle HO (HBO + WO) — filter `NIVEAU` voor HBO-bereik
- [ ] `ERKENDEOPLEIDINGSCODE` hier als tekst opgeslagen vs numeric in ho_opleidingsoverzicht — typemismatching vereist CAST bij combinatie op CROHO-code
- [ ] Veel accrediteringsdatumvelden worden naar verwachting meestal null (alleen ingevuld wanneer specifieke gebeurtenis plaatsvond)
- [ ] `INSTROOM_EINDDATUM` null geeft aan dat programma momenteel instroom accepteert

---

### Dataset: Adressen hogescholen en universiteiten

Referentiedataset met bezoek- en correspondentieadressen voor alle HBO- en WO-instellingen. Een rij per instelling (alleen hoofdvestiging).

**Aantal rijen:** ~50 | **Granulariteit:** Een rij per instelling | **Bereik:** Alle HO — filter `SOORT HO` = 'hbo' voor HBO
**Bron:** RIO | **Updatefrequentie:** Maandelijks

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | SOORT HO | text | Type onderwijs (kleine letters) | Nee | hbo, wo | 2 | 0% | Bereikfilter |
| 2 | PROVINCIE | text | Provincie | Nee | Friesland, Gelderland | 12 | 0% | Geografiedimensie |
| 3 | BEVOEGD GEZAG NUMMER | text | Nummer bevoegd gezag | Nee | 30156, 40235 | ~50 | 0% | Instellingsdimensiesleutel |
| 4 | INSTELLINGSCODE | text | Instellingscode (BRIN) | Nee | 31FR, 25BA | ~50 | 0% | Instellingsdimensiesleutel (BRIN) |
| 5 | INSTELLINGSNAAM | text | Instellingsnaam | Nee | NHL Stenden Hogeschool, CHE | ~50 | 0% | Instellingsdimensie |
| 6 | STRAATNAAM | text | Straatnaam (bezoekadres) | Nee | Rengerslaan, Oude Kerkweg | ~50 | 0% | Adreskenm erk |
| 7 | HUISNUMMER-TOEVOEGING | text | Huisnummer + toevoeging | Nee | 10, 100 | ~50 | 0% | Adeskenmerk |
| 8 | POSTCODE | text | Postcode (bezoek) | Nee | 8917 DD, 6717 JS | ~50 | 0% | Adeskenmerk |
| 9 | PLAATSNAAM | text | Plaats (bezoekadres, hoofdletters) | Nee | LEEUWARDEN, EDE | ~50 | 0% | Geografiedimensie |
| 10 | GEMEENTENUMMER | text | Gemeentecode (CBS) | Nee | 0080, 0228 | ~50 | 0% | Geografiedimensiesleutel |
| 11 | GEMEENTENAAM | text | Gemeentenaam (hoofdletters) | Nee | LEEUWARDEN, EDE | ~50 | 0% | Geografiedimensie |
| 12 | DENOMINATIE | text | Religieuze/filosofische achtergrond | Nee | Overige, Protestants-Christelijk | ~5 | 0% | Instellingskenmerk |
| 13 | TELEFOONNUMMER | text | Telefoonnummer | Ja | 0582512345 | ~50 | Onbekend | Contactinfo |
| 14 | INTERNETADRES | text | Website-URL | Ja | www.nhl.nl | ~50 | Onbekend | Contactinfo |
| 15 | STRAATNAAM CORRESPONDENTIEADRES | text | Straatnaam (correspondentieadres) | Ja | Postbus | ~50 | Onbekend | Adreskenmerk |
| 16 | HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES | text | Huisnummer (correspondentie) | Ja | 1080 | ~50 | Onbekend | Adreskenmerk |
| 17 | POSTCODE CORRESPONDENTIEADRES | text | Postcode (correspondentie) | Ja | 8900 CB | ~50 | Onbekend | Adreskenmerk |
| 18 | PLAATSNAAM CORRESPONDENTIEADRES | text | Plaats (correspondentieadres) | Ja | LEEUWARDEN | ~50 | Onbekend | Adreskenmerk |
| 19 | NODAAL GEBIED CODE | text | Code nodale regio | Nee | 10, 29 | ~40 | 0% | Geografiedimensie |
| 20 | NODAAL GEBIED NAAM | text | Naam nodale regio | Nee | Leeuwarden, Ede | ~40 | 0% | Geografiedimensie |
| 21 | RPA-GEBIED CODE | text | Code RPA-regio | Nee | 04, 10 | ~30 | 0% | Geografiedimensie |
| 22 | RPA-GEBIED NAAM | text | Naam RPA-regio | Nee | Fryslân, De Vallei | ~30 | 0% | Geografiedimensie |
| 23 | WGR-GEBIED CODE | text | Code WGR-regio | Nee | 04, 16 | ~30 | 0% | Geografiedimensie |
| 24 | WGR-GEBIED NAAM | text | Naam WGR-regio | Nee | Friesland-Noord, Eem en Vallei | ~30 | 0% | Geografiedimensie |
| 25 | COROPGEBIED CODE | text | Code COROP-regio | Nee | 04, 13 | ~40 | 0% | Geografiedimensie |
| 26 | COROPGEBIED NAAM | text | Naam COROP-regio | Nee | Noord-Friesland, Veluwe | ~40 | 0% | Geografiedimensie |
| 27 | ONDERWIJSGEBIED CODE | text | Code onderwijsregio | Nee | 03, 09 | ~12 | 0% | Geografiedimensie |
| 28 | ONDERWIJSGEBIED NAAM | text | Naam onderwijsregio | Nee | Friesland, Arnhem en omstreken | ~12 | 0% | Geografiedimensie |
| 29 | RMC-REGIO CODE | text | Code RMC-regio | Nee | 04, 16 | ~39 | 0% | Geografiedimensie |
| 30 | RMC-REGIO NAAM | text | Naam RMC-regio | Nee | Friesland Noord, Eem en Vallei | ~39 | 0% | Geografiedimensie |

#### Datakwaliteitsopmerkingen (Adressen hogescholen)

- [ ] Kolomnamen bevatten spaties — vereist transformatie (aanhalingstekens of hernoemen) vóór laden
- [ ] `SOORT HO` is kleine letters ("hbo", "wo") — inconsistent met hoofdletterconventie in statistische datasets
- [ ] Alleen primair campusadres per instelling — instellingen met meerdere locaties hebben één rij
- [ ] `GEMEENTENAAM` en `PLAATSNAAM` zijn hoofdletters — hetzelfde veld, verschillende gebruik van hoofdletters vs statistische datasets
- [ ] Zes geografische classificatiesystemen aanwezig (Nodaal, RPA, WGR, COROP, Onderwijsgebied, RMC) — alternatieve geografische hiërarchieën; meeste kunnen in één dim_geography worden samengevat

---

### Dataset: Adressen besturen hogescholen en universiteiten

Referentiedataset met adressen voor bevoegde gezagen (besturen) van alle HBO- en WO-instellingen.

**Aantal rijen:** ~50 | **Granulariteit:** Een rij per bevoegd gezag | **Bereik:** Alle HO — filter `SOORT HO` = 'hbo' voor HBO
**Updatefrequentie:** Maandelijks

| # | Veld | Type | Beschrijving | Null mogelijk | Voorbeeldwaarden | Kardinaliteit | Null % | Verwachte rol |
|---|-------|------|-------------|----------|---------------|-------------|--------|------------|
| 1 | SOORT HO | text | Type onderwijs (kleine letters) | Nee | hbo, wo | 2 | 0% | Bereikfilter |
| 2 | BEVOEGD GEZAG NUMMER | text | Nummer bevoegd gezag | Nee | 24832, 28901, 29615 | ~50 | 0% | **Sleutel bevoegd gezag** |
| 3 | BEVOEGD GEZAG NAAM | text | Naam bevoegd gezag | Nee | Stichting Codarts, Stichting HKU | ~50 | 0% | Dimensie bevoegd gezag |
| 4 | STRAATNAAM | text | Straatnaam (bezoekadres) | Nee | Kruisplein, Nieuwekade | ~50 | 0% | Adreskenmerk |
| 5 | HUISNUMMER-TOEVOEGING | text | Huisnummer + toevoeging | Nee | 26, 1 | ~50 | 0% | Adreskenmerk |
| 6 | POSTCODE | text | Postcode (bezoek) | Nee | 3012 CC, 3511 RV | ~50 | 0% | Adreskenmerk |
| 7 | PLAATSNAAM | text | Plaats (bezoekadres, hoofdletters) | Nee | ROTTERDAM, UTRECHT | ~50 | 0% | Geografiedimensie |
| 8 | GEMEENTENUMMER | text | Gemeentecode (CBS) | Nee | 0599, 0344 | ~50 | 0% | Geografiedimensiesleutel |
| 9 | GEMEENTENAAM | text | Gemeentenaam (hoofdletters) | Nee | ROTTERDAM, UTRECHT | ~50 | 0% | Geografiedimensie |
| 10 | DENOMINATIE | text | Religieuze/filosofische achtergrond | Nee | Algemeen bijzonder, Openbaar | ~5 | 0% | Instellingskenmerk |
| 11 | TELEFOONNUMMER | text | Telefoonnummer | Ja | 0102171100 | ~50 | Onbekend | Contactinfo |
| 12 | INTERNETADRES | text | Website-URL | Ja | www.codarts.nl | ~50 | Onbekend | Contactinfo |
| 13 | STRAATNAAM CORRESPONDENTIEADRES | text | Straatnaam (correspondentieadres) | Ja | Kruisplein, Postbus | ~50 | Onbekend | Adreskenmerk |
| 14 | HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES | text | Huisnummer (correspondentie) | Ja | 26, 1520 | ~50 | Onbekend | Adreskenmerk |
| 15 | POSTCODE CORRESPONDENTIEADRES | text | Postcode (correspondentie) | Ja | 3012 CC, 3500 BM | ~50 | Onbekend | Adreskenmerk |
| 16 | PLAATSNAAM CORRESPONDENTIEADRES | text | Plaats (correspondentieadres) | Ja | ROTTERDAM, UTRECHT | ~50 | Onbekend | Adreskenmerk |
| 17 | ADMINISTRATIEKANTOORNUMMER | text | Nummer administratiekantoor | Ja | 164, 639 | ~50 | Onbekend | Kruisverwijzing |
| 18 | KVK-NUMMER | text | KvK-nummer | Ja | 41126801, 41178974 | ~50 | Onbekend | Juridisch kenmerk |

#### Datakwaliteitsopmerkingen (Adressen besturen)

- [ ] Kolomnamen bevatten spaties — dezelfde transformatie nodig als Adressen hogescholen
- [ ] `BEVOEGD GEZAG NUMMER` waarden verschillen in formaat van `BEVOEGD_GEZAG_CODE` in overzicht-erkenningen-ho (bijv. "24832" vs "20045") — verificatie of dezelfde namespace vóór combinatie

---

## Relaties

| Bron | Doel | Relatie | Zekerheid | Opmerkingen |
|--------|--------|--------------|------------|-------|
| p01hoinges.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | Hoog | Beide zijn BRIN-codes; statistische datasets voegen toe aan adresopzoeking |
| p01hoinges.INSTELLINGSCODE_ACTUEEL | overzicht-erkenningen-ho.INSTELLINGSCODE | N:1 | Hoog | BRIN-code: meerdere programma's per instelling |
| p02ho1ejrs.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | Hoog | Identiek aan p01 |
| p03hoinschr.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | Hoog | Identiek aan p01 |
| p04hogdipl.INSTELLINGSCODE_ACTUEEL | adressen-hogescholen.INSTELLINGSCODE | N:1 | Hoog | Identiek aan p01 |
| p01b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | Hoog | CROHO-code voegt statistische gegevens toe aan programmamaster (beide numeric) |
| p02b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | Hoog | Identiek aan p01b |
| p03b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | Hoog | Identiek aan p01b |
| p04b.OPLEIDINGSCODE_ACTUEEL | ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | N:1 | Hoog | Identiek aan p01b |
| ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE | overzicht-erkenningen-ho.ERKENDEOPLEIDINGSCODE | 1:N | Hoog | **Typemismatching**: numeric vs text — vereist CAST bij combinatie op CROHO-code |
| ho_opleidingsoverzicht.OPLEIDINGSEENHEIDCODE | overzicht-erkenningen-ho.OPLEIDINGSEENHEIDCODE | 1:N | Hoog | RIO-programma-eenheidscode — consistente teksttype |
| adressen-hogescholen.INSTELLINGSCODE | overzicht-erkenningen-ho.INSTELLINGSCODE | 1:N | Hoog | BRIN-code: één instellingsadres → veel programmaerkenningen |
| adressen-hogescholen.BEVOEGD GEZAG NUMMER | adressen-besturen.BEVOEGD GEZAG NUMMER | N:1 | Hoog | Nummer bevoegd gezag: instelling → adres bestuursorgaan |
| adressen-hogescholen.BEVOEGD GEZAG NUMMER | overzicht-erkenningen-ho.BEVOEGD_GEZAG_CODE | N:1 | Gemiddeld | Hetzelfde bevoegd gezag-concept; **verificatie van waarde-overlap** — naming/formaat verschillen |
| p01–p04.ONDERDEEL | overzicht-erkenningen-ho.ONDERDEEL | N:N | Hoog | Gedeeld vocabulaire (TECHNIEK, ECONOMIE, etc.) — hetzelfde classificatiesysteem |
| p01–p04.SUBONDERDEEL | overzicht-erkenningen-ho.SUBONDERDEEL | N:N | Hoog | Gedeeld vocabulaire |

---

## Datakwaliteitsopmerkingen

- [ ] **Privacyonderdrukking (alle p01–p04):** Meetvelden gebruiken `-1` voor aantallen < 5 (AVG). DUO-documentatie stelt dat waarden < 5 als 4 worden weergegeven, maar werkelijke gegevens gebruiken -1. Frequentie in p01-bronbestand 1a: 5,7% (273/4.833 records). Frequentie voor p02–p04 nog niet gemeten.
- [ ] **p01 vs p03 semantische overlap:** "Ingeschrevenen" (ingeschrevenen personen) vs "Inschrijvingen" (inschrijvingen) — bijna identieke structuur en vergelijkbare aantallen rijen (15.892 vs 15.900 totaal). Precieus semantisch verschil vereist verificatie met DUO-documentatie.
- [ ] **Inconsistentie jaarveldenaming:** p01–p03 gebruiken `STUDIEJAAR`, p04 gebruikt `DIPLOMAJAAR`. Beide zijn gehele getallen die academisch/kalenderjaar vertegenwoordigen maar beschrijven verschillende gebeurtenissen.
- [ ] **SOORT_INSTELLING altijd = "reguliere inst."** in alle p01–p04 datasets — nul analytische waarde voor HBO-bereik. Kan verschillen bij combinatie met WO-gegevens.
- [ ] **TYPE_HOGER_ONDERWIJS ontbreekt in p04hogdipl** — vervangen door `SOORT_DIPLOMA`. Hetzelfde concept, ander vocabulaire: "bachelor" (p01–p03) vs "hbo bachelor" (p04).
- [ ] **Kolomnaamconventie-mismatch:** p01–p04 gebruiken UPPER_SNAKE_CASE. Adresgegevenssets gebruiken "UPPER CASE WITH SPACES". Vereist normalisatie bij laden.
- [ ] **CROHO-codetype-mismatch:** `ho_opleidingsoverzicht.ERKENDEOPLEIDINGSCODE` is numeric; `overzicht-erkenningen-ho.ERKENDEOPLEIDINGSCODE` is text. Waarden zijn equivalent — vereist CAST bij combinatie.
- [ ] **Referentiedatasets omvatten alle HO (HBO + WO):** Filter ho_opleidingsoverzicht en overzicht-erkenningen-ho op `NIVEAU IN ('HBO-BA','HBO-MA','HBO-AD')` om HBO-bereik in te stellen.
- [ ] **GEMEENTENUMMER opgeslagen als tekst** (voorloopnullen, bijv. "0106") in alle datasets — consistent, maar mag niet naar integer worden geconverteerd.
- [ ] **Drie resourcesplitsingen per dataset (p01–p04):** Elke statistische dataset heeft 3 bronbestanden die verschillende kruistabellaties vertegenwoordigen (geslacht, programmacode, opleidingsvorm). Dit zijn GEEN onafhankelijke waarnemingen — ze vertegenwoordigen verschillende aggregaties van dezelfde onderliggende gegevens. Kunnen niet eenvoudig worden gecombineerd of samengevoegd zonder dubbeltelling.
- [ ] **Nulfrequentie voor referentiedataset-nullabelvelden onbekend** — vooral EINDDATUM (null voor actieve programma's), locatievelden in ho_opleidingsoverzicht en accrediteringsdatumvelden in overzicht-erkenningen-ho.
- [ ] **DIPLOMAJAAR historisch venster kan verschillen** — samples tonen 2019 als vroegste waarde voor p04hogdipl vs 2020 voor p01–p03. Verificatie van volledig beschikbaar jaarbereik.
- [ ] **GEMEENTENAAM hoofdlettergebruik-inconsistentie:** Hoofdletters in adresgegevenssets ("LEEUWARDEN"), gemengde letters in statistische datasets ("Leeuwarden"). Vereist normalisatie voor combinatie.
