import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# WEEK 4 - PREDICTIVE MODELING IN LOGISTICS
# ============================================================

print("=" * 60)
print("WEEK 4 - LOGISTICS PREDICTIVE MODELING")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

DATA_PATH = "data/SCMS_Delivery_History_Cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. DEFINE TARGET
# ------------------------------------------------------------

TARGET = "Delivery Delay Days"

df = df.dropna(subset=[TARGET]).copy()

print(f"\nTarget variable: {TARGET}")
print(f"Records available for modeling: {len(df):,}")


# ------------------------------------------------------------
# 3. SELECT PREDICTOR VARIABLES
# ------------------------------------------------------------
# These variables are selected as shipment characteristics.
# Delivery dates are intentionally excluded to avoid data leakage.

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

features = numeric_features + categorical_features

# Keep only columns that exist in the dataset
features = [col for col in features if col in df.columns]

X = df[features]
y = df[TARGET]


# ------------------------------------------------------------
# 4. TRAIN / TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ------------------------------------------------------------
# 5. PREPROCESSING
# ------------------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=True
        ))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ]
)


# ------------------------------------------------------------
# 6. RANDOM FOREST MODEL
# ------------------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)


# ------------------------------------------------------------
# 7. COMPLETE MODEL PIPELINE
# ------------------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", model)
    ]
)


# ------------------------------------------------------------
# 8. TRAIN MODEL
# ------------------------------------------------------------

print("\nTraining Random Forest model...")

pipeline.fit(X_train, y_train)

print("Model training completed.")


# ------------------------------------------------------------
# 9. MAKE PREDICTIONS
# ------------------------------------------------------------

y_pred = pipeline.predict(X_test)


# ------------------------------------------------------------
# 10. MODEL EVALUATION
# ------------------------------------------------------------

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"MAE  : {mae:.4f} days")
print(f"RMSE : {rmse:.4f} days")
print(f"R²   : {r2:.4f}")


# ------------------------------------------------------------
# 11. SAVE MODEL RESULTS
# ------------------------------------------------------------

results = pd.DataFrame({
    "Metric": [
        "Mean Absolute Error",
        "Root Mean Squared Error",
        "R-Squared"
    ],
    "Value": [
        mae,
        rmse,
        r2
    ]
})

results.to_csv(
    "week4_outputs/model_evaluation.csv",
    index=False
)


# ------------------------------------------------------------
# 12. SAVE ACTUAL VS PREDICTED VALUES
# ------------------------------------------------------------

prediction_results = pd.DataFrame({
    "Actual_Delay_Days": y_test.values,
    "Predicted_Delay_Days": y_pred
})

prediction_results.to_csv(
    "week4_outputs/predictions.csv",
    index=False
)


# ------------------------------------------------------------
# 13. SAVE SUMMARY
# ------------------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Training Records",
        "Testing Records",
        "Number of Features",
        "MAE (Days)",
        "RMSE (Days)",
        "R-Squared"
    ],
    "Value": [
        len(df),
        len(X_train),
        len(X_test),
        len(features),
        mae,
        rmse,
        r2
    ]
})

summary.to_csv(
    "week4_outputs/model_summary.csv",
    index=False
)


print("\nOutput files created:")
print("- week4_outputs/model_evaluation.csv")
print("- week4_outputs/predictions.csv")
print("- week4_outputs/model_summary.csv")

print("\n" + "=" * 60)
print("WEEK 4 PREDICTIVE MODELING COMPLETED")
print("=" * 60)