# Demo Walkthrough

This 5-7 minute walkthrough is designed for portfolio visitors, interviewers, and reviewers.

## Goal

Show that the project is not a notebook collection. It is an Excel-to-Python analytics platform that can ingest business workbooks, profile data, clean issues, run analytics, visualize results, and export Excel reports.

## Demo Flow

1. Launch the platform.
   - Command: `streamlit run app/streamlit_app.py`
   - Show the Home dashboard, dataset status, and guided demo panel.

2. Load the Retail analytics sample.
   - Click `Start guided demo`.
   - Explain that the sample workbook has orders, order items, customers, products, and inventory sheets.

3. Inspect Upload & Profile.
   - Open `Upload Profile`.
   - Show row counts, sheet counts, quality score, duplicates, missing values, and issue table.

4. Run Cleaning.
   - Open `Cleaning Workbench`.
   - Click `Run cleaning pipeline`.
   - Compare before/after tables and download the cleaned workbook.

5. Run Business Analytics.
   - Open `Business Analytics`.
   - Click `Run analytics`.
   - Use date, region, category, and RFM segment filters.
   - Show KPI cards, revenue trend, RFM summary, cohort size, ABC mix, and market basket sliders.

6. Export Excel report.
   - Open `Report Export`.
   - Click `Generate Excel analysis report`.
   - Download the workbook and explain openpyxl formatting.

7. Show Openpyxl Showcase.
   - Open `Openpyxl Showcase`.
   - Generate the showcase workbook.
   - Explain formulas, named styles, comments, hyperlinks, validation, protection, conditional formatting, and charts.

## Generated Demo Assets

```bash
python scripts/run_e2e_demo.py --port 8511 --record
excel-analysis demo
```

Expected outputs:

- `assets/demo/demo_walkthrough.mp4`
- `assets/demo/demo_steps.gif`
- `artifacts/playwright/demo_report.html`
- `artifacts/playwright/traces/dashboard_demo_trace.zip`
- `reports/demo_summary.html`
- `reports/portfolio_excel_analysis_report.xlsx`
- `reports/openpyxl_feature_showcase.xlsx`
