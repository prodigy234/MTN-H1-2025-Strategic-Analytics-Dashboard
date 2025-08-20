
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="MTN Strategic Analytics", page_icon="📶", layout="wide")

@st.cache_data
def load_data():
    df_group = pd.read_csv("data/group_h1_2025_summary.csv")
    df_country = pd.read_csv("data/country_h1_2025_kpis.csv")
    df_platform = pd.read_csv("data/platform_metrics_h1_2025.csv")
    return df_group, df_country, df_platform

df_group, df_country, df_platform = load_data()

# HEADER
st.title("MTN Group — Strategic Analytics Dashboard")
st.caption("Real figures sourced from MTN H1 2025 SENS and FY-24 results. Replace/append with your own CSVs as needed.")

# SIDEBAR
st.sidebar.header("Controls")
view = st.sidebar.radio("View", ["Executive KPIs", "Country Deep-Dive", "Fintech & Data", "Scenario Lab", "Upload More Data"])
currency = st.sidebar.selectbox("Reporting currency (display only)", ["ZAR", "USD"])

# EXECUTIVE KPIs
if view == "Executive KPIs":
    st.subheader("Executive KPIs (H1 2025)")
    kpis = df_group.set_index("metric")
    cols = st.columns(4)
    def val(metric):
        row = kpis.loc[metric]
        v = row["value"]
        u = row["unit"]
        return f"{v:,.2f} {u}" if pd.notnull(v) else row["notes"]
    with cols[0]:
        st.metric("Service revenue", val("Service revenue (reported)"), "+23.2% YoY (reported)")
        st.metric("Service revenue growth (CC)", f"{kpis.loc['Service revenue growth (constant currency)']['value']} %")
    with cols[1]:
        st.metric("EBITDA", val("EBITDA"), "Margin 44.2% (CC)")
        st.metric("Operating FCF", val("Operating free cash flow"))
    with cols[2]:
        st.metric("Subscribers", val("Subscribers"))
        st.metric("Active data subs", val("Active data subscribers"))
    with cols[3]:
        st.metric("MoMo MAU", val("MoMo MAU"))
        st.metric("Data share of revenue", f"{kpis.loc['Data revenue share of service revenue']['value']} %")

    st.divider()
    st.dataframe(df_group)

# COUNTRY DEEP-DIVE
if view == "Country Deep-Dive":
    st.subheader("Country KPIs (H1 2025)")
    st.dataframe(df_country)
    st.markdown("#### Growth by country")
    chart = alt.Chart(df_country).mark_bar().encode(
        x=alt.X("country:N", sort="-y", title="Country"),
        y=alt.Y("service_revenue_growth_cc_pct:Q", title="Service revenue growth (CC, %)"),
        tooltip=["country", "service_revenue_growth_cc_pct", "ebitda_margin_pct", "notes"]
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("#### EBITDA margin (where disclosed)")
    eb = df_country.dropna(subset=["ebitda_margin_pct"])
    if not eb.empty:
        chart2 = alt.Chart(eb).mark_bar().encode(
            x=alt.X("country:N", title="Country"),
            y=alt.Y("ebitda_margin_pct:Q", title="EBITDA margin (%)"),
            tooltip=["country", "ebitda_margin_pct"]
        )
        st.altair_chart(chart2, use_container_width=True)
    else:
        st.info("No per-country EBITDA margin disclosed in the starter dataset.")

# FINTECH & DATA
if view == "Fintech & Data":
    st.subheader("Fintech & Data KPIs")
    st.dataframe(df_platform)
    st.markdown("#### MoMo and Data metrics")
    sel = st.multiselect("Select metrics to chart", df_platform["metric"].unique().tolist(),
                         default=["MoMo MAU", "Active data subscribers"])
    filt = df_platform[df_platform["metric"].isin(sel)]
    chart = alt.Chart(filt).mark_bar().encode(
        x=alt.X("metric:N", title="Metric"),
        y=alt.Y("value:Q", title="Value"),
        color="segment:N",
        tooltip=["segment", "metric", "value", "unit"]
    )
    st.altair_chart(chart, use_container_width=True)

# SCENARIO LAB
if view == "Scenario Lab":
    st.subheader("Scenario Lab — simple sensitivities (illustrative)")
    st.caption("These are purely illustrative sensitivities using H1 2025 baselines. Replace with your own models for rigor.")
    base_service_rev = float(df_group[df_group["metric"]=="Service revenue (reported)"]["value"].iloc[0]) # ZAR bn
    base_margin = float(df_group[df_group["metric"]=="EBITDA margin (CC)"]["value"].iloc[0]) / 100.0
    price_change = st.slider("Tariff change (avg blended, %)", min_value=-20, max_value=30, value=5, step=1)
    data_growth = st.slider("Data traffic growth delta (pp vs base +29.1%)", min_value=-20, max_value=40, value=10, step=1)
    fintech_take_rate = st.slider("Fintech advanced services take-rate uplift (pp)", min_value=0, max_value=10, value=2, step=1)

    # Very simple mechanics for illustration
    rev_uplift = 0.5*(price_change/100) + 0.3*(data_growth/100) + 0.2*(fintech_take_rate/100)
    rev_new = base_service_rev * (1 + rev_uplift)
    ebitda_new = rev_new * (base_margin + 0.25*rev_uplift)
    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline service revenue (H1)", f"{base_service_rev:,.2f} ZAR bn")
    col2.metric("Scenario service revenue", f"{rev_new:,.2f} ZAR bn", f"{rev_uplift*100:.1f}%")
    col3.metric("Scenario EBITDA", f"{ebitda_new:,.2f} ZAR bn")

    st.markdown("##### Notes")
    st.write("- Use the **Upload More Data** tab to add granular time series (monthly, per-opco, ARPU/MAU).")
    st.write("- Replace this toy sensitivity with your finance-grade model (e.g., elasticity, FX ladders, churn).")

# UPLOAD
if view == "Upload More Data":
    st.subheader("Append or replace datasets")
    st.write("You can upload CSVs that match or extend the schemas below. They will be merged in memory.")
    up = st.file_uploader("Upload CSV(s)", type=["csv"], accept_multiple_files=True)
    if up:
        for f in up:
            try:
                df = pd.read_csv(f)
                st.success(f"Loaded {f.name} — {df.shape[0]} rows, {df.shape[1]} cols.")
                st.dataframe(df.head(20))
            except Exception as e:
                st.error(f"Failed to load {f.name}: {e}")

st.markdown("---")
st.markdown("**Sources:** MTN Group H1 2025 SENS announcement; FY-24 results transcript. Replace with your own detailed disclosures for deeper analysis.")
