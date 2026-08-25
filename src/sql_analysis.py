from sqlalchemy import create_engine, text
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "ecommerce.db"
)

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


queries = {

    "TOTAL REVENUE": """
        SELECT
            SUM(Net_Sales) AS Total_Revenue
        FROM sales;
    """,

    "TOTAL PROFIT": """
        SELECT
            SUM(Profit) AS Total_Profit
        FROM sales;
    """,

    "TOTAL ORDERS": """
        SELECT
            COUNT(DISTINCT Order_ID) AS Total_Orders
        FROM sales;
    """,

    "TOTAL CUSTOMERS": """
        SELECT
            COUNT(DISTINCT Customer_ID) AS Total_Customers
        FROM sales;
    """,

    "TOP CATEGORY": """
        SELECT
            Category,
            SUM(Net_Sales) AS Total_Revenue
        FROM sales
        GROUP BY Category
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    """,

    "TOP PRODUCT": """
        SELECT
            Product,
            SUM(Net_Sales) AS Total_Revenue
        FROM sales
        GROUP BY Product
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    """,

    "TOP REGION": """
        SELECT
            Region,
            SUM(Net_Sales) AS Total_Revenue
        FROM sales
        GROUP BY Region
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    """,

    "TOP CITY": """
        SELECT
            City,
            SUM(Net_Sales) AS Total_Revenue
        FROM sales
        GROUP BY City
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    """,

    "RETURN RATE": """
        SELECT
            COUNT(
                DISTINCT CASE
                    WHEN Order_Status = 'Returned'
                    THEN Order_ID
                END
            ) * 100.0
            / COUNT(DISTINCT Order_ID) AS Return_Rate
        FROM sales;
    """,

    "CANCELLATION RATE": """
        SELECT
            COUNT(
                DISTINCT CASE
                    WHEN Order_Status = 'Cancelled'
                    THEN Order_ID
                END
            ) * 100.0
            / COUNT(DISTINCT Order_ID) AS Cancellation_Rate
        FROM sales;
    """
}


with engine.connect() as connection:

    for name, query in queries.items():

        print("\n" + "=" * 50)
        print(name)
        print("=" * 50)

        result = connection.execute(text(query))

        for row in result:
            print(row)