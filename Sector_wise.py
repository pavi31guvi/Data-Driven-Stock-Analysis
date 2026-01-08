import pandas as pd
import os

OUTPUT_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
MASTER_FILE = os.path.join(OUTPUT_PATH, "yearly_returns.csv")
SECTOR_FILE = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\Sector_data.csv"

# Load yearly returns
yearly_returns = pd.read_csv(MASTER_FILE)

# Load sector CSV
sector_df = pd.read_csv(SECTOR_FILE)
# Extract actual ticker from Symbol
sector_df["Ticker"] = sector_df["Symbol"].str.split(":").str[-1].str.strip()

# Keep only needed columns
sector_df = sector_df[["Ticker", "sector"]].rename(columns={"sector": "Sector"})
ticker_map = {
    "ADANIGREEN": "ADANIENT",
    "AIRTEL": "BHARTIARTL",
    "BRITANNIA" : "BRITANNIA",
    "TATACONSUMER" : "TATACONSUM"
}
sector_df["Ticker"] = sector_df["Ticker"].replace(ticker_map)
sector_returns = yearly_returns.merge(
    sector_df,
    on="Ticker",
    how="left"
)

manual_sector_map = {
    'BRITANNIA': 'FMCG'
}
sector_returns['Sector'] = sector_returns['Sector'].fillna(sector_returns['Ticker'].map(manual_sector_map))
# Average yearly return per sector
sector_perf = (sector_returns.groupby("Sector").agg(
        avg_yearly_return=("yearly_return", "mean"),
        stock_count=("Ticker", "count")).reset_index()
        .sort_values("avg_yearly_return", ascending=False)
)

# Save CSV for Streamlit / Power BI
sector_perf.to_csv(os.path.join(OUTPUT_PATH, "sector_performance.csv"), index=False)
print("Sector-wise performance calculated successfully")