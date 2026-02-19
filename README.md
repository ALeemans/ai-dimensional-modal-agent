# AI Dimensioneel Modelleeringsagent

**Auteur:** Anne Leemans, in samenwerking met Claude Sonnet 4.6

Een AI-gestuurde agent die automatisch dimensionele modellen (sterrenmodellen) opbouwt vanuit brongegevens.

**Pilotdataset:** DUO Open Onderwijsdata — Hoger Beroeps Onderwijs (HBO)

## Projectdoel

Een herbruikbare AI-agent bouwen die dimensionele modellen kan genereren vanuit elke gegevensbron door:

1. Bronmetagegevens te verzamelen en te analyseren
2. Kandidaten voor feitentabellen en dimensietabellen te identificeren
3. Sterrenmodelontwerpen te genereren
4. Gevalideerde, inzetbare dimensionele modellen op te leveren

De DUO HBO-data dient als eerste pilotonderdeel — het echte eindproduct is de **agent en zijn instructies**, die op elke toekomstige gegevensbron kunnen worden toegepast.

## Mappenstructuur

```
ai-dimensional-modeling/
├── docs/                    # Projectdocumentatie en plannen
├── agent/
│   ├── instructions/        # Agentinstructiedocumenten (het kernproduct)
│   ├── templates/           # Herbruikbare sjablonen voor dimensioneel modelleren
│   └── prompts/             # AI-prompts per fase
├── data/
│   ├── raw/                 # Ruwe API-responsen en downloads
│   ├── processed/           # Opgeschoonde en gestructureerde gegevens
│   └── metadata/            # Verzamelde metagegevens over bronnen
├── src/
│   ├── exploration/         # Scripts voor API-verkenning en metagegevensverzameling
│   ├── modeling/            # Logica voor het genereren van dimensionele modellen
│   └── validation/          # Modelvalidatie en -testing
├── examples/                # Voorbeeldoutputs en referentiemodellen
└── tests/                   # Testcases
```

## Links

- [Projectplan](docs/PLAN.md)
- [Agentinstructies](agent/instructions/)
- DUO API-info: https://duo.nl/open_onderwijsdata/api.jsp
- DUO Datasets: https://onderwijsdata.duo.nl/datasets/
- HBO data-overzicht: https://duo.nl/open_onderwijsdata/hoger-onderwijs/
