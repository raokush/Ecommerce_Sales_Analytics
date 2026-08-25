-- =====================================================
-- ECOMMERCE SALES ANALYTICS
-- SQL ANALYSIS
-- =====================================================


-- 1. View Sample Records
SELECT *
FROM sales
LIMIT 10;


-- 2. Total Revenue
SELECT
    SUM(Net_Sales) AS Total_Revenue
FROM sales;


-- 3. Total Profit
SELECT
    SUM(Profit) AS Total_Profit
FROM sales;


-- 4. Total Orders
SELECT
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales;


-- 5. Total Customers
SELECT
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM sales;


-- 6. Total Units Sold
SELECT
    SUM(Quantity) AS Total_Units_Sold
FROM sales;


-- 7. Average Order Value
SELECT
    SUM(Net_Sales) / COUNT(DISTINCT Order_ID)
        AS Average_Order_Value
FROM sales;


-- 8. Revenue by Category
SELECT
    Category,
    SUM(Net_Sales) AS Total_Revenue
FROM sales
GROUP BY Category
ORDER BY Total_Revenue DESC;


-- 9. Profit by Category
SELECT
    Category,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Category
ORDER BY Total_Profit DESC;


-- 10. Top 10 Products by Revenue
SELECT
    Product,
    SUM(Net_Sales) AS Total_Revenue
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
LIMIT 10;


-- 11. Top 10 Products by Profit
SELECT
    Product,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Product
ORDER BY Total_Profit DESC
LIMIT 10;


-- 12. Revenue by Region
SELECT
    Region,
    SUM(Net_Sales) AS Total_Revenue
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC;


-- 13. Top 10 Cities by Revenue
SELECT
    City,
    SUM(Net_Sales) AS Total_Revenue
FROM sales
GROUP BY City
ORDER BY Total_Revenue DESC
LIMIT 10;


-- 14. Monthly Revenue
SELECT
    Year,
    Month,
    Month_Name,
    SUM(Net_Sales) AS Total_Revenue
FROM sales
GROUP BY
    Year,
    Month,
    Month_Name
ORDER BY
    Year,
    Month;


-- 15. Monthly Profit
SELECT
    Year,
    Month,
    Month_Name,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY
    Year,
    Month,
    Month_Name
ORDER BY
    Year,
    Month;


    -- 16. Orders by Payment Method
SELECT
    Payment_Method,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales
GROUP BY Payment_Method
ORDER BY Total_Orders DESC;


-- 17. Orders by Status
SELECT
    Order_Status,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales
GROUP BY Order_Status
ORDER BY Total_Orders DESC;


-- 18. Return Rate
SELECT
    COUNT(
        DISTINCT CASE
            WHEN Order_Status = 'Returned'
            THEN Order_ID
        END
    ) * 100.0
    / COUNT(DISTINCT Order_ID) AS Return_Rate
FROM sales;


-- 19. Cancellation Rate
SELECT
    COUNT(
        DISTINCT CASE
            WHEN Order_Status = 'Cancelled'
            THEN Order_ID
        END
    ) * 100.0
    / COUNT(DISTINCT Order_ID) AS Cancellation_Rate
FROM sales;


-- =====================================================
-- 20. Top 10 Customers by Revenue
-- =====================================================

SELECT
    Customer_ID,
    SUM(Net_Sales) AS Total_Revenue,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales
GROUP BY Customer_ID
ORDER BY Total_Revenue DESC
LIMIT 10;


-- =====================================================
-- 21. Customer Average Order Value
-- =====================================================

SELECT
    Customer_ID,
    SUM(Net_Sales) AS Total_Revenue,
    COUNT(DISTINCT Order_ID) AS Total_Orders,

    ROUND(
        SUM(Net_Sales) /
        COUNT(DISTINCT Order_ID),
        2
    ) AS Average_Order_Value

FROM sales

GROUP BY Customer_ID

ORDER BY Average_Order_Value DESC

LIMIT 10;


-- =====================================================
-- 22. Category Profit Margin
-- =====================================================

SELECT
    Category,

    SUM(Net_Sales) AS Revenue,

    SUM(Profit) AS Profit,

    ROUND(
        SUM(Profit) * 100.0 /
        NULLIF(SUM(Net_Sales), 0),
        2
    ) AS Profit_Margin

FROM sales

GROUP BY Category

ORDER BY Profit_Margin DESC;

-- =====================================================
-- 23. Product Profitability
-- =====================================================

SELECT
    Product,

    SUM(Net_Sales) AS Revenue,

    SUM(Profit) AS Profit,

    ROUND(
        SUM(Profit) * 100.0 /
        NULLIF(SUM(Net_Sales), 0),
        2
    ) AS Profit_Margin

FROM sales

GROUP BY Product

ORDER BY Profit DESC

LIMIT 10;