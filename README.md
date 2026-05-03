# Superstore Sales Intelligence Pipeline | NTT DATA Project

## Overview
End-to-end BI pipeline analyzing 9,994 sales records across 4 regions 
to identify revenue drivers, profit leakages, and shipping performance. 
Built to mirror enterprise data workflow standards used at NTT DATA.

## Pipeline Architecture
| Stage | Description | Tool |
|---|---|---|
| Ingestion | Raw CSV loading with schema validation | Python, Pandas |
| Quality Checks | Null detection, duplicate flagging | Pandas |
| Cleaning | Date parsing, standardization | Pandas |
| Transformation | Profit margin, revenue band, shipping days | Pandas |
| Join | Region lookup table integration | Pandas |
| Validation | 4 assertion-based quality checks | Python |
| SQL Analysis | 6 business queries | SQLite |
| EDA | 4-panel dashboard + discount impact chart | Matplotlib, Seaborn |
| BI Dashboard | KPI cards, charts, trend analysis | Power BI, DAX |

## Key Business Insights
- West region leads revenue at **$725K** with 21.95% profit margin
- Central region has **negative profit margin of -10.41%** — needs investigation
- Copiers most profitable sub-category at **31.72% margin**
- High discounts directly cause losses — Cubify 3D Printer lost **$9,239**
- Consumer segment drives **50%+ of total revenue**
- Standard Class shipping averages **5 days** vs Same Day at 0 days

## Tech Stack
Python | Pandas | NumPy | Matplotlib | Seaborn | SQLite | Power BI | DAX | GitHub
## Results
- 9,994 records processed through 8-stage pipeline
- 29 columns after feature engineering
- 6 SQL business queries executed
- 4 validation checks passed
- Power BI dashboard with 5 DAX measures
