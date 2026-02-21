"""
build_feit_inschrijvingen_oplvorm.py
Bouwt feit_inschrijvingen_oplvorm vanuit p03c (inschrijvingenoplvhbo.csv).

Korrel: studiejaar × gemeente × instelling × sector × opleidingsvorm
Meetwaarde: aantal_inschrijvingen

Vereisten (run eerst):
  build_dim_tijd.py, build_dim_instelling.py, build_dim_sector.py,
  build_dim_geografie.py, build_dim_opleidingsvorm.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, PROCESSED, read_stat_csv, write_parquet

print("Bouwen feit_inschrijvingen_oplvorm...")

df = read_stat_csv(RAW / "p03hoinschr" / "inschrijvingenoplvhbo.csv")

dim_tijd    = pd.read_parquet(PROCESSED / "dim_tijd.parquet")[["tijd_key", "jaar"]]
dim_inst    = pd.read_parquet(PROCESSED / "dim_instelling.parquet")[["instelling_key", "brin_code"]]
dim_sector  = pd.read_parquet(PROCESSED / "dim_sector.parquet")[["sector_key", "onderdeel", "subonderdeel", "type_hoger_onderwijs"]]
dim_geo     = pd.read_parquet(PROCESSED / "dim_geografie.parquet")[["geografie_key", "gemeentenummer"]]
dim_oplvorm = pd.read_parquet(PROCESSED / "dim_opleidingsvorm.parquet")[["opleidingsvorm_key", "opleidingsvorm_code"]]

df["_jaar"] = pd.to_numeric(df["STUDIEJAAR"], errors="coerce").astype("Int64")
dim_tijd["jaar"] = dim_tijd["jaar"].astype("Int64")

df = df.merge(dim_tijd,    left_on="_jaar",                       right_on="jaar",                how="left")
df = df.merge(dim_inst,    left_on="INSTELLINGSCODE_ACTUEEL",    right_on="brin_code",           how="left")
df = df.merge(dim_sector,  left_on=["ONDERDEEL", "SUBONDERDEEL", "TYPE_HOGER_ONDERWIJS"],
                            right_on=["onderdeel", "subonderdeel", "type_hoger_onderwijs"],       how="left")
df = df.merge(dim_geo,     left_on="GEMEENTENUMMER",             right_on="gemeentenummer",      how="left")
df = df.merge(dim_oplvorm, left_on="OPLEIDINGSVORM",             right_on="opleidingsvorm_code", how="left")

aantallen = pd.to_numeric(df["AANTAL_INSCHRIJVINGEN"], errors="coerce")
df["is_onderdrukt"]         = aantallen == -1
df["aantal_inschrijvingen"] = aantallen.where(aantallen != -1).astype("Int64")

df_feit = df[[
    "tijd_key", "instelling_key", "sector_key", "geografie_key", "opleidingsvorm_key",
    "aantal_inschrijvingen", "is_onderdrukt",
]].copy()
df_feit.insert(0, "id", range(1, len(df_feit) + 1))

write_parquet(df_feit, "feit_inschrijvingen_oplvorm")
