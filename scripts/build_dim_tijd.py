"""
build_dim_tijd.py
Bouwt dim_tijd op basis van alle studiejaren (p01b, p02b, p03b) en diplomajaren (p04b).
Output: data/processed/dim_tijd.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, write_parquet

print("Bouwen dim_tijd...")

B_FILES = [
    RAW / "p01hoinges" / "ingeschrevenenhbo.csv",
    RAW / "p02ho1ejrs" / "eerstejaarsingeschrevenenhbo.csv",
    RAW / "p03hoinschr" / "inschrijvingenhbo.csv",
]

jaren: set[int] = set()

for f in B_FILES:
    df = pd.read_csv(f, sep=",", encoding="utf-8-sig", usecols=["STUDIEJAAR"], dtype=str)
    jaren.update(int(j) for j in df["STUDIEJAAR"].dropna().unique())

df4 = pd.read_csv(
    RAW / "p04hogdipl" / "gediplomeerdenhbo.csv",
    sep=",", encoding="utf-8-sig", usecols=["DIPLOMAJAAR"], dtype=str,
)
jaren.update(int(j) for j in df4["DIPLOMAJAAR"].dropna().unique())

records = [
    {
        "jaar": jaar,
        "academisch_jaar_label": f"{jaar}/{jaar + 1}",
        "decennium": (jaar // 10) * 10,
    }
    for jaar in sorted(jaren)
]

df_dim = pd.DataFrame(records)
df_dim.insert(0, "tijd_key", range(1, len(df_dim) + 1))

write_parquet(df_dim, "dim_tijd")
