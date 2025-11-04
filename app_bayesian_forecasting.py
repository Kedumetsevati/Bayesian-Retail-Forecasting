# app_bayesian_forecasting.py
import streamlit as st
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Retail Forecast (Bayesian-style)", layout="wide")
st.title("Interactive Retail Forecasting (Bayesian-style)")

# ---------- Data loader (uses your file if present; otherwise generates) ----------
@st.cache_data
def load_or_make_data():
    try:
        df = pd.read_csv("bayesian_forecasting_advanced_data.csv", parse_dates=["Date"])
        # If file exists but missing columns, fall back to generate
        needed = {"Date", "t", "Promo", "Holiday", "PriceIndex", "Revenue"}
        if not needed.issubset(df.columns):
            raise ValueError("CSV missing columns.")
        return df
    except Exception:
        # generate 36 months with promo/holiday/price features
        np.random.seed(10)
        months = pd.date_range(start="2022-01-01", periods=36, freq="MS")
        t = np.arange(1, len(months)+1)
        promo = ((months.month >= 10) | (months.month <= 2)).astype(int)
        holiday = np.isin(months.month, [11, 12]).astype(int)
        price_index = 1.0 + 0.01*(t - t.mean()) + 0.03*np.sin(2*np.pi*t/12)

        # true dgp
        beta0, beta1, beta2, beta3, beta4 = 21000.0, 330.0, 1800.0, 2500.0, -4000.0
        sigma = 3600.0
        y = beta0 + beta1*t + beta2*promo + beta3*holiday + beta4*(price_index-1.0) + np.random.normal(0, sigma, size=len(t))

        df = pd.DataFrame({
            "Date": months,
            "t": t,
            "Promo": promo,
            "Holiday": holiday,
            "PriceIndex": price_index,
            "Revenue": y
        })
        return df

df = load_or_make_data()

# ---------- Sidebar controls ----------
st.sidebar.header("Scenario")
h = st.sidebar.slider("Forecast horizon (months)", 3, 12, 6)
price_step = st.sidebar.slider("Monthly price-index change (Δ)", -0.03, 0.05, 0.01, 0.01)
assume_promo = st.sidebar.checkbox("Assume promos Oct–Feb", True)
assume_holiday = st.sidebar.checkbox("Include holiday effect (Nov/Dec)", True)
B = st.sidebar.select_slider("Uncertainty draws (bootstrap)", options=[200, 500, 1000, 2000], value=1000)

st.sidebar.caption("Tip: increase draws for smoother intervals (slower).")

# ---------- Fit quick OLS on extended features ----------
X = np.column_stack([
    np.ones(len(df)),
    df["t"].values,
    df["Promo"].values,
    df["Holiday"].values,
    df["PriceIndex"].values - 1.0
])
y = df["Revenue"].values
beta_hat, *_ = np.linalg.lstsq(X, y, rcond=None)

# residual scale
y_hat = X @ beta_hat
resid = y - y_hat
sigma_hat = resid.std(ddof=X.shape[1])

# ---------- Build future scenario ----------
last_t = df["t"].values[-1]
t_future = np.arange(last_t+1, last_t+h+1)
months_future = pd.date_range(start=df["Date"].iloc[-1] + pd.offsets.MonthBegin(), periods=h, freq="MS")

promo_future = np.where((months_future.month >= 10) | (months_future.month <= 2), 1, 0) if assume_promo else np.zeros(h, dtype=int)
holiday_future = np.isin(months_future.month, [11, 12]).astype(int) if assume_holiday else np.zeros(h, dtype=int)

price_last = df["PriceIndex"].values[-1]
price_future = price_last + price_step*np.arange(1, h+1)

Xf = np.column_stack([
    np.ones(h),
    t_future,
    promo_future,
    holiday_future,
    price_future - 1.0
])

y_mean = Xf @ beta_hat

# ---------- Bootstrap predictive intervals ----------
rng = np.random.default_rng(1)
draws = y_mean + rng.normal(0, sigma_hat, size=(B, h))
lo = np.percentile(draws, 2.5, axis=0)
hi = np.percentile(draws, 97.5, axis=0)

# ---------- Plot ----------
st.subheader("Forecast")
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Revenue"], marker="o", linestyle="-", label="Observed")
ax.plot(months_future, y_mean, marker="o", linestyle="-", label="Forecast mean")
ax.plot(months_future, lo, linestyle="--", label="2.5%")
ax.plot(months_future, hi, linestyle="--", label="97.5%")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue"); ax.set_title("Interactive Forecast (OLS + Bootstrap)")
ax.legend()
st.pyplot(fig)

# ---------- Table + download ----------
out = pd.DataFrame({
    "Month": months_future,
    "Forecast_Mean": y_mean,
    "CI_2.5%": lo,
    "CI_97.5%": hi,
    "Promo": promo_future,
    "Holiday": holiday_future,
    "PriceIndex": price_future
})
st.subheader("Forecast Table")
st.dataframe(out, use_container_width=True)

csv_buf = StringIO()
out.to_csv(csv_buf, index=False)
st.download_button("Download forecast as CSV", data=csv_buf.getvalue(), file_name="forecast_table.csv", mime="text/csv")

st.caption("Model: OLS on (t, Promo, Holiday, PriceIndex) with bootstrap predictive intervals. For full Bayesian MCMC, run the PyMC notebook in this project.")

