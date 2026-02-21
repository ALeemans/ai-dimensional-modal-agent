"""
build_feit_ingeschrevenen.py
Bouwt feit_ingeschrevenen vanuit p01b (ingeschrevenenhbo.csv).
Koppelt dimensiesleutels via de reeds gebouwde dim_*.parquet-bestanden.

Korrel: studiejaar × gemeente × instelling × opleiding (CROHO)
Meetwaarde: aantal_ingeschrevenen (unieke personen, hoofdinschrijving)
Privacyonderdrukking: -1 → NULL + is_onderdrukt = True

Vereisten (run eerst):
  build_dim_tijd.py, build_dim_instelling.py,
  build_dim_opleiding.py, build_dim_geografie.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, PROCESSED, read_stat_csv, write_parquet

print("Bouwen feit_ingeschrevenen...")

# --- Brondata laden ---
df = read_stat_csv(RAW / "p01hoinges" / "ingeschrevenenhbo.csv")

# --- Dimensies laden (alleen benodigde kolommen) ---
dim_tijd = pd.read_parquet(PROCESSED / "dim_tijd.parquet")[["tijd_key", "jaar"]]
dim_inst = pd.read_parquet(PROCESSED / "dim_instelling.parquet")[["instelling_key", "brin_code"]]
dim_opl  = pd.read_parquet(PROCESSED / "dim_opleiding.parquet")[["opleiding_key", "croho_code"]]
dim_geo  = pd.read_parquet(PROCESSED / "dim_geografie.parquet")[["geografie_key", "gemeentenummer"]]

# --- Sleutelkolommen casten voor join ---
df["_jaar"]  = pd.to_numeric(df["STUDIEJAAR"], errors="coerce").astype("Int64")
df["_croho"] = pd.to_numeric(df["OPLEIDINGSCODE_ACTUEEL"], errors="coerce").astype("Int64")
dim_tijd["jaar"] = dim_tijd["jaar"].astype("Int64")
dim_opl["croho_code"] = dim_opl["croho_code"].astype("Int64")

# --- Dimensiesleutels koppelen ---
df = df.merge(dim_tijd, left_on="_jaar",                       right_on="jaar",          how="left")
df = df.merge(dim_inst, left_on="INSTELLINGSCODE_ACTUEEL",    right_on="brin_code",     how="left")
df = df.merge(dim_opl,  left_on="_croho",                     right_on="croho_code",    how="left")
df = df.merge(dim_geo,  left_on="GEMEENTENUMMER",             right_on="gemeentenummer", how="left")

# --- Privacyonderdrukking (-1 → NULL) ---
aantallen = pd.to_numeric(df["AANTAL_INGESCHREVENEN"], errors="coerce")
df["is_onderdrukt"]         = aantallen == -1
df["aantal_ingeschrevenen"] = aantallen.where(aantallen != -1).astype("Int64")

# --- Feitentabel samenstellen ---
df_feit = df[[
    "tijd_key", "instelling_key", "opleiding_key", "geografie_key",
    "aantal_ingeschrevenen", "is_onderdrukt",
]].copy()

df_feit.insert(0, "ingeschrevenen_key", range(1, len(df_feit) + 1))

write_parquet(df_feit, "feit_ingeschrevenen")
