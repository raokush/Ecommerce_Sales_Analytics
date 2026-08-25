from sqlalchemy import create_engine, text
from pathlib import Path


# =====================================================
# PROJECT PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "ecommerce.db"
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# =====================================================
# SQL QUERY
# =====================================================

query = """
SELECT *
FROM sales
LIMIT 10;
"""


# =====================================================
# EXECUTE QUERY
# =====================================================

with engine.connect() as connection:

    result = connection.execute(
        text(query)
    )

    print("\nFirst 10 records from sales table:")
    print("=" * 100)

    for row in result:
        print(row)