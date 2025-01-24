import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


def migrate_data():
    df = pd.read_csv('./archive/symbols.csv')
    cols = ['Nasdaq Traded','Listing Exchange','Market Category','ETF','Round Lot Size','Test Issue','Financial Status','CQS Symbol','NASDAQ Symbol','NextShares']
    df.drop(cols,inplace=True,axis=1)
    df.columns = ["symbol", "name"]
    engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)
    try:
        df.to_sql(name='tickers', con=engine, if_exists = 'append', index=False)
    except Exception as e:
        print("Skipping population of tickers table...")
