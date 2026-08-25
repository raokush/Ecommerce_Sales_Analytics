import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of cleaned CSV
CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_ecommerce_sales.csv"
)

# Database folder
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(exist_ok=True)

# SQLite database
DATABASE_PATH = DATABASE_DIR / "ecommerce.db"


# Create database connection
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# Load cleaned data
df = pd.read_csv(CSV_PATH)


# Store data in SQLite
df.to_sql(
    "sales",
    engine,
    if_exists="replace",
    index=False
)


print("Database created successfully!")
print(f"Database: {DATABASE_PATH}")
print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")