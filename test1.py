import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

# Create SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://sqluser:password@localhost:3306/Stock_DB', echo=False)

# Sample DataFrame
df = pd.DataFrame({"ticker": ["msft", "a"], "name": ["name1", "name2"]})

# Initialize an empty list to store DataFrames for each symbol
dfs = []

for i in df["ticker"]:
    tick=yf.Ticker(i)
    t_news=tick.news


# Iterate over each symbol in the 'ticker' column
for symbol in df["ticker"]:
    # Fetch information for the current symbol
    tick = yf.Ticker(symbol)
    t_info = tick.info
    
    # Create a DataFrame from the information and add 'ticker' column
    df_temp = pd.DataFrame([t_info])
    df_temp.insert(0, 'ticker', symbol)
    
    # Append the DataFrame to the list
    dfs.append(df_temp)

# Concatenate all DataFrames in the list into a single DataFrame
df_combined = pd.concat(dfs, ignore_index=True)
df_final=df_combined[['currentPrice','volume','shortName','marketCap','trailingEps','grossMargins','profitMargins','freeCashflow','currentRatio','numberOfAnalystOpinions','totalCash','totalDebt','totalRevenue','currentPrice','volume','shortName','marketCap','trailingEps','grossMargins','profitMargins','freeCashflow','currentRatio','numberOfAnalystOpinions','totalCash','totalDebt','totalRevenue','yield','earningsQuarterlyGrowth','shortPercentOfFloat','beta','averageVolume','floatShares','heldPercentInstitutions''earningsQuarterlyGrowth','shortPercentOfFloat','beta','averageVolume','floatShares',
 'heldPercentInstitutions']]

df_final.to_sql("try", engine, if_exists="append", index=False)

from stocknews import StockNews
...
stocks = ['AAPL', 'MSFT', 'NFLX']
sn = StockNews(stocks, wt_key='MY_WORLD_TRADING_DATA_KEY')
df = sn.summarize()