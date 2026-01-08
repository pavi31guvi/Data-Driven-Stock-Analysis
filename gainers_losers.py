import pandas as pd
import os

OUTPUT_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
MASTER_FILE = os.path.join(OUTPUT_PATH, "master.csv")

master_df = pd.read_csv(MASTER_FILE)
master_df["date"] = pd.to_datetime(master_df["date"])


monthly_returns = (master_df.sort_values(["Ticker", "date"]).groupby(["Ticker", "month"]).agg(
        first_close=("close", "first"),
        last_close=("close", "last")
    ).reset_index())

monthly_returns["monthly_return"] = (
    (monthly_returns["last_close"] - monthly_returns["first_close"])
    / monthly_returns["first_close"]
)

top_gainers = (
    monthly_returns
    .groupby("month")
    .apply(lambda x: x.sort_values("monthly_return", ascending=False).head(5))
    .reset_index(drop=True)
)

top_losers = (
    monthly_returns
    .groupby("month")
    .apply(lambda x: x.sort_values("monthly_return", ascending=True).head(5))
    .reset_index(drop=True)
)
top_gainers.to_csv(
    os.path.join(OUTPUT_PATH, "monthly_top_5_gainers.csv"),
    index=False
)

top_losers.to_csv(
    os.path.join(OUTPUT_PATH, "monthly_top_5_losers.csv"),
    index=False
)

print("Hour-5 Monthly Gainers & Losers completed")