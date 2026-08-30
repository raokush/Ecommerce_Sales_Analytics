import pandas as pd
from pathlib import Path


# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ecommerce_sales.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_ecommerce_sales.csv"
)


# =====================================================
# LOAD RAW DATA
# =====================================================

print("=" * 60)
print("E-COMMERCE DATA CLEANING")
print("=" * 60)

print(f"\nLoading raw data from:")
print(RAW_DATA_PATH)

df = pd.read_csv(RAW_DATA_PATH)

print(f"\nOriginal rows: {len(df):,}")
print(f"Original columns: {len(df.columns)}")


# =====================================================
# REMOVE DUPLICATE RECORDS
# =====================================================

duplicates = df.duplicated().sum()

print(f"\nDuplicate rows found: {duplicates:,}")

if duplicates > 0:
    df = df.drop_duplicates()

print(f"Rows after duplicate removal: {len(df):,}")


# =====================================================
# HANDLE MISSING VALUES
# =====================================================

print("\nMissing values before cleaning:")

print(
    df.isnull()
    .sum()
    .sort_values(ascending=False)
)


# Fill numeric missing values with median
numeric_columns = df.select_dtypes(
    include="number"
).columns

for column in numeric_columns:

    if df[column].isnull().any():

        df[column] = df[column].fillna(
            df[column].median()
        )


# Fill text missing values with "Unknown"
text_columns = df.select_dtypes(
    include="object"
).columns

for column in text_columns:

    if df[column].isnull().any():

        df[column] = df[column].fillna(
            "Unknown"
        )


# =====================================================
# DATE CONVERSION
# =====================================================

if "Order_Date" in df.columns:

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )


# =====================================================
# REMOVE INVALID DATES
# =====================================================

if "Order_Date" in df.columns:

    invalid_dates = df["Order_Date"].isnull().sum()

    print(
        f"\nInvalid dates found: {invalid_dates:,}"
    )

    df = df.dropna(
        subset=["Order_Date"]
    )


# =====================================================
# CREATE TIME FEATURES
# =====================================================

if "Order_Date" in df.columns:

    df["Year"] = df["Order_Date"].dt.year

    df["Month"] = df["Order_Date"].dt.month

    df["Month_Name"] = (
        df["Order_Date"]
        .dt.strftime("%B")
    )


# =====================================================
# CLEAN TEXT COLUMNS
# =====================================================

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )


# =====================================================
# SAVE PROCESSED DATA
# =====================================================

PROCESSED_DATA_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    PROCESSED_DATA_PATH,
    index=False
)


# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print(f"\nFinal rows: {len(df):,}")
print(f"Final columns: {len(df.columns)}")

print(
    f"\nCleaned dataset saved to:"
)

print(PROCESSED_DATA_PATH)

print("\n" + "=" * 60)
