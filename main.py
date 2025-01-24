import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta
import streamlit as st
import numpy as np
import plotly.express as px

# import logging
# import argparse

# parser = argparse.ArgumentParser(description ='Ticker name')
# logging.basicConfig(filename="/Users/pvalluri09/Desktop/pvalluri09/Work/college/packages/intraday-stock/logs.log",
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)

# parser.add_argument('-t', '--ticker',
#                     type = str,
#                     help ='Ticker to watch')

# args = parser.parse_args()

x=input("enter a ticker")
# x = args.ticker

df = yf.download(x, start=pd.to_datetime('today') - timedelta(7), interval='1m')
print(df)
df.to_sql(name=x, con=engine, if_exists="replace", index=False)
# logging.info(f"Downloaded data from YFinance for {x} containing {df.shape[0]} records")

query = f"SELECT * FROM `{x}`"
df_from_sql = pd.read_sql(query, engine)
print(df_from_sql)
 
