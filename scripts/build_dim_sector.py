"""
build_dim_sector.py
Bouwt dim_sector op basis van unieke (ONDERDEEL, SUBONDERDEEL, TYPE_HOGER_ONDERWIJS)
combinaties in de a/c-varianten.
Gebruikt door aanvullende feitentabellen (geslacht- en opleidingsvorm-varianten).
Output: data/processed/dim_sector.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_stat_csv, write_parquet

print("Bouwen dim_sector...")

COLS = ["ONDERDEEL", "SUBONDERDEEL", "TYPE_HOGER_ONDERWIJS"]

# p01/p02/p03 a/c-varianten hebben TYPE_HOGER_ONDERWIJS
FILES_P01_P03 = [
    RAW / "p01hoinges" / "ingeschrevenengeslhbo.csv",
    RAW / "p01hoinges" / "ingeschrevenenoplvhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenengeslhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenenoplvhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingengeslhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingenoplvhbo.csv",
]

# p04 a/c-varianten hebben SOORT_DIPLOMA i.p.v. TYPE_HOGER_ONDERWIJS
FILES_P04 = [
    RAW / "p04hogdipl" / "gediplomeerdengeslhbo.csv",
    RAW / "p04hogdipl" / "gediplomeerdenoplvhbo.csv",
]

frames = [read_stat_csv(f, usecols=COLS) for f in FILES_P01_P03]

# p04: lees ONDERDEEL + SUBONDERDEEL + SOORT_DIPLOMA, leid TYPE_HOGER_ONDERWIJS af
for f in FILES_P04:
    tmp = read_stat_csv(f, usecols=["ONDERDEEL", "SUBONDERDEEL", "SOORT_DIPLOMA"])
    tmp["TYPE_HOGER_ONDERWIJS"] = tmp["SOORT_DIPLOMA"].str.replace("hbo ", "", regex=False)
    tmp.drop(columns=["SOORT_DIPLOMA"], inplace=True)
    frames.append(tmp)

df = pd.concat(frames, ignore_index=True).drop_duplicates().dropna(subset=COLS)
df = df.sort_values(COLS).reset_index(drop=True)

df.rename(columns={
    "ONDERDEEL": "onderdeel",
    "SUBONDERDEEL": "subonderdeel",
    "TYPE_HOGER_ONDERWIJS": "type_hoger_onderwijs",
}, inplace=True)

df.insert(0, "sector_key", range(1, len(df) + 1))

write_parquet(df, "dim_sector")
