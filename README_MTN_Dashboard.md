
# MTN Strategic Analytics Dashboard (Streamlit)

This package includes a ready-to-run Streamlit app with **real H1 2025 MTN figures** extracted from official disclosures (MTN Group SENS/interim results and FY-24 results materials). It is designed for rapid pitching and can be extended with more granular datasets (monthly, per-opco, product-level).

## Files
- `app/streamlit_app.py` — Streamlit app.
- `app/requirements.txt` — Python dependencies.
- `data/group_h1_2025_summary.csv` — Group KPIs (H1 2025).
- `data/country_h1_2025_kpis.csv` — Nigeria, Ghana, South Africa growth and margins.
- `data/platform_metrics_h1_2025.csv` — Data & MoMo metrics (traffic, MAU, etc.).

## Run locally
```bash
pip install -r app/requirements.txt
streamlit run app/streamlit_app.py
```

## Deploy to Streamlit Cloud
1. Create a GitHub repo and upload the `app/` and `data/` folders.
2. On share.streamlit.io, point to `app/streamlit_app.py`.
3. Set Python version to 3.11+.

## Extend with more real data
- Append quarterly or monthly CSVs (ARPU, churn, net adds, MoMo volumes/values, FX rates).
- Maintain tidy schemas: date, country/opco, metric, value, unit, notes.
- Use the **Upload More Data** tab to verify file structure before committing to code.

## Notes
- All starter values are sourced from public MTN filings in Aug 2025.
- Replace or enrich with line-by-line tables from the official PDFs for deeper analysis.
