# 📊 MTN-H1-2025-Strategic-Analytics-Dashboard

An interactive **Streamlit dashboard** delivering **strategic,
financial, and operational insights** into **MTN Group's H1 2025
performance**.\
It covers **Executive KPIs, country deep-dives, fintech & data, Bayobab
infrastructure, pricing/FX, capex, regional analysis, and scenario
modeling** --- empowering **data-driven decision-making** across telecom
strategy.

------------------------------------------------------------------------

## ✨ Features

-   **Executive KPIs**\
    📌 Group-wide revenue, EBITDA, OCF, subscribers, data share, MoMo,
    etc.

-   **Country Deep-Dive**\
    📌 Per-country revenue growth, EBITDA margins, ARPU trends.

-   **Fintech & Data**\
    📌 MoMo, data subscribers, advanced services, and platform metrics.

-   **Regional Performance**\
    📌 Data growth trends across MTN's operating regions.

-   **Bayobab Infra**\
    📌 Insights on cross-border capacity, wholesale pricing, and fibre
    rollout.

-   **Pricing & FX**\
    📌 Country-level ARPU and FX sensitivity scenarios.

-   **Capex & Infra**\
    📌 H1 capex spend, FY guidance, and network rollout insights.

-   **Scenario Lab**\
    📌 Interactive sensitivity models (tariffs, traffic growth, fintech
    take rates).

-   **Data-driven Insights Report**\
    📌 Download a **full Word report** with structured insights.

------------------------------------------------------------------------

## 🗂 Dataset Sources

The dashboard loads structured CSVs from the `/data` folder:

-   `group_h1_2025_summary.csv` → Group-wide executive KPIs\
-   `country_h1_2025_kpis.csv` → Country-level KPIs\
-   `platform_metrics_h1_2025.csv` → Platform performance\
-   `regional_h1_2025.csv` → Regional breakdowns\
-   `bayobab_h1_2025.csv` → Infrastructure & wholesale metrics\
-   `fintech_h1_2025.csv` → Fintech & MoMo KPIs\
-   `pricing_fx_h1_2025.csv` → Pricing & FX scenarios\
-   `capex_h1_2025.csv` → Capex deployment

👉 Extendable: You can add more CSVs (e.g per-country capex, site
counts, 4G/5G rollouts).

------------------------------------------------------------------------

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/prodigy234/MTN-H1-2025-Strategic-Analytics-Dashboard.git
cd MTN-H1-2025-Strategic-Analytics-Dashboard
```

### 2️⃣ Create & activate virtual environment

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app

``` bash
streamlit run app.py
```

👉 The dashboard will open at `http://localhost:8501/`

------------------------------------------------------------------------

## 🌐 Deployment

This dashboard is **Streamlit-ready** for quick deployment.

1.  Push repo to GitHub.\

2.  Go to [Streamlit Cloud](https://share.streamlit.io).\

3.  Deploy directly by linking your repo.\


------------------------------------------------------------------------

## 📥 Downloadable Insights

From the **Data-driven Insights** section, you can download:\
📄 `Complete_MTN_Strategic_Analytics_Report.docx` → Full strategic
insights & analysis.

------------------------------------------------------------------------

## 👨‍💻 About the Developer

![Developer](image/My%20image.jpg)

### **Kajola Gbenga**

📊 Certified Data Analyst \| 📈 Data Scientist \| 💻 SQL Programmer \|
📱 Mobile App Developer \| 🤖 AI/ML Engineer

-   🔗 [LinkedIn](https://www.linkedin.com/in/kajolagbenga)\
-   📜 [Certifications &
    Licenses](https://www.datacamp.com/portfolio/kgbenga234)\
-   💻 [GitHub](https://github.com/prodigy234)\
-   🌍 [Portfolio](https://kajolagbenga.netlify.app/)\
-   ✉️ k.gbenga234@gmail.com

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**.\
You are free to use, modify, and distribute with attribution.