import pandas as pd
import numpy as np

df = pd.read_csv('data/superstore.csv', encoding='latin-1')

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nNull counts:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nData types:\n", df.dtypes)
print("\nSample rows:")
print(df.head())