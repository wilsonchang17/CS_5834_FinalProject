import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# -----------------------------
# Load raw source files
# -----------------------------
df_liv = pd.read_csv("Livability_Scores.csv")
df_hp  = pd.read_csv("DMV_House_Price_Data.csv")
df_yelp = pd.read_csv("DMV_Yelp_Dataset.csv")

# -----------------------------
# Merge all datasets
# -----------------------------
df = df_hp.merge(df_yelp, on="ZipCode", how="left")
df = df.merge(df_liv, on="ZipCode", how="left")

# -----------------------------
# Fix column naming: prioritize _x version
# -----------------------------
rename_map = {
    "City_x": "City",
    "State_x": "State",
    "MedianPrice_x": "MedianPrice",
    "Latitude_x": "Latitude",
    "Longitude_x": "Longitude",
    "NearestStation_x": "NearestStation",
    "MetroDistanceMeters_x": "MetroDistanceMeters",
    "DistanceToDC_Meters_x": "DistanceToDC_Meters",
    "Growth_1Y_x": "Growth_1Y",
    "Growth_3Y_x": "Growth_3Y",
    "Growth_5Y_x": "Growth_5Y",
    "Growth_10Y_x": "Growth_10Y",
    "Price_Volatility_x": "Price_Volatility"
}
df = df.rename(columns=rename_map)

# Drop unnecessary duplicated columns (_y)
df = df[[c for c in df.columns if not c.endswith("_y")]]

# -----------------------------
# Function to plot top/bottom
# -----------------------------
def plot_top_bottom(df_sorted, col, title, filename):
    top5 = df_sorted.head(5)
    bottom5 = df_sorted.tail(5)
    combined = pd.concat([top5, bottom5])
    colors = ["tomato"] * 5 + ["skyblue"] * 5

    plt.figure(figsize=(14, 7))
    plt.bar(combined["ZipCode"].astype(str), combined[col], color=colors, edgecolor="black")

    for i, v in enumerate(combined[col]):
        plt.text(i, v + 0.01, f"{v:.2f}", ha="center", fontsize=10)

    plt.title(title)
    plt.xlabel("ZipCode")
    plt.ylabel(col)
    plt.xticks(rotation=45)

    legend = [
        Patch(facecolor="tomato", edgecolor="black", label="Top 5"),
        Patch(facecolor="skyblue", edgecolor="black", label="Bottom 5")
    ]
    plt.legend(handles=legend)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# -----------------------------
# 5-Year Growth Ranking
# -----------------------------
df5 = df.dropna(subset=["Growth_5Y"])
df5_sorted = df5.sort_values("Growth_5Y", ascending=False)
df5_sorted.to_csv("Growth_5Y_Ranking.csv", index=False)

plot_top_bottom(df5_sorted, "Growth_5Y",
                "5-Year Growth — Top 5 vs Bottom 5",
                "Top5_Bottom5_5Y.png")

# -----------------------------
# 10-Year Growth Ranking
# -----------------------------
df10 = df.dropna(subset=["Growth_10Y"])
df10_sorted = df10.sort_values("Growth_10Y", ascending=False)
df10_sorted.to_csv("Growth_10Y_Ranking.csv", index=False)

plot_top_bottom(df10_sorted, "Growth_10Y",
                "10-Year Growth — Top 5 vs Bottom 5",
                "Top5_Bottom5_10Y.png")

print("Done! All ranking CSV and PNG charts exported.")
