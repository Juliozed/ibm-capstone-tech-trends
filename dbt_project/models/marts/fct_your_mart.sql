-- models/marts/fct_your_mart.sql
-- =================================
-- TEMPLATE: Copy this for each mart model
-- Replace with your actual business logic
--
-- PURPOSE: Business logic and final analytical tables
--   - Join staging models together
--   - Apply business rules and calculations
--   - Pre-calculate KPIs
--   - This is what Power BI / Tableau connects to
--
-- NAMING CONVENTION:
--   fct_  = fact tables (transactions, events — many rows)
--   dim_  = dimension tables (entities — one row per thing)
--   mart_ = aggregated summary tables (one row per group)

-- Reference staging models using {{ ref() }}
-- dbt automatically runs dependencies in the right order

WITH main_data AS (
    SELECT * FROM {{ ref('stg_your_main_table') }}
),

reference_data AS (
    SELECT * FROM {{ ref('stg_your_reference_table') }}
)

-- ── YOUR BUSINESS LOGIC HERE ──────────────────────────────────

SELECT
    -- ── Keys & Identifiers ────────────────────────────────────
    m.id_column,
    m.date_column,

    -- ── Descriptive fields (from reference tables) ────────────
    r.name_column,
    r.category_column,

    -- ── Measures ──────────────────────────────────────────────
    m.revenue,
    m.cost,
    m.profit,

    -- ── Calculated fields ─────────────────────────────────────
    ROUND(m.profit / NULLIF(m.revenue, 0) * 100, 2)  AS profit_margin_pct,

    -- ── Status flags ──────────────────────────────────────────
    CASE
        WHEN m.status = 'COMPLETED' THEN true
        ELSE false
    END AS is_completed,

    -- ── Date parts (for easy filtering in Power BI) ───────────
    m.created_year,
    m.created_month,
    m.created_period

FROM main_data m
LEFT JOIN reference_data r ON m.ref_id = r.id_column

-- ── Optional filters ──────────────────────────────────────────
-- WHERE m.is_deleted = false
-- WHERE m.created_year >= 2022
