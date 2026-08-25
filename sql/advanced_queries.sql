WITH product_sales AS (

    SELECT
        Product,
        SUM(Net_Sales) AS Revenue
    FROM sales
    GROUP BY Product
)

SELECT
    Product,
    Revenue,

    RANK() OVER (
        ORDER BY Revenue DESC
    ) AS Revenue_Rank

FROM product_sales

ORDER BY Revenue_Rank;


SELECT

    Year,
    Month,
    Month_Name,

    SUM(Net_Sales) AS Revenue

FROM sales

GROUP BY
    Year,
    Month,
    Month_Name

ORDER BY
    Year,
    Month;



SELECT

    Year,
    Month,
    Month_Name,

    SUM(Profit) AS Profit

FROM sales

GROUP BY
    Year,
    Month,
    Month_Name

ORDER BY
    Year,
    Month;


WITH monthly_sales AS (

    SELECT

        Year,
        Month,
        Month_Name,

        SUM(Net_Sales) AS Revenue

    FROM sales

    GROUP BY
        Year,
        Month,
        Month_Name
)

SELECT

    Year,
    Month,
    Month_Name,

    ROUND(Revenue, 2) AS Revenue,

    ROUND(
        LAG(Revenue) OVER (
            ORDER BY Year, Month
        ),
        2
    ) AS Previous_Month_Revenue,

    ROUND(

        (
            Revenue
            -
            LAG(Revenue) OVER (
                ORDER BY Year, Month
            )
        )
        * 100.0
        /
        NULLIF(
            LAG(Revenue) OVER (
                ORDER BY Year, Month
            ),
            0
        ),

        2

    ) AS MoM_Growth_Percentage

FROM monthly_sales

ORDER BY
    Year,
    Month;


WITH monthly_sales AS (

    SELECT

        Year,
        Month,
        Month_Name,

        SUM(Net_Sales) AS Revenue

    FROM sales

    GROUP BY
        Year,
        Month,
        Month_Name
),

monthly_growth AS (

    SELECT

        Year,
        Month,
        Month_Name,
        Revenue,

        LAG(Revenue) OVER (
            ORDER BY Year, Month
        ) AS Previous_Revenue

    FROM monthly_sales
)

SELECT

    Year,
    Month,
    Month_Name,

    ROUND(Revenue, 2) AS Revenue,

    ROUND(Previous_Revenue, 2) AS Previous_Revenue,

    ROUND(

        (
            Revenue - Previous_Revenue
        )
        * 100.0
        /
        NULLIF(Previous_Revenue, 0),

        2

    ) AS Growth_Percentage

FROM monthly_growth

WHERE Previous_Revenue IS NOT NULL

ORDER BY Growth_Percentage DESC

LIMIT 1;


WITH monthly_sales AS (

    SELECT

        Year,
        Month,
        Month_Name,

        SUM(Net_Sales) AS Revenue

    FROM sales

    GROUP BY
        Year,
        Month,
        Month_Name
),

monthly_growth AS (

    SELECT

        Year,
        Month,
        Month_Name,
        Revenue,

        LAG(Revenue) OVER (
            ORDER BY Year, Month
        ) AS Previous_Revenue

    FROM monthly_sales
)

SELECT

    Year,
    Month,
    Month_Name,

    ROUND(Revenue, 2) AS Revenue,

    ROUND(Previous_Revenue, 2) AS Previous_Revenue,

    ROUND(

        (
            Revenue - Previous_Revenue
        )
        * 100.0
        /
        NULLIF(Previous_Revenue, 0),

        2

    ) AS Growth_Percentage

FROM monthly_growth

WHERE Previous_Revenue IS NOT NULL

ORDER BY Growth_Percentage ASC

LIMIT 1;


SELECT

    Year,
    Quarter,

    SUM(Net_Sales) AS Revenue,

    SUM(Profit) AS Profit,

    ROUND(

        SUM(Profit) * 100.0
        /
        NULLIF(SUM(Net_Sales), 0),

        2

    ) AS Profit_Margin

FROM sales

GROUP BY
    Year,
    Quarter

ORDER BY
    Year,
    Quarter;


SELECT

    Category,

    ROUND(
        AVG(Discount),
        2
    ) AS Average_Discount,

    ROUND(
        SUM(Net_Sales),
        2
    ) AS Revenue,

    ROUND(
        SUM(Profit),
        2
    ) AS Profit,

    ROUND(
        SUM(Profit) * 100.0
        /
        NULLIF(SUM(Net_Sales), 0),
        2
    ) AS Profit_Margin

FROM sales

GROUP BY Category

ORDER BY Average_Discount DESC;


SELECT

    Product,

    ROUND(
        AVG(Discount),
        2
    ) AS Average_Discount,

    ROUND(
        SUM(Net_Sales),
        2
    ) AS Revenue,

    ROUND(
        SUM(Profit),
        2
    ) AS Profit,

    ROUND(
        SUM(Profit) * 100.0
        /
        NULLIF(SUM(Net_Sales), 0),
        2
    ) AS Profit_Margin

FROM sales

GROUP BY Product

ORDER BY Profit_Margin DESC;


SELECT

    Product,

    ROUND(
        AVG(Discount),
        2
    ) AS Average_Discount,

    ROUND(
        SUM(Net_Sales),
        2
    ) AS Revenue,

    ROUND(
        SUM(Profit),
        2
    ) AS Profit,

    ROUND(
        SUM(Profit) * 100.0
        /
        NULLIF(SUM(Net_Sales), 0),
        2
    ) AS Profit_Margin

FROM sales

GROUP BY Product

HAVING AVG(Discount) >= 15

ORDER BY Average_Discount DESC;


SELECT

    Category,

    COUNT(DISTINCT Order_ID)
        AS Total_Orders,

    COUNT(
        DISTINCT CASE
            WHEN Order_Status = 'Returned'
            THEN Order_ID
        END
    ) AS Returned_Orders,

    ROUND(

        COUNT(
            DISTINCT CASE
                WHEN Order_Status = 'Returned'
                THEN Order_ID
            END
        )
        * 100.0
        /
        COUNT(DISTINCT Order_ID),

        2

    ) AS Return_Rate

FROM sales

GROUP BY Category

ORDER BY Return_Rate DESC;


SELECT

    Region,

    COUNT(DISTINCT Order_ID)
        AS Total_Orders,

    COUNT(
        DISTINCT CASE
            WHEN Order_Status = 'Cancelled'
            THEN Order_ID
        END
    ) AS Cancelled_Orders,

    ROUND(

        COUNT(
            DISTINCT CASE
                WHEN Order_Status = 'Cancelled'
                THEN Order_ID
            END
        )
        * 100.0
        /
        COUNT(DISTINCT Order_ID),

        2

    ) AS Cancellation_Rate

FROM sales

GROUP BY Region

ORDER BY Cancellation_Rate DESC;


WITH customer_sales AS (

    SELECT

        Customer_ID,

        COUNT(DISTINCT Order_ID)
            AS Total_Orders,

        SUM(Net_Sales)
            AS Total_Revenue,

        SUM(Profit)
            AS Total_Profit

    FROM sales

    GROUP BY Customer_ID
)

SELECT

    Customer_ID,

    Total_Orders,

    ROUND(
        Total_Revenue,
        2
    ) AS Total_Revenue,

    ROUND(
        Total_Profit,
        2
    ) AS Total_Profit,

    CASE

        WHEN Total_Revenue >= 200000
            THEN 'High Value'

        WHEN Total_Revenue >= 100000
            THEN 'Medium Value'

        ELSE 'Low Value'

    END AS Customer_Segment

FROM customer_sales

ORDER BY Total_Revenue DESC;


WITH customer_sales AS (

    SELECT

        Customer_ID,

        SUM(Net_Sales)
            AS Total_Revenue

    FROM sales

    GROUP BY Customer_ID
),

customer_segments AS (

    SELECT

        Customer_ID,

        Total_Revenue,

        CASE

            WHEN Total_Revenue >= 200000
                THEN 'High Value'

            WHEN Total_Revenue >= 100000
                THEN 'Medium Value'

            ELSE 'Low Value'

        END AS Customer_Segment

    FROM customer_sales
)

SELECT

    Customer_Segment,

    COUNT(*) AS Customer_Count,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS Segment_Revenue,

    ROUND(

        SUM(Total_Revenue)
        * 100.0
        /
        SUM(SUM(Total_Revenue)) OVER (),

        2

    ) AS Revenue_Contribution_Percentage

FROM customer_segments

GROUP BY Customer_Segment

ORDER BY Segment_Revenue DESC;


SELECT

    COUNT(DISTINCT Order_ID)
        AS Total_Orders,

    COUNT(DISTINCT Customer_ID)
        AS Total_Customers,

    SUM(Quantity)
        AS Total_Units_Sold,

    ROUND(
        SUM(Net_Sales),
        2
    ) AS Total_Revenue,

    ROUND(
        SUM(Profit),
        2
    ) AS Total_Profit,

    ROUND(

        SUM(Net_Sales)
        /
        COUNT(DISTINCT Order_ID),

        2

    ) AS Average_Order_Value,

    ROUND(

        SUM(Profit)
        * 100.0
        /
        NULLIF(SUM(Net_Sales), 0),

        2

    ) AS Profit_Margin,

    ROUND(

        COUNT(
            DISTINCT CASE
                WHEN Order_Status = 'Returned'
                THEN Order_ID
            END
        )
        * 100.0
        /
        COUNT(DISTINCT Order_ID),

        2

    ) AS Return_Rate,

    ROUND(

        COUNT(
            DISTINCT CASE
                WHEN Order_Status = 'Cancelled'
                THEN Order_ID
            END
        )
        * 100.0
        /
        COUNT(DISTINCT Order_ID),

        2

    ) AS Cancellation_Rate

FROM sales;