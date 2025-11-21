import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Bayesian Retail Forecasting",
    layout="wide"
)

# ---------- CUSTOM CSS FOR DARK "WOLF" THEME ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #05070A;
        color: #E4E4E7;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    .kpi-card {
        padding: 16px 20px;
        border-radius: 10px;
        background: #10141C;
        border: 1px solid #1C2230;
        box-shadow: 0 0 18px rgba(0,0,0,0.7);
    }

    .kpi-label {
        font-size: 0.8rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F4B400;
    }

    .kpi-sub {
        font-size: 0.85rem;
        color: #60A5FA;
    }

    h1, h2, h3 {
        color: #F9FAFB;
    }

    .small-muted {
        color: #9CA3AF;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/forecast_results.csv", parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"]).dt.to_pydatetime()
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("⚙️ Controls")

series_options = ["All"] + sorted(df["product"].unique().tolist())
selected_product = st.sidebar.selectbox("Series", series_options)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# date_input can return single date or tuple
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
)

if selected_product != "All":
    mask &= (df["product"] == selected_product)

df_filtered = df[mask].copy()

# ---------- HEADER ----------
st.markdown("### Wolf of Wall Street Style Dashboard")

st.markdown(
    """
    <h1 style="margin-bottom:0.1rem;">Bayesian Retail Demand Forecasting</h1>
    <p class="small-muted">
        Uncertainty-aware forecasts for smarter inventory and revenue decisions (Bayesian model with 95% credible intervals).
    </p>
    """,
    unsafe_allow_html=True
)

# ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)

if not df_filtered.empty:
    total_forecast = df_filtered["yhat"].sum()
    avg_interval_width = (df_filtered["yhat_upper"] - df_filtered["yhat_lower"]).mean()
    total_upside = df_filtered["yhat_upper"].sum()
    total_downside = df_filtered["yhat_lower"].sum()
else:
    total_forecast = avg_interval_width = total_upside = total_downside = 0

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Forecasted Demand</div>
            <div class="kpi-value">{total_forecast:,.0f}</div>
            <div class="kpi-sub">Units in selected window</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg 95% Interval Width</div>
            <div class="kpi-value">{avg_interval_width:,.1f}</div>
            <div class="kpi-sub">Uncertainty per period</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Upside (95% Upper)</div>
            <div class="kpi-value">{total_upside:,.0f}</div>
            <div class="kpi-sub">High-demand scenario</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Downside (95% Lower)</div>
            <div class="kpi-value">{total_downside:,.0f}</div>
            <div class="kpi-sub">Low-demand scenario</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------- MAIN CHARTS ----------
left_col, right_col = st.columns((2.3, 1.7))

with left_col:
    st.subheader("Forecast with 95% Credible Interval")

    if df_filtered.empty:
        st.warning("No data for this selection.")
    else:
        # Shaded credible interval + forecast mean
        fig = go.Figure()

        # Upper band (plotted first)
        fig.add_trace(go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["yhat_upper"],
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            name="Upper 95%"
        ))

        # Lower band with fill to previous trace
        fig.add_trace(go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["yhat_lower"],
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(96,165,250,0.25)",  # soft blue
            hoverinfo="skip",
            showlegend=False,
            name="Lower 95%"
        ))

        # Mean forecast line
        fig.add_trace(go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["yhat"],
            line=dict(width=2),
            name="Forecast mean"
        ))

        fig.update_layout(
            title="Expected Demand Forecast with 95% Credible Interval",
            paper_bgcolor="#05070A",
            plot_bgcolor="#05070A",
            font=dict(color="#E4E4E7"),
            title_font=dict(color="#F9FAFB", size=16),
            xaxis=dict(gridcolor="#1C2230"),
            yaxis=dict(gridcolor="#1C2230"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Daily Interval Width")

    if df_filtered.empty:
        st.info("Adjust filters to view interval width.")
    else:
        df_filtered["interval_width"] = df_filtered["yhat_upper"] - df_filtered["yhat_lower"]
        fig2 = px.bar(
            df_filtered,
            x="date",
            y="interval_width",
            title="Uncertainty Over Time",
        )
        fig2.update_layout(
            paper_bgcolor="#05070A",
            plot_bgcolor="#05070A",
            font=dict(color="#E4E4E7"),
            title_font=dict(color="#F9FAFB", size=16),
            xaxis=dict(gridcolor="#1C2230"),
            yaxis=dict(gridcolor="#1C2230"),
        )
        st.plotly_chart(fig2, use_container_width=True)

# ---------- TABLE + DOWNLOAD + INSIGHT ----------
st.markdown("### Recommended Order Range")

if df_filtered.empty:
    st.info("No data to show recommendations.")
else:
    rec_df = df_filtered[["date", "product", "yhat_lower", "yhat", "yhat_upper"]].copy()
    rec_df.rename(
        columns={
            "date": "Date",
            "product": "Series",
            "yhat_lower": "Order Min (95%)",
            "yhat": "Expected Order",
            "yhat_upper": "Order Max (95%)",
        },
        inplace=True
    )

    st.dataframe(rec_df.tail(30), use_container_width=True)

    # Download button (C)
    csv_data = rec_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download forecast recommendations (CSV)",
        data=csv_data,
        file_name="bayesian_forecast_recommendations.csv",
        mime="text/csv",
    )

    st.markdown("#### Insight")

    total_min = rec_df["Order Min (95%)"].sum()
    total_exp = rec_df["Expected Order"].sum()
    total_max = rec_df["Order Max (95%)"].sum()

    insight_text = (
        f"For **{selected_product if selected_product != 'All' else 'the selected series'}** "
        f"in this date range, expected demand is about **{total_exp:,.0f} units**, "
        f"with a 95% credible range from **{total_min:,.0f}** to **{total_max:,.0f}** units. "
        "Ordering closer to the upper bound reduces stockout risk, while ordering closer to the "
        "lower bound limits overstock. The shaded band in the chart visualizes this trade-off."
    )
    st.markdown(insight_text)

