"""
duo_hbo_extractor.py — DUO HBO Gegevensextractie
=================================================
Downloads alle benodigde ruwe brongegevens van DUO Open Onderwijsdata
en slaat ze op in data/raw/ voor gebruik in Fase 4 (modelontwerp) en Fase 5 (validatie).

Gebruik (vanuit projectroot):
    python scripts/duo_hbo_extractor.py

Vereisten:
    pip install requests
    (of: pip install -r requirements.txt)

Uitvoer:
    data/raw/{dataset}/         — gedownloade CSV-bestanden
    data/raw/manifest.json      — downloadlog met rijtellingen en status
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import requests

# ─── Configuratie ─────────────────────────────────────────────────────────────

CKAN_BASE_URL = "https://onderwijsdata.duo.nl"
OUTPUT_DIR = Path("data/raw")
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

# CKAN datasets: key = dataset_id, subdir = uitvoermap onder data/raw/
# hbo_only=True filtert resources op 'hbo' in de bestandsnaam (sluit WO-bestanden uit)
CKAN_DATASETS = {
    "p01hoinges": {
        "subdir": "p01hoinges",
        "hbo_only": True,
    },
    "p02ho1ejrs": {
        "subdir": "p02ho1ejrs",
        "hbo_only": True,
    },
    "p03hoinschr": {
        "subdir": "p03hoinschr",
        "hbo_only": True,
    },
    "p04hogdipl": {
        "subdir": "p04hogdipl",
        "hbo_only": True,
    },
    "ho_opleidingsoverzicht": {
        "subdir": "ho_opleidingsoverzicht",
        "hbo_only": False,
    },
    "overzicht-erkenningen-ho": {
        "subdir": "overzicht-erkenningen-ho",
        "hbo_only": False,
    },
}

# Directe downloads — adresbestanden staan niet in CKAN maar op duo.nl
DIRECT_DOWNLOADS = [
    {
        "url": "https://duo.nl/open_onderwijsdata/images/01.-instellingen-hbo-en-wo.csv",
        "subdir": "adressen",
        "filename": "01.-instellingen-hbo-en-wo.csv",
    },
    {
        "url": "https://duo.nl/open_onderwijsdata/images/03.-bevoegde-gezagen-hbo-en-wo.csv",
        "subdir": "adressen",
        "filename": "03.-bevoegde-gezagen-hbo-en-wo.csv",
    },
]

# Verwachte minimale rijtellingen (uit metagegevenscatalogus Fase 1, ~10% marge)
EXPECTED_MIN_ROWS: dict[str, int] = {
    "ingeschrevenengeslhbo.csv":       4_300,
    "ingeschrevenenhbo.csv":           6_400,
    "ingeschrevenenoplvhbo.csv":       3_500,
    "1ejrsingeschrevenengeslhbo.csv":  3_000,
    "1ejrsingeschrevenenhbo.csv":      5_200,
    "1ejrsingeschrevenenoplvhbo.csv":  2_600,
    "inschrijvingengeslhbo.csv":       4_300,
    "inschrijvingenhbo.csv":           6_400,
    "inschrijvingenoplvhbo.csv":       3_500,
    "gediplomeerdengeslhbo.csv":       4_000,
    "gediplomeerdenhbo.csv":           6_100,
    "gediplomeerdenoplvhbo.csv":       3_200,
    "ho_opleidingsoverzicht.csv":      6_300,
    "ho_erkenningen_rio.csv":          6_000,
}

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ─── CKAN API ─────────────────────────────────────────────────────────────────

def get_package_resources(session: requests.Session, dataset_id: str) -> list[dict]:
    """Haalt alle resources op voor een CKAN dataset via package_show."""
    url = f"{CKAN_BASE_URL}/api/3/action/package_show"
    response = session.get(url, params={"id": dataset_id}, timeout=30)
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise ValueError(f"CKAN API fout voor '{dataset_id}': {data.get('error')}")
    return data["result"]["resources"]


def is_hbo_csv(resource: dict) -> bool:
    """
    Controleert of een resource een HBO-specifieke CSV is.
    Filtert op 'hbo' in de bestandsnaam én op CSV-formaat.
    """
    url = resource.get("url", "").lower()
    fmt = resource.get("format", "").upper()
    filename = url.split("/")[-1].lower()

    is_csv = fmt == "CSV" or filename.endswith(".csv")
    return is_csv and "hbo" in filename


def is_csv(resource: dict) -> bool:
    """Controleert of een resource een CSV is (voor datasets zonder HBO-filter)."""
    url = resource.get("url", "").lower()
    fmt = resource.get("format", "").upper()
    filename = url.split("/")[-1].lower()
    return fmt == "CSV" or filename.endswith(".csv")


# ─── Downloaden & Verificatie ─────────────────────────────────────────────────

def download_file(session: requests.Session, url: str, dest_path: Path) -> int:
    """
    Downloadt een bestand via streaming naar dest_path.
    Geeft het aantal geschreven bytes terug.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        bytes_written = 0
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=16_384):
                f.write(chunk)
                bytes_written += len(chunk)
    return bytes_written


def count_rows(path: Path) -> int:
    """Telt het aantal datarijen in een CSV (exclusief header)."""
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            total = sum(1 for _ in f)
        return max(total - 1, 0)  # -1 voor header, nooit negatief
    except Exception:
        return -1


def verify_file(path: Path) -> dict:
    """Verifieert een gedownload bestand. Geeft status en eventuele waarschuwingen."""
    rows = count_rows(path)
    filename = path.name
    min_expected = EXPECTED_MIN_ROWS.get(filename, 1)

    warnings = []

    if rows < 0:
        return {"rows": rows, "size_bytes": 0, "status": "error",
                "warnings": ["Kon bestand niet lezen"]}

    if rows == 0:
        warnings.append("Bestand bevat geen datarijen")
        status = "error"
    elif rows < min_expected:
        warnings.append(f"Minder rijen dan verwacht: {rows} < minimaal {min_expected}")
        status = "warning"
    else:
        status = "ok"

    return {
        "rows": rows,
        "size_bytes": path.stat().st_size,
        "status": status,
        "warnings": warnings,
    }


# ─── Extractie ────────────────────────────────────────────────────────────────

def extract_ckan_dataset(
    session: requests.Session,
    dataset_id: str,
    config: dict,
) -> dict:
    """Downloadt alle relevante resources van één CKAN dataset."""
    log.info(f"[{dataset_id}]")
    subdir = OUTPUT_DIR / config["subdir"]
    dataset_result: dict = {"resources": []}

    try:
        all_resources = get_package_resources(session, dataset_id)
    except Exception as exc:
        log.error(f"  Kon resources niet ophalen: {exc}")
        dataset_result["status"] = "error"
        dataset_result["error"] = str(exc)
        return dataset_result

    # Filter op HBO-CSV of gewone CSV
    if config["hbo_only"]:
        resources = [r for r in all_resources if is_hbo_csv(r)]
    else:
        resources = [r for r in all_resources if is_csv(r)]

    log.info(f"  {len(resources)} CSV-resource(s) geselecteerd van {len(all_resources)} totaal")

    for resource in resources:
        url = resource.get("url", "")
        filename = url.split("/")[-1] or (resource.get("name", "resource") + ".csv")
        dest_path = subdir / filename

        log.info(f"  → {filename}")
        try:
            bytes_written = download_file(session, url, dest_path)
            verification = verify_file(dest_path)

            icon = "✓" if verification["status"] == "ok" else "⚠"
            log.info(f"    {icon}  {verification['rows']:,} rijen  |  {bytes_written:,} bytes")
            for warning in verification["warnings"]:
                log.warning(f"       ! {warning}")

            dataset_result["resources"].append({
                "filename": filename,
                "url": url,
                "downloaded_at": datetime.now().isoformat(),
                **verification,
            })

        except Exception as exc:
            log.error(f"    ✗ Download mislukt: {exc}")
            dataset_result["resources"].append({
                "filename": filename,
                "url": url,
                "status": "error",
                "error": str(exc),
            })

    return dataset_result


def extract_direct_downloads(session: requests.Session) -> dict:
    """Downloadt adresbestanden via directe URL (niet via CKAN)."""
    log.info("[adressen]  (directe download)")
    result: dict = {"resources": []}

    for item in DIRECT_DOWNLOADS:
        dest_path = OUTPUT_DIR / item["subdir"] / item["filename"]
        log.info(f"  → {item['filename']}")
        try:
            bytes_written = download_file(session, item["url"], dest_path)
            verification = verify_file(dest_path)

            icon = "✓" if verification["status"] == "ok" else "⚠"
            log.info(f"    {icon}  {verification['rows']:,} rijen  |  {bytes_written:,} bytes")
            for warning in verification["warnings"]:
                log.warning(f"       ! {warning}")

            result["resources"].append({
                "filename": item["filename"],
                "url": item["url"],
                "downloaded_at": datetime.now().isoformat(),
                **verification,
            })

        except Exception as exc:
            log.error(f"    ✗ Download mislukt: {exc}")
            result["resources"].append({
                "filename": item["filename"],
                "url": item["url"],
                "status": "error",
                "error": str(exc),
            })

    return result


# ─── Hoofdprogramma ───────────────────────────────────────────────────────────

def main() -> None:
    log.info("=" * 55)
    log.info("  DUO HBO Gegevensextractie")
    log.info(f"  Uitvoermap : {OUTPUT_DIR.resolve()}")
    log.info(f"  Gestart op : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 55)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest: dict = {
        "extracted_at": datetime.now().isoformat(),
        "datasets": {},
    }

    with requests.Session() as session:
        session.headers.update({"User-Agent": "DUO-HBO-Extractor/1.0"})

        # CKAN datasets
        for dataset_id, config in CKAN_DATASETS.items():
            manifest["datasets"][dataset_id] = extract_ckan_dataset(
                session, dataset_id, config
            )

        # Directe downloads
        manifest["datasets"]["adressen"] = extract_direct_downloads(session)

    # Manifest opslaan
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Samenvatting
    all_resources = [
        r
        for ds in manifest["datasets"].values()
        for r in ds.get("resources", [])
    ]
    n_ok      = sum(1 for r in all_resources if r.get("status") == "ok")
    n_warning = sum(1 for r in all_resources if r.get("status") == "warning")
    n_error   = sum(1 for r in all_resources if r.get("status") == "error")

    log.info("=" * 55)
    log.info(f"  Klaar. {len(all_resources)} bestanden verwerkt.")
    log.info(f"  ✓ ok: {n_ok}   ⚠ waarschuwing: {n_warning}   ✗ fout: {n_error}")
    log.info(f"  Manifest: {MANIFEST_PATH}")
    log.info("=" * 55)

    if n_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
