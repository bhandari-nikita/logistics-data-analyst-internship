import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("data/SCMS_Delivery_History_Cleaned.csv")
TARGET = "Delivery Delay Days"
df = df.dropna(subset=[TARGET]).copy()

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

X = df[numeric_features + categorical_features]
y = df[TARGET]

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

pipeline.fit(X, y)

feature_names = pipeline.named_steps["preprocessing"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values("Importance", ascending=False)

importance_df.to_csv(
    "week4_outputs/feature_importance.csv",
    index=False
)

top = importance_df.head(15).sort_values("Importance")

plt.figure(figsize=(10, 7))
plt.barh(top["Feature"], top["Importance"])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Top 15 Features Used by Random Forest")
plt.tight_layout()
plt.savefig(
    "week4_outputs/04_feature_importance.png",
    dpi=200
)
plt.close()

print("Feature importance analysis completed.")
print("\nTop 10 features:")
print(importance_df.head(10).to_string(index=False))
