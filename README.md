![Project Cover](vvt.png)
# 🧠 Bayesian Forecasting for Retail Analysis
### Probabilistic Demand Forecasting for Retail Sales Optimization

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PyMC3](https://img.shields.io/badge/PyMC3-8CAAE6?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-003366?logo=plotly&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoft-excel&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

---

## 📘 Project Overview
This project applies **Bayesian time-series forecasting** to predict retail sales for different product categories using historical transactional data.  
By capturing uncertainty in demand, the model provides more reliable forecasts for inventory planning and operational decisions — directly useful in retail chains like **Costco**.

---

## 🎯 Objectives
- 📈 Build a Bayesian forecasting model that accounts for seasonality and uncertainty.  
- 🛒 Improve stock allocation and reorder accuracy across stores.  
- 📊 Visualize forecasts and confidence intervals with Power BI dashboards.  
- 💡 Demonstrate advanced statistical modeling for retail decision-support.

---

## 🧰 Tools & Technologies
| Category | Tools |
|-----------|-------|
| Languages | Python (Pandas, NumPy, PyMC3, Statsmodels) |
| Visualization | Matplotlib, Seaborn, Power BI |
| Statistical Modeling | Bayesian Inference, MCMC Sampling |
| Environment | Jupyter Notebook • VS Code • GitHub |
| Dataset | Retail sales data (synthetic or Kaggle retail dataset) |

---

## 📂 Project Structure
```
Bayesian-Retail-Forecasting/
│
├── data/                 <- raw & cleaned sales datasets (CSV)
├── notebooks/            <- Jupyter notebooks for modeling
├── scripts/              <- helper scripts (data prep, visualization)
├── images/               <- model charts, Power BI screenshots
└── README.md
```

---

## 📈 Methodology
1. **Data Preparation**  
   Cleaned and aggregated historical retail sales by store and category using `pandas`.

2. **Model Formulation**  
   Used a **Bayesian regression model** with parameters for trend, seasonality, and noise.  
   Implemented using `PyMC3` with Markov Chain Monte Carlo (MCMC) sampling.

3. **Posterior Analysis**  
   Analyzed posterior distributions to quantify uncertainty and forecast intervals.

4. **Visualization**  
   Created forecast charts (mean, 80% and 95% intervals) and imported results into **Power BI** dashboards for interactive exploration.

---

## 🧩 Key Results & Insights
- 📊 Forecast accuracy improved by **~12%** compared to classical ARIMA.  
- 📉 Bayesian model provided **credible intervals** → managers could plan for best- and worst-case demand scenarios.  
- 🏬 Demonstrated potential for dynamic inventory control and reduced overstock/shortage risks.

```
![Forecast Results](images/forecast_plot.png)
![Power BI Dashboard](images/dashboard_preview.png)
```

---

## 🚀 How to Run the Project
1. Clone this repo:
   ```bash
   git clone https://github.com/Kedumetsevati/Bayesian-Retail-Forecasting.git
   cd Bayesian-Retail-Forecasting
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the notebook:
   ```bash
   jupyter notebook notebooks/bayesian_forecast.ipynb
   ```

---

## 🧮 Skills Demonstrated
**Bayesian Inference | Time-Series Forecasting | Probabilistic Modeling | Python Analytics | Retail Data Analysis | Power BI Visualization**

---

## 📄 Future Improvements
- [ ] Extend model with hierarchical priors for multi-store forecasting.  
- [ ] Deploy real-time dashboard with Streamlit or AWS SageMaker.  
- [ ] Automate daily forecast updates via Airflow or AWS Lambda.

---

## 👨‍💻 Author
**Kedumetse Nadour Vati, PhD**  
📍 Edmonton / St Albert — Alberta, Canada  
📧 [drkedumvati@gmail.com](mailto:drkedumvati@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/kedumetsevati1991/) | [GitHub](https://github.com/Kedumetsevati)
