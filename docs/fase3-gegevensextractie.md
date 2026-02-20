# Fase 3: Gegevensextractie — Uitvoeringsplan

**Auteur:** Anne Leemans, in samenwerking met Claude Sonnet 4.6
**Datum:** 2026-02-20

---

## Doel

Alle benodigde ruwe DUO HBO-brongegevens lokaal en reproduceerbaar beschikbaar maken. De gedownloade bestanden dienen als invoer voor Fase 4 (modelontwerp) en Fase 5 (validatie).

---

## Stap 3.1 — Extractiestrategie per Dataset

Er zijn twee typen bronnen, elk met een eigen downloadmethode:

### Type A: CKAN Datastore API

Datasets die via de DUO CKAN API beschikbaar zijn als datastore-resources (querybaar, pagineerbaar).

| Dataset-ID | Naam | Resources (HBO) | Methode |
|------------|------|-----------------|---------|
| p01hoinges | Ingeschrevenen HBO | 3 CSV's | CKAN resource download |
| p02ho1ejrs | Eerstejaars ingeschrevenen HBO | 3 CSV's | CKAN resource download |
| p03hoinschr | Inschrijvingen HBO | 3 CSV's | CKAN resource download |
| p04hogdipl | Gediplomeerden HBO | 3 CSV's | CKAN resource download |
| ho_opleidingsoverzicht | HO Opleidingsoverzicht | 1 CSV | CKAN resource download |
| overzicht-erkenningen-ho | Overzicht Erkenningen HO | 1 CSV | CKAN resource download |

**API-stroom:**
1. `GET /api/3/action/package_show?id={dataset_id}` → haalt lijst van resources op
2. Filter op HBO-specifieke resources (op bestandsnaam of beschrijving)
3. `GET /api/3/action/resource_show?id={resource_id}` → haalt download-URL op
4. Download CSV via de directe URL

**Basispunt:** `https://onderwijsdata.duo.nl`

### Type B: Directe bestandsdownload

Datasets die niet in CKAN zitten maar als statische bestanden op duo.nl staan.

| Naam | Bestand | Bron-URL |
|------|---------|----------|
| Adressen hogescholen en universiteiten | `01.-instellingen-hbo-en-wo.csv` | `https://duo.nl/open_onderwijsdata/images/01.-instellingen-hbo-en-wo.csv` |
| Adressen besturen hogescholen en universiteiten | `03.-bevoegde-gezagen-hbo-en-wo.csv` | `https://duo.nl/open_onderwijsdata/images/03.-bevoegde-gezagen-hbo-en-wo.csv` |

**Let op:** Deze bestanden gebruiken `;` als scheidingsteken en hebben spaties in kolomnamen.

---

## Stap 3.2 — Uitvoerdirectorystructuur

```
data/
└── raw/
    ├── p01hoinges/
    │   ├── ingeschrevenengeslhbo.csv       # resource 1a: geslacht
    │   ├── ingeschrevenenhbo.csv           # resource 1b: niveau (CROHO)
    │   └── ingeschrevenenoplvhbo.csv       # resource 1c: opleidingsvorm
    ├── p02ho1ejrs/
    │   ├── 1ejrsingeschrevenengeslhbo.csv
    │   ├── 1ejrsingeschrevenenhbo.csv
    │   └── 1ejrsingeschrevenenoplvhbo.csv
    ├── p03hoinschr/
    │   ├── inschrijvingengeslhbo.csv
    │   ├── inschrijvingenhbo.csv
    │   └── inschrijvingenoplvhbo.csv
    ├── p04hogdipl/
    │   ├── gediplomeerdengeslhbo.csv
    │   ├── gediplomeerdenhbo.csv
    │   └── gediplomeerdenoplvhbo.csv
    ├── ho_opleidingsoverzicht/
    │   └── ho_opleidingsoverzicht.csv
    ├── overzicht-erkenningen-ho/
    │   └── ho_erkenningen_rio.csv
    └── adressen/
        ├── 01.-instellingen-hbo-en-wo.csv
        └── 03.-bevoegde-gezagen-hbo-en-wo.csv
```

---

## Stap 3.3 — Scriptstructuur (`scripts/duo_hbo_extractor.py`)

Het script wordt opgebouwd uit de volgende onderdelen:

### Configuratie

```python
# Vaste instellingen — geen hardcoded waarden in functies
CKAN_BASE_URL = "https://onderwijsdata.duo.nl"
OUTPUT_DIR = Path("data/raw")

# CKAN datasets met hun HBO-resource filters
CKAN_DATASETS = {
    "p01hoinges": {"filter": "hbo"},      # 3 resources
    "p02ho1ejrs": {"filter": "hbo"},      # 3 resources
    "p03hoinschr": {"filter": "hbo"},     # 3 resources
    "p04hogdipl":  {"filter": "hbo"},     # 3 resources
    "ho_opleidingsoverzicht": {},          # 1 resource
    "overzicht-erkenningen-ho": {},        # 1 resource
}

# Directe downloads (niet via CKAN)
DIRECT_DOWNLOADS = {
    "adressen/01.-instellingen-hbo-en-wo.csv":
        "https://duo.nl/open_onderwijsdata/images/01.-instellingen-hbo-en-wo.csv",
    "adressen/03.-bevoegde-gezagen-hbo-en-wo.csv":
        "https://duo.nl/open_onderwijsdata/images/03.-bevoegde-gezagen-hbo-en-wo.csv",
}
```

### Functies

| Functie | Invoer | Uitvoer | Beschrijving |
|---------|--------|---------|-------------|
| `get_package_resources(dataset_id)` | Dataset-ID | Lijst van resources | Haalt alle resources op via `package_show` |
| `filter_hbo_resources(resources)` | Resourcelijst | Gefilterde lijst | Behoudt alleen HBO-specifieke CSV-resources |
| `download_resource(resource, output_path)` | Resource-object, pad | Bestand op schijf | Downloadt één resource-CSV |
| `download_direct(url, output_path)` | URL, pad | Bestand op schijf | Downloadt een bestand rechtstreeks |
| `verify_download(path, expected_min_rows)` | Bestandspad, minimum | bool | Controleert bestand op rijen en leesbaarheid |
| `run_extraction()` | — | Manifest-dict | Orkestreert alle downloads, logt resultaten |

### Manifest / Logbestand

Na afronding schrijft het script een `data/raw/manifest.json` met:

```json
{
  "extracted_at": "2026-02-20T10:00:00",
  "datasets": {
    "p01hoinges": {
      "resources": [
        {
          "filename": "ingeschrevenengeslhbo.csv",
          "rows": 4833,
          "size_bytes": 780288,
          "downloaded_at": "2026-02-20T10:00:05",
          "status": "ok"
        }
      ]
    }
  }
}
```

---

## Stap 3.4 — Uitvoering

Het script wordt uitgevoerd via de commandoregel:

```bash
python scripts/duo_hbo_extractor.py
```

**Vereisten:**
- Python 3.10+
- Paketten: `requests`, `pathlib` (standaard), `json` (standaard)

**Installatie afhankelijkheden:**
```bash
pip install requests
```

Of via een nog aan te maken `requirements.txt`.

---

## Stap 3.5 — Verificatie

Na het downloaden controleren we per dataset:

| Controle | Methode | Drempelwaarde |
|----------|---------|--------------|
| Bestand aanwezig | `Path.exists()` | Verplicht |
| Bestandsgrootte > 0 | `Path.stat().st_size` | > 0 bytes |
| Leesbaar als CSV | `pandas.read_csv()` of `csv.reader` | Geen parseerfout |
| Rijtellingen | Vergelijk met metagegevenscatalogus | ±10% van verwachte aantallen |
| Kolomnamen aanwezig | Vergelijk met veldprofielen | Exacte match verwacht |

**Verwachte rijtellingen (uit metagegevenscatalogus Fase 1):**

| Bestand | Verwacht |
|---------|---------|
| ingeschrevenengeslhbo.csv | ~4.833 |
| ingeschrevenenhbo.csv | ~7.170 |
| ingeschrevenenoplvhbo.csv | ~3.889 |
| 1ejrsingeschrevenengeslhbo.csv | ~3.407 |
| 1ejrsingeschrevenenhbo.csv | ~5.834 |
| 1ejrsingeschrevenenoplvhbo.csv | ~2.908 |
| inschrijvingengeslhbo.csv | ~4.835 |
| inschrijvingenhbo.csv | ~7.174 |
| inschrijvingenoplvhbo.csv | ~3.891 |
| gediplomeerdengeslhbo.csv | ~4.445 |
| gediplomeerdenhbo.csv | ~6.813 |
| gediplomeerdenoplvhbo.csv | ~3.591 |
| ho_opleidingsoverzicht.csv | ~7.090 |
| ho_erkenningen_rio.csv | ~6.747 |
| 01.-instellingen-hbo-en-wo.csv | ~50 |
| 03.-bevoegde-gezagen-hbo-en-wo.csv | ~50 |

---

## Stap 3.6 — Agentinstructie

Na afronding schrijven we `agent/instructions/03-gegevensextractie.md` (Engels, herbruikbaar) met:
- Wanneer een extractiescript bouwen vs. directe API-aanroepen gebruiken
- Hoe CKAN-gebaseerde open data APIs te bevragen
- Manifestpatroon voor reproduceerbare downloads
- Verificatiestrategie voor ruwe gegevens

---

## Openstaande Vragen / Risico's

| Vraag | Risico | Actie |
|-------|--------|-------|
| Zijn de CKAN resource-download-URLs stabiel? | URLs kunnen veranderen bij heruitgave | Altijd via `package_show` ophalen, nooit hardcoden |
| Vereist duo.nl authenticatie? | Blokkade download | Testen bij uitvoering; waarschijnlijk niet (open data) |
| Kunnen bestanden te groot zijn voor geheugen? | Crash bij grote datasets | Streaming download gebruiken (geen volledige buffer in geheugen) |
| Semantisch verschil p01 vs. p03? | Verkeerde modellering | Vergelijken na download: zijn de rijen identiek, bijna identiek, of wezenlijk anders? |
