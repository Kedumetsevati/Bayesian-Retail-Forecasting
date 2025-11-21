import numpy as np, pandas as pd, math
import matplotlib.pyplot as plt

# === 1) Generate 36 months of synthetic data ===
np.random.seed(7)
months = pd.date_range(start="2022-01-01", periods=36, freq="MS")
t = np.arange(1, len(months)+1)
promo = ((months.month >= 10) | (months.month <= 2)).astype(int)

beta0_true, beta1_true, beta2_true, sigma_true = 20000.0, 350.0, 1500.0, 3500.0
y = beta0_true + beta1_true*t + beta2_true*promo + np.random.normal(0, sigma_true, size=len(t))
df = pd.DataFrame({"Date": months, "t": t, "Promo": promo, "Revenue": y})

# === 2) Conjugate Bayesian Posterior ===
X = np.column_stack([np.ones_like(t), t, promo])
y_vec = y.reshape(-1, 1)

m0 = np.array([[0.0],[0.0],[0.0]])
V0 = np.diag([1e6,1e6,1e6]).astype(float)
a0, b0 = 2.0, (5000.0**2)
XtX, Xty = X.T @ X, X.T @ y_vec
V0_inv = np.linalg.inv(V0)
Vn_inv = V0_inv + XtX
Vn = np.linalg.inv(Vn_inv)
mn = Vn @ (V0_inv @ m0 + Xty)
an = a0 + len(t)/2.0
resid0 = y_vec - X @ m0
bn = float((b0 + 0.5*(resid0.T @ resid0 + (m0.T @ V0_inv @ m0) - (mn.T @ Vn_inv @ mn))).squeeze())

S = 4000
sigma2_samples = 1.0 / np.random.gamma(shape=an, scale=1.0/bn, size=S)
beta_samples = np.empty((S, 3))
L = np.linalg.cholesky(Vn)
for s in range(S):
    z = np.random.normal(size=(3,1))
    beta_samples[s,:] = (mn + math.sqrt(sigma2_samples[s])*(L @ z)).flatten()

beta_mean = beta_samples.mean(axis=0)
y_fit = (X @ beta_mean.reshape(-1,1)).flatten()

# === 3) Historical Fit Plot ===
plt.figure()
plt.plot(df["Date"], df["Revenue"], marker="o", label="Observed")
plt.plot(df["Date"], y_fit, linestyle="--", label="Posterior Mean Fit")
plt.legend()
plt.title("Historical Revenue and Posterior Mean Fit")
plt.xlabel("Month"); plt.ylabel("Revenue")
plt.savefig("bayes_forecast_plot1_history.png", bbox_inches="tight")
plt.close()

# === 4) Forecast Next 6 Months ===
future_h = 6
t_future = np.arange(t[-1]+1, t[-1]+future_h+1)
months_future = pd.date_range(start=months[-1] + pd.offsets.MonthBegin(), periods=future_h, freq="MS")
promo_future = np.where((months_future.month >= 10) | (months_future.month <= 2), 1, 0)
X_future = np.column_stack([np.ones_like(t_future), t_future, promo_future])

pred_draws = np.zeros((S, future_h))
for s in range(S):
    mu = X_future @ beta_samples[s,:].reshape(-1,1)
    pred_draws[s,:] = (mu.flatten() + np.random.normal(0, np.sqrt(sigma2_samples[s]), size=future_h))

pred_mean = pred_draws.mean(axis=0)
pred_lo = np.percentile(pred_draws, 2.5, axis=0)
pred_hi = np.percentile(pred_draws, 97.5, axis=0)
# ---- Save forecast table for Streamlit dashboard ----
import pandas as pd
import os

forecast_df = pd.DataFrame({
    "date": months_future,
    "product": "Total Revenue",          # or use real product name if you have multiple
    "yhat": pred_mean,
    "yhat_lower": pred_lo,
    "yhat_upper": pred_hi,
})

# ensure project data folder exists
os.makedirs("data", exist_ok=True)

forecast_path = os.path.join("data", "forecast_results.csv")
forecast_df.to_csv(forecast_path, index=False)

print("Saved forecast table to:", forecast_path)
print(forecast_df.head())

plt.figure()
plt.plot(df["Date"], df["Revenue"], marker="o", linestyle="-", label="Observed")
plt.plot(months_future, pred_mean, marker="o", linestyle="-", label="Forecast Mean")
plt.plot(months_future, pred_lo, linestyle="--", label="2.5%")
plt.plot(months_future, pred_hi, linestyle="--", label="97.5%")
plt.legend()
plt.title("Bayesian Forecast (Mean & 95% Credible Interval)")
plt.xlabel("Month"); plt.ylabel("Revenue")
plt.savefig("bayes_forecast_plot2_forecast.png", bbox_inches="tight")
plt.close()

print("✅ Charts saved:")
print("bayes_forecast_plot1_history.png")
print("bayes_forecast_plot2_forecast.png")

