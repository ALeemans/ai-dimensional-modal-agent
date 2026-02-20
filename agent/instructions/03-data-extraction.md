# Agent Instruction: 03 — Data Extraction

**Author:** Anne Leemans, in collaboration with Claude Sonnet 4.6

> This is a reusable instruction document. It describes how an AI agent should build a reproducible data extraction script to download raw source data locally — the prerequisite for dimensional model design (Phase 4) and validation (Phase 5).

## Language Policy

🌍 **Communication & Instructions:** English (this document and agent-human discussion)

🇳🇱 **Project Content & Artifacts:** Use the project language for all outputs (e.g. Dutch for DUO HBO projects). Script comments and code may be in English.

---

## Purpose

Before a dimensional model can be designed or validated, the raw source data must be available locally. This phase produces:

- A **reproducible extraction script** that can be re-run on any machine to download the latest data
- A **manifest file** (`manifest.json`) that logs what was downloaded, when, and in what condition
- A structured **`data/raw/`** directory organized by dataset

Working with local files rather than live API calls is essential for:
- Offline and cross-machine consistency (important when working across multiple machines)
- Reproducibility — knowing exactly which data version a model was designed against
- Performance — no repeated API calls during design and validation iterations

---

## Prerequisites

- Completed metadata catalog from Phase 1 (field profiles, API endpoints, resource IDs)
- Python 3.10+ with `requests` installed
- Network access to the data source

---

## Instructions for the Agent

### Step 1: Identify Data Sources and Extraction Methods

**Goal:** Classify every dataset by how it must be retrieved.

For each dataset in scope, determine the extraction method:

| Method | When to use | Example |
|--------|-------------|---------|
| **CKAN API** | Source uses CKAN (common in government open data portals) | DUO onderwijsdata.duo.nl |
| **REST API with pagination** | Source exposes a paginated JSON/XML API | Most modern REST APIs |
| **Direct file download** | Source publishes static files at a known URL | DUO address CSVs on duo.nl |
| **Database query** | Source is a directly accessible database | Internal systems |
| **Manual export** | No automated access available | Legacy systems |

**For CKAN sources specifically:**
1. Use `GET /api/3/action/package_show?id={dataset_id}` to discover all resources in a package
2. Each resource object contains a direct download `url` field — use this, never hardcode URLs
3. Filter resources by format (`"CSV"`) and, if needed, by filename pattern (e.g. `"hbo"` to exclude WO variants)
4. CKAN resource URLs can change when data is republished — always resolve them via the API, never hardcode

**Output:** A list of (dataset_id, extraction_method, filter_rules) for all datasets in scope

---

### Step 2: Define the Output Directory Structure

**Goal:** Agree on a consistent, navigable layout for downloaded files before writing any code.

**Recommended structure:**
```
data/
└── raw/
    ├── {dataset_id}/
    │   └── {filename}.csv
    └── manifest.json
```

**Principles:**
- One subdirectory per logical dataset (not per file)
- Keep original filenames as received from the source — do not rename
- `data/raw/` is for **unmodified source data only** — no transformations here
- Add `data/raw/` to `.gitignore` — raw data files should not be committed to git

**Output:** Documented directory structure (see project `docs/fase3-gegevensextractie.md` as example)

---

### Step 3: Write the Extraction Script

**Goal:** A single Python script that downloads all required files, verifies them, and writes a manifest.

**Script location:** `scripts/{project}_extractor.py`

**Script must:**
1. **Anchor paths to the script file**, not the working directory:
   ```python
   PROJECT_ROOT = Path(__file__).resolve().parent.parent
   OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
   ```
   This ensures the script runs correctly regardless of which directory it is invoked from.

2. **Keep all configuration at the top** — no hardcoded values inside functions:
   ```python
   CKAN_BASE_URL = "https://..."
   CKAN_DATASETS = { "dataset_id": {"subdir": "...", "hbo_only": True}, ... }
   DIRECT_DOWNLOADS = [ {"url": "...", "subdir": "...", "filename": "..."}, ... ]
   EXPECTED_MIN_ROWS = { "filename.csv": 4300, ... }
   ```

3. **Use streaming downloads** — never load an entire file into memory:
   ```python
   with session.get(url, stream=True, timeout=120) as response:
       for chunk in response.iter_content(chunk_size=16_384):
           f.write(chunk)
   ```

4. **Isolate failures per file** — one broken download must not stop the rest. Wrap each download in a try/except and continue.

5. **Verify each download** immediately after saving:
   - File exists and size > 0
   - Row count (line count minus header) meets the expected minimum
   - Log a warning if below threshold, an error if unreadable

6. **Write a manifest** at the end:
   ```json
   {
     "extracted_at": "2026-02-20T10:00:00",
     "datasets": {
       "dataset_id": {
         "resources": [
           {
             "filename": "file.csv",
             "url": "https://...",
             "downloaded_at": "...",
             "rows": 4833,
             "size_bytes": 780288,
             "status": "ok",
             "warnings": []
           }
         ]
       }
     }
   }
   ```

7. **Exit with code 1** if any file failed — this makes the script usable in CI/automation pipelines.

**Minimum required functions:**

| Function | Responsibility |
|----------|----------------|
| `get_package_resources(session, dataset_id)` | Query CKAN `package_show`, return resource list |
| `is_hbo_csv(resource)` / `is_csv(resource)` | Filter resources by format and filename pattern |
| `download_file(session, url, dest_path)` | Streaming download, returns bytes written |
| `count_rows(path)` | Count data rows (excluding header) |
| `verify_file(path)` | Return status dict: rows, size, status, warnings |
| `extract_ckan_dataset(session, dataset_id, config)` | Orchestrate one CKAN dataset |
| `extract_direct_downloads(session)` | Download static files |
| `main()` | Top-level orchestration, manifest writing, summary |

---

### Step 4: Run the Script

```bash
pip install -r requirements.txt
python scripts/{project}_extractor.py
```

The script should run from any directory. Expected output format:
```
10:00:01  INFO      === DUO HBO Gegevensextractie ===
10:00:01  INFO      [p01hoinges]
10:00:01  INFO        3 CSV-resource(s) geselecteerd van 8 totaal
10:00:02  INFO        → ingeschrevenengeslhbo.csv
10:00:03  INFO          ✓  4,833 rijen  |  780,288 bytes
...
10:00:45  INFO      Klaar. 16 bestanden verwerkt.
10:00:45  INFO      ✓ ok: 16   ⚠ waarschuwing: 0   ✗ fout: 0
```

**Human review step:** Before proceeding to Phase 4, the human should:
- Confirm all expected files are present in `data/raw/`
- Spot-check 2–3 files by opening them and verifying structure
- Review `manifest.json` for any warnings or unexpected row counts

---

### Step 5: Verify Downloads

Cross-check the manifest against the metadata catalog from Phase 1:

| Check | Source | Threshold |
|-------|--------|-----------|
| File present | `manifest.json` status = "ok" | All files |
| Row count plausible | ±10% of Phase 1 catalog value | All statistical files |
| Column names correct | Open file, check header row | Spot-check |
| No encoding errors | Script reads without `errors="replace"` firing | All files |

If row counts differ significantly from Phase 1 catalog values, the data may have been updated since profiling — note the difference and update the catalog.

---

## Tips for the Agent

- **Never hardcode resource download URLs.** CKAN URLs are stable for humans but can change when data is republished. Always resolve URLs via `package_show` at runtime.
- **Filter by filename, not by resource name.** Resource names in CKAN are free-text and inconsistent. Filenames in the URL are the reliable signal (e.g. `"hbo"` in filename to separate HBO from WO resources).
- **Use a `requests.Session()`** for all downloads in one run — it reuses TCP connections and is significantly faster for many small files.
- **Set a `User-Agent` header** — some servers block requests without one:
  ```python
  session.headers.update({"User-Agent": "ProjectName-Extractor/1.0"})
  ```
- **Keep `data/raw/` out of git** with `.gitignore`. Raw data can be large and changes frequently. The extraction script + manifest is the reproducible artifact, not the data files themselves.
- **Expected row counts should have a margin (±10%).** Data is updated periodically and counts will drift. Warn on deviation but don't fail unless the file is empty or unreadable.
- **Re-running is safe.** The script overwrites existing files. This is intentional — re-running always gives you the latest version of the data.

---

## Output Checklist

Before marking Phase 3 complete:

- [ ] All datasets listed in the metadata catalog have been downloaded
- [ ] `data/raw/manifest.json` exists and shows all files as `"ok"` or `"warning"`
- [ ] No files with status `"error"` remain unresolved
- [ ] Row counts are within ±10% of Phase 1 catalog values (or differences are documented)
- [ ] Script runs cleanly from a fresh working directory
- [ ] `requirements.txt` is updated with all dependencies
- [ ] `data/raw/` is in `.gitignore`
