"""
build_dim_geslacht.py
Bouwt dim_geslacht (statische tabel: MAN, VROUW).
Output: data/processed/dim_geslacht.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import write_parquet

print("Bouwen dim_geslacht...")

df = pd.DataFrame([
    {"geslacht_key": 1, "geslacht": "MAN"},
    {"geslacht_key": 2, "geslacht": "VROUW"},
])

write_parquet(df, "dim_geslacht")
