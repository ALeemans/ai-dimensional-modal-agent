"""
build_dim_opleiding.py
Bouwt dim_opleiding op basis van unieke CROHO-codes in de b-varianten.
Verrijkt met ECTS, EQF, ISCED, NLQF en voertaal uit ho_opleidingsoverzicht.
Output: data/processed/dim_opleiding.parquet

Noot: ho_opleidingsoverzicht bevat meerdere rijen per CROHO-code (per locatie/aanbieder).
Bij de join wordt gededupliceerd op ERKENDEOPLEIDINGSCODE (eerste voorkomen).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_stat_csv, write_parquet

print("Bouwen dim_opleiding...")

OPL_COLS = [
    "OPLEIDINGSCODE_ACTUEEL", "OPLEIDINGSNAAM_ACTUEEL",
    "TYPE_HOGER_ONDERWIJS", "ONDERDEEL", "SUBONDERDEEL",
]

# p01b/p02b/p03b hebben TYPE_HOGER_ONDERWIJS
FILES_P01_P03 = [
    RAW / "p01hoinges" / "ingeschrevenenhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenenhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingenhbo.csv",
]

frames = [read_stat_csv(f, usecols=OPL_COLS) for f in FILES_P01_P03]

# p04b heeft SOORT_DIPLOMA i.p.v. TYPE_HOGER_ONDERWIJS
P04_COLS = ["OPLEIDINGSCODE_ACTUEEL", "OPLEIDINGSNAAM_ACTUEEL", "ONDERDEEL", "SUBONDERDEEL", "SOORT_DIPLOMA"]
p04 = read_stat_csv(RAW / "p04hogdipl" / "gediplomeerdenhbo.csv", usecols=P04_COLS)
p04["TYPE_HOGER_ONDERWIJS"] = p04["SOORT_DIPLOMA"].str.replace("hbo ", "", regex=False)
p04.drop(columns=["SOORT_DIPLOMA"], inplace=True)
frames.append(p04)

df_opl = (
    pd.concat(frames, ignore_index=True)
    .dropna(subset=["OPLEIDINGSCODE_ACTUEEL"])
    .drop_duplicates(subset=["OPLEIDINGSCODE_ACTUEEL"])
)

# Verrijking via ho_opleidingsoverzicht
RIO_COLS = ["ERKENDEOPLEIDINGSCODE", "GRAAD", "STUDIELAST", "EQF", "ISCED", "NLQF", "VOERTAAL"]
rio = read_stat_csv(RAW / "ho_opleidingsoverzicht" / "ho_opleidingsoverzicht.csv", usecols=RIO_COLS)
rio = rio.drop_duplicates(subset=["ERKENDEOPLEIDINGSCODE"])

df_opl = df_opl.merge(
    rio,
    left_on="OPLEIDINGSCODE_ACTUEEL",
    right_on="ERKENDEOPLEIDINGSCODE",
    how="left",
)
df_opl.drop(columns=["ERKENDEOPLEIDINGSCODE"], inplace=True)

# Cast CROHO-code naar nullable integer
df_opl["OPLEIDINGSCODE_ACTUEEL"] = pd.to_numeric(
    df_opl["OPLEIDINGSCODE_ACTUEEL"], errors="coerce"
).astype("Int64")

df_opl.rename(columns={
    "OPLEIDINGSCODE_ACTUEEL": "croho_code",
    "OPLEIDINGSNAAM_ACTUEEL": "opleidingsnaam",
    "TYPE_HOGER_ONDERWIJS": "type_hoger_onderwijs",
    "ONDERDEEL": "onderdeel",
    "SUBONDERDEEL": "subonderdeel",
    "GRAAD": "graad",
    "STUDIELAST": "studielast_ects",
    "EQF": "eqf_niveau",
    "ISCED": "isced_code",
    "NLQF": "nlqf_niveau",
    "VOERTAAL": "voertaal",
}, inplace=True)

df_opl = df_opl.sort_values("croho_code").reset_index(drop=True)
df_opl.insert(0, "opleiding_key", range(1, len(df_opl) + 1))

write_parquet(df_opl, "dim_opleiding")
