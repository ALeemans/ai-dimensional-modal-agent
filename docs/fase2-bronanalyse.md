# Fase 2: Bronanalyse & Businessbegrip — DUO HBO

**Auteur:** Anne Leemans, in samenwerking met Claude Sonnet 4.6
**Datum:** 2026-02-20
**Bron:** DUO Open Onderwijsdata HBO — Metagegevenscatalogus (Fase 1)

---

## Stap 2.1 — Businessentiteiten

Op basis van de metagegevenscatalogus zijn de volgende businessentiteiten geïdentificeerd:

| # | Entiteit | Omschrijving | Primaire sleutel | Bronbestand(en) |
|---|----------|-------------|------------------|-----------------|
| 1 | Student | Een ingeschrevene of afgestudeerde aan een HBO-instelling. Niet als persoon opgeslagen — alleen als geaggregeerd getal per combinatie van attributen. | — (geaggregeerd) | p01hoinges, p02ho1ejrs, p03hoinschr, p04hogdipl |
| 2 | Instelling | Een HBO-instelling (hogeschool). Geïdentificeerd door een BRIN-code. | BRIN-code (`INSTELLINGSCODE_ACTUEEL`) | Alle datasets |
| 3 | Opleiding | Een door CROHO erkende HBO-opleiding, inclusief niveau en studiegebied. | CROHO-code (`OPLEIDINGSCODE_ACTUEEL`) | p01b–p04b, ho_opleidingsoverzicht, overzicht-erkenningen-ho |
| 4 | Studiejaar | Het academisch jaar waarop de peildatum (1 oktober) betrekking heeft. | `STUDIEJAAR` (bijv. 2024) | p01hoinges, p02ho1ejrs, p03hoinschr |
| 5 | Diplomajaar | Het kalenderjaar waarin het diploma is uitgereikt. | `DIPLOMAJAAR` (bijv. 2023) | p04hogdipl |
| 6 | Gemeente | De gemeente waar de instelling gevestigd is (CBS-codering). | `GEMEENTENUMMER` (tekst, bijv. "0363") | Alle statistische datasets + adressen |
| 7 | Provincie | De provincie waar de instelling gevestigd is. | `PROVINCIENAAM` | Alle statistische datasets |
| 8 | Bestuur | Het bevoegd gezag dat één of meer instellingen bestuurt. | `BEVOEGD GEZAG NUMMER` | adressen-besturen, overzicht-erkenningen-ho |
| 9 | Erkenning | Een formele accreditatie van een opleiding door NVAO, gekoppeld aan een vestiging. | Combinatie `INSTELLINGSCODE` + `OPLEIDINGSEENHEIDCODE` + `ACCREDITATIE_BEGINDATUM` | overzicht-erkenningen-ho |
| 10 | Vestiging | Een locatie (campus) van een instelling waar een opleiding wordt aangeboden. | `VESTIGINGSCODE` | overzicht-erkenningen-ho |

### Opmerkingen

- **Student als aggregaat:** DUO publiceert geen persoonsrecords. Elke rij in p01–p04 is een vooraf geaggregeerd getal (aantal ingeschrevenen / gediplomeerden) voor een specifieke combinatie van jaar, gemeente, instelling en opleiding. Dit heeft directe gevolgen voor de granulariteit van de feitentabellen.
- **Twee tijdsentiteiten:** Inschrijvingen gebruiken `STUDIEJAAR` (peildatum 1 oktober), diploma's gebruiken `DIPLOMAJAAR` (jaar van diplomaverlening). Dit zijn conceptueel verschillende tijddimensies.
- **Opleiding via twee registers:** Opleidingen zijn beschikbaar via het RIO-register (`ho_opleidingsoverzicht`) én via het erkenningenregister (`overzicht-erkenningen-ho`). Beide gebruiken de CROHO-code, maar met een typeverschil (numeric vs. text).

---

## Stap 2.2 — Granulariteit per Dataset

De granulariteit beschrijft wat één rij in de dataset vertegenwoordigt.

### Statistische datasets (p01–p04)

Elke dataset bestaat uit **drie bronbestanden** die elk een andere dwarsdoorsnede van dezelfde onderliggende data bevatten. Ze zijn **niet onafhankelijk** — ze mogen niet worden gecombineerd zonder risico op dubbeltellingen.

| Bronbestand | Granulariteit (één rij = ...) | Meetwaarde |
|-------------|-------------------------------|------------|
| p01a — geslacht | Ingeschrevenen per studiejaar × gemeente × instelling × sector × niveau × **geslacht** | `AANTAL_INGESCHREVENEN` |
| p01b — niveau | Ingeschrevenen per studiejaar × gemeente × instelling × **CROHO-opleiding** | `AANTAL_INGESCHREVENEN` |
| p01c — opleidingsvorm | Ingeschrevenen per studiejaar × gemeente × instelling × sector × niveau × **opleidingsvorm** (VT/DT/DU) | `AANTAL_INGESCHREVENEN` |
| p02a — geslacht | Eerstejaars per studiejaar × gemeente × instelling × sector × niveau × **geslacht** | `AANTAL_EERSTEJAARS_INGESCHREVENEN` |
| p02b — niveau | Eerstejaars per studiejaar × gemeente × instelling × **CROHO-opleiding** | `AANTAL_EERSTEJAARS_INGESCHREVENEN` |
| p02c — opleidingsvorm | Eerstejaars per studiejaar × gemeente × instelling × sector × niveau × **opleidingsvorm** | `AANTAL_EERSTEJAARS_INGESCHREVENEN` |
| p03a — geslacht | Inschrijvingen per studiejaar × gemeente × instelling × sector × niveau × **geslacht** | `AANTAL_INSCHRIJVINGEN` |
| p03b — niveau | Inschrijvingen per studiejaar × gemeente × instelling × **CROHO-opleiding** | `AANTAL_INSCHRIJVINGEN` |
| p03c — opleidingsvorm | Inschrijvingen per studiejaar × gemeente × instelling × sector × niveau × **opleidingsvorm** | `AANTAL_INSCHRIJVINGEN` |
| p04a — geslacht | Gediplomeerden per diplomajaar × gemeente × instelling × sector × diplomatype × **geslacht** | `AANTAL_GEDIPLOMEERDEN` |
| p04b — niveau | Gediplomeerden per diplomajaar × gemeente × instelling × **CROHO-opleiding** × diplomatype | `AANTAL_GEDIPLOMEERDEN` |
| p04c — opleidingsvorm | Gediplomeerden per diplomajaar × gemeente × instelling × sector × diplomatype × **opleidingsvorm** | `AANTAL_GEDIPLOMEERDEN` |

### Referentiedatasets

| Dataset | Granulariteit (één rij = ...) |
|---------|-------------------------------|
| ho_opleidingsoverzicht | Eén aangeboden programmavariant (opleiding × opleidingsvorm × locatie) — huidig actief |
| overzicht-erkenningen-ho | Eén accreditatierecord (opleiding × vestiging × accreditatieperiode) |
| adressen-hogescholen | Eén instelling (hoofdvestiging) |
| adressen-besturen | Eén bevoegd gezag |

### Sleutelconstatering: pre-aggregatie

De statistische datasets zijn **geen transactierecords** maar **vooraf geaggregeerde snapshots per peildatum**. Dit betekent:
- Er zijn geen individuele studentrecords beschikbaar
- De laagst beschikbare granulariteit is reeds een geaggregeerd getal
- Feitentabellen in het dimensioneel model zullen **geaggregeerde feitentabellen** (snapshot fact tables) zijn, niet transactiefeitentabellen

---

## Stap 2.3 — Bedrijfsprocessen

Twee kernbedrijfsprocessen zijn geïdentificeerd in de DUO HBO-data:

### Bedrijfsproces 1: Inschrijving

| Kenmerk | Waarde |
|---------|--------|
| Omschrijving | Het aantal studenten dat op peildatum 1 oktober staat ingeschreven aan een HBO-instelling |
| Type | Periodieke snapshot (jaarlijks, peildatum 1 oktober) |
| Brondata | p01hoinges (ingeschrevenen), p02ho1ejrs (eerstejaars), p03hoinschr (inschrijvingen) |
| Meetwaarden | `AANTAL_INGESCHREVENEN`, `AANTAL_EERSTEJAARS_INGESCHREVENEN`, `AANTAL_INSCHRIJVINGEN` |
| Dimensies | Studiejaar, Instelling, Opleiding/Sector, Gemeente, Provincie, Geslacht, Opleidingsvorm |
| Peildatum | 1 oktober van het studiejaar |
| Historische diepte | 5 studiejaren |

**Semantisch onderscheid p01 vs p03:** "Ingeschrevenen" verwijst naar het aantal unieke personen dat ingeschreven staat; "Inschrijvingen" verwijst naar het aantal inschrijvingsrecords. Conceptueel vergelijkbaar maar technisch mogelijk verschillend. Nader te verifiëren met DUO-documentatie.

### Bedrijfsproces 2: Afstudering

| Kenmerk | Waarde |
|---------|--------|
| Omschrijving | Het aantal studenten dat in een bepaald jaar een HBO-diploma heeft ontvangen |
| Type | Periodieke snapshot (jaarlijks, per diplomajaar) |
| Brondata | p04hogdipl |
| Meetwaarden | `AANTAL_GEDIPLOMEERDEN` |
| Dimensies | Diplomajaar, Instelling, Opleiding/Sector, Gemeente, Provincie, Geslacht, Diplomatype, Opleidingsvorm |
| Peildatum | Kalenderjaar van diplomaverlening |
| Historische diepte | 5 diplomajaren |

### Ondersteunende processen (referentiedata)

| Proces | Omschrijving | Brondata |
|--------|-------------|----------|
| Opleidingserkenning | NVAO accrediteert een opleiding voor een bepaalde periode | overzicht-erkenningen-ho |
| Programmaregistratie | Een instelling biedt een bekostigde opleiding aan op een locatie | ho_opleidingsoverzicht |

---

## Stap 2.4 — Relaties tussen Entiteiten

### Entiteitrelatiediagram (tekstueel)

```
BESTUUR (1) ──────────────────── heeft (N) INSTELLING
INSTELLING (1) ────────────────── is gevestigd in (N) GEMEENTE
GEMEENTE (N) ──────────────────── ligt in (1) PROVINCIE
INSTELLING (1) ────────────────── biedt aan (N) OPLEIDING [via ho_opleidingsoverzicht]
OPLEIDING (1) ──────────────────── heeft (N) ERKENNING [via overzicht-erkenningen-ho]
INSTELLING + OPLEIDING + STUDIEJAAR ──── telt (1) INSCHRIJVING [p01/p02/p03 feit]
INSTELLING + OPLEIDING + DIPLOMAJAAR ─── telt (1) DIPLOMA [p04 feit]
```

### Sleutelrelaties

| Van | Naar | Type | Via | Opmerking |
|-----|------|------|-----|-----------|
| Statistische datasets | adressen-hogescholen | N:1 | `INSTELLINGSCODE_ACTUEEL` → `INSTELLINGSCODE` | BRIN-sleutel |
| Statistische datasets | overzicht-erkenningen-ho | N:1 | `INSTELLINGSCODE_ACTUEEL` → `INSTELLINGSCODE` | BRIN-sleutel |
| p01b/p02b/p03b/p04b | ho_opleidingsoverzicht | N:1 | `OPLEIDINGSCODE_ACTUEEL` → `ERKENDEOPLEIDINGSCODE` | Beide numeric |
| ho_opleidingsoverzicht | overzicht-erkenningen-ho | 1:N | `ERKENDEOPLEIDINGSCODE` → `ERKENDEOPLEIDINGSCODE` | **Let op:** numeric → text, CAST nodig |
| adressen-hogescholen | adressen-besturen | N:1 | `BEVOEGD GEZAG NUMMER` → `BEVOEGD GEZAG NUMMER` | Spaties in kolomnaam |
| Alle datasets | Gemeentedimensie | N:1 | `GEMEENTENUMMER` | Tekst, voorloopnullen bewaren |

### Aandachtspunten voor het model

1. **Drie bronbestanden per dataset zijn alternatieve aggregaties** — niet stapelbaar. In het model worden ze als aparte feitentabellen of als één feitentabel met nullable dimensies modelleerd.
2. **p01 vs p03:** Semantisch overlap — vermoedelijk dezelfde onderliggende data, anders geëxtraheerd. Aanbeveling: gebruik p01 als primaire bron voor ingeschrevenen, tenzij documentatie anders uitwijst.
3. **Geen studentsleutel beschikbaar** — privacy-wetgeving voorkomt persoonsidentificatie. Het model werkt uitsluitend met geaggregeerde aantallen.
4. **Historische wijzigingen:** Instellingen kunnen fuseren, opgaan in andere instellingen of nieuwe BRIN-codes krijgen. `INSTELLINGSCODE_ACTUEEL` weerspiegelt de huidige code — historische codes niet beschikbaar in deze datasets.

---

## Samenvatting voor Fase 3

Op basis van deze analyse zijn de volgende kandidaten voor het dimensioneel model geïdentificeerd:

### Kandidaat-feitentabellen

| Feitentabel | Bedrijfsproces | Type | Primaire meetwaarde |
|-------------|----------------|------|---------------------|
| `feit_inschrijvingen` | Inschrijving | Periodieke snapshot | Aantal ingeschrevenen |
| `feit_eerstejaars` | Inschrijving (eerstejaars) | Periodieke snapshot | Aantal eerstejaars ingeschrevenen |
| `feit_gediplomeerden` | Afstudering | Periodieke snapshot | Aantal gediplomeerden |

### Kandidaat-dimensietabellen

| Dimensietabel | Sleutel | Bronbestand(en) |
|---------------|---------|-----------------|
| `dim_tijd` | Studiejaar / Diplomajaar | Afgeleid uit statistische datasets |
| `dim_instelling` | BRIN-code | adressen-hogescholen + statistische datasets |
| `dim_opleiding` | CROHO-code | ho_opleidingsoverzicht + p01b–p04b |
| `dim_geografie` | Gemeentenummer | Alle statistische datasets + adressen |
| `dim_geslacht` | M/V | p01a–p04a |
| `dim_opleidingsvorm` | VT/DT/DU | p01c–p04c |
| `dim_bestuur` | Bevoegd gezag nummer | adressen-besturen |
