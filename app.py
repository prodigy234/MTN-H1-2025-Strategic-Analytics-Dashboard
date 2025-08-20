
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
    df_regional = pd.read_csv("data/regional_h1_2025.csv")
    df_bayobab = pd.read_csv("data/bayobab_h1_2025.csv")
    df_fintech = pd.read_csv("data/fintech_h1_2025.csv")
    df_pricingfx = pd.read_csv("data/pricing_fx_h1_2025.csv")
    df_capex = pd.read_csv("data/capex_h1_2025.csv")
    return df_group, df_country, df_platform, df_regional, df_bayobab, df_fintech, df_pricingfx, df_capex

df_group, df_country, df_platform, df_regional, df_bayobab, df_fintech, df_pricingfx, df_capex = load_data()

# HEADER
st.title("📊 MTN Group: Strategic Analytics Dashboard")
st.markdown("An interactive, data-driven view into MTN's H1 2025 performance covering revenue, MoMo, Bayobab, regional insights, pricing, FX, and capex.")
st.caption("Scroll to the bottom to know more about the data professional behind this highly talented analytical project.")

# SIDEBAR
st.sidebar.header("Controls")
view = st.sidebar.radio("View", ["Executive KPIs", "Country Deep-Dive", "Fintech & Data", "Regional Performance", "Bayobab Infra", "Pricing & FX", "Capex & Infra", "Scenario Lab", "Data-driven Insights"])
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

# COUNTRY DEEP-DIVE (unchanged)
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

# FINTECH & DATA (extended to show fintech_h1_2025)
if view == "Fintech & Data":
    st.subheader("Fintech & Data KPIs")
    st.dataframe(df_platform)
    st.markdown("#### MoMo and Data metrics")
    sel = st.multiselect("Select metrics to chart", df_platform["metric"].unique().tolist() + df_fintech["metric"].tolist(),
                         default=["MoMo MAU", "Active data subscribers"])
    # combine for plotting convenience
    pp = df_platform.rename(columns={"segment":"segment_or_source"}).copy()
    ff = df_fintech.rename(columns={"metric":"metric","value":"value","unit":"unit","notes":"notes"}).copy()
    ff["segment_or_source"] = "Fintech"
    ff = ff[["segment_or_source","metric","value","unit","notes"]]
    combined = pd.concat([pp, ff], ignore_index=True, sort=False)
    filt = combined[combined["metric"].isin(sel)]
    chart = alt.Chart(filt).mark_bar().encode(
        x=alt.X("metric:N", title="Metric"),
        y=alt.Y("value:Q", title="Value"),
        color="segment_or_source:N",
        tooltip=["segment_or_source", "metric", "value", "unit"]
    )
    st.altair_chart(chart, use_container_width=True)

# REGIONAL PERFORMANCE
if view == "Regional Performance":
    st.subheader("Regional Performance (H1 2025)")
    st.dataframe(df_regional)
    st.markdown("#### Regional data revenue growth (CC %)")
    chart = alt.Chart(df_regional).mark_bar().encode(
        x=alt.X("region:N", sort="-y", title="Region"),
        y=alt.Y("data_revenue_cc_growth_pct:Q", title="Data revenue growth (CC %)"),
        tooltip=["region", "data_revenue_cc_growth_pct", "notes"]
    )
    st.altair_chart(chart, use_container_width=True)

# BAYOBAB INFRA
if view == "Bayobab Infra":
    st.subheader("Bayobab — Infrastructure & Wholesale (H1 2025)")
    st.dataframe(df_bayobab)
    st.markdown("""Bayobab is MTN's transport & wholesale arm. You can use these figures to model
                 cross-border capacity, wholesale pricing, and fibre roll-out economics.""")

# PRICING & FX
if view == "Pricing & FX":
    st.subheader("Pricing, ARPU & FX Headwinds")
    st.dataframe(df_pricingfx)
    st.markdown("""You can use the Nigeria rows to build FX scenarios; use the South Africa rows for ARPU
                 and usage-based elasticity sims.""")

# CAPEX & INFRA
if view == "Capex & Infra":
    st.subheader("Capex & Infrastructure Deployment")
    st.dataframe(df_capex)
    st.markdown("""Capex figures show H1 spend and FY guidance. You can go ahead to add your own per-country capex CSVs
                 to extend this (e.g per-opco site counts, 4G/5G rollouts).""")

# SCENARIO LAB (unchanged)
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


# UPLOAD
if view == "Data-driven Insights":
    st.subheader("MTN H1 2025 Data-driven Insights")
    st.write("This report gives a well detailed analytical insights for deep financial, operational, and strategic insights from MTN Group’s H1 2025 results. It includes real datasets (revenue, fintech, capex, Bayobab, FX/pricing, and regional KPIs), dynamic visualizations, and a detailed Word report designed to support data-driven decision-making and telecom strategy.")

    # Word Report Download
    st.markdown("### \U0001F4DD Download Complete MTN H1 Strategic Insights Report")
    with open("report/Complete_MTN_Strategic_Analytics_Report.docx", "rb") as doc_file:
        st.download_button(
            label="\U0001F4E5 Download Full Word Report",
            data=doc_file,
            file_name="Complete MTN Strategic Analytics Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# Footer
st.markdown("---")
st.markdown("# About the Developer")

st.image("image/My image.jpg", width=250)
st.markdown("## **Kajola Gbenga**")

st.markdown(
    """
\U0001F4C7 Certified Data Analyst | Certified Data Scientist | Certified SQL Programmer | Mobile App Developer | AI/ML Engineer

\U0001F517 [LinkedIn](https://www.linkedin.com/in/kajolagbenga)  
\U0001F4DC [View My Certifications & Licences](https://www.datacamp.com/portfolio/kgbenga234)  
\U0001F4BB [GitHub](https://github.com/prodigy234)  
\U0001F310 [Portfolio](https://kajolagbenga.netlify.app/)  
\U0001F4E7 k.gbenga234@gmail.com
"""
)