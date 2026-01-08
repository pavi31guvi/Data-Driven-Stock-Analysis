import os
import yaml as yml
import pandas as pd

# Required directories to save csv files.
BASE_DIR = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data"
OUTPUT_DIR = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
TICKER_DIR = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\ticker_csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TICKER_DIR, exist_ok=True)

all_rows =[]

for MON_DIR in os.listdir(BASE_DIR):
    if os.path.isdir(os.path.join(BASE_DIR,MON_DIR)):
        month_path = os.path.join(BASE_DIR,MON_DIR)
        for file in os.listdir(month_path):
            if file.lower().endswith(".yaml") or file.lower().endswith(".yml"):
                    day_file = os.path.join(month_path,file)  
                    if os.path.getsize(day_file) != 0:
                        with open(day_file,"r") as f:
                            data = yml.safe_load(f)
                        if data:
                            df = pd.DataFrame(data)
                            all_rows.append(df)

# Combine all yaml data
master_df = pd.concat(all_rows,ignore_index=True)
# date parsing
master_df["date"] = pd.to_datetime(master_df["date"])
# Sort once
master_df = master_df.sort_values(["Ticker", "date"])
master_df = master_df.drop_duplicates(subset=["Ticker", "date"])
master_file = os.path.join(OUTPUT_DIR,f"master.csv")
master_df.to_csv(master_file,index=False)

# Save individual ticker CSVs
for ticker_name,ticker_row in master_df.groupby('Ticker'):
    ticker_file = os.path.join(TICKER_DIR,f"{ticker_name}.csv")
    ticker_row.to_csv(ticker_file,index=False)

print(f"YAML to CSV conversion completed successfully")
