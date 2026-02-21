"""
build_dim_geografie.py
Bouwt dim_geografie op basis van unieke gemeenten in de b-varianten.
Verrijkt met COROP- en RPA-regio's uit het adressen-hogescholen-bestand.
Output: data/processed/dim_geografie.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_stat_csv, read_adres_csv, write_parquet

print("Bouwen dim_geografie...")

GEO_COLS = ["GEMEENTENUMMER", "GEMEENTENAAM", "PROVINCIENAAM"]

B_FILES = [
    RAW / "p01hoinges" / "ingeschrevenenhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenenhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingenhbo.csv",
    RAW / "p04hogdipl" / "gediplomeerdenhbo.csv",
]

frames = [read_stat_csv(f, usecols=GEO_COLS) for f in B_FILES]
df_geo = pd.concat(frames, ignore_index=True).drop_duplicates().dropna(subset=GEO_COLS)

# Normaliseer gemeentenaam naar title case (bron heeft mixed case)
df_geo["GEMEENTENAAM"] = df_geo["GEMEENTENAAM"].str.title()

# Verrijking: COROP en RPA uit adressen-hogescholen
adr = read_adres_csv(RAW / "adressen" / "01.-instellingen-hbo-en-wo.csv")
adr = adr[adr["SOORT HO"] == "hbo"]

enrich = (
    adr[["GEMEENTENUMMER", "COROPGEBIED CODE", "COROPGEBIED NAAM", "RPA-GEBIED CODE", "RPA-GEBIED NAAM"]]
    .drop_duplicates(subset=["GEMEENTENUMMER"])
    .rename(columns={
        "GEMEENTENUMMER": "gem_nr",
        "COROPGEBIED CODE": "corop_code",
        "COROPGEBIED NAAM": "corop_naam",
        "RPA-GEBIED CODE": "rpa_code",
        "RPA-GEBIED NAAM": "rpa_naam",
    })
)

df_geo = df_geo.merge(enrich, left_on="GEMEENTENUMMER", right_on="gem_nr", how="left")
df_geo.drop(columns=["gem_nr"], inplace=True)

df_geo.rename(columns={
    "GEMEENTENUMMER": "gemeentenummer",
    "GEMEENTENAAM": "gemeentenaam",
    "PROVINCIENAAM": "provincienaam",
}, inplace=True)

df_geo = df_geo.sort_values("gemeentenummer").reset_index(drop=True)
df_geo.insert(0, "geografie_key", range(1, len(df_geo) + 1))

write_parquet(df_geo, "dim_geografie")
