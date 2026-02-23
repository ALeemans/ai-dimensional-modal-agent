"""
generate_powerbi_tmdl.py

Generates Power BI TMDL files for the DUO HBO dimensional model.
Reads actual column schemas from data/processed/ parquet files and writes
TMDL to powerbi/dim-duo-ai-model.SemanticModel/definition/.

Output:
  definition/model.tmdl               — full model file (queryGroups, ref tables, annotations)
  definition/relationships.tmdl       — all FK relationships
  definition/tables/<TableName>.tmdl  — one file per table (21 total)

Usage:
  python scripts/generate_powerbi_tmdl.py

Re-run whenever parquet schemas change.
"""

import uuid
import pyarrow.parquet as pq
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).parent.parent
PROCESSED = ROOT / "data" / "processed"
DEFINITION = ROOT / "powerbi" / "dim-duo-ai-model.SemanticModel" / "definition"
TABLES_DIR = DEFINITION / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)


# === Display names ===

TABLE_NAMES: dict[str, str] = {
    "dim_bestuur":                   "Bestuur",
    "dim_geografie":                 "Geografie",
    "dim_geslacht":                  "Geslacht",
    "dim_instelling":                "Instelling",
    "dim_opleiding":                 "Opleiding",
    "dim_opleidingsvorm":            "Opleidingsvorm",
    "dim_sector":                    "Sector",
    "dim_soort_diploma":             "Soort Diploma",
    "dim_tijd":                      "Tijd",
    "feit_ingeschrevenen":           "Ingeschrevenen",
    "feit_inschrijvingen":           "Inschrijvingen",
    "feit_eerstejaars":              "Eerstejaars",
    "feit_gediplomeerden":           "Gediplomeerden",
    "feit_ingeschrevenen_geslacht":  "Ingeschrevenen naar Geslacht",
    "feit_inschrijvingen_geslacht":  "Inschrijvingen naar Geslacht",
    "feit_eerstejaars_geslacht":     "Eerstejaars naar Geslacht",
    "feit_gediplomeerden_geslacht":  "Gediplomeerden naar Geslacht",
    "feit_ingeschrevenen_oplvorm":   "Ingeschrevenen naar Opleidingsvorm",
    "feit_inschrijvingen_oplvorm":   "Inschrijvingen naar Opleidingsvorm",
    "feit_eerstejaars_oplvorm":      "Eerstejaars naar Opleidingsvorm",
    "feit_gediplomeerden_oplvorm":   "Gediplomeerden naar Opleidingsvorm",
}

# source_column_name -> display name shown in Power BI
COLUMN_NAMES: dict[str, str] = {
    # dim_tijd
    "tijd_key":               "Tijd Key",
    "jaar":                   "Jaar",
    "academisch_jaar_label":  "Academisch Jaar",
    "decennium":              "Decennium",
    # dim_instelling
    "instelling_key":         "Instelling Key",
    "brin_code":              "BRIN Code",
    "instellingsnaam":        "Instellingsnaam",
    "soort_instelling":       "Soort Instelling",
    "denominatie":            "Denominatie",
    "bevoegd_gezag_nummer":   "Bevoegd Gezag Nummer",
    "straatnaam":             "Straatnaam",
    "postcode":               "Postcode",
    "plaatsnaam":             "Plaatsnaam",
    "website":                "Website",
    # dim_opleiding
    "opleiding_key":          "Opleiding Key",
    "croho_code":             "CROHO Code",
    "opleidingsnaam":         "Opleidingsnaam",
    "type_hoger_onderwijs":   "Type Hoger Onderwijs",
    "onderdeel":              "Onderdeel",
    "subonderdeel":           "Subonderdeel",
    "graad":                  "Graad",
    "studielast_ects":        "Studielast ECTS",
    "eqf_niveau":             "EQF Niveau",
    "isced_code":             "ISCED Code",
    "nlqf_niveau":            "NLQF Niveau",
    "voertaal":               "Voertaal",
    # dim_sector
    "sector_key":             "Sector Key",
    # dim_geografie
    "geografie_key":          "Geografie Key",
    "gemeentenummer":         "Gemeentenummer",
    "gemeentenaam":           "Gemeente",
    "provincienaam":          "Provincie",
    "corop_code":             "COROP Code",
    "corop_naam":             "COROP Naam",
    "rpa_code":               "RPA Code",
    "rpa_naam":               "RPA Naam",
    # dim_geslacht
    "geslacht_key":           "Geslacht Key",
    "geslacht":               "Geslacht",
    # dim_opleidingsvorm
    "opleidingsvorm_key":     "Opleidingsvorm Key",
    "opleidingsvorm_code":    "Opleidingsvorm Code",
    "opleidingsvorm_naam":    "Opleidingsvorm",
    # dim_bestuur
    "bestuur_key":            "Bestuur Key",
    "bevoegd_gezag_naam":     "Bevoegd Gezag Naam",
    "kvk_nummer":             "KvK Nummer",
    # dim_soort_diploma
    "soort_diploma_key":      "Soort Diploma Key",
    "soort_diploma":          "Soort Diploma",
    # fact surrogate keys
    "ingeschrevenen_key":     "ID",
    "inschrijvingen_key":     "ID",
    "eerstejaars_key":        "ID",
    "gediplomeerden_key":     "ID",
    "id":                     "ID",
    # fact measures
    "aantal_ingeschrevenen":  "Aantal Ingeschrevenen",
    "aantal_inschrijvingen":  "Aantal Inschrijvingen",
    "aantal_eerstejaars":     "Aantal Eerstejaars",
    "aantal_gediplomeerden":  "Aantal Gediplomeerden",
    "is_onderdrukt":          "Privacy Onderdrukt",
}

# Surrogate and foreign key columns to hide in Power BI
HIDDEN_COLS: set[str] = {
    "tijd_key", "instelling_key", "opleiding_key", "geografie_key",
    "sector_key", "geslacht_key", "opleidingsvorm_key", "bestuur_key",
    "soort_diploma_key", "ingeschrevenen_key", "inschrijvingen_key",
    "eerstejaars_key", "gediplomeerden_key", "id",
}

# Name of the dedicated measures bucket table (no parquet file — generated separately)
MEASURES_TABLE_NAME = "Measures DM"

# All DAX measures live in the dedicated measures table.
# Tuple structure: (display_name, dax_expression, format_string)
MEASURES: list[tuple[str, str, str]] = [
    ("Totaal Ingeschrevenen",
     "SUM('Ingeschrevenen'[Aantal Ingeschrevenen])",
     "#,0"),
    ("% Privacy Onderdrukt",
     "DIVIDE(COUNTROWS(FILTER('Ingeschrevenen', 'Ingeschrevenen'[Privacy Onderdrukt])), COUNTROWS('Ingeschrevenen'))",
     "0.00%"),
    ("Totaal Inschrijvingen",
     "SUM('Inschrijvingen'[Aantal Inschrijvingen])",
     "#,0"),
    ("Totaal Eerstejaars",
     "SUM('Eerstejaars'[Aantal Eerstejaars])",
     "#,0"),
    ("Totaal Gediplomeerden",
     "SUM('Gediplomeerden'[Aantal Gediplomeerden])",
     "#,0"),
    ("Totaal Ingeschrevenen (Geslacht)",
     "SUM('Ingeschrevenen naar Geslacht'[Aantal Ingeschrevenen])",
     "#,0"),
    ("Totaal Inschrijvingen (Geslacht)",
     "SUM('Inschrijvingen naar Geslacht'[Aantal Inschrijvingen])",
     "#,0"),
    ("Totaal Eerstejaars (Geslacht)",
     "SUM('Eerstejaars naar Geslacht'[Aantal Eerstejaars])",
     "#,0"),
    ("Totaal Gediplomeerden (Geslacht)",
     "SUM('Gediplomeerden naar Geslacht'[Aantal Gediplomeerden])",
     "#,0"),
    ("Totaal Ingeschrevenen (Oplvorm)",
     "SUM('Ingeschrevenen naar Opleidingsvorm'[Aantal Ingeschrevenen])",
     "#,0"),
    ("Totaal Inschrijvingen (Oplvorm)",
     "SUM('Inschrijvingen naar Opleidingsvorm'[Aantal Inschrijvingen])",
     "#,0"),
    ("Totaal Eerstejaars (Oplvorm)",
     "SUM('Eerstejaars naar Opleidingsvorm'[Aantal Eerstejaars])",
     "#,0"),
    ("Totaal Gediplomeerden (Oplvorm)",
     "SUM('Gediplomeerden naar Opleidingsvorm'[Aantal Gediplomeerden])",
     "#,0"),
]

# Relationships: (from_table_key, from_column, to_table_key, to_column)
# All many-to-one (fact/child → dimension/parent)
RELATIONSHIPS: list[tuple[str, str, str, str]] = [
    # --- Primary fact tables ---
    ("feit_ingeschrevenen",  "tijd_key",         "dim_tijd",          "tijd_key"),
    ("feit_ingeschrevenen",  "instelling_key",    "dim_instelling",    "instelling_key"),
    ("feit_ingeschrevenen",  "opleiding_key",     "dim_opleiding",     "opleiding_key"),
    ("feit_ingeschrevenen",  "geografie_key",     "dim_geografie",     "geografie_key"),

    ("feit_inschrijvingen",  "tijd_key",          "dim_tijd",          "tijd_key"),
    ("feit_inschrijvingen",  "instelling_key",    "dim_instelling",    "instelling_key"),
    ("feit_inschrijvingen",  "opleiding_key",     "dim_opleiding",     "opleiding_key"),
    ("feit_inschrijvingen",  "geografie_key",     "dim_geografie",     "geografie_key"),

    ("feit_eerstejaars",     "tijd_key",          "dim_tijd",          "tijd_key"),
    ("feit_eerstejaars",     "instelling_key",    "dim_instelling",    "instelling_key"),
    ("feit_eerstejaars",     "opleiding_key",     "dim_opleiding",     "opleiding_key"),
    ("feit_eerstejaars",     "geografie_key",     "dim_geografie",     "geografie_key"),

    ("feit_gediplomeerden",  "tijd_key",          "dim_tijd",          "tijd_key"),
    ("feit_gediplomeerden",  "instelling_key",    "dim_instelling",    "instelling_key"),
    ("feit_gediplomeerden",  "opleiding_key",     "dim_opleiding",     "opleiding_key"),
    ("feit_gediplomeerden",  "geografie_key",     "dim_geografie",     "geografie_key"),
    ("feit_gediplomeerden",  "soort_diploma_key", "dim_soort_diploma", "soort_diploma_key"),

    # --- Geslacht variants ---
    ("feit_ingeschrevenen_geslacht", "tijd_key",         "dim_tijd",          "tijd_key"),
    ("feit_ingeschrevenen_geslacht", "instelling_key",   "dim_instelling",    "instelling_key"),
    ("feit_ingeschrevenen_geslacht", "sector_key",       "dim_sector",        "sector_key"),
    ("feit_ingeschrevenen_geslacht", "geografie_key",    "dim_geografie",     "geografie_key"),
    ("feit_ingeschrevenen_geslacht", "geslacht_key",     "dim_geslacht",      "geslacht_key"),

    ("feit_inschrijvingen_geslacht", "tijd_key",         "dim_tijd",          "tijd_key"),
    ("feit_inschrijvingen_geslacht", "instelling_key",   "dim_instelling",    "instelling_key"),
    ("feit_inschrijvingen_geslacht", "sector_key",       "dim_sector",        "sector_key"),
    ("feit_inschrijvingen_geslacht", "geografie_key",    "dim_geografie",     "geografie_key"),
    ("feit_inschrijvingen_geslacht", "geslacht_key",     "dim_geslacht",      "geslacht_key"),

    ("feit_eerstejaars_geslacht",    "tijd_key",         "dim_tijd",          "tijd_key"),
    ("feit_eerstejaars_geslacht",    "instelling_key",   "dim_instelling",    "instelling_key"),
    ("feit_eerstejaars_geslacht",    "sector_key",       "dim_sector",        "sector_key"),
    ("feit_eerstejaars_geslacht",    "geografie_key",    "dim_geografie",     "geografie_key"),
    ("feit_eerstejaars_geslacht",    "geslacht_key",     "dim_geslacht",      "geslacht_key"),

    ("feit_gediplomeerden_geslacht", "tijd_key",         "dim_tijd",          "tijd_key"),
    ("feit_gediplomeerden_geslacht", "instelling_key",   "dim_instelling",    "instelling_key"),
    ("feit_gediplomeerden_geslacht", "sector_key",       "dim_sector",        "sector_key"),
    ("feit_gediplomeerden_geslacht", "geografie_key",    "dim_geografie",     "geografie_key"),
    ("feit_gediplomeerden_geslacht", "soort_diploma_key","dim_soort_diploma", "soort_diploma_key"),
    ("feit_gediplomeerden_geslacht", "geslacht_key",     "dim_geslacht",      "geslacht_key"),

    # --- Opleidingsvorm variants ---
    ("feit_ingeschrevenen_oplvorm",  "tijd_key",          "dim_tijd",           "tijd_key"),
    ("feit_ingeschrevenen_oplvorm",  "instelling_key",    "dim_instelling",     "instelling_key"),
    ("feit_ingeschrevenen_oplvorm",  "sector_key",        "dim_sector",         "sector_key"),
    ("feit_ingeschrevenen_oplvorm",  "geografie_key",     "dim_geografie",      "geografie_key"),
    ("feit_ingeschrevenen_oplvorm",  "opleidingsvorm_key","dim_opleidingsvorm", "opleidingsvorm_key"),

    ("feit_inschrijvingen_oplvorm",  "tijd_key",          "dim_tijd",           "tijd_key"),
    ("feit_inschrijvingen_oplvorm",  "instelling_key",    "dim_instelling",     "instelling_key"),
    ("feit_inschrijvingen_oplvorm",  "sector_key",        "dim_sector",         "sector_key"),
    ("feit_inschrijvingen_oplvorm",  "geografie_key",     "dim_geografie",      "geografie_key"),
    ("feit_inschrijvingen_oplvorm",  "opleidingsvorm_key","dim_opleidingsvorm", "opleidingsvorm_key"),

    ("feit_eerstejaars_oplvorm",     "tijd_key",          "dim_tijd",           "tijd_key"),
    ("feit_eerstejaars_oplvorm",     "instelling_key",    "dim_instelling",     "instelling_key"),
    ("feit_eerstejaars_oplvorm",     "sector_key",        "dim_sector",         "sector_key"),
    ("feit_eerstejaars_oplvorm",     "geografie_key",     "dim_geografie",      "geografie_key"),
    ("feit_eerstejaars_oplvorm",     "opleidingsvorm_key","dim_opleidingsvorm", "opleidingsvorm_key"),

    ("feit_gediplomeerden_oplvorm",  "tijd_key",          "dim_tijd",           "tijd_key"),
    ("feit_gediplomeerden_oplvorm",  "instelling_key",    "dim_instelling",     "instelling_key"),
    ("feit_gediplomeerden_oplvorm",  "sector_key",        "dim_sector",         "sector_key"),
    ("feit_gediplomeerden_oplvorm",  "geografie_key",     "dim_geografie",      "geografie_key"),
    ("feit_gediplomeerden_oplvorm",  "soort_diploma_key", "dim_soort_diploma",  "soort_diploma_key"),
    ("feit_gediplomeerden_oplvorm",  "opleidingsvorm_key","dim_opleidingsvorm", "opleidingsvorm_key"),

    # --- Outrigger: Instelling → Bestuur ---
    ("dim_instelling", "bevoegd_gezag_nummer", "dim_bestuur", "bevoegd_gezag_nummer"),
]

# Power Query editor group for each table (shown in Power BI's query organiser)
QUERY_GROUPS: dict[str, str] = {
    "dim_bestuur":                  "Dimensies",
    "dim_geografie":                "Dimensies",
    "dim_geslacht":                 "Dimensies",
    "dim_instelling":               "Dimensies",
    "dim_opleiding":                "Dimensies",
    "dim_opleidingsvorm":           "Dimensies",
    "dim_sector":                   "Dimensies",
    "dim_soort_diploma":            "Dimensies",
    "dim_tijd":                     "Dimensies",
    "feit_ingeschrevenen":          "Feiten",
    "feit_inschrijvingen":          "Feiten",
    "feit_eerstejaars":             "Feiten",
    "feit_gediplomeerden":          "Feiten",
    "feit_ingeschrevenen_geslacht": "Feiten",
    "feit_inschrijvingen_geslacht": "Feiten",
    "feit_eerstejaars_geslacht":    "Feiten",
    "feit_gediplomeerden_geslacht": "Feiten",
    "feit_ingeschrevenen_oplvorm":  "Feiten",
    "feit_inschrijvingen_oplvorm":  "Feiten",
    "feit_eerstejaars_oplvorm":     "Feiten",
    "feit_gediplomeerden_oplvorm":  "Feiten",
}


# === Helpers ===

def gen_uuid() -> str:
    return str(uuid.uuid4())


def q(name: str) -> str:
    """Wrap in single quotes if name contains spaces or special chars."""
    if " " in name or any(c in name for c in "[](){}#'"):
        return f"'{name}'"
    return name


def pa_to_tmdl_type(pa_type) -> str:
    """Map a pyarrow type to a TMDL dataType string."""
    s = str(pa_type).lower()
    if "bool" in s:
        return "boolean"
    if "int" in s or "uint" in s:
        return "int64"
    if "float" in s or "double" in s:
        return "double"
    if "timestamp" in s or "date" in s:
        return "dateTime"
    return "string"


def summarize_by(src_col: str, tmdl_type: str) -> str:
    """Choose Power BI summarizeBy behaviour for a column."""
    if src_col in HIDDEN_COLS:
        return "none"
    if tmdl_type == "boolean":
        return "none"
    if tmdl_type == "int64" and src_col.startswith("aantal_"):
        return "sum"
    return "none"


def tmdl_file_name(display_name: str) -> str:
    """Use the display name directly as filename (spaces allowed on all platforms)."""
    return display_name + ".tmdl"


# === Table TMDL generator ===

def generate_table_tmdl(parquet_path: Path) -> str:
    table_key = parquet_path.stem
    display_name = TABLE_NAMES.get(table_key, table_key)

    # Read column schema from parquet (no data loaded)
    pf = pq.ParquetFile(parquet_path)
    schema = pf.schema_arrow

    # Path for M expression — forward slashes work on Windows in Power Query
    m_path = str(parquet_path.resolve()).replace("\\", "/")

    lines: list[str] = []
    lines.append(f"table {q(display_name)}")
    lines.append(f"\tlineageTag: {gen_uuid()}")
    lines.append("")

    # --- Columns ---
    for field in schema:
        src = field.name
        if str(field.type).lower() == "null":
            print(f"    SKIP  {display_name}.{src}  (null type — all values are null, cannot map to TMDL dataType)")
            continue
        tmdl_type = pa_to_tmdl_type(field.type)
        disp = COLUMN_NAMES.get(src, src)
        hidden = src in HIDDEN_COLS
        sum_by = summarize_by(src, tmdl_type)

        lines.append(f"\tcolumn {q(disp)}")
        lines.append(f"\t\tdataType: {tmdl_type}")
        lines.append(f"\t\tlineageTag: {gen_uuid()}")
        if hidden:
            lines.append("\t\tisHidden")
        lines.append(f"\t\tsummarizeBy: {sum_by}")
        # sourceColumn only needed when display name differs from source name
        if disp != src:
            lines.append(f"\t\tsourceColumn: {src}")
        lines.append("")

    # --- Measures (none — all measures live in the Measures DM table) ---
    for mname, dax, fmt in []:
        lines.append(f"\tmeasure {q(mname)} = {dax}")
        lines.append(f'\t\tformatString: "{fmt}"')
        lines.append(f"\t\tlineageTag: {gen_uuid()}")
        lines.append("")

    # --- Partition (M expression) ---
    query_group = QUERY_GROUPS.get(table_key, "")
    lines.append(f"\tpartition {q(display_name)} = m")
    lines.append("\t\tmode: import")
    if query_group:
        lines.append(f"\t\tqueryGroup: {query_group}")
    lines.append("\t\tsource = ```")
    lines.append("\t\t\tlet")
    lines.append(f'\t\t\t    Source = Parquet.Document(File.Contents("{m_path}"))')
    lines.append("\t\t\tin")
    lines.append("\t\t\t    Source")
    lines.append("\t\t```")
    lines.append("")

    return "\n".join(lines)


# === Measures table generator ===

def generate_measures_table_tmdl() -> str:
    """
    Generate a dedicated 'Measures DM' table that acts as a bucket for all DAX
    measures.  The table itself contains a single hidden placeholder column so
    that the M partition returns a valid (non-empty) table.  No fact-table keys
    or columns are exposed.
    """
    lines: list[str] = []
    lines.append(f"table {q(MEASURES_TABLE_NAME)}")
    lines.append(f"\tlineageTag: {gen_uuid()}")
    lines.append("")

    # Hidden placeholder column — required for a valid M import partition
    lines.append("\tcolumn Column1")
    lines.append("\t\tdataType: string")
    lines.append(f"\t\tlineageTag: {gen_uuid()}")
    lines.append("\t\tisHidden")
    lines.append("\t\tsummarizeBy: none")
    lines.append("")

    # All DAX measures
    for mname, dax, fmt in MEASURES:
        lines.append(f"\tmeasure {q(mname)} = {dax}")
        lines.append(f'\t\tformatString: "{fmt}"')
        lines.append(f"\t\tlineageTag: {gen_uuid()}")
        lines.append("")

    # Dummy M partition — one-row table so Power BI accepts the import mode
    lines.append(f"\tpartition {q(MEASURES_TABLE_NAME)} = m")
    lines.append("\t\tmode: import")
    lines.append("\t\tsource = ```")
    lines.append("\t\t\tlet")
    lines.append('\t\t\t    Source = Table.FromRows({{""}}, {"Column1"})')
    lines.append("\t\t\tin")
    lines.append("\t\t\t    Source")
    lines.append("\t\t```")
    lines.append("")

    return "\n".join(lines)


# === relationships.tmdl generator ===

def q_rel_col(name: str) -> str:
    """Quote column name in relationship dot notation if it contains spaces."""
    return f"'{name}'" if " " in name else name


def build_relationships_tmdl() -> str:
    """
    Generate relationships.tmdl content using TMDL dot notation:
        fromColumn: 'Table Name'.'Column Name'
        toColumn: 'Dim Name'.ColumnName
    Table names are ALWAYS single-quoted, regardless of spaces.
    Column names are single-quoted when they contain spaces.
    """
    lines: list[str] = []
    for from_key, from_col, to_key, to_col in RELATIONSHIPS:
        from_disp     = TABLE_NAMES.get(from_key, from_key)
        to_disp       = TABLE_NAMES.get(to_key,   to_key)
        from_col_disp = COLUMN_NAMES.get(from_col, from_col)
        to_col_disp   = COLUMN_NAMES.get(to_col,   to_col)

        lines.append(f"relationship {gen_uuid()}")
        lines.append(f"\tfromColumn: '{from_disp}'.{q_rel_col(from_col_disp)}")
        lines.append(f"\ttoColumn: '{to_disp}'.{q_rel_col(to_col_disp)}")
        lines.append("")
    return "\n".join(lines)


# === model.tmdl generator ===

def generate_model_tmdl(existing_keys: set[str]) -> str:
    """
    Generate the full model.tmdl:
      - model Model block (culture, data access settings)
      - queryGroup definitions with PBI_QueryGroupOrder annotations
      - annotation PBI_QueryOrder (table display names, facts first then dims)
      - annotation __PBI_TimeIntelligenceEnabled
      - annotation PBI_ProTooling
      - ref table for every table present in data/processed/
      - ref cultureInfo
    """
    import json

    # Ordered display names: measures table first, then facts, then dimensions
    fact_keys = [k for k in TABLE_NAMES if k.startswith("feit_") and k in existing_keys]
    dim_keys  = [k for k in TABLE_NAMES if k.startswith("dim_")  and k in existing_keys]
    ordered_keys = fact_keys + dim_keys
    query_order  = [MEASURES_TABLE_NAME] + [TABLE_NAMES[k] for k in ordered_keys]

    lines: list[str] = []

    # model Model block
    lines.append("model Model")
    lines.append("\tculture: en-US")
    lines.append("\tdefaultPowerBIDataSourceVersion: powerBI_V3")
    lines.append("\tsourceQueryCulture: nl-NL")
    lines.append("\tdataAccessOptions")
    lines.append("\t\tlegacyRedirects")
    lines.append("\t\treturnErrorValuesAsNull")
    lines.append("")

    # queryGroup definitions (top-level, zero indentation)
    lines.append("queryGroup Feiten")
    lines.append("")
    lines.append("\tannotation PBI_QueryGroupOrder = 0")
    lines.append("")
    lines.append("queryGroup Dimensies")
    lines.append("")
    lines.append("\tannotation PBI_QueryGroupOrder = 1")
    lines.append("")

    # Annotations
    lines.append(f"annotation PBI_QueryOrder = {json.dumps(query_order)}")
    lines.append("")
    lines.append("annotation __PBI_TimeIntelligenceEnabled = 1")
    lines.append("")
    lines.append('annotation PBI_ProTooling = ["DevMode"]')
    lines.append("")

    # ref table: measures table first, then all parquet-based tables
    lines.append(f"ref table {q(MEASURES_TABLE_NAME)}")
    for key in ordered_keys:
        lines.append(f"ref table {q(TABLE_NAMES[key])}")
    lines.append("")
    lines.append("ref cultureInfo en-US")
    lines.append("")

    return "\n".join(lines)


# === Main ===

def main() -> None:
    print("Generating Power BI TMDL for DUO HBO dimensional model")
    print(f"  Source : {PROCESSED}")
    print(f"  Output : {TABLES_DIR}")
    print()

    parquet_files = sorted(
        f for f in PROCESSED.glob("*.parquet") if f.stem != ".gitkeep"
    )

    if not parquet_files:
        print("ERROR: No parquet files found in", PROCESSED)
        return

    # 0. Remove all existing TMDL files so no stale or duplicate-named files remain
    removed = list(TABLES_DIR.glob("*.tmdl"))
    for f in removed:
        f.unlink()
    if removed:
        print(f"  Removed {len(removed)} existing .tmdl files from tables/")
        print()

    # 1. Generate one TMDL file per parquet-based table
    for pf_path in parquet_files:
        table_key = pf_path.stem
        display_name = TABLE_NAMES.get(table_key, table_key)
        tmdl_content = generate_table_tmdl(pf_path)
        out_file = TABLES_DIR / tmdl_file_name(display_name)
        out_file.write_text(tmdl_content, encoding="utf-8")
        print(f"  OK  {display_name:<48} -> tables/{out_file.name}")

    # 2. Generate Measures DM table (no parquet — dedicated measures bucket)
    measures_file = TABLES_DIR / tmdl_file_name(MEASURES_TABLE_NAME)
    measures_file.write_text(generate_measures_table_tmdl(), encoding="utf-8")
    print(f"  OK  {MEASURES_TABLE_NAME:<48} -> tables/{measures_file.name}  ({len(MEASURES)} measures)")

    # 3. Write relationships.tmdl (separate file, correct dot notation)
    rel_file = DEFINITION / "relationships.tmdl"
    rel_file.write_text(build_relationships_tmdl(), encoding="utf-8")
    print()
    print(f"  OK  relationships.tmdl -- {len(RELATIONSHIPS)} relationships")

    # 4. Write model.tmdl (queryGroups, ref tables, annotations)
    existing_keys = {f.stem for f in parquet_files}
    model_content = generate_model_tmdl(existing_keys)
    model_tmdl = DEFINITION / "model.tmdl"
    model_tmdl.write_text(model_content, encoding="utf-8")
    print(f"  OK  model.tmdl -- queryGroups + {len(existing_keys) + 1} ref tables")

    print()
    print(f"Done. {len(parquet_files) + 1} tables written ({len(parquet_files)} parquet + 1 measures).")
    print()
    print("Next step: open powerbi/dim-duo-ai-model.pbip in Power BI Desktop.")
    print("           Power BI will detect the new tables and load them on refresh.")


if __name__ == "__main__":
    main()
