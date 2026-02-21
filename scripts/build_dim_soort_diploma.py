"""
build_dim_soort_diploma.py
Bouwt dim_soort_diploma op basis van unieke waarden in p04b.
Output: data/processed/dim_soort_diploma.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import RAW, read_stat_csv, write_parquet

print("Bouwen dim_soort_diploma...")

df = read_stat_csv(RAW / "p04hogdipl" / "gediplomeerdenhbo.csv", usecols=["SOORT_DIPLOMA"])
soorten = sorted(df["SOORT_DIPLOMA"].dropna().unique())

df_dim = pd.DataFrame({"soort_diploma": soorten})
df_dim.insert(0, "soort_diploma_key", range(1, len(df_dim) + 1))

write_parquet(df_dim, "dim_soort_diploma")
