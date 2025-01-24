import pandas as pd
import numpy as np
import yfinance as yf
from sqlalchemy import create_engine
import sqlalchemy
from stocknews import StockNews
import mysql.connector
import pandas as pd
from mysql.connector import Error

def fetch_ticker_data(ticker: str, start_date, end_date) -> pd.DataFrame:
    engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)
    if sqlalchemy.inspect(engine).has_table(ticker):
        data = pd.read_sql(f"select * from {ticker}", engine)
    else:
        data = yf.download(ticker)
        data["Date"] = data.index
        data.to_sql(name=ticker, con=engine, if_exists="replace", index=False)

    data = data[(data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))]
    return data


def fetch_portfolio():
    engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)
    if sqlalchemy.inspect(engine).has_table("portfolio"):
        portfolio = pd.read_sql("select * from portfolio", engine)
        return portfolio
    else:
        return None


def add_to_portfolio(ticker: str, name: str):
    columns = ["ticker","city","state","zip","country","website","sector","open","dayLow","dayHigh","payoutRatio","beta","volume","marketCap","currentPrice","targetHighPrice","totalCash"]
    engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)
    if sqlalchemy.inspect(engine).has_table("portfolio"):
        df = pd.read_sql(f"select * from portfolio where ticker='{ticker}'", engine)
        if df.shape[0] == 0:
            df = pd.DataFrame({"ticker": [ticker], "name": [name]})
            df.to_sql("portfolio", engine, if_exists="append", index=False)
            tick = yf.Ticker(ticker)
            t_info = tick.info
            df = pd.DataFrame([t_info])
            df.insert(0, 'ticker', ticker)
            df_cols = df.columns.to_list()
            missing_cols = set(columns) - set(df_cols)
            for col in missing_cols:
                df[col] = [np.nan] * df.shape[0]
            df_final=df[columns]
            print(df_final.info())
            print(df_final.head())
            df_final.to_sql("fundamental_data", engine, if_exists="append", index=False)         
    else:
        df = pd.DataFrame({"ticker": [ticker], "name": [name]})
        df.to_sql("portfolio", engine, if_exists="append", index=False)
        tick = yf.Ticker(ticker)
        t_info = tick.info
        df = pd.DataFrame([t_info])
        df.insert(0, 'ticker', ticker)
        df_cols = df.columns.to_list()
        missing_cols = set(columns) - set(df_cols)
        for col in missing_cols:
            df[col] = [np.nan] * df.shape[0]
        df_final=df[columns]
        df_final=df[["ticker","city","state","zip","country","website","sector","open","dayLow","dayHigh","payoutRatio","beta","volume","marketCap","currentPrice","targetHighPrice","totalCash"]]
        print(df_final.info())
        print(df_final.head())
        df_final.to_sql("fundamental_data", engine, if_exists="append", index=False)
    


def delete_stock_procedure(stock_ticker):
    try:
        # Connect to the database
        #mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB
        host = "junction.proxy.rlwy.net:13793"
        user = "root"
        password = "WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu"
        database = "Stock_DB"
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        
        if connection.is_connected():
            cursor = connection.cursor()

            # Call the stored procedure
            cursor.callproc("delete_stock", [stock_ticker])

            # Commit the transaction
            connection.commit()
            print("Stock deleted successfully.")

    except Error as e:
        print("Error:", e)

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection is closed")
