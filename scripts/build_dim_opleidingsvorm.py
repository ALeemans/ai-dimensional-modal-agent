"""
build_dim_opleidingsvorm.py
Bouwt dim_opleidingsvorm (statische tabel: VT, DT, DU).
Output: data/processed/dim_opleidingsvorm.parquet
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from etl_utils import write_parquet

print("Bouwen dim_opleidingsvorm...")

df = pd.DataFrame([
    {"opleidingsvorm_key": 1, "opleidingsvorm_code": "VT", "opleidingsvorm_naam": "Voltijd"},
    {"opleidingsvorm_key": 2, "opleidingsvorm_code": "DT", "opleidingsvorm_naam": "Deeltijd"},
    {"opleidingsvorm_key": 3, "opleidingsvorm_code": "DU", "opleidingsvorm_naam": "Duaal"},
])

write_parquet(df, "dim_opleidingsvorm")
