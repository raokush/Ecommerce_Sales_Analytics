from sqlalchemy import create_engine, text
from pathlib import Path


# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "database" / "ecommerce.db"
SQL_FILE = PROJECT_ROOT / "sql" / "advanced_queries.sql"


# =====================================================
# CHECK FILES
# =====================================================

print("=" * 70)
print("ADVANCED SQL ANALYTICS")
print("=" * 70)

print(f"Database: {DATABASE_PATH}")
print(f"SQL File: {SQL_FILE}")


if not DATABASE_PATH.exists():
    print("\nERROR: Database file not found.")
    print("Run: python src/database.py")
    raise SystemExit


if not SQL_FILE.exists():
    print("\nERROR: advanced_queries.sql not found.")
    raise SystemExit


# =====================================================
# DATABASE CONNECTION
# =====================================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# =====================================================
# READ SQL FILE
# =====================================================

sql_text = SQL_FILE.read_text(
    encoding="utf-8"
)

print(f"\nSQL characters loaded: {len(sql_text)}")


# =====================================================
# REMOVE SQL COMMENTS
# =====================================================

clean_lines = []

for line in sql_text.splitlines():

    stripped = line.strip()

    # Ignore comment lines
    if stripped.startswith("--"):
        continue

    clean_lines.append(line)


clean_sql = "\n".join(clean_lines)


# =====================================================
# SPLIT QUERIES
# =====================================================

queries = [
    query.strip()
    for query in clean_sql.split(";")
    if query.strip()
]


print(f"Queries detected: {len(queries)}")


# =====================================================
# EXECUTE QUERIES
# =====================================================

with engine.connect() as connection:

    for number, query in enumerate(queries, start=1):

        print("\n" + "=" * 70)
        print(f"QUERY {number}")
        print("=" * 70)

        try:

            result = connection.execute(
                text(query)
            )

            rows = result.fetchall()

            if rows:

                for row in rows:
                    print(row)

            else:

                print("Query executed successfully.")
                print("No rows returned.")

        except Exception as error:

            print("\nERROR IN QUERY:")
            print(error)

            print("\nSQL:")
            print(query)


print("\n" + "=" * 70)
print("ADVANCED SQL ANALYSIS COMPLETED")
print("=" * 70)