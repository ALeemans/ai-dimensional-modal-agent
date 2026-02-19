# AI Dimensional Modeling Agent

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6

An AI-driven agent that automatically creates dimensional models (star schemas) from source data.

**Pilot dataset:** DUO Open Onderwijsdata — Hoger Beroeps Onderwijs (HBO)

## Project Goal

Build a reusable AI agent that can generate dimensional models from any data source by:

1. Collecting and analyzing source metadata
2. Identifying fact and dimension candidates
3. Generating star schema designs
4. Producing validated, deployable dimensional models

The DUO HBO data serves as the first subject — the real deliverable is the **agent and its instructions**, which can be applied to any future data source.

## Folder Structure

```
ai-dimensional-modeling/
├── docs/                    # Project documentation and plans
├── agent/
│   ├── instructions/        # Agent instruction documents (the core deliverable)
│   ├── templates/           # Reusable templates for dimensional modeling
│   └── prompts/             # AI prompts for each phase
├── data/
│   ├── raw/                 # Raw API responses and downloads
│   ├── processed/           # Cleaned and structured data
│   └── metadata/            # Collected metadata about sources
├── src/
│   ├── exploration/         # Scripts for API exploration and metadata collection
│   ├── modeling/            # Dimensional model generation logic
│   └── validation/          # Model validation and testing
├── examples/                # Example outputs and reference models
└── tests/                   # Test cases
```

## Links

- [Project Plan](docs/PLAN.md)
- [Agent Instructions](agent/instructions/)
- DUO API info: https://duo.nl/open_onderwijsdata/api.jsp
- DUO Datasets: https://onderwijsdata.duo.nl/datasets/
- HBO data overview: https://duo.nl/open_onderwijsdata/hoger-onderwijs/
