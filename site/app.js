const map = L.map("map").setView([39.0, -75.5], 8);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

Promise.all([
  fetch("../data/published/latest/metrics.json").then(r => r.json()),
  fetch("../data/published/latest/zcta.geojson").then(r => r.json())
]).then(([metrics, geojson]) => {

  const metricMap = {};
  metrics.forEach(m => {
    metricMap[m.zcta] = m;
  });

  function getColor(category) {
    if (!category) return "#ccc";
    if (category === "Affordable") return "#2ca25f";
    if (category === "Cost Burdened") return "#feb24c";
    return "#de2d26";
  }

  L.geoJSON(geojson, {
    style: feature => {
      const m = metricMap[feature.properties.zcta];
      return {
        fillColor: getColor(m?.category),
        weight: 1,
        color: "white",
        fillOpacity: 0.7
      };
    },
    onEachFeature: (feature, layer) => {
      const m = metricMap[feature.properties.zcta];
      if (!m) return;

      layer.bindPopup(`
        <strong>ZCTA:</strong> ${m.zcta}<br/>
        <strong>Median Income:</strong> $${m.median_income}<br/>
        <strong>Median Rent:</strong> $${m.median_rent}<br/>
        <strong>Rent Burden:</strong> ${(m.rent_burden * 100).toFixed(1)}%
      `);
    }
  }).addTo(map);
});

