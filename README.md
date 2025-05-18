# Supply Chain Simulator

Synthetic data generator for a high-end sports shoe and clothing retailer in France. The simulator creates realistic datasets for supply chain management, including:

- Point-of-sale (POS) transaction data
- SKU-level warehouse inventory data
- Product metadata
- Store location and type

## 📦 Features

- Configurable number of products and stores
- Daily-level aggregation with seasonality patterns
- Simulated stockouts, overstocks, and lead times
- Outputs CSV files and a SQLite database
- Realistic promotions and discounting patterns

## 🛠 Project Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install uv if you haven't
pip install uv

# Clone the repository and install dependencies
git clone https://github.com/your-username/supply_chain_sim.git
cd supply_chain_simulator
uv venv
source .venv/bin/activate
```

## 🚀 Usage

Data generation will be run via a CLI tool:

```bash
uv run python generate_data.py \\
    --num-products 20 \\
    --num-stores 100 \\
    --start-date 2024-01-01 \\
    --end-date 2024-12-31
```

Output files:
- `data/products.csv`
- `data/stores.csv`
- `data/transactions.csv`
- `data/inventory.csv`
- `data/supply_chain.db` (SQLite)

## 📂 Project Structure

```
supply_chain_simulator/
├── data/                       # Generated data (CSV & SQLite)
├── src/                        # Source code
│   └── supply_chain_simulator  
│       └── generate_data.py    # Main script
├── .gitignore
├── pyproject.toml
└── README.md
```

## 📄 License

MIT License
