import os
from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

DATA_DIR = "UC"
LIV_FILE = "Livability_Scores.csv"
HOUSE_FILE = "DMV_House_Price_Data.csv"

def ensure_output_dir(path: str = DATA_DIR) -> None:
    os.makedirs(path, exist_ok=True)

def load_and_merge(liv_path: str = LIV_FILE,
                   house_path: str = HOUSE_FILE) -> pd.DataFrame:
    liv_df = pd.read_csv(liv_path)
    house_df = pd.read_csv(house_path)

    merged_df = pd.merge(
        house_df[["ZipCode", "City", "State", "MedianPrice"]],
        liv_df[["ZipCode", "Livability_Score"]],
        on="ZipCode",
        how="inner",
    )
    return merged_df


def fit_model_and_add_residuals(df: pd.DataFrame) -> Tuple[pd.DataFrame, LinearRegression]:
    model = LinearRegression()
    X = df[["Livability_Score"]]
    y = df["MedianPrice"]
    model.fit(X, y)

    df = df.copy()
    df["PredictedPrice"] = model.predict(X)
    df["Residual"] = df["MedianPrice"] - df["PredictedPrice"]
    return df, model

def save_full_sorted_tables(df: pd.DataFrame, out_dir: str = DATA_DIR) -> None:
    df_sorted_low = df.sort_values(by="Residual", ascending=True)
    df_sorted_low.to_csv(os.path.join(out_dir, "all_zip_low_to_high.csv"), index=False)
    df_sorted_high = df.sort_values(by="Residual", ascending=False)
    df_sorted_high.to_csv(os.path.join(out_dir, "all_zip_high_to_low.csv"), index=False)


def plot_price_vs_livability(df: pd.DataFrame,
                             model: LinearRegression,
                             out_dir: str = DATA_DIR) -> None:
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Livability_Score"], df["MedianPrice"], alpha=0.6)
    x_vals = np.linspace(df["Livability_Score"].min(),
                         df["Livability_Score"].max(), 100).reshape(-1, 1)
    y_vals = model.predict(pd.DataFrame(x_vals, columns=["Livability_Score"]))
    plt.plot(x_vals, y_vals)
    plt.title("Livability Score vs Median House Price")
    plt.xlabel("Livability Score")
    plt.ylabel("Median Price ($)")
    plt.grid(True)
    out_path = os.path.join(out_dir, "price_vs_livability.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def plot_residual_distribution(df: pd.DataFrame,
                               out_dir: str = DATA_DIR) -> None:
    plt.figure(figsize=(10, 6))
    plt.hist(df["Residual"], bins=30)
    plt.title("Distribution of Residuals (Actual - Predicted)")
    plt.xlabel("Residual (USD)")
    plt.ylabel("Count")
    plt.grid(True)
    out_path = os.path.join(out_dir, "residual_distribution.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def plot_residual_housing_matrix(df: pd.DataFrame,
                                 out_dir: str = DATA_DIR) -> None:
    plt.figure(figsize=(12, 8))
    colors = df["Residual"].apply(lambda x: "green" if x < 0 else "red")
    plt.scatter(
        df["MedianPrice"],
        df["Livability_Score"],
        c=colors,
        alpha=0.75,
        s=70,
        edgecolor="black",
        linewidth=0.3,
    )

    price_mid = df["MedianPrice"].median()
    liv_mid = df["Livability_Score"].median()

    plt.axvline(price_mid, color="gray", linestyle="--", linewidth=1)
    plt.axhline(liv_mid, color="gray", linestyle="--", linewidth=1)

    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()

    plt.text(
        xmin - (xmax - xmin) * 0.10,
        ymax + (ymax - ymin) * 0.05,
        "HIDDEN GEMS\nLow Price × High Livability",
        fontsize=13,
        color="green",
        ha="left",
        va="bottom",
    )

    plt.text(
        xmax + (xmax - xmin) * 0.10,
        ymax + (ymax - ymin) * 0.05,
        "LUXURY\nHigh Price × High Livability",
        fontsize=13,
        color="blue",
        ha="right",
        va="bottom",
    )

    plt.text(
        xmin - (xmax - xmin) * 0.10,
        ymin - (ymax - ymin) * 0.05,
        "ECONOMY\nLow Price × Low Livability",
        fontsize=13,
        color="orange",
        ha="left",
        va="top",
    )

    plt.text(
        xmax + (xmax - xmin) * 0.10,
        ymin - (ymax - ymin) * 0.05,
        "OVERPRICED\nHigh Price × Low Livability",
        fontsize=13,
        color="red",
        ha="right",
        va="top",
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="Undervalued (Residual < 0)",
            markerfacecolor="green",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="Overpriced (Residual > 0)",
            markerfacecolor="red",
            markersize=10,
        ),
    ]

    plt.legend(
        handles=legend_elements,
        title="Market Mispricing",
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="black",
    )

    plt.title("Strategic Housing Matrix (Residual-Based)")
    plt.xlabel("Median Price ($)")
    plt.ylabel("Livability Score")
    plt.grid(True, linestyle="--", alpha=0.3)

    out_path = os.path.join(out_dir, "housing_matrix_residual_based.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


def main() -> None:
    ensure_output_dir(DATA_DIR)
    merged_df = load_and_merge()
    merged_df, model = fit_model_and_add_residuals(merged_df)

    save_full_sorted_tables(merged_df, DATA_DIR)
    plot_price_vs_livability(merged_df, model, DATA_DIR)
    plot_residual_distribution(merged_df, DATA_DIR)
    plot_residual_housing_matrix(merged_df, DATA_DIR)

if __name__ == "__main__":
    main()
