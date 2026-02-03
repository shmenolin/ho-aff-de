import requests
import pandas as pd
from pathlib import Path

OUT = Path("data/raw/census")
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://api.census.gov/data/2022/acs/acs5"

FIELDS = [
    "NAME",
    "B19013_001E",  # median household income
    "B25064_001E",  # median gross rent
    "B01003_001E",  # population
]

params = {
    "get": ",".join(FIELDS),
    "for": "zip code tabulation area:*"
}

print("Fetching ACS data...")
resp = requests.get(BASE, params=params, timeout=30)
resp.raise_for_status()

data = resp.json()
df = pd.DataFrame(data[1:], columns=data[0])

df.rename(columns={
    "zip code tabulation area": "zcta",
    "B19013_001E": "median_income",
    "B25064_001E": "median_rent",
    "B01003_001E": "population"
}, inplace=True)

# Convert to numeric safely
for col in ["median_income", "median_rent", "population"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.to_parquet(OUT / "acs_zcta.parquet", index=False)

print(f"Saved {len(df)} ZCTAs")
