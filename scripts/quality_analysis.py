import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "SCMS_Delivery_History_Cleaned.csv"

df = pd.read_csv(file_path)

# Convert date columns
date_columns = [
    "Scheduled Delivery Date",
    "Delivered to Client Date",
    "Delivery Recorded Date",
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")



# --------------------------------------------------
# 1. Delivery performance
# --------------------------------------------------

print("=" * 60)
print("DELIVERY PERFORMANCE")
print("=" * 60)

print("\nOn-time delivery:")
print(df["On Time Delivery"].value_counts())

print("\nOn-time delivery percentage:")
print(
    df["On Time Delivery"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)



# --------------------------------------------------
# 2. Delay analysis
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY DELAY ANALYSIS")
print("=" * 60)

print(df["Delivery Delay Days"].describe())

print("\nMost delayed shipments:")

print(
    df[
        [
            "ID",
            "Country",
            "Vendor",
            "Shipment Mode",
            "Scheduled Delivery Date",
            "Delivered to Client Date",
            "Delivery Delay Days",
        ]
    ]
    .sort_values("Delivery Delay Days", ascending=False)
    .head(10)
)



# --------------------------------------------------
# 2. Delay analysis
# --------------------------------------------------

print("\n" + "=" * 60)
print("NUMERIC DATA QUALITY CHECK")
print("=" * 60)

print(
    "\nZero Line Item Quantity:",
    (df["Line Item Quantity"] == 0).sum()
)

print(
    "Zero Line Item Value:",
    (df["Line Item Value"] == 0).sum()
)

print(
    "Zero Unit Price:",
    (df["Unit Price"] == 0).sum()
)

print(
    "Zero Weight:",
    (df["Weight (Kilograms)"] == 0).sum()
)

print(
    "Zero Freight Cost:",
    (df["Freight Cost (USD)"] == 0).sum()
)


# --------------------------------------------------
# 4. Freight cost outliers
# --------------------------------------------------

print("\n" + "=" * 60)
print("FREIGHT COST OUTLIERS")
print("=" * 60)

print(
    df[
        [
            "ID",
            "Country",
            "Shipment Mode",
            "Weight (Kilograms)",
            "Freight Cost (USD)",
            "Freight Cost per KG",
        ]
    ]
    .sort_values("Freight Cost per KG", ascending=False)
    .head(10)
)


# --------------------------------------------------
# 5. Cost per unit outliers
# --------------------------------------------------

print("\n" + "=" * 60)
print("COST PER UNIT OUTLIERS")
print("=" * 60)

print(
    df[
        [
            "ID",
            "Country",
            "Product Group",
            "Line Item Quantity",
            "Line Item Value",
            "Cost per Unit",
        ]
    ]
    .sort_values("Cost per Unit", ascending=False)
    .head(10)
)


# --------------------------------------------------
# 6. Missing-value summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUE SUMMARY")
print("=" * 60)

missing = df.isna().sum()

print(
    missing[missing > 0]
    .sort_values(ascending=False)
)



# --------------------------------------------------
# 7. Shipment mode performance
# --------------------------------------------------

print("\n" + "=" * 60)
print("SHIPMENT MODE PERFORMANCE")
print("=" * 60)

mode_analysis = (
    df.groupby("Shipment Mode")
    .agg(
        Shipments=("ID", "count"),
        Average_Delay_Days=("Delivery Delay Days", "mean"),
        On_Time_Rate=(
            "On Time Delivery",
            lambda x: (x == "Yes").mean() * 100,
        )
    )
    .round(2)
)

print(mode_analysis)



# --------------------------------------------------
# 8. Country performance
# --------------------------------------------------

print("\n" + "=" * 60)
print("COUNTRY PERFORMANCE")
print("=" * 60)

country_analysis = (
    df.groupby("Country")
    .agg(
        Shipments=("ID", "count"),
        Average_Delay_Days=("Delivery Delay Days", "mean"),
        On_Time_Rate=(
            "On Time Delivery",
            lambda x: (x == "Yes").mean() * 100
        )
    )
    .sort_values("Shipments", ascending=False)
    .round(2)
)

print(country_analysis.head(15))