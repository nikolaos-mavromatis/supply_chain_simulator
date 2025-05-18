# 🏬 Synthetic Supply Chain Data Generator

This project generates synthetic supply chain data for a high-end **shoe and clothing retailer** operating in **France**. It simulates:

- 🛍️ Daily point-of-sale (POS) transactions
- 🏭 Daily warehouse inventory levels
- 🧾 Product and store attributes

The dataset captures **realistic seasonality, stockouts, promotions, and supply chain lead times**, and exports the results to **CSV and SQLite** formats.

---

## 🚀 Features

- 🏷️ **Product metadata** with seasonal categories and pricing
- 🏪 **100 configurable French stores**
- 📅 **1 year of daily simulation**
- 📈 **Seasonal demand patterns**
- 🔁 **Inventory updates with restocking logic**
- 📉 **Stockouts and overstocks**
- 💸 **Promotions and discounts every 3rd weekend**
- 🐢 **Factory lead times to warehouse (7-day delay)**
- 💾 Outputs as **CSV files** and a **SQLite database**

---

## 📦 Installation

Install dependencies using [`uv`](https://github.com/astral-sh/uv):

```bash
uv pip install -r requirements.txt
```

---

## ⚙️ How to Use
Run the CLI script:

```bash
uv python src/generate_data.py --num-products 20 --num-stores 100
```

**Optional Arguments**
| Argument         | Default      | Description                      |
| ---------------- | ------------ | -------------------------------- |
| `--num-products` | `20`         | Number of unique products (SKUs) |
| `--num-stores`   | `100`        | Number of stores in France       |
| `--start-date`   | `2024-01-01` | Simulation start date            |
| `--end-date`     | `2024-12-31` | Simulation end date              |

---

## 📂 Output Files
Generated files are saved to the `data/` directory:

### CSV Files
* `products.csv` — Product catalog with attributes

* `stores.csv` — List of POS store locations

* `transactions.csv` — Daily sales per store and SKU

* `inventory.csv` — Daily warehouse inventory per SKU

### SQLite Database
* `supply_chain.db` — Includes all four tables above

---

## 🗃️ Project Structure

```bash
supply_chain_sim/
├── data/                    # Output files
├── src/
│   ├── generate_data.py     # CLI entry point
│   ├── simulation.py        # Transaction + inventory simulation
│   └── db_utils.py          # SQLite saving logic
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔍 Highlights
* Seasonality:

    * Products are tagged for Summer or Winter demand peaks

    * Simulated demand increases in those seasons

* Discounts:

    * Every 3rd weekend, random promotions (10–30%) drive increased sales

* Stock Flow:

    * Store-level restocking from warehouse when low

    * Warehouse receives delayed shipments from factory (7-day lead time)

---

## 📌 Notes
* All prices are in euros (€)

* Store locations are in France

* Promotions occur every 3rd weekend

* Lead time from factory to warehouse is **7
