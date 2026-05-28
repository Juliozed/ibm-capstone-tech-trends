-- models/staging/stg_your_table.sql
-- ====================================
-- TEMPLATE: Copy this for each source table
-- Replace 'your_source' and 'your_table' with actual names
-- Replace column transformations with your actual columns
--
-- PURPOSE: Light cleaning only
--   - Fix data types
--   - Standardize text (UPPER, TRIM)
--   - Handle NULLs
--   - Rename columns to snake_case
--   - Add derived columns (dates parts)
--   - NO business logic here

WITH source AS (

    -- Reference your raw source table
    -- 'your_source' must match sources.yml name
    -- 'your_table'  must match the actual table name
    SELECT * FROM {{ source('your_source', 'your_table') }}

),

cleaned AS (

    SELECT
        -- ── IDs ───────────────────────────────────────────────
        id_column,                                    -- keep as-is

        -- ── TEXT COLUMNS ──────────────────────────────────────
        UPPER(TRIM(status_column))   AS status,       -- standardize text
        TRIM(name_column)            AS name,          -- remove spaces

        -- ── NUMERIC COLUMNS ───────────────────────────────────
        amount_column::NUMERIC(12,2) AS amount,        -- fix type
        COALESCE(qty_column, 0)      AS quantity,      -- handle NULLs

        -- ── DATE COLUMNS ──────────────────────────────────────
        date_column::DATE            AS created_date,  -- fix type

        -- ── DERIVED DATE PARTS ────────────────────────────────
        EXTRACT(YEAR  FROM date_column::DATE)::INTEGER AS created_year,
        EXTRACT(MONTH FROM date_column::DATE)::INTEGER AS created_month,
        TO_CHAR(date_column::DATE, 'YYYY-MM')          AS created_period,

        -- ── CALCULATED COLUMNS ────────────────────────────────
        ROUND(
            profit_col::NUMERIC / NULLIF(revenue_col::NUMERIC, 0),
            4
        ) AS profit_margin

    FROM source
    WHERE id_column IS NOT NULL    -- remove rows missing primary key

)

SELECT * FROM cleaned
