import pandas as pd
from pathlib import Path

IN = Path("data/processed/zcta_de.parquet")
OUT = Path("data/processed")
OUT.mkdir(exist_ok=True)

df = pd.read_parquet(IN)

# Drop unusable rows
df = df.dropna(subset=["median_income", "median_rent"])
df = df[df["median_income"] > 0]

df["monthly_income"] = df["median_income"] / 12
df["rent_burden"] = df["median_rent"] / df["monthly_income"]

def categorize(rb):
    if rb <= 0.30:
        return "Affordable"
    elif rb <= 0.50:
        return "Cost Burdened"
    else:
        return "Severely Cost Burdened"

df["category"] = df["rent_burden"].apply(categorize)

df = df[[
    "zcta",
    "median_income",
    "median_rent",
    "rent_burden",
    "category",
    "population"
]]

df.to_parquet(OUT / "metrics.parquet", index=False)
print("Metrics computed")

