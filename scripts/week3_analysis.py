import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# WEEK 3 - ADVANCED DATA ANALYSIS & VISUALIZATION
# Logistics Data Analyst Internship
# ============================================================

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "SCMS_Delivery_History_Cleaned.csv"

output_dir = BASE_DIR / "week3_outputs"
output_dir.mkdir(exist_ok=True)


# ------------------------------------------------------------
# 2. Load cleaned dataset
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print("=" * 70)
print("WEEK 3 - ADVANCED LOGISTICS DATA ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 3. Basic dataset overview
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

print("\nNumber of records:", len(df))
print("Number of columns:", len(df.columns))

print("\nCountries:", df["Country"].nunique())
print("Vendors:", df["Vendor"].nunique())
print("Product Groups:", df["Product Group"].nunique())

print("\nShipment Modes:")
print(df["Shipment Mode"].value_counts(dropna=False))


# ------------------------------------------------------------
# 4. Descriptive statistics
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. DESCRIPTIVE STATISTICS")
print("=" * 70)

numeric_columns = [
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Weight (Kilograms)",
    "Freight Cost (USD)",
    "Freight Cost per KG",
    "Cost per Unit",
    "Delivery Delay Days"
]

available_numeric = [
    col for col in numeric_columns
    if col in df.columns
]

print("\nSummary statistics:")
print(df[available_numeric].describe().round(2))


# ------------------------------------------------------------
# 5. Overall logistics KPIs
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. KEY LOGISTICS KPIs")
print("=" * 70)

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

on_time_rate = (
    on_time_count / total_shipments * 100
)

average_delay = df["Delivery Delay Days"].mean()

average_freight = df["Freight Cost (USD)"].mean()

average_cost_per_unit = df["Cost per Unit"].mean()

total_quantity = df["Line Item Quantity"].sum()

total_value = df["Line Item Value"].sum()


print(f"\nTotal Shipments: {total_shipments:,}")
print(f"On-Time Shipments: {on_time_count:,}")
print(f"Delayed Shipments: {delayed_count:,}")
print(f"On-Time Delivery Rate: {on_time_rate:.2f}%")
print(f"Average Delivery Delay: {average_delay:.2f} days")
print(f"Average Freight Cost: ${average_freight:,.2f}")
print(f"Average Cost per Unit: ${average_cost_per_unit:,.2f}")
print(f"Total Shipment Quantity: {total_quantity:,.0f}")
print(f"Total Line Item Value: ${total_value:,.2f}")


# ------------------------------------------------------------
# 6. Delivery delay distribution
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. DELIVERY DELAY DISTRIBUTION")
print("=" * 70)

delay_stats = df["Delivery Delay Days"].describe()

print(delay_stats.round(2))

print("\nMedian delay:",
      df["Delivery Delay Days"].median())

print("90th percentile delay:",
      df["Delivery Delay Days"].quantile(0.90))

print("95th percentile delay:",
      df["Delivery Delay Days"].quantile(0.95))


# ------------------------------------------------------------
# 7. Shipment mode performance
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. SHIPMENT MODE PERFORMANCE")
print("=" * 70)

mode_analysis = (
    df.groupby("Shipment Mode")
    .agg(
        Shipments=("ID", "count"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100),
        Average_Freight_Cost=("Freight Cost (USD)", "mean"),
        Average_Freight_Cost_per_KG=("Freight Cost per KG", "mean")
    )
    .sort_values("Shipments", ascending=False)
)

print(
    mode_analysis.round(2)
)

mode_analysis.to_csv(
    output_dir / "shipment_mode_analysis.csv"
)


# ------------------------------------------------------------
# 8. Country performance
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. COUNTRY PERFORMANCE")
print("=" * 70)

country_analysis = (
    df.groupby("Country")
    .agg(
        Shipments=("ID", "count"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100),
        Average_Freight_Cost=("Freight Cost (USD)", "mean"),
        Average_Cost_per_Unit=("Cost per Unit", "mean")
    )
    .sort_values("Shipments", ascending=False)
)

print("\nTop 10 countries by shipment volume:")
print(country_analysis.head(10).round(2))

print("\nLowest 10 countries by on-time rate:")
print(
    country_analysis
    .sort_values("On_Time_Rate")
    .head(10)
    .round(2)
)

country_analysis.to_csv(
    output_dir / "country_analysis.csv"
)


# ------------------------------------------------------------
# 9. Product group analysis
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. PRODUCT GROUP ANALYSIS")
print("=" * 70)

product_analysis = (
    df.groupby("Product Group")
    .agg(
        Shipments=("ID", "count"),
        Total_Quantity=("Line Item Quantity", "sum"),
        Total_Value=("Line Item Value", "sum"),
        Average_Cost_per_Unit=("Cost per Unit", "mean"),
        Average_Freight_Cost=("Freight Cost (USD)", "mean"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100)
    )
    .sort_values("Shipments", ascending=False)
)

print(product_analysis.round(2))

product_analysis.to_csv(
    output_dir / "product_group_analysis.csv"
)


# ------------------------------------------------------------
# 10. Vendor performance
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. VENDOR PERFORMANCE")
print("=" * 70)

vendor_analysis = (
    df.groupby("Vendor")
    .agg(
        Shipments=("ID", "count"),
        Average_Delay=("Delivery Delay Days", "mean"),
        On_Time_Rate=("On Time Delivery",
                      lambda x: (x == "Yes").mean() * 100),
        Average_Freight_Cost=("Freight Cost (USD)", "mean")
    )
    .sort_values("Shipments", ascending=False)
)

print("\nTop 10 vendors by shipment volume:")
print(vendor_analysis.head(10).round(2))

vendor_analysis.to_csv(
    output_dir / "vendor_analysis.csv"
)


# ------------------------------------------------------------
# 11. Freight cost analysis
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. FREIGHT COST ANALYSIS")
print("=" * 70)

freight_analysis = (
    df.groupby("Shipment Mode")
    .agg(
        Shipments=("ID", "count"),
        Average_Freight_Cost=("Freight Cost (USD)", "mean"),
        Median_Freight_Cost=("Freight Cost (USD)", "median"),
        Average_Freight_Cost_per_KG=("Freight Cost per KG", "mean"),
        Median_Freight_Cost_per_KG=("Freight Cost per KG", "median")
    )
)

print(freight_analysis.round(2))

freight_analysis.to_csv(
    output_dir / "freight_analysis.csv"
)


# ------------------------------------------------------------
# 12. Freight outlier analysis
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. FREIGHT COST OUTLIERS")
print("=" * 70)

if "Freight Cost Outlier" in df.columns:

    outlier_count = (
        df["Freight Cost Outlier"]
        .eq("Potential Outlier")
        .sum()
    )

    print(
        "Potential freight-cost outliers:",
        outlier_count
    )

    print(
        "\nPercentage of records flagged:",
        round(outlier_count / len(df) * 100, 2),
        "%"
    )

    outliers = df[
        df["Freight Cost Outlier"]
        == "Potential Outlier"
    ].copy()

    outliers = outliers.sort_values(
        "Freight Cost per KG",
        ascending=False
    )

    print("\nTop 10 potential outliers:")

    columns_to_show = [
        "ID",
        "Country",
        "Shipment Mode",
        "Weight (Kilograms)",
        "Freight Cost (USD)",
        "Freight Cost per KG",
        "Freight Cost Outlier"
    ]

    available = [
        col for col in columns_to_show
        if col in outliers.columns
    ]

    print(
        outliers[available]
        .head(10)
        .to_string(index=False)
    )

    outliers.to_csv(
        output_dir / "freight_cost_outliers.csv",
        index=False
    )


# ------------------------------------------------------------
# 13. Correlation analysis
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. CORRELATION ANALYSIS")
print("=" * 70)

correlation_columns = [
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Weight (Kilograms)",
    "Freight Cost (USD)",
    "Freight Cost per KG",
    "Cost per Unit",
    "Delivery Delay Days"
]

available_corr = [
    col for col in correlation_columns
    if col in df.columns
]

correlation_matrix = (
    df[available_corr]
    .corr(numeric_only=True)
)

print(
    correlation_matrix.round(2)
)

correlation_matrix.to_csv(
    output_dir / "correlation_matrix.csv"
)


# ------------------------------------------------------------
# 14. Strongest correlations
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. STRONGEST NUMERICAL RELATIONSHIPS")
print("=" * 70)

corr_pairs = (
    correlation_matrix
    .where(
        np.triu(
            np.ones(
                correlation_matrix.shape
            ),
            k=1
        ).astype(bool)
    )
    .stack()
    .sort_values(
        key=abs,
        ascending=False
    )
)

print(
    corr_pairs.head(10).round(3)
)


# ------------------------------------------------------------
# 15. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("WEEK 3 INITIAL ANALYSIS COMPLETED")
print("=" * 70)

print("\nOutput files saved in:")
print(output_dir)

print("\nGenerated:")
print("- shipment_mode_analysis.csv")
print("- country_analysis.csv")
print("- product_group_analysis.csv")
print("- vendor_analysis.csv")
print("- freight_analysis.csv")
print("- freight_cost_outliers.csv")
print("- correlation_matrix.csv")

print("\nNext stage:")
print("Generate visualizations and interpret the findings.")