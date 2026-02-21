"""
build_dim_bestuur.py
Bouwt dim_bestuur op basis van het adressen-besturen-bestand (gefilterd op HBO).
Output: data/processed/dim_bestuur.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_adres_csv, write_parquet

print("Bouwen dim_bestuur...")

adr = read_adres_csv(RAW / "adressen" / "03.-bevoegde-gezagen-hbo-en-wo.csv")
df = adr[adr["SOORT HO"] == "hbo"].copy()

df = (
    df[["BEVOEGD GEZAG NUMMER", "BEVOEGD GEZAG NAAM", "DENOMINATIE", "PLAATSNAAM", "KVK-NUMMER"]]
    .drop_duplicates()
    .dropna(subset=["BEVOEGD GEZAG NUMMER"])
)

df.rename(columns={
    "BEVOEGD GEZAG NUMMER": "bevoegd_gezag_nummer",
    "BEVOEGD GEZAG NAAM": "bevoegd_gezag_naam",
    "DENOMINATIE": "denominatie",
    "PLAATSNAAM": "plaatsnaam",
    "KVK-NUMMER": "kvk_nummer",
}, inplace=True)

df = df.sort_values("bevoegd_gezag_nummer").reset_index(drop=True)
df.insert(0, "bestuur_key", range(1, len(df) + 1))

write_parquet(df, "dim_bestuur")
