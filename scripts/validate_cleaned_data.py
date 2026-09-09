import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "SCMS_Delivery_History_Cleaned.csv"

df = pd.read_csv(file_path)

print("Cleaned dataset shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nDate range:")
print("Scheduled Delivery:",
      df["Scheduled Delivery Date"].min(),
      "to",
      df["Scheduled Delivery Date"].max())

print("Delivered to Client:",
      df["Delivered to Client Date"].min(),
      "to",
      df["Delivered to Client Date"].max())

print("\nDelivery Delay statistics:")
print(df["Delivery Delay Days"].describe())

print("\nOn-time delivery:")
print(df["On Time Delivery"].value_counts())

print("\nFreight Cost per KG:")
print(df["Freight Cost per KG"].describe())

print("\nCost per Unit:")
print(df["Cost per Unit"].describe())

print("\nRemaining missing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())