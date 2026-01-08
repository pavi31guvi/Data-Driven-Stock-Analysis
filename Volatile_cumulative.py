import pandas as pd

OUTPUT_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"
master_df = pd.read_csv(f"{OUTPUT_PATH}/master_with_returns.csv")
master_df["date"] = pd.to_datetime(master_df["date"])

# Volatile Calculations
volatility_df = (master_df.groupby("Ticker")["daily_return"].std().reset_index().rename(columns={"daily_return": "volatility"}))
top_10_volatile = volatility_df.sort_values("volatility", ascending=False).head(10)

#Cumulative Calculations
master_df["cumulative_return"] = (master_df.groupby("Ticker")["daily_return"].transform(lambda x: (1 + x).cumprod() - 1))
final_cum_returns = (master_df.groupby("Ticker").agg(final_cumulative_return=("cumulative_return", "last")).reset_index())

top_5_cumulative = final_cum_returns.sort_values("final_cumulative_return", ascending=False).head(5)
top_5_tickers = top_5_cumulative["Ticker"].tolist()

cum_return_plot_df = master_df[master_df["Ticker"].isin(top_5_tickers)]
volatility_df.to_csv(f"{OUTPUT_PATH}/volatility.csv", index=False)
top_10_volatile.to_csv(f"{OUTPUT_PATH}/top_10_volatile.csv", index=False)
cum_return_plot_df.to_csv(f"{OUTPUT_PATH}/cumulative_returns_top5.csv", index=False)

print("Volatile and Cumulative Calculation completed sucessfully ")