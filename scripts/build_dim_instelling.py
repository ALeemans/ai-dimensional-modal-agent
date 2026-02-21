"""
build_dim_instelling.py
Bouwt dim_instelling op basis van unieke instellingen in de b-varianten.
Verrijkt met bestuursnummer, denominatie en contactgegevens uit adressen-hogescholen.
Output: data/processed/dim_instelling.parquet

Vereisten: geen (leest direct uit raw data)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_stat_csv, read_adres_csv, write_parquet

print("Bouwen dim_instelling...")

INST_COLS = ["INSTELLINGSCODE_ACTUEEL", "INSTELLINGSNAAM_ACTUEEL", "SOORT_INSTELLING"]

B_FILES = [
    RAW / "p01hoinges" / "ingeschrevenenhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenenhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingenhbo.csv",
    RAW / "p04hogdipl" / "gediplomeerdenhbo.csv",
]

frames = [read_stat_csv(f, usecols=INST_COLS) for f in B_FILES]
df_inst = (
    pd.concat(frames, ignore_index=True)
    .dropna(subset=["INSTELLINGSCODE_ACTUEEL"])
    .drop_duplicates(subset=["INSTELLINGSCODE_ACTUEEL"])
)

# Verrijking via adressen-hogescholen
adr = read_adres_csv(RAW / "adressen" / "01.-instellingen-hbo-en-wo.csv")
adr = adr[adr["SOORT HO"] == "hbo"]

adr_enrich = (
    adr[["INSTELLINGSCODE", "BEVOEGD GEZAG NUMMER", "DENOMINATIE", "STRAATNAAM", "POSTCODE", "PLAATSNAAM", "INTERNETADRES"]]
    .drop_duplicates(subset=["INSTELLINGSCODE"])
)

df_inst = df_inst.merge(
    adr_enrich,
    left_on="INSTELLINGSCODE_ACTUEEL",
    right_on="INSTELLINGSCODE",
    how="left",
)
df_inst.drop(columns=["INSTELLINGSCODE"], inplace=True)

df_inst.rename(columns={
    "INSTELLINGSCODE_ACTUEEL": "brin_code",
    "INSTELLINGSNAAM_ACTUEEL": "instellingsnaam",
    "SOORT_INSTELLING": "soort_instelling",
    "BEVOEGD GEZAG NUMMER": "bevoegd_gezag_nummer",
    "DENOMINATIE": "denominatie",
    "STRAATNAAM": "straatnaam",
    "POSTCODE": "postcode",
    "PLAATSNAAM": "plaatsnaam",
    "INTERNETADRES": "website",
}, inplace=True)

df_inst = df_inst.sort_values("brin_code").reset_index(drop=True)
df_inst.insert(0, "instelling_key", range(1, len(df_inst) + 1))

write_parquet(df_inst, "dim_instelling")
