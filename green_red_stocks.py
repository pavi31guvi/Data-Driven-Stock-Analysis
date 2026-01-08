import pandas as pd

MASTER_FILE = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir\master.csv"
master_df = pd.read_csv(MASTER_FILE)

# Date handling
master_df["date"] = pd.to_datetime(master_df["date"])
master_df = master_df.sort_values(["Ticker", "date"])

#Daily returns
master_df["prev_close"] = master_df.groupby("Ticker")["close"].shift(1)
master_df["daily_return"] = (master_df["close"] - master_df["prev_close"]) / master_df["prev_close"]
master_df.dropna(subset=["daily_return"], inplace=True)
#Yearly returns
yearly_returns = (master_df.groupby("Ticker").agg(first_close=("close", "first"),last_close=("close", "last")))
yearly_returns["yearly_return"] = ((yearly_returns["last_close"] - yearly_returns["first_close"])/ yearly_returns["first_close"])
yearly_returns = yearly_returns.reset_index()

# Top 10 Green/Red Stocks
top_10_green = yearly_returns.sort_values("yearly_return", ascending=False).head(10)
top_10_red = yearly_returns.sort_values("yearly_return", ascending=True).head(10)

green_count = (yearly_returns["yearly_return"] > 0).sum()
red_count = (yearly_returns["yearly_return"] <= 0).sum()

avg_price = master_df["close"].mean()
avg_volume = master_df["volume"].mean()

OUTPUT_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
master_df.to_csv( f"{OUTPUT_PATH}/master_with_returns.csv",index=False)
yearly_returns.to_csv(f"{OUTPUT_PATH}/yearly_returns.csv",index=False)