import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible results
np.random.seed(42)

# Number of transactions
n = 1000

# Product information
products = {
    "Laptop": ("Electronics", 55000, 42000),
    "Smartphone": ("Electronics", 25000, 19000),
    "Headphones": ("Electronics", 2500, 1600),
    "Smartwatch": ("Electronics", 5000, 3300),
    "Office Chair": ("Furniture", 8500, 6000),
    "Desk": ("Furniture", 12000, 8500),
    "Backpack": ("Accessories", 1800, 1100),
    "Shoes": ("Fashion", 3500, 2200),
    "T-Shirt": ("Fashion", 900, 500),
    "Coffee Maker": ("Home Appliances", 4500, 3000),
    "Mixer Grinder": ("Home Appliances", 3500, 2300),
    "Bookshelf": ("Furniture", 7000, 4800),
}

cities = {
    "Delhi": "North",
    "Lucknow": "North",
    "Jaipur": "North",
    "Mumbai": "West",
    "Pune": "West",
    "Ahmedabad": "West",
    "Bengaluru": "South",
    "Chennai": "South",
    "Hyderabad": "South",
    "Kolkata": "East",
    "Patna": "East",
    "Bhubaneswar": "East",
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Cancelled",
    "Returned",
]

product_names = list(products.keys())
city_names = list(cities.keys())

# Generate transaction data
data = []

for i in range(n):
    product = np.random.choice(product_names)
    category, price, product_cost = products[product]

    city = np.random.choice(city_names)
    region = cities[city]

    order_date = pd.Timestamp("2025-01-01") + pd.Timedelta(
        days=np.random.randint(0, 365)
    )

    quantity = np.random.randint(1, 5)
    discount = np.random.choice([0, 5, 10, 15, 20])
    shipping_cost = np.random.randint(50, 501)

    data.append(
        {
            "Order_ID": f"ORD{10001 + i}",
            "Order_Date": order_date,
            "Customer_ID": f"CUST{np.random.randint(1, 301):03d}",
            "Product": product,
            "Category": category,
            "Quantity": quantity,
            "Unit_Price": price,
            "Product_Cost": product_cost,
            "Discount": discount,
            "Payment_Method": np.random.choice(payment_methods),
            "Region": region,
            "City": city,
            "Order_Status": np.random.choice(order_statuses),
            "Shipping_Cost": shipping_cost,
        }
    )

df = pd.DataFrame(data)

# Introduce realistic data-quality issues
df.loc[10, "City"] = None
df.loc[25, "Payment_Method"] = None
df.loc[40, "Discount"] = None

# Add one duplicate transaction
df = pd.concat([df, df.iloc[[50]]], ignore_index=True)

# Save the raw dataset
output_path = Path("data/raw/ecommerce_sales.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")