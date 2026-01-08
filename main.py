import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="NIFTY 50 Stock Dashboard", layout="wide")

OUTPUT_PATH = r"C:\Users\91770\Documents\Data Science\Stock Analysis\data\output_dir"

# ---------------- CACHE DATA LOADING ----------------
@st.cache_data
def load_data():
    master_df = pd.read_csv(f"{OUTPUT_PATH}/master_with_returns.csv", parse_dates=["date"])
    yearly_returns = pd.read_csv(f"{OUTPUT_PATH}/yearly_returns.csv")
    volatility_df = pd.read_csv(f"{OUTPUT_PATH}/top_10_volatile.csv")
    sector_perf = pd.read_csv(f"{OUTPUT_PATH}/sector_performance.csv")
    gainers_df = pd.read_csv(f"{OUTPUT_PATH}/monthly_top_5_gainers.csv")
    losers_df = pd.read_csv(f"{OUTPUT_PATH}/monthly_top_5_losers.csv")
    return master_df, yearly_returns, volatility_df, sector_perf, gainers_df, losers_df


master_df, yearly_returns, volatility_df, sector_perf, gainers_df, losers_df = load_data()
# FIX month column format
gainers_df["month"] = pd.to_datetime(gainers_df["month"]).dt.strftime("%Y-%m")
losers_df["month"] = pd.to_datetime(losers_df["month"]).dt.strftime("%Y-%m")

# ---------------- CACHE CUMULATIVE CALC ----------------
@st.cache_data
def compute_cumulative(df):
    df = df.copy()
    df["cumulative_return"] = (
        df.groupby("Ticker")["daily_return"]
          .transform(lambda x: (1 + x).cumprod() - 1)
    )
    return df

# ---------------- CACHE CORRELATION ----------------
@st.cache_data
def compute_correlation(df, tickers):
    pivot = df[df["Ticker"].isin(tickers)].pivot_table(
        index="date", columns="Ticker", values="daily_return"
    )
    return pivot.corr()

# ---------------- TITLE ----------------
st.title("📊 Data-Driven Stock Analysis Dashboard (NIFTY 50)")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Market Overview",
    "Volatility",
    "Green & Red Stocks",
    "Cumulative",
    "Sector Performance",
    "Correlation",
    "Monthly Gainers & Losers"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("Market Summary")
    green_count = (yearly_returns["yearly_return"] > 0).sum()
    red_count = (yearly_returns["yearly_return"] <= 0).sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Green Stocks", green_count)
    col2.metric("Red Stocks", red_count)
    col3.metric("Avg Price", f"{master_df['close'].mean():.2f}")
    col4.metric("Avg Volume", f"{int(master_df['volume'].mean()):,}")

# ================= TAB 2 =================
with tab2:
    st.subheader("Top 10 Most Volatile Stocks")
    fig = px.bar(
        volatility_df, x="Ticker", y="volatility",
        text_auto=".4f", title="Top 10 Most Volatile Stocks"
    )
    fig.update_traces(marker_color="#e74c3c", textposition="outside", cliponaxis=False)
    fig.update_layout(height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 3 =================
with tab3:
    st.subheader("Top 10 Green & Red Stocks (Yearly Return)")
    col1, col2 = st.columns(2)
    with col1:
        top_green = yearly_returns.sort_values("yearly_return", ascending=False).head(10)
        fig = px.bar(
            top_green, x="Ticker", y="yearly_return",
            text=top_green["yearly_return"].apply(lambda x: f"{x:.2%}"),
            title="Top 10 Green Stocks"
        )
        fig.update_traces(marker_color="#2ecc71", textposition="outside", cliponaxis=False,
                          textfont=dict(size=15))
        fig.update_layout(yaxis_range=[0, top_green["yearly_return"].max() * 1.3])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_red = yearly_returns.sort_values("yearly_return").head(10)
        fig = px.bar(
            top_red, x="Ticker", y="yearly_return",
            text=top_red["yearly_return"].apply(lambda x: f"{x:.2%}"),
            title="Top 10 Red Stocks"
        )
        fig.update_traces(marker_color="#e74c3c", textposition="outside", cliponaxis=False,
                          textfont=dict(size=15))
        fig.update_layout(yaxis_range=[top_red["yearly_return"].min() * 1.3, 0])
        st.plotly_chart(fig, use_container_width=True)

# ================= TAB 4 =================
with tab4:
    st.subheader("Cumulative Returns-Top 5 Stocks")
    col1, col2 = st.columns(2)
    min_date, max_date = master_df["date"].min(), master_df["date"].max()

    with col1:
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    with col2:
        end_date = st.date_input("End Date", min_value=start_date, max_value=max_date, value=max_date)

    df = master_df[(master_df["date"] >= pd.to_datetime(start_date)) &
                   (master_df["date"] <= pd.to_datetime(end_date))]

    df = compute_cumulative(df)

    top5 = (
        df.groupby("Ticker")["cumulative_return"]
        .last().sort_values(ascending=False).head(5).index
    )

    fig = px.line(
        df[df["Ticker"].isin(top5)],
        x="date", y="cumulative_return", color="Ticker",
        title="Top 5 Stocks – Cumulative Return"
    )
    fig.update_yaxes(tickformat=".2%")
    fig.update_layout(height=520, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 5 =================
with tab5:
    st.subheader("Sector-wise Performance (Average Yearly Return)")
    fig = px.bar(
        sector_perf, x="Sector", y="avg_yearly_return",
        text_auto=".2%", title="Sector-wise Average Yearly Return",
        color_discrete_sequence=["#6c5ce7"]
    )
    fig.update_traces(textposition="outside", textfont=dict(size=13))
    fig.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 6 =================
with tab6:
    st.subheader("Stock Correlation Heatmap")
    stocks = st.multiselect(
        "Select up to 10 stocks",
        master_df["Ticker"].unique(),
        default=master_df["Ticker"].unique()[:5]
    )

    if len(stocks) < 2:
        st.warning("Please select at least 2 stocks.")
        st.stop()

    if len(stocks) > 10:
        st.warning("Please select maximum 10 stocks.")
        st.stop()

    if 2 <= len(stocks) <= 10:
        corr = compute_correlation(master_df, tuple(stocks))
        fig = px.imshow(
            corr, text_auto=".2f", zmin=-1, zmax=1,
            color_continuous_scale="RdBu",
            title="Stock Correlation Heatmap"
        )
        fig.update_layout(height=600)
    
        st.plotly_chart(fig, use_container_width=True)
        st.info("Darker color indicates stronger correlation.")

# ================= TAB 7 =================
with tab7:
    st.subheader("Monthly Top Gainers & Losers")
    months = sorted(gainers_df["month"].unique())
    month_map = {m: datetime.datetime.strptime(m, "%Y-%m").strftime("%b %Y") for m in months}
    label_to_month = {v: k for k, v in month_map.items()}

    selected = st.selectbox("Select Month", list(label_to_month.keys()))
    month = label_to_month[selected]

    col1, col2 = st.columns(2)

    with col1:
        g = gainers_df[gainers_df["month"] == month]
        fig = px.bar(g, x="Ticker", y="monthly_return", text_auto=".2%",
                     title=f"Top Gainers – {month}")
        fig.update_traces(marker_color="#27ae60", textposition="outside", cliponaxis=False,
                          textfont=dict(size=14))
        fig.update_layout(yaxis_range=[0, g["monthly_return"].max() * 1.3])
        if g.empty:
            st.warning("No data available for this month")
        else:
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        l = losers_df[losers_df["month"] == month]
        fig = px.bar(l, x="Ticker", y="monthly_return", text_auto=".2%",
                     title=f"Top Losers – {month}")
        fig.update_traces(marker_color="#c0392b", textposition="outside", cliponaxis=False,
                          textfont=dict(size=14))
        #fig.update_layout(yaxis_range=[l["monthly_return"].min() * 1.3, 0])
        if l.empty:
            st.warning("No data available for this month")
        else:
            st.plotly_chart(fig, use_container_width=True)