import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "SCMS_Delivery_History_Raw_Data.xlsx"
output_file = BASE_DIR / "data" / "SCMS_Delivery_History_Cleaned.csv"


# --------------------------------------------------
# 2. Load raw dataset
# --------------------------------------------------

df = pd.read_excel(input_file)

print("Original dataset shape:", df.shape)


# --------------------------------------------------
# 3. Clean column names
# --------------------------------------------------

# Remove BOM/encoding issue from ID column
df.columns = (
    df.columns
    .str.replace("Ã¯Â»Â¿", "", regex=False)
    .str.strip()
)

print("\nCleaned column names:")
print(df.columns.tolist())


# --------------------------------------------------
# 4. Check duplicate records
# --------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate rows:", duplicates)

if duplicates > 0:
    df = df.drop_duplicates()


# --------------------------------------------------
# 5. Standardize missing values
# --------------------------------------------------

df = df.replace(
    ["", " ", "NA", "N/A", "NaN", "NULL", "null"],
    np.nan
)


# --------------------------------------------------
# 6. Handle Shipment Mode
# --------------------------------------------------

print("\nMissing Shipment Mode before:",
      df["Shipment Mode"].isna().sum())

df["Shipment Mode"] = df["Shipment Mode"].fillna("Unknown")


# --------------------------------------------------
# 7. Handle Dosage
# --------------------------------------------------

print("Missing Dosage before:",
      df["Dosage"].isna().sum())

df["Dosage"] = df["Dosage"].fillna("Unknown")


# --------------------------------------------------
# 8. Convert numeric columns
# --------------------------------------------------

numeric_columns = [
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Line Item Insurance (USD)"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# 9. Clean Weight
# --------------------------------------------------

df["Weight (Kilograms)"] = pd.to_numeric(
    df["Weight (Kilograms)"],
    errors="coerce"
)


# --------------------------------------------------
# 10. Clean Freight Cost
# --------------------------------------------------

df["Freight Cost (USD)"] = pd.to_numeric(
    df["Freight Cost (USD)"],
    errors="coerce"
)


# --------------------------------------------------
# 11. Convert date columns
# --------------------------------------------------

date_columns = [
    "PQ First Sent to Client Date",
    "PO Sent to Vendor Date",
    "Scheduled Delivery Date",
    "Delivered to Client Date",
    "Delivery Recorded Date"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# 12. Create delivery delay metric
# --------------------------------------------------

df["Delivery Delay Days"] = (
    df["Delivered to Client Date"]
    - df["Scheduled Delivery Date"]
).dt.days


# --------------------------------------------------
# 13. Create on-time delivery flag
# --------------------------------------------------

df["On Time Delivery"] = np.where(
    df["Delivery Delay Days"] <= 0,
    "Yes",
    "No"
)


# --------------------------------------------------
# 14. Create freight cost per kg
# --------------------------------------------------

df["Freight Cost per KG"] = np.where(
    df["Weight (Kilograms)"] > 0,
    df["Freight Cost (USD)"] /
    df["Weight (Kilograms)"],
    np.nan
)



# --------------------------------------------------
# 15. Flag potential freight cost outliers
# --------------------------------------------------

freight_q1 = df["Freight Cost per KG"].quantile(0.25)
freight_q3 = df["Freight Cost per KG"].quantile(0.75)

freight_iqr = freight_q3 - freight_q1

freight_upper_limit = freight_q3 + (1.5 * freight_iqr)

df["Freight Cost Outlier"] = np.select(
    [
        df["Freight Cost per KG"].isna(),
        df["Freight Cost per KG"] > freight_upper_limit
    ],
    [
        "Not Available",
        "Potential Outlier"
    ],
    default="Normal"
)



# --------------------------------------------------
# 16. Create cost per unit
# --------------------------------------------------

df["Cost per Unit"] = np.where(
    df["Line Item Quantity"] > 0,
    df["Line Item Value"] /
    df["Line Item Quantity"],
    np.nan
)


# --------------------------------------------------
# 17. Remove useless metadata columns
# --------------------------------------------------

# These columns were added during the local data-loading
# process and are mostly empty in the dataset.

for column in ["Load_Date", "Source_System"]:
    if column in df.columns:
        df = df.drop(columns=column)



# --------------------------------------------------
# 18. Fix known text encoding issue
# --------------------------------------------------

df["Country"] = df["Country"].replace(
    {
        "CÃ_x0083_Â´te d'Ivoire": "Côte d'Ivoire"
    }
)



# --------------------------------------------------
# 19. Final validation
# --------------------------------------------------

print("\nFinal dataset shape:", df.shape)

print("\nRemaining missing values:")
print(df.isna().sum())

print("\nDuplicate rows after cleaning:",
      df.duplicated().sum())


# --------------------------------------------------
# 20. Save cleaned dataset
# --------------------------------------------------

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file)