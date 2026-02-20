---
title: Annotate Tables and Columns
---

# 🎯 Goal
Add comprehensive documentation to TMDL tables and columns with Dutch descriptions and original database column names for improved model understanding and maintenance.

# 📌 Instructions

## 1. **Systematic Scope Identification** (Follow this process exactly):

   ### **Step 1: Complete Table Discovery**
   a. **List ALL .tmdl files** in the `DM {name of model}.SemanticModel\\definition\\tables\\` directory
   b. **Read each file** to understand its structure and purpose
   c. **CRITICAL: DO NOT make assumptions** based on table names - examine the actual content
   
   ### **Step 2: Table Classification**
   **✅ INCLUDE these tables:**
   - All dimension tables (contain business entities like Student, Minor, Opleiding, etc.)
   - All fact tables (contain transactional data like Student minoren)
   - All lookup/reference tables (contain codes, statuses, etc.)
   - System monitoring tables (ZZ_Actualiteit tables for data quality)
   - ANY table with actual business data or relationships
   
   **❌ EXCLUDE only these tables:**
   - **Measure container tables**: Tables that exist solely to hold DAX measures
     - Typically named "Meetwaardes" + suffix
     - Contain compressed JSON dummy data in partition source
     - Have no meaningful columns except lineageTag properties
     - **Identification pattern in source code:**
       ```powerquery
       Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("...", BinaryEncoding.Base64), Compression.Deflate)))
       ```
     - **Example files**: `Meetwaardes DM Minoren.tmdl`, `Meetwaardes Rapport.tmdl`
     - **Key characteristic**: The table serves as a container for DAX measures, not actual data
   
   ### **Step 3: Verification**
   **MANDATORY**: Apply annotations to **EVERY** table in scope. No exceptions.
   - If unsure about a table, include it rather than exclude it
   - When complete, verify ALL tables in the directory have been processed

## 2. **Table-Level Documentation**:
   Add **triple-slash (`///`) comments** at the top of each table with:
   
   ### **Required Information:**
   - **Purpose**: Brief Dutch description of what the table contains/does
   - **Relationships**: List related tables with connection details (from relationships.tmdl)
   - **Source**: Database source information (schema, view/table name)
   
   ### **Format Example:**
   ```tmdl
   /// Dimensietabel voor collegejaarperiodes en blokken. Bevat informatie over academische periodes en hun eigenschappen.
   /// Gerelateerde tabellen: Student minoren (via D_BLOK_MINOR_ID), Collegejaar (bidirectionele relatie via D_BLOK_ID).
   /// Bron: VW_DM_D_BLOK view in DB_DENA_DWH database.
   table Blok
   ```

## 3. **Column-Level Documentation**:
   Add **triple-slash (`///`) comments** before each column with:
   
   ### **Required Information:**
   - **Functional description** in Dutch explaining what the column represents
   - **Original database column name** (extracted from Table.RenameColumns operations)
   
   ### **Format Example:**
   ```tmdl
   /// Naam van het blok. Originele databasekolom: BLOK
   column Blok
       dataType: string
       // ... rest of column definition
   ```

## 4. **Information Sources**:

   ### **For Table Relationships:**
   - Read `DM {name of model}.SemanticModel\\definition\\relationships.tmdl`
   - Look for `fromColumn` and `toColumn` references
   - Note relationship properties (crossFilteringBehavior, fromCardinality)
   
   ### **For Original Column Names:**
   - Examine the `partition` section's `source` property
   - Find `Table.RenameColumns` steps in the Power Query code
   - Extract the mapping: `{{"ORIGINAL_NAME", "New Name"}}`
   - If no rename operation exists, the column name is unchanged from source

## 5. **Implementation Rules**:

   ### **✅ WHAT TO DO:**
   - Use **triple-slash (`///`)** format for ALL descriptions
   - Write descriptions in **Dutch**
   - Include **original database column names** for all columns
   - List **all related tables** with connection details
   - Maintain **existing TMDL structure** and formatting
   - Keep all existing properties, lineageTags, and annotations unchanged
   
   ### **❌ WHAT NOT TO DO:**
   - Don't change column names, data types, or any existing properties
   - Don't modify partition definitions or Power Query code
   - Don't change indentation or structural formatting
   - Don't add descriptions to measure container tables
   - Don't remove existing comments or annotations

## 6. **Column Name Mapping Process**:

   ### **Step-by-Step:**
   1. **Locate** the `Table.RenameColumns` step in the table's source query
   2. **Extract** the mapping pairs: `{{"SOURCE_NAME", "Display_Name"}}`
   3. **Apply** the original name in the description: `Originele databasekolom: SOURCE_NAME`
   4. **Handle edge cases:**
      - If no rename operation: Use the current column name as original
      - If multiple renames: Use the earliest source name in the chain

   ### **Example Mapping:**
   ```powerquery
   #"Renamed Columns" = Table.RenameColumns(#"Previous Step",{
       {"BLOK", "Blok"}, 
       {"BLOKNUMMER", "Blok (nummer)"}, 
       {"COLLEGEJAAR", "Collegejaar"}
   })
   ```
   Results in:
   - `Blok` → `Originele databasekolom: BLOK`
   - `Blok (nummer)` → `Originele databasekolom: BLOKNUMMER`
   - `Collegejaar` → `Originele databasekolom: COLLEGEJAAR`

## 7. **Quality Standards**:

   ### **Table Descriptions Should:**
   - Be concise but informative (1-2 sentences)
   - Explain the business purpose of the table
   - Use proper Dutch grammar and terminology
   - Include all direct relationships to other tables
   
   ### **Column Descriptions Should:**
   - Clearly explain what the column represents
   - Use consistent terminology across the model
   - Always include the original database column name
   - Be brief but descriptive

## 8. **Relationship Documentation Format**:
   
   ### **Standard Format:**
   ```
   Gerelateerde tabellen: [Table1] (via [column_connection]), [Table2] (bidirectionele relatie via [column_connection]).
   ```
   
   ### **Relationship Types:**
   - Standard: `Table (via COLUMN_ID)`
   - Bidirectional: `Table (bidirectionele relatie via COLUMN_ID)`
   - One-to-many: `Table (een-op-veel via COLUMN_ID)` (if specified)

# 🧠 Mindset
Act like a **thorough documentation specialist**. Prioritize clarity, consistency, and completeness. Every table and column should be self-documenting for future developers and business users.

# ✅ **Completion Checklist**

## **Before Starting:**
1. **List all .tmdl files** in `DM {name of model}.SemanticModel\\definition\\tables\\`
2. **Count total files** to track progress
3. **Identify measure container tables** by examining their partition source code

## **During Implementation:**
1. **Work systematically** through each table file
2. **Document progress** - mark each table as completed
3. **Don't skip any table** unless it's confirmed as a measure container

## **Final Verification:**
1. **Count annotated tables** vs total table files
2. **Verify coverage** - every non-measure table should have annotations
3. **Check relationships** - all connections from relationships.tmdl should be documented

# 🎯 Success Criteria
- **100% coverage**: Every table in scope has comprehensive annotations
- **Complete table descriptions**: Purpose, relationships, and database source documented
- **Complete column descriptions**: Functional description + original database column name for ALL columns
- **Consistent terminology**: All descriptions use proper Dutch grammar and consistent terms
- **TMDL compatibility**: All documentation follows triple-slash format
- **Structure preservation**: No existing TMDL structure or properties modified
- **Accurate relationships**: All model relationships from relationships.tmdl documented correctly
- **No tables missed**: Systematic verification that all tables in directory are processed