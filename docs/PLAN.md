# Projectplan: AI Dimensioneel Modelleeringsagent

**Auteur:** Anne Leemans, in samenwerking met Claude Opus 4.6

## Doel

Een AI-agent ontwikkelen die vanuit elke gegevensbron (API, database, platte bestanden) een volledig dimensioneel model (sterrenmodel) kan opbouwen. De agent moet werken met **elke** gegevensbron die aan de basisvereisten voldoet — niet alleen DUO-data.

### Drie eindproducten

1. **Een dimensioneel model** van DUO HBO-data (proof of concept)
2. **Een AI-gestuurde workflow** die dimensionele modellen genereert vanuit brongegevens
3. **Agentinstructiedocumenten** waarmee de agent herbruikbaar is voor elke toekomstige gegevensbron

---

## Stapsgewijs Plan

### Fase 1: Metagegevensverzameling & Bronprofilering

> _"Je kunt niet modelleren wat je niet begrijpt."_

**Doel:** Zo veel mogelijk nauwkeurige metagegevens verzamelen uit de DUO HBO-gegevensbronnen.

**Stappen:**

1.1. **Alle HBO-datasets inventariseren** uit DUO Open Onderwijsdata
   - Studenten HBO (ingeschrevenen)
   - Inschrijvingen HBO
   - Studenten eerstejaars HBO (eerstejaars ingeschrevenen)
   - Inschrijvingen eerstejaars HBO
   - Afgestudeerden HBO (gediplomeerden)
   - Adressen hogescholen en universiteiten
   - Adressen besturen

1.2. **Elk API-eindpunt verkennen** en documenteren:
   - Beschikbare velden (kolomnamen, gegevenstypes)
   - Voorbeelddata (eerste rijen)
   - Kardinaliteit van elk veld
   - Null/lege waarden percentage
   - Waardeverdeling voor categorische velden
   - Relaties tussen datasets (gedeelde sleutels)
   - Updatefrequentie en historische diepte

1.3. **Een metagegevenscatalogus aanmaken** met gestructureerde output per dataset

1.4. **Agentinstructie schrijven:** `01-metagegevensverzameling.md` — Hoe een gegevensbron te profileren

---

### Fase 2: Bronanalyse & Businessbegrip

**Doel:** Begrijpen wat de data vertegenwoordigt in bedrijfskundige termen.

**Stappen:**

2.1. **Businessentiteiten identificeren** (student, instelling, opleiding, inschrijving, diploma)

2.2. **Granulariteit bepalen** per dataset — wat stelt één rij voor?

2.3. **Bedrijfsprocessen identificeren** (inschrijving, afstudering, enz.)

2.4. **Relaties tussen entiteiten documenteren**

2.5. **Agentinstructie schrijven:** `02-bronanalyse.md` — Hoe bedrijfskundige betekenis af te leiden uit metagegevens

---

### Fase 3: Ontwerp van het Dimensionele Model

**Doel:** Het sterrenmodel ontwerpen — feitentabellen en dimensietabellen identificeren.

**Stappen:**

3.1. **Kandidaten voor feitentabellen identificeren** — Wat zijn de meetbare gebeurtenissen/transacties?
   - Inschrijvingen
   - Diploma's (gediplomeerden)
   - Studentenaantallen (geaggregeerde feiten)

3.2. **Kandidaten voor dimensietabellen identificeren** — Wat zijn de beschrijvende attributen?
   - Studentdemografie (geslacht, nationaliteit, leeftijd)
   - Instelling (naam, adres, type, bestuur)
   - Opleiding (CROHO-code, studiegebied, niveau)
   - Tijd (studiejaar, peildatum)
   - Geografie (provincie, gemeente)

3.3. **Granulariteit definiëren** per feitentabel

3.4. **Meetwaarden in kaart brengen** (aantallen, sommen, afgeleide metrieken)

3.5. **Dimensiehiërarchieën definiëren** en strategieën voor langzaam veranderende dimensies

3.6. **Het sterrenmodel tekenen**

3.7. **Agentinstructie schrijven:** `03-dimensioneel-ontwerp.md` — Hoe feiten en dimensies te ontwerpen vanuit geanalyseerde bronnen

---

### Fase 4: Modelvalidatie

**Doel:** Het gegenereerde model valideren aan de hand van best practices en de werkelijke data.

**Stappen:**

4.1. **Conformiteit controleren** met de Kimball-methodologie

4.2. **Referentiële integriteit valideren** — Houden alle FK-relaties stand?

4.3. **Testen met voorbeeldqueries** — Kan het model typische bedrijfsvragen beantwoorden?

4.4. **Vergelijken met handmatig ontwerp** — Zou een menselijke DWH-architect dezelfde keuzes maken?

4.5. **Agentinstructie schrijven:** `04-modelvalidatie.md` — Hoe een gegenereerd dimensioneel model te valideren

---

### Fase 5: Agentassemblage

**Doel:** Alle instructies samenvoegen tot een coherente, herbruikbare agent.

**Stappen:**

5.1. **Alle instructiedocumenten compileren** tot een complete agentworkflow

5.2. **Vereisten definiëren** — Aan welke eisen moet een gegevensbron voldoen?

5.3. **Sjablonen aanmaken** voor metagegevenscatalogi, modeldefinities, validatiechecklists

5.4. **De agent testen** op een tweede gegevensbron (indien tijd beschikbaar)

5.5. **Agentinstructie schrijven:** `05-agentworkflow.md` — Het hoofdorchestratiedocument

---

## DUO HBO-gegevensbronnen

| Dataset | Beschrijving | Bijgewerkt | Bereik |
|---------|-------------|------------|--------|
| Studenten HBO | Studentenaantallen per peildatum 1 oktober | Mrt 2025 | Laatste 5 jaar |
| Inschrijvingen HBO | Inschrijvingsrecords | Mrt 2025 | Laatste 5 jaar |
| Studenten eerstejaars HBO | Eerstejaars studentenaantallen | Mrt 2025 | Laatste 5 jaar |
| Inschrijvingen eerstejaars HBO | Eerstejaars inschrijvingsrecords | Mrt 2025 | Laatste 5 jaar |
| Afgestudeerden HBO | Diplomarecords | Mrt 2025 | Laatste 5 jaar |
| Adressen hogescholen/universiteiten | Instellingsadressen | Feb 2026 | Huidig |
| Adressen besturen | Bestuursadressen | Feb 2026 | Huidig |

**API-portaal:** https://onderwijsdata.duo.nl/datasets/

**Belangrijke dataset-ID's:**
- `p01hoinges` — Ingeschrevenen hoger onderwijs
- `p03hoinschr` — Inschrijvingen hoger onderwijs

---

## Vereisten voor Toekomstige Gegevensbronnen

Voor de agent om op een nieuwe gegevensbron te werken, moet deze beschikken over:

- [ ] Toegankelijke data (API, database of gestructureerde bestanden)
- [ ] Machineleesbare metagegevens (veldnamen, types) of documentatie
- [ ] Voldoende datavolume om feiten van dimensies te onderscheiden
- [ ] Identificeerbaar(e) bedrijfsproces(sen) die de data beschrijft
- [ ] Minimaal één meetbare gebeurtenis of transactie

---

## Succescriteria

- Het gegenereerde DUO HBO-dimensionele model is valide en bruikbaar
- De agentinstructies zijn helder genoeg om een model op een nieuwe gegevensbron te produceren zonder projectspecifieke kennis
- De workflow is herhaalbaar en levert consistente resultaten
