# 📊 NIFTY 50 Stock Analysis Dashboard

## 🔗 Project Overview
This project is a data-driven dashboard built with **Python, Pandas, Streamlit, Plotly**.  
It analyzes NIFTY 50 stock data, providing insights into volatility, cumulative returns, sector performance, correlations, and monthly gainers/losers.  
The workflow converts raw YAML files into structured CSVs, computes financial metrics, and visualizes them interactively.

---

## 🗂️ Project Structure
project/
├── main.py  (streamlit.py)       # Streamlit dashboard with 7 tabs
├── yml_to_csv.py                # Converts raw YAML files to master CSV + ticker CSVs
├── green_red_stock.py           # Computes daily & yearly returns, saves master_with_returns.csv
├── volatile_cumulative.py       # Calculates volatility & cumulative returns, saves top 10/5 CSVs
├── sector.py                     # Maps tickers to sectors, computes sector-wise performance
├── correlation.py                # Generates correlation matrix CSV for stocks
├── gainers_losers.py            # Extracts monthly top 5 gainers & losers
├── data/                        # Raw YAML data (organized by month)
│   ├── output_dir/              # Processed CSV outputs for dashboard
│   ├── ticker_csv/              # Individual ticker-level CSVs
│   └── Sector_data.csv          # Sector mapping file
└── README.md                     # Documentation

## Features

- **Market Overview**: Displays count of Green vs Red stocks, along with average price & volume  
- **Volatility**: Highlights the Top 10 most volatile stocks  
- **Green & Red Stocks**: Shows yearly top gainers & losers  
- **Cumulative Returns**: Interactive date range filter with Top 5 cumulative performers  
- **Sector Performance**: Average yearly return per sector with bar chart visualization

---

## Installation & Setup
```bash
# Clone the repository
git clone https://github.com/pavi31guvi/Data-Driven-Stock-Analysis.git

# Navigate to project folder
cd Data-Driven-Stock-Analysis
```

```
# For Data preparation - Run the below python scripts 
python yml_to_csv.py

pyhton green_red_stock.py

python volatile_cumulative.py

python sector.py

python correlation.py

python gainers_losers.py
```

```
# Run Streamlit app
streamlit run main.py
```

### Data Preparation
- `yml_to_csv.py` → Converts raw YAML files into `master.csv`
- `green_red_stock.py` → Adds daily & yearly returns
- `volatile_cumulative.py` → Computes volatility & cumulative returns
- `sector.py` → Maps tickers to sectors & aggregates performance
- `correlation.py` → Generates correlation matrix
- `gainers_losers.py` → Extracts monthly top gainers & losers

### Dashboard Execution
- `main.py` → Loads processed CSVs
- Interactive tabs → Display charts using **Plotly + Streamlit**

## Requirements

- **Python**  
- **Libraries**:  
  - `pandas`  
  - `streamlit`  
  - `plotly`  
  - `matplotlib`  
  - `seaborn`  
  - `pyyaml`  
---

## Visualizations

- Bar chart of **Top 10 Volatile Stocks**  
- Line chart of **Top 5 Cumulative Returns**  
- Sector-wise **Average Yearly Return**  
- **Correlation Heatmap** of selected stocks  
- Monthly **Top Gainers & Losers**  
- **Correlation Heatmap**: Select up to 10 stocks and visualize their correlations  
- **Monthly Gainers & Losers**: Top 5 stocks per month with side-by-side charts  
