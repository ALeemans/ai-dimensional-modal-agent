"""
build_all.py
Voert alle ETL-scripts uit in de juiste volgorde (op basis van afhankelijkheden).
Run vanuit de projectroot: python scripts/build_all.py

Bouwvolgorde:
  1. Triviale dimensies (geen brondataafhankelijkheden)
  2. Verrijkte dimensies (lezen uit raw data + cross-joins)
  3. Feitentabellen (vereisen alle dimensies)
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PYTHON = sys.executable

STAPPEN = [
    # Stap 1: Triviale dimensies
    ("build_dim_tijd.py",           "dim_tijd"),
    ("build_dim_geslacht.py",       "dim_geslacht"),
    ("build_dim_opleidingsvorm.py", "dim_opleidingsvorm"),
    ("build_dim_soort_diploma.py",  "dim_soort_diploma"),
    # Stap 2: Sector (afgeleid van a/c-varianten)
    ("build_dim_sector.py",         "dim_sector"),
    # Stap 3: Verrijkte dimensies
    ("build_dim_geografie.py",      "dim_geografie"),
    ("build_dim_bestuur.py",        "dim_bestuur"),
    ("build_dim_instelling.py",     "dim_instelling"),
    ("build_dim_opleiding.py",      "dim_opleiding"),
    # Stap 4: Primaire feitentabellen (b-varianten, CROHO-niveau)
    ("build_feit_ingeschrevenen.py",  "feit_ingeschrevenen"),
    ("build_feit_inschrijvingen.py",  "feit_inschrijvingen"),
    ("build_feit_eerstejaars.py",     "feit_eerstejaars"),
    ("build_feit_gediplomeerden.py",  "feit_gediplomeerden"),
    # Stap 5: Aanvullende feitentabellen (a-varianten: sectorniveau + geslacht)
    ("build_feit_ingeschrevenen_geslacht.py",  "feit_ingeschrevenen_geslacht"),
    ("build_feit_inschrijvingen_geslacht.py",  "feit_inschrijvingen_geslacht"),
    ("build_feit_eerstejaars_geslacht.py",     "feit_eerstejaars_geslacht"),
    ("build_feit_gediplomeerden_geslacht.py",  "feit_gediplomeerden_geslacht"),
    # Stap 6: Aanvullende feitentabellen (c-varianten: sectorniveau + opleidingsvorm)
    ("build_feit_ingeschrevenen_oplvorm.py",   "feit_ingeschrevenen_oplvorm"),
    ("build_feit_inschrijvingen_oplvorm.py",   "feit_inschrijvingen_oplvorm"),
    ("build_feit_eerstejaars_oplvorm.py",      "feit_eerstejaars_oplvorm"),
    ("build_feit_gediplomeerden_oplvorm.py",   "feit_gediplomeerden_oplvorm"),
]

start_totaal = time.time()
fouten: list[str] = []

for script_naam, label in STAPPEN:
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    start = time.time()
    result = subprocess.run(
        [PYTHON, str(SCRIPTS_DIR / script_naam)],
        capture_output=True, text=True,
    )
    duur = time.time() - start
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode == 0:
        print(f"  OK ({duur:.1f}s)")
    else:
        err = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "onbekende fout"
        print(f"  FOUT: {err}")
        fouten.append(f"{label}: {err}")

print(f"\n{'='*55}")
print(f"Klaar in {time.time() - start_totaal:.1f}s")
if fouten:
    print(f"\n{len(fouten)} fout(en):")
    for f in fouten:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("Alle tabellen succesvol gebouwd.")
