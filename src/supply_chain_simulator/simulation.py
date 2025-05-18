# src/simulation.py

import pandas as pd
import numpy as np
from datetime import timedelta


def simulate_transactions_and_inventory(products_df, stores_df, start_date, end_date):
    np.random.seed(42)

    # Dates
    date_range = pd.date_range(start=start_date, end=end_date)

    # Inventory settings
    initial_warehouse_stock = 500
    initial_store_stock = 20
    reorder_threshold = 100
    reorder_quantity = 300
    factory_lead_time = 7  # days

    # Dicts for tracking inventory
    warehouse_inventory = {
        pid: [initial_warehouse_stock] for pid in products_df["product_id"]
    }
    factory_shipments = {pid: [] for pid in products_df["product_id"]}

    # Simulated outputs
    transaction_records = []
    inventory_records = []

    # Set up store inventory per product
    store_inventory = {
        (store_id, product_id): initial_store_stock
        for store_id in stores_df["store_id"]
        for product_id in products_df["product_id"]
    }

    for current_date in date_range:
        weekday = current_date.weekday()
        is_weekend = weekday >= 5
        is_promo = (current_date.day // 7) % 3 == 0 and is_weekend

        for product in products_df.itertuples():
            # -------------------
            # Seasonality factor
            # -------------------
            month = current_date.month
            seasonal_multiplier = 1.0
            if product.season == "Summer" and 6 <= month <= 8:
                seasonal_multiplier = 2.0
            elif product.season == "Winter" and (month <= 2 or month == 12):
                seasonal_multiplier = 2.0

            # -------------------
            # Discounting logic
            # -------------------
            if is_promo:
                discount = np.random.choice([10, 15, 20, 30])
            else:
                discount = 0
            price = product.price_eur * (1 - discount / 100)

            # -------------------
            # Sales simulation per store
            # -------------------
            for store in stores_df.itertuples():
                inventory_key = (store.store_id, product.product_id)
                stock = store_inventory[inventory_key]

                demand_lambda = 2 * seasonal_multiplier
                expected_sales = np.random.poisson(lam=demand_lambda)

                # More sales if discounted
                if discount > 0:
                    expected_sales = int(expected_sales * 1.5)

                # Actual sales cannot exceed inventory
                units_sold = min(stock, expected_sales)
                store_inventory[inventory_key] -= units_sold

                if units_sold > 0:
                    transaction_records.append(
                        {
                            "transaction_id": f"{store.store_id}_{product.product_id}_{current_date}",
                            "date": current_date,
                            "store_id": store.store_id,
                            "product_id": product.product_id,
                            "units_sold": units_sold,
                            "unit_price_eur": round(price, 2),
                            "discount_applied": discount,
                            "promo_flag": is_promo,
                        }
                    )

            # -------------------
            # Warehouse inventory simulation
            # -------------------
            prev_inventory = warehouse_inventory[product.product_id][-1]

            # Check for incoming shipment from factory
            incoming = sum(
                [
                    q
                    for d, q in factory_shipments[product.product_id]
                    if d == current_date
                ]
            )

            # Total demand: restock each store to 20 units if understocked
            shipped = 0
            for store in stores_df["store_id"]:
                inventory_key = (store, product.product_id)
                if store_inventory[inventory_key] < 10:
                    restock = 10
                    if prev_inventory >= restock:
                        store_inventory[inventory_key] += restock
                        prev_inventory -= restock
                        shipped += restock

            # Trigger factory reorder if low stock
            if prev_inventory + incoming < reorder_threshold:
                factory_delivery_date = current_date + timedelta(days=factory_lead_time)
                factory_shipments[product.product_id].append(
                    (factory_delivery_date, reorder_quantity)
                )

            ending_inventory = prev_inventory + incoming - shipped
            ending_inventory = max(0, ending_inventory)

            warehouse_inventory[product.product_id].append(ending_inventory)

            inventory_records.append(
                {
                    "date": current_date,
                    "product_id": product.product_id,
                    "starting_inventory": prev_inventory,
                    "received_from_factory": incoming,
                    "shipped_to_stores": shipped,
                    "ending_inventory": ending_inventory,
                    "stockout_flag": ending_inventory == 0,
                    "overstock_flag": ending_inventory > 800,
                }
            )

    return (pd.DataFrame(transaction_records), pd.DataFrame(inventory_records))
