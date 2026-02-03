import geopandas as gpd
import pandas as pd
from pathlib import Path

RAW_GEO = Path("data/raw/geo/zcta_raw.geojson")
RAW_ACS = Path("data/raw/census/acs_zcta.parquet")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# Load data
zcta = gpd.read_file(RAW_GEO)
acs = pd.read_parquet(RAW_ACS)

# Load Delaware boundary
de = gpd.read_file(
    "https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip"
)
de = de[de["STUSPS"] == "DE"].to_crs(zcta.crs)

# Spatial filter
zcta_de = zcta[zcta.intersects(de.unary_union)]

# Join census data
df = zcta_de.merge(acs, on="zcta", how="left")

df.to_parquet(OUT / "zcta_de.parquet", index=False)
df.to_file(OUT / "zcta_de.geojson", driver="GeoJSON")

print(f"Delaware ZCTAs: {len(df)}")

