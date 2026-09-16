import pandas as pd

comparison = pd.DataFrame({
    "Model": ["Baseline (Mean Prediction)", "Random Forest"],
    "MAE (Days)": [14.5127, 10.9038],
    "RMSE (Days)": [28.5997, 24.2883],
    "R-Squared": [0.0000, 0.2788]
})

comparison.to_csv("week4_outputs/model_comparison.csv", index=False)

print(comparison)
print("\nModel comparison saved successfully.")
