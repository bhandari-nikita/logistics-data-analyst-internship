import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pred = pd.read_csv("week4_outputs/predictions.csv")
comparison = pd.read_csv("week4_outputs/model_comparison.csv")

actual = pred["Actual_Delay_Days"]
predicted = pred["Predicted_Delay_Days"]
residuals = actual - predicted

# 1. Actual vs Predicted
plt.figure(figsize=(9, 6))
plt.scatter(actual, predicted, alpha=0.35)
plt.axline((0, 0), slope=1, linestyle="--")
plt.xlabel("Actual Delay (Days)")
plt.ylabel("Predicted Delay (Days)")
plt.title("Actual vs Predicted Delivery Delay")
plt.tight_layout()
plt.savefig("week4_outputs/01_actual_vs_predicted.png", dpi=200)
plt.close()

# 2. Residual distribution
plt.figure(figsize=(9, 6))
plt.hist(residuals, bins=40, edgecolor="black")
plt.axvline(0, linestyle="--")
plt.xlabel("Prediction Error (Actual - Predicted Days)")
plt.ylabel("Number of Shipments")
plt.title("Distribution of Prediction Errors")
plt.tight_layout()
plt.savefig("week4_outputs/02_prediction_error_distribution.png", dpi=200)
plt.close()

# 3. Model comparison
x = np.arange(len(comparison))
width = 0.35

plt.figure(figsize=(9, 6))
plt.bar(x - width/2, comparison["MAE (Days)"], width, label="MAE")
plt.bar(x + width/2, comparison["RMSE (Days)"], width, label="RMSE")
plt.xticks(x, comparison["Model"], rotation=10)
plt.ylabel("Error (Days)")
plt.title("Baseline vs Random Forest Model Performance")
plt.legend()
plt.tight_layout()
plt.savefig("week4_outputs/03_model_comparison.png", dpi=200)
plt.close()

print("3 Week 4 visualizations created successfully.")
