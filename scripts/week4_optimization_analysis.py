import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("data/SCMS_Delivery_History_Cleaned.csv")
df = df.dropna(subset=["Delivery Delay Days"]).copy()

numeric_features = [
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Weight (Kilograms)",
    "Freight Cost (USD)",
    "Line Item Insurance (USD)",
]

categorical_features = [
    "Country",
    "Shipment Mode",
    "Product Group",
    "Sub Classification",
    "Vendor",
    "Manufacturing Site",
    "First Line Designation",
    "Managed By",
    "Fulfill Via",
    "Vendor INCO Term",
]

numeric_features = [c for c in numeric_features if c in df.columns]
categorical_features = [c for c in categorical_features if c in df.columns]

features = numeric_features + categorical_features

X = df[features]
y = df["Delivery Delay Days"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=True))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", model)
])

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)

optimization_df = X_test.copy()
optimization_df["Actual Delay Days"] = y_test.values
optimization_df["Predicted Delay Days"] = predictions

mode_summary = optimization_df.groupby("Shipment Mode").agg(
    Shipments=("Predicted Delay Days", "count"),
    Average_Actual_Delay=("Actual Delay Days", "mean"),
    Average_Predicted_Delay=("Predicted Delay Days", "mean"),
    Average_Freight_Cost=("Freight Cost (USD)", "mean")
).reset_index()

mode_summary["Prediction Gap"] = (
    mode_summary["Average_Actual_Delay"]
    - mode_summary["Average_Predicted_Delay"]
)

mode_summary = mode_summary.sort_values(
    "Average_Predicted_Delay",
    ascending=False
)

mode_summary.to_csv(
    "week4_outputs/shipment_mode_optimization.csv",
    index=False
)

print("=" * 70)
print("SHIPMENT MODE OPTIMIZATION ANALYSIS")
print("=" * 70)
print(mode_summary.to_string(index=False))

print("\nOptimization analysis saved successfully.")
