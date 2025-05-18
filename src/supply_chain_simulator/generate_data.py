# src/generate_data.py

import argparse
import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime
from supply_chain_simulator.db_utils import save_to_sqlite
from supply_chain_simulator.simulation import simulate_transactions_and_inventory


fake = Faker("fr_FR")
np.random.seed(42)

# ----------------------------
# Utility Functions
# ----------------------------


def generate_products(n=20):
    categories = ["Shoes", "Jackets", "T-Shirts", "Shorts", "Pants"]
    brands = ["Nike", "Adidas", "Puma", "Under Armour", "Asics"]
    genders = ["Men", "Women", "Unisex"]
    colors = ["Black", "White", "Blue", "Red", "Green"]
    sizes = ["S", "M", "L", "XL", "38", "40", "42", "44"]
    seasons = ["Spring", "Summer", "Autumn", "Winter"]

    products = []

    for i in range(n):
        product = {
            "product_id": f"SKU{i+1:03}",
            "category": np.random.choice(categories),
            "brand": np.random.choice(brands),
            "gender": np.random.choice(genders),
            "color": np.random.choice(colors),
            "size": np.random.choice(sizes),
            "price_eur": round(np.random.uniform(50, 250), 2),
            "season": np.random.choice(seasons),
        }
        products.append(product)

    return pd.DataFrame(products)


def generate_stores(n=100):
    store_types = ["Flagship", "Outlet", "Regular"]
    regions = [
        "Île-de-France",
        "Auvergne-Rhône-Alpes",
        "Provence-Alpes-Côte d’Azur",
        "Nouvelle-Aquitaine",
        "Occitanie",
        "Hauts-de-France",
        "Grand Est",
        "Bretagne",
        "Normandie",
        "Pays de la Loire",
    ]

    stores = []

    for i in range(n):
        city = fake.city()
        region = np.random.choice(regions)
        store = {
            "store_id": f"FR{i+1:03}",
            "city": city,
            "region": region,
            "store_type": np.random.choice(store_types),
        }
        stores.append(store)

    return pd.DataFrame(stores)


def save_to_csv(df, path):
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


# ----------------------------
# Main CLI
# ----------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic supply chain data."
    )
    parser.add_argument(
        "--num-products",
        type=int,
        default=20,
        help="Number of unique products to generate",
    )
    parser.add_argument(
        "--num-stores", type=int, default=100, help="Number of stores to simulate"
    )
    parser.add_argument(
        "--start-date", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", type=str, default="2024-12-31", help="End date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)

    # Generate data
    products_df = generate_products(args.num_products)
    stores_df = generate_stores(args.num_stores)

    # Simulate transactions and warehouse inventory
    transactions_df, inventory_df = simulate_transactions_and_inventory(
        products_df, stores_df, args.start_date, args.end_date
    )

    # Save to CSV
    save_to_csv(products_df, "data/products.csv")
    save_to_csv(stores_df, "data/stores.csv")
    save_to_csv(transactions_df, "data/transactions.csv")
    save_to_csv(inventory_df, "data/inventory.csv")

    # Save to SQLite
    save_to_sqlite(
        "data/supply_chain.db",
        {
            "products": products_df,
            "stores": stores_df,
            "transactions": transactions_df,
            "inventory": inventory_df,
        },
    )


if __name__ == "__main__":
    main()
