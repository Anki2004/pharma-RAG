"""
data_loader.py
--------------
Loads all CSV files from the data/ folder and merges them into a unified
knowledge base with columns: id, title, description, industry, source.
"""

import os
import glob
import pandas as pd
from config import DATA_DIR


def load_all_data() -> pd.DataFrame:
    """Load every CSV in DATA_DIR and return a single DataFrame."""
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    records = []
    record_id = 1

    for csv_path in sorted(csv_files):
        source = os.path.splitext(os.path.basename(csv_path))[0]  # e.g. "api_products"
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            # title = value of the first column
            title = str(row.iloc[0])

            # description = all columns as "key: value" pairs
            parts = [f"{col}: {row[col]}" for col in df.columns]
            description = " | ".join(parts)

            records.append({
                "id": str(record_id),
                "title": title,
                "description": description,
                "industry": "Chemical/Pharma",
                "source": source,
            })
            record_id += 1

    return pd.DataFrame(records)


if __name__ == "__main__":
    data = load_all_data()
    print(f"Loaded {len(data)} records from {data['source'].nunique()} sources.")
    print(data.head(10).to_string(index=False))
