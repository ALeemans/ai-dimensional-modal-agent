---
title: Applied Steps Cleaner
---

# 🎯 Objective
Ensure ALL Applied Steps in Power BI queries are systematically cleaned, structured, and understandable for both users and developers.

# 🏷 Applied Step Naming
- Use clear and descriptive names for each Applied Step.
- Use Dutch names for consistency.
- Add a description via the step's properties using `/*Description*/` format.
- Descriptions are mandatory for steps where the name does not clearly indicate the action.

# 📌 Instructions

## 1. **Systematic Scope Identification** (Follow this process exactly):
   a. **List ALL .tmdl files recursively** in the `DM {name of model}.SemanticModel\\definition\\tables` directory (no exceptions)
   b. **Open each file and detect Applied Steps** by checking if the partition `source =` contains ANY of the following (case-sensitive):
      - A `let` ... `in` block (Power Query present)
      - Any `Table.*` transformation (e.g., `Table.SelectRows`, `Table.RenameColumns`, `Table.AddColumn`, `Table.TransformColumnTypes`, `Table.Sort`, `Table.RemoveColumns`, `Table.SelectColumns`)
      - `Value.NativeQuery(`, or `Sql.Database(..., [Query="..."])` (direct SQL still requires baseline comments)
      - Common connector functions: `Excel.Workbook`, `Csv.Document`, `Web.Contents`, `SharePoint.Files`, `OData.Feed`, `Azure*`
   c. **Apply this rule to EVERY table** that meets ANY detection condition in step b
   d. **CRITICAL: DO NOT make assumptions** based on table names (ZZ_, DateTableTemplate, LocalDateTable, Meetwaardes, etc.). Use the detection rules only
   e. **Keep the formatting** exactly as-is; pay attention to indentation and tabs. Never reflow lines

## 2. **Include These Tables:**
   - ✅ Any table whose partition `source` contains a `let` block
   - ✅ Any table with `Table.*` transformations or step assignments like `#"Renamed Columns" = ...`
   - ✅ Any table using `Sql.Database` with `[Query=...]` or `Value.NativeQuery`
   - ✅ Tables with file/web connectors (CSV, Excel, Web, SharePoint, OData, Azure)

## 3. **Exclude Only These:**
   - ❌ Measure container tables (dummy tables with compressed JSON data)
     - Detection pattern: `Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("...", BinaryEncoding.Base64), Compression.Deflate)))`
   - ❌ Auto-generated internal tables that never contain Applied Steps (skip safely):
     - `DateTableTemplate_*`, `LocalDateTable_*`
   - ❌ Tables with no `let` block

## 4. **CRITICAL: Applied Steps Formatting Rules**:

### **✅ WHAT TO DO:**
- **Add `/*Dutch comments*/`** above each Applied Step
- **Rename step names to Dutch** - change `#"Renamed Columns"` to `#"Kolom namen vertalen"`
- **Keep ALL existing formatting exactly as is** - no indentation changes
- **Don't touch `source =`** (TMDL property) - leave completely untouched
- **Only work inside the `let` expression** - add comments and rename steps

### **❌ WHAT NOT TO DO:**
- Don't change indentation of `source =` or any existing code
- Don't change any structural formatting
- Don't touch TMDL properties (mode, queryGroup, etc.)
- Don't change step references - if step A references step B, update both consistently

### **✅ CORRECT APPROACH:**
```m
	source =                    # <-- DON'T TOUCH THIS LINE
		let                     # <-- DON'T TOUCH THIS LINE
		    /*Database connectie maken*/
		    Source = ...        # <-- DON'T TOUCH: keep Source as is
		    
		    /*Kolom namen vertalen naar Nederlands*/  
		    #"Kolom namen vertalen" = ... # <-- CHANGE: rename to Dutch
		in
		    #"Kolom namen vertalen"   # <-- CHANGE: update final reference
```

## 5. **Standard Comment Patterns**:

### **Database Connection Comments:**
```m
/*Database connectie maken*/
Source = Sql.Database("server", "database"),

/*[Table name] tabel selecteren*/  
TableName = Source{[Schema="Marketing",Item="VW_TABLE_NAME"]}[Data],
```

### **Data Transformation Comments & Names:**
```m
/*Benodigde kolommen selecteren*/
#"Benodigde kolommen selecteren" = Table.SelectColumns(...),

/*Kolom namen vertalen naar Nederlands*/
#"Kolom namen vertalen" = Table.RenameColumns(...),

/*Alleen [criteria] filteren*/
#"Alleen [criteria] filteren" = Table.SelectRows(...),

/*Kolom type wijzigen naar [type]*/
#"Kolom type wijzigen" = Table.TransformColumnTypes(...),

/*Rijen sorteren op [column] [oplopend/aflopend]*/
#"Rijen sorteren" = Table.Sort(...),
```

### **Business Logic Comments:**
```m
/*Filter laatste X [items] toevoegen*/
#"Add Custom Column" = Table.AddColumn(...),

/*[Specific transformation] uitvoeren*/
#"Existing Step Name" = Table.Transform(...),
```

## 6. **Example - BEFORE and AFTER**

### **❌ BEFORE (needs comments):**
```m
partition Cohort = m
	mode: import
	queryGroup: Dimensies\Datum/tijd
	source =
		let
			Source = Sql.Database("server", "DB", [Query="SELECT ..."]),
			#"Added Column" = Table.AddColumn(Source, "Filter", each ...),
			#"Changed Type" = Table.TransformColumnTypes(#"Added Column", ...),
			#"Renamed Columns" = Table.RenameColumns(#"Changed Type", ...)
		in
			#"Renamed Columns"
```

## 7. **Robust Detection Heuristics (MANDATORY)**

When scanning each `.tmdl` file, treat the table as in-scope if ANY of the following are present inside the partition `source`:
- `let` followed by step assignments (`StepName = ...`) and a closing `in`
- Any `Table.*` function call (e.g., `Table.SelectRows`, `Table.RenameColumns`, `Table.AddColumn`, `Table.TransformColumnTypes`, `Table.RemoveColumns`, `Table.SelectColumns`, `Table.Sort`, `Table.Join`, `Table.Group`)
- `Value.NativeQuery(` or `Sql.Database(` with a `[Query="..."]` argument
- Connector functions (non-exhaustive): `Excel.Workbook`, `Csv.Document`, `Web.Contents`, `OData.Feed`, `SharePoint.Files`, `SharePoint.Contents`, `Azure*`

Notes:
- Direct SQL via `[Query=...]` still requires baseline comments above the key steps (database connectie, selectie, kolommen selecteren)
- Skip only if the partition lacks all of the above AND matches an exclusion in section 3

## 8. **Implementation Algorithm (APPLY TO EACH IN-SCOPE TABLE)**
1. Locate the partition `source =` and the `let ... in` block. If absent but `Value.NativeQuery`/`[Query=...]` is used, add comments above the key single-step assignments
2. Above each step assignment, insert a concise Dutch comment describing the transformation
3. Rename common English step names to Dutch equivalents (update the final `in` reference accordingly):
   - `#"Renamed Columns"` → `#"Kolom namen vertalen"`
   - `#"Changed Type"` → `#"Kolom type wijzigen"`
   - `#"Removed Other Columns"` → `#"Benodigde kolommen selecteren"`
   - `#"Filtered Rows"` → `#"Rijen filteren"`
4. Preserve original indentation, tabs, and spacing exactly. Do not wrap or reflow existing lines
5. Do not alter `mode`, `queryGroup`, annotations, or any TMDL properties

## 9. **Coverage & Logging (DON’T SKIP)**
Before finishing:
- Count total `.tmdl` files discovered and total in-scope tables processed
- For every skipped file, record the exact reason (measure container, LocalDateTable/DateTableTemplate, no transformations detected)
- Confirm that 100% of in-scope tables received comments and Dutch step names where applicable

### **✅ AFTER (with Dutch comments):**
```m
partition Cohort = m
	mode: import
	queryGroup: Dimensies\Datum/tijd
	source =
		let
			/*Database connectie maken*/
			Source = Sql.Database("server", "DB", [Query="SELECT ..."]),
			
			/*Filter laatste 4 cohorten toevoegen*/
			#"Added Column" = Table.AddColumn(Source, "Filter", each ...),
			
			/*Kolom type wijzigen naar boolean*/
			#"Changed Type" = Table.TransformColumnTypes(#"Added Column", ...),
			
			/*Kolom naam vertalen naar Nederlands*/
			#"Renamed Columns" = Table.RenameColumns(#"Changed Type", ...)
		in
			#"Renamed Columns"
```

# 🧠 Mindset
Work like a **systematic and thorough** Power BI developer. 

**CRITICAL RULES:**
- Check EVERY table methodically - never skip based on name assumptions
- **Add concise Dutch comments AND rename steps to Dutch** - preserve formatting exactly
- **Don't touch `source =` or any indentation** - preserve formatting exactly
- **Work only inside `let` expressions** - add `/*comments*/` and rename `#"Step Names"`
- **Update step references consistently** - if you rename a step, update all places it's referenced
- **Be concise** - brief, clear comments that explain what the step does
- Follow the systematic identification process exactly to prevent missing tables
