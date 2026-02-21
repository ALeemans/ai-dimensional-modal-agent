"""
etl_utils.py
Gedeelde hulpfuncties voor de DUO HBO ETL-scripts.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def read_stat_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Leest een DUO statistisch CSV-bestand (komma-gescheiden, UTF-8-BOM, quoted)."""
    return pd.read_csv(path, sep=",", encoding="utf-8-sig", dtype=str, **kwargs)


def read_adres_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Leest een DUO adressenbestand (puntkomma-gescheiden, cp1252, niet quoted)."""
    return pd.read_csv(path, sep=";", encoding="cp1252", dtype=str, **kwargs)


def write_parquet(df: pd.DataFrame, name: str) -> None:
    """Schrijft een DataFrame naar de processed-map als Parquet-bestand."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out = PROCESSED / f"{name}.parquet"
    df.to_parquet(out, index=False)
    print(f"  Geschreven: {out.relative_to(ROOT)} ({len(df):,} rijen)")
