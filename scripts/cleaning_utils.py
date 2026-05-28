"""
cleaning_utils.py
=================
Standard data cleaning functions.
Copy into any project — import what you need.

USAGE:
    from scripts.cleaning_utils import profile, run_clean_pipeline
    
    profile(df, 'My Dataset')
    
    df_clean = run_clean_pipeline(df, {
        'clean_column_names': True,
        'text_columns': ['status', 'region'],
        'currency_cols': ['revenue', 'cost'],
        'date_cols': ['order_date'],
        'date_parts_col': 'order_date',
        'required_cols': ['order_id'],
    })
"""

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════
# PROFILING
# ══════════════════════════════════════════════════════════════

def profile(df, name='DataFrame'):
    """Full data quality report. Run on every new dataset first."""
    print(f"\n{'='*55}")
    print(f"  PROFILE: {name}")
    print(f"{'='*55}")
    print(f"  Rows:    {df.shape[0]:,}")
    print(f"  Columns: {df.shape[1]}")
    print(f"  Memory:  {df.memory_usage(deep=True).sum()/1024**2:.1f} MB")

    print(f"\n  DATA TYPES")
    print(f"  {'─'*40}")
    for col, dtype in df.dtypes.items():
        print(f"  {col:<30} {str(dtype)}")

    print(f"\n  MISSING VALUES")
    print(f"  {'─'*40}")
    missing = df.isnull().sum()
    has_missing = missing[missing > 0]
    if len(has_missing) == 0:
        print("  No missing values ✓")
    else:
        for col, count in has_missing.items():
            pct = count / len(df) * 100
            print(f"  {col:<30} {count:>6,}  ({pct:.1f}%)")

    print(f"\n  DUPLICATES")
    print(f"  {'─'*40}")
    dupes = df.duplicated().sum()
    print(f"  Duplicate rows: {dupes:,}")

    print(f"\n  NUMERIC SUMMARY")
    print(f"  {'─'*40}")
    print(df.describe().round(2).to_string())

    print(f"\n  CATEGORICAL COLUMNS")
    print(f"  {'─'*40}")
    for col in df.select_dtypes(include='object').columns:
        print(f"\n  {col} ({df[col].nunique()} unique):")
        for val, cnt in df[col].value_counts().head(5).items():
            print(f"    {str(val):<25} {cnt:>6,}")
    print(f"\n{'='*55}\n")


# ══════════════════════════════════════════════════════════════
# COLUMN CLEANING
# ══════════════════════════════════════════════════════════════

def clean_column_names(df):
    """Standardize all column names: lowercase, underscores, no special chars."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(r'[^a-z0-9]+', '_', regex=True)
        .str.strip('_')
    )
    return df


def clean_text_column(df, col):
    """Strip whitespace, fix extra spaces. Use before any JOIN or filter."""
    df = df.copy()
    df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
    return df


def fix_currency_column(df, col):
    """Convert '$1,234.56' strings to float 1234.56."""
    df = df.copy()
    df[col] = (
        df[col].astype(str)
        .str.replace(r'[$,\s]', '', regex=True)
        .str.replace(r'[^\d.-]', '', regex=True)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def fix_percentage_column(df, col):
    """Convert '45.5%' to decimal 0.455."""
    df = df.copy()
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace('%', '').str.strip(),
        errors='coerce'
    ) / 100
    return df


def fix_date_column(df, col, format=None):
    """Convert any date string to proper datetime."""
    df = df.copy()
    df[col] = pd.to_datetime(df[col], format=format, errors='coerce')
    n_failed = df[col].isnull().sum()
    if n_failed > 0:
        print(f"Warning: {n_failed} dates could not be parsed in '{col}'")
    return df


def extract_date_parts(df, date_col):
    """Extract year, month, day, quarter, period from a datetime column."""
    df = df.copy()
    df['year']       = df[date_col].dt.year
    df['month']      = df[date_col].dt.month
    df['month_name'] = df[date_col].dt.strftime('%b %Y')
    df['quarter']    = df[date_col].dt.quarter
    df['weekday']    = df[date_col].dt.day_name()
    df['period']     = df[date_col].dt.strftime('%Y-%m')
    return df


# ══════════════════════════════════════════════════════════════
# NULL HANDLING
# ══════════════════════════════════════════════════════════════

def fill_nulls(df, fills):
    """Fill nulls in multiple columns. fills = {'col': value}"""
    df = df.copy()
    for col, value in fills.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)
    return df


def drop_nulls_in(df, required_cols):
    """Drop rows where required columns are null."""
    before = len(df)
    df = df.dropna(subset=required_cols)
    dropped = before - len(df)
    if dropped > 0:
        print(f"Dropped {dropped:,} rows with nulls in: {required_cols}")
    return df


def remove_duplicates(df, key_cols=None, keep='first'):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates(subset=key_cols, keep=keep)
    dropped = before - len(df)
    if dropped > 0:
        print(f"Removed {dropped:,} duplicate rows")
    return df


# ══════════════════════════════════════════════════════════════
# OUTLIER DETECTION
# ══════════════════════════════════════════════════════════════

def flag_outliers(df, col, method='iqr', threshold=1.5):
    """Add boolean column flagging outliers. Adds {col}_is_outlier."""
    df = df.copy()
    if method == 'iqr':
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        df[f'{col}_is_outlier'] = (
            (df[col] < Q1 - threshold * IQR) |
            (df[col] > Q3 + threshold * IQR)
        )
    elif method == 'zscore':
        z = np.abs((df[col] - df[col].mean()) / df[col].std())
        df[f'{col}_is_outlier'] = z > threshold
    n = df[f'{col}_is_outlier'].sum()
    print(f"Flagged {n:,} outliers in '{col}' ({n/len(df)*100:.1f}%)")
    return df


# ══════════════════════════════════════════════════════════════
# FULL PIPELINE
# ══════════════════════════════════════════════════════════════

def run_clean_pipeline(df, config):
    """
    Run a full cleaning pipeline from a config dict.
    
    config = {
        'clean_column_names': True,
        'text_columns':   ['status', 'rep_name'],
        'currency_cols':  ['revenue', 'cost'],
        'pct_cols':       ['profit_pct'],
        'date_cols':      ['order_date'],
        'date_parts_col': 'order_date',
        'fill_nulls':     {'revenue': 0},
        'required_cols':  ['order_id'],
        'dedup_key':      ['order_id'],
    }
    """
    print("Running cleaning pipeline...")

    if config.get('clean_column_names'):
        df = clean_column_names(df)
        print("  ✓ Column names standardized")

    for col in config.get('text_columns', []):
        df = clean_text_column(df, col)
    if config.get('text_columns'):
        print(f"  ✓ Text cleaned: {config['text_columns']}")

    for col in config.get('currency_cols', []):
        df = fix_currency_column(df, col)
    if config.get('currency_cols'):
        print(f"  ✓ Currency fixed: {config['currency_cols']}")

    for col in config.get('pct_cols', []):
        df = fix_percentage_column(df, col)
    if config.get('pct_cols'):
        print(f"  ✓ Percentages fixed: {config['pct_cols']}")

    for col in config.get('date_cols', []):
        df = fix_date_column(df, col)
    if config.get('date_cols'):
        print(f"  ✓ Dates fixed: {config['date_cols']}")

    if config.get('date_parts_col'):
        df = extract_date_parts(df, config['date_parts_col'])
        print(f"  ✓ Date parts extracted from: {config['date_parts_col']}")

    if config.get('fill_nulls'):
        df = fill_nulls(df, config['fill_nulls'])
        print("  ✓ Nulls filled")

    if config.get('required_cols'):
        df = drop_nulls_in(df, config['required_cols'])

    if config.get('dedup_key'):
        df = remove_duplicates(df, key_cols=config['dedup_key'])

    print(f"Pipeline complete: {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df
