import geopandas as gpd
from pathlib import Path

OUT = Path("data/raw/geo")
OUT.mkdir(parents=True, exist_ok=True)

URL = "https://www2.census.gov/geo/tiger/TIGER2022/ZCTA5/tl_2022_us_zcta520.zip"

print("Downloading ZCTA shapefile...")
gdf = gpd.read_file(URL)

# Keep only what we need
gdf = gdf[["ZCTA5CE20", "geometry"]]
gdf = gdf.rename(columns={"ZCTA5CE20": "zcta"})

gdf.to_file(OUT / "zcta_raw.geojson", driver="GeoJSON")

print(f"Saved {len(gdf)} ZCTAs")

