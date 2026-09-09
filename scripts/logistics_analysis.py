import pandas as pd

# Load raw logistics dataset
df = pd.read_excel("data/SCMS_Delivery_History_Raw_Data.xlsx")

# Basic dataset inspection
print("Dataset shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nUnique shipment modes:")
print(df["Shipment Mode"].value_counts(dropna=False))

print("\nUnique countries:", df["Country"].nunique())

print("\nUnique vendors:", df["Vendor"].nunique())

print("\nUnique product groups:", df["Product Group"].nunique())

print("\nShipment mode percentages:")
print(df["Shipment Mode"].value_counts(normalize=True, dropna=False) * 100)


print("\n\n--- Business Analysis Setup ---")

print("Total shipments:", len(df))
print("Total countries:", df["Country"].nunique())
print("Total vendors:", df["Vendor"].nunique())
print("Total product groups:", df["Product Group"].nunique())

print("\nShipment mode distribution:")
print(df["Shipment Mode"].value_counts(dropna=False))