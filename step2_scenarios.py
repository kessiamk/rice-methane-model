# STEP 2: compare scenarios in a table and a chart.
# In Colab, run the ch4_core.py cell first, then this one.
import pandas as pd
import matplotlib.pyplot as plt

region = "south_asia"
scenarios = [
    ("Flooded", "continuous_flood", "nonflooded_lt180d", {}),
    ("AWD", "multiple_drainage", "nonflooded_lt180d", {}),
    ("Flooded + straw 5 t/ha (<30 d)", "continuous_flood", "nonflooded_lt180d", {"straw_lt30d": 5}),
    ("AWD + straw 5 t/ha (<30 d)", "multiple_drainage", "nonflooded_lt180d", {"straw_lt30d": 5}),
]

rows = []
for name, water, pre, amend in scenarios:
    rows.append({"Scenario": name,
                 "CH4 (kg/ha/season)": round(season_ch4_per_ha(region, water, pre, amend), 1)})
table = pd.DataFrame(rows)
base = table["CH4 (kg/ha/season)"][0]
table["Change vs flooded (%)"] = ((table["CH4 (kg/ha/season)"] / base - 1) * 100).round(0)
print(table.to_string(index=False))

colours = ["#4C72B0", "#55A868", "#C44E52", "#DD8452"]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(table["Scenario"], table["CH4 (kg/ha/season)"], color=colours)
ax.set_ylabel("Methane emitted (kg CH4 per hectare per season)")
ax.set_title("Estimated methane from one rice crop, South Asia (IPCC 2019 Tier 1)")
plt.xticks(rotation=20, ha="right")
ax.legend(bars, table["Scenario"], title="Management scenario", loc="upper left")
plt.tight_layout()
plt.savefig("scenarios.png", dpi=150)
plt.show()
