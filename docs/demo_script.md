# Demo Script

## Opening

This project demonstrates a full Excel-to-Python analytics workflow. The goal is to show how Excel business data can be moved into a repeatable Python system for profiling, cleaning, analysis, dashboard visualization, and formatted Excel report generation.

## Step 1: Home

Start at the Home dashboard. Point out the dataset status bar, workflow steps, and `Start guided demo` button.

Key message: the app is organized around a business workflow, not isolated notebooks.

## Step 2: Upload & Profile

Open Upload & Profile and load the Retail analytics sample.

Explain:

- multi-sheet Excel ingestion
- schema and dtype detection
- missing values
- duplicate rows
- issue table
- quality score

Key message: analysis starts with data understanding, not charts.

## Step 3: Cleaning Workbench

Run the cleaning pipeline.

Explain:

- text normalization
- date parsing
- numeric and currency conversion
- duplicate removal
- before/after comparison

Key message: cleaning logic is reusable and testable.

## Step 4: Business Analytics

Run analytics and use filters.

Explain:

- revenue, orders, AOV, items sold
- date/region/category/segment filters
- RFM segmentation
- cohort retention
- ABC inventory classification
- market basket rules with support/confidence/lift

Key message: pandas is used to build structured business analysis modules.

## Step 5: Report Export

Generate the Excel report.

Explain:

- summary sheet
- analytics sheets
- quality sheet
- formatting, freeze panes, filters, charts

Key message: Python can generate polished Excel artifacts for business users.

## Step 6: Openpyxl Showcase

Generate the openpyxl feature showcase workbook.

Explain:

- formulas
- named styles
- comments
- hyperlinks
- data validation
- worksheet protection
- conditional formatting
- charts

Key message: this project demonstrates practical Excel automation skills, not only pandas.

## Closing

The project combines data engineering, analytics, dashboard development, Excel automation, CLI workflows, and automated UI testing with Playwright.
