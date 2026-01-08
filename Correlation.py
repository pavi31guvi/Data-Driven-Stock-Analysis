import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

correlation_results = []
CORRELATION_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
master_file=r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir\master.csv"
master_df = pd.read_csv(master_file)
master_df['date'] = pd.to_datetime(master_df['date'])

# Step 1: Pivot master_df so each ticker is a column
price_df = master_df.pivot(index='date', columns='Ticker', values='close')

# Step 2: Calculate daily percentage returns
returns_df = price_df.pct_change().dropna()

# Step 3: Compute correlation matrix
corr_matrix = returns_df.corr()

file_path = os.path.join(CORRELATION_PATH, f"correlation_matrix.csv")
corr_matrix.to_csv(file_path)