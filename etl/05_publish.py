import json
import pandas as pd
import geopandas as gpd
from pathlib import Path
from datetime import datetime

OUT = Path("data/published")
OUT.mkdir(parents=True, exist_ok=True)

metrics = pd.read_parquet("data/processed/metrics.parquet")
geo = gpd.read_file("data/processed/zcta_de.geojson")

# Slim geometry for web
geo["geometry"] = geo["geometry"].simplify(tolerance=0.001)

# Write metrics.json
metrics_out = metrics.to_dict(orient="records")
with open(OUT / "metrics.json", "w") as f:
    json.dump(metrics_out, f)

# Write geojson
geo[["zcta", "geometry"]].to_file(
    OUT / "zcta.geojson", driver="GeoJSON"
)

# Metadata
metadata = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "sources": {
        "income_rent": "US Census ACS 5-Year (2022)",
        "geography": "TIGER/Line ZCTA"
    },
    "metric_definition": "Median gross rent / (median household income / 12)"
}

with open(OUT / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Published static artifacts")

