import pandas as pd
import numpy as np
import os

os.makedirs('outputs', exist_ok=True)

print("=== STEP 1: INGESTION ===")
df = pd.read_csv('data/superstore.csv', encoding='latin-1')
raw_count = len(df)
print(f"Raw records loaded: {raw_count}")

print("\n=== STEP 2: DATA QUALITY CHECKS ===")
quality_report = {
    'total_records': len(df),
    'duplicate_records': df.duplicated().sum(),
    'null_values': df.isnull().sum().sum(),
    'columns_with_nulls': df.columns[df.isnull().any()].tolist()
}
for k, v in quality_report.items():
    print(f"  {k}: {v}")

print("\n=== STEP 3: CLEANING ===")
df = df.drop_duplicates()
df = df.dropna()
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
clean_count = len(df)
print(f"  Records after cleaning: {clean_count}")
print(f"  Records removed: {raw_count - clean_count}")

print("\n=== STEP 4: TRANSFORMATION ===")
df['profit_margin'] = (df['profit'] / df['sales'] * 100).round(2)
df['revenue_band'] = pd.cut(
    df['sales'],
    bins=[0, 100, 500, 1000, 10000],
    labels=['Low', 'Medium', 'High', 'Very High']
)
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_quarter'] = df['order_date'].dt.quarter
print("  Derived columns added: profit_margin, revenue_band, order_year, order_month, order_quarter, shipping_days")

print("\n=== STEP 5: REGION LOOKUP JOIN ===")
region_lookup = pd.DataFrame({
    'region': ['East', 'West', 'Central', 'South'],
    'region_code': ['EST', 'WST', 'CNT', 'STH'],
    'region_manager': ['Manager A', 'Manager B', 'Manager C', 'Manager D']
})
df = df.merge(region_lookup, on='region', how='left')
print("  Region lookup joined successfully")
print(f"  Columns now: {df.shape[1]}")

print("\n=== STEP 6: DATA VALIDATION ===")
assert df['sales'].gt(0).all(), "Sales has zero/negative values"
assert df['order_date'].notnull().all(), "Order date has nulls"
assert df['shipping_days'].ge(0).all(), "Shipping days negative"
assert df.duplicated().sum() == 0, "Duplicates still exist"
print("  All validation checks passed")

print("\n=== STEP 7: SAVE OUTPUTS ===")
df.to_csv('outputs/superstore_clean.csv', index=False)
df.to_excel('outputs/superstore_clean.xlsx', index=False)

summary = pd.DataFrame({
    'metric': ['Raw Records', 'Clean Records', 'Removed',
               'Columns Added', 'Validation Checks'],
    'value': [raw_count, clean_count,
              raw_count - clean_count, 6, 4]
})
summary.to_csv('outputs/pipeline_summary.csv', index=False)

print("\nOutputs saved to /outputs folder")
print(f"Final dataset: {df.shape[0]} rows x {df.shape[1]} columns")
print("\n=== PIPELINE COMPLETE ===")