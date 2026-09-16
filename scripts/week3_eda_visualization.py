import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# WEEK 3: ADVANCED DATA ANALYSIS AND VISUALIZATION
# Logistics Data Analyst Internship
# ============================================================

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "SCMS_Delivery_History_Cleaned.csv"
output_dir = BASE_DIR / "reports" / "week3_visualizations"

output_dir.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load cleaned dataset
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print("=" * 60)
print("WEEK 3 - LOGISTICS EDA")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 3. Basic dataset overview
# ------------------------------------------------------------

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isna().sum().sort_values(ascending=False).head(10))


# ------------------------------------------------------------
# 4. Key performance metrics
# ------------------------------------------------------------

total_shipments = len(df)

on_time_count = (
    df["On Time Delivery"]
    .eq("Yes")
    .sum()
)

delayed_count = (
    df["On Time Delivery"]
    .eq("No")
    .sum()
)

on_time_percentage = (
    on_time_count / total_shipments * 100
)

average_delay = df["Delivery Delay Days"].mean()

total_value = df["Line Item Value"].sum()

average_freight = df["Freight Cost (USD)"].mean()

average_cost_per_unit = df["Cost per Unit"].mean()

print("\nKEY PERFORMANCE INDICATORS")
print("-" * 40)

print(f"Total shipments: {total_shipments:,}")
print(f"On-time shipments: {on_time_count:,}")
print(f"Delayed shipments: {delayed_count:,}")
print(f"On-time delivery rate: {on_time_percentage:.2f}%")
print(f"Average delivery delay: {average_delay:.2f} days")
print(f"Total line item value: ${total_value:,.2f}")
print(f"Average freight cost: ${average_freight:,.2f}")
print(f"Average cost per unit: ${average_cost_per_unit:.2f}")


# ------------------------------------------------------------
# 5. Shipment mode analysis
# ------------------------------------------------------------

shipment_mode_summary = (
    df.groupby("Shipment Mode")
    .agg(
        Shipments=("Shipment Mode", "size"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100),
        Average_Freight_Cost=("Freight Cost (USD)", "mean")
    )
    .sort_values("Shipments", ascending=False)
)

print("\nSHIPMENT MODE ANALYSIS")
print(shipment_mode_summary)


# ------------------------------------------------------------
# 6. Country analysis
# ------------------------------------------------------------

country_summary = (
    df.groupby("Country")
    .agg(
        Shipments=("Country", "size"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100),
        Average_Freight_Cost=("Freight Cost (USD)", "mean")
    )
    .sort_values("Shipments", ascending=False)
)

print("\nTOP 10 COUNTRIES BY SHIPMENT VOLUME")
print(country_summary.head(10))


# ------------------------------------------------------------
# 7. Visualization 1
# On-time vs delayed shipments
# ------------------------------------------------------------

delivery_counts = df["On Time Delivery"].value_counts()

plt.figure(figsize=(8, 5))
delivery_counts.plot(kind="bar")
plt.title("On-Time vs Delayed Shipments")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Shipments")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    output_dir / "01_on_time_vs_delayed.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 8. Visualization 2
# Shipment volume by mode
# ------------------------------------------------------------

mode_counts = df["Shipment Mode"].value_counts()

plt.figure(figsize=(8, 5))
mode_counts.plot(kind="bar")
plt.title("Shipment Volume by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("Number of Shipments")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    output_dir / "02_shipment_volume_by_mode.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 9. Visualization 3
# Delivery delay distribution
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))
df["Delivery Delay Days"].dropna().plot(
    kind="hist",
    bins=40
)

plt.title("Distribution of Delivery Delay Days")
plt.xlabel("Delivery Delay (Days)")
plt.ylabel("Number of Shipments")
plt.tight_layout()

plt.savefig(
    output_dir / "03_delivery_delay_distribution.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 10. Visualization 4
# Average delay by shipment mode
# ------------------------------------------------------------

mode_delay = (
    df.groupby("Shipment Mode")["Delivery Delay Days"]
    .mean()
    .sort_values()
)

plt.figure(figsize=(8, 5))
mode_delay.plot(kind="bar")

plt.title("Average Delivery Delay by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("Average Delay (Days)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    output_dir / "04_average_delay_by_mode.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 11. Visualization 5
# Average freight cost by shipment mode
# ------------------------------------------------------------

mode_freight = (
    df.groupby("Shipment Mode")["Freight Cost (USD)"]
    .mean()
    .sort_values()
)

plt.figure(figsize=(8, 5))
mode_freight.plot(kind="bar")

plt.title("Average Freight Cost by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("Average Freight Cost (USD)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    output_dir / "05_freight_cost_by_mode.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 12. Visualization 6
# Freight cost per KG distribution
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

df["Freight Cost per KG"].dropna().plot(
    kind="hist",
    bins=40
)

plt.title("Distribution of Freight Cost per KG")
plt.xlabel("Freight Cost per KG (USD)")
plt.ylabel("Number of Shipments")
plt.tight_layout()

plt.savefig(
    output_dir / "06_freight_cost_per_kg_distribution.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 13. Visualization 7
# Top 10 countries by shipment volume
# ------------------------------------------------------------

top_countries = (
    df["Country"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))
top_countries.plot(kind="barh")

plt.title("Top 10 Countries by Shipment Volume")
plt.xlabel("Number of Shipments")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig(
    output_dir / "07_top_10_countries.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 14. Visualization 8
# On-time delivery rate by shipment mode
# ------------------------------------------------------------

mode_on_time = (
    df.groupby("Shipment Mode")["On Time Delivery"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values()
)

plt.figure(figsize=(8, 5))
mode_on_time.plot(kind="bar")

plt.title("On-Time Delivery Rate by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("On-Time Delivery Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    output_dir / "08_on_time_rate_by_mode.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 15. Visualization 9
# Weight vs freight cost
# ------------------------------------------------------------

scatter_df = df[
    [
        "Weight (Kilograms)",
        "Freight Cost (USD)"
    ]
].dropna()

plt.figure(figsize=(9, 6))

plt.scatter(
    scatter_df["Weight (Kilograms)"],
    scatter_df["Freight Cost (USD)"],
    alpha=0.4
)

plt.title("Relationship Between Shipment Weight and Freight Cost")
plt.xlabel("Weight (Kilograms)")
plt.ylabel("Freight Cost (USD)")
plt.tight_layout()

plt.savefig(
    output_dir / "09_weight_vs_freight_cost.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 16. Visualization 10
# Shipment trend by year
# ------------------------------------------------------------

df["Scheduled Delivery Date"] = pd.to_datetime(
    df["Scheduled Delivery Date"],
    errors="coerce"
)

df["Year"] = (
    df["Scheduled Delivery Date"]
    .dt.year
)

yearly_shipments = (
    df["Year"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10, 5))
yearly_shipments.plot(kind="line", marker="o")

plt.title("Shipment Volume Trend by Year")
plt.xlabel("Year")
plt.ylabel("Number of Shipments")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    output_dir / "10_yearly_shipment_trend.png",
    dpi=200
)

plt.close()


# ------------------------------------------------------------
# 17. Correlation analysis
# ------------------------------------------------------------

correlation_columns = [
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Weight (Kilograms)",
    "Freight Cost (USD)",
    "Delivery Delay Days",
    "Freight Cost per KG",
    "Cost per Unit"
]

correlation_df = df[correlation_columns].corr()

print("\nCORRELATION MATRIX")
print(correlation_df.round(3))


# ------------------------------------------------------------
# 18. Save analytical summaries
# ------------------------------------------------------------

shipment_mode_summary.to_csv(
    output_dir / "shipment_mode_analysis.csv"
)

country_summary.head(20).to_csv(
    output_dir / "country_analysis_top20.csv"
)

correlation_df.to_csv(
    output_dir / "correlation_matrix.csv"
)


# ------------------------------------------------------------
# 19. Final message
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("WEEK 3 EDA COMPLETED")
print("=" * 60)

print("\nVisualizations saved in:")
print(output_dir)

print("\nFiles created:")
for file in sorted(output_dir.iterdir()):
    print("-", file.name)