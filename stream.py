import os
import re

import streamlit as st
import numpy as np
import plotly.express as px
import yfinance as yf
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text
import mysql.connector
import pandas as pd
from mysql.connector import Error

from db import fetch_ticker_data, add_to_portfolio
from move_ticker_data import migrate_data


# st.set_page_config(
#      page_title="Stock dash",
#      page_icon="🦈"
# )

st.title("Stock Dashboard")

st.subheader("Track Stock")
engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB', echo=False)

def setup_db():
    sql_files = os.listdir("database")
    queries = []
    for sql_file in sql_files:
        with open(os.path.join("database", sql_file), "r") as f:
            sql_query = f.read()
            sql_query = sql_query.replace("\n", "")
            # sql_query = re.sub(r"\s+", "", sql_query)
            queries.append(sql_query)

    with engine.connect() as con:
        for query in queries:
            con.execute(text(query))
            con.commit()
    migrate_data()

setup_db()

try:
    # Connect to the database
    #mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_DB
    host = "junction.proxy.rlwy.net"
    user = "root"
    port = 13793
    password = "WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu"
    database = "Stock_DB"
    connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    
    if connection.is_connected():
        cursor = connection.cursor()

        # Call the stored procedure without parentheses
        cursor.execute("select * from Stock_DB.tickers;")

        # Process the result set returned by the stored procedure

        results = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()
        print("Connection is closed")

        # Convert the results list into a DataFrame
        df1 = pd.DataFrame(results, columns=["symbol", "name"])

except Error as e:
    print("Error:", e)


df1["options"] = df1["symbol"] + ":" + df1["name"]
# st.dataframe(df1)
ticker=st.selectbox('Ticker', options=df1["options"])
start_date=st.date_input('Start Date')
end_date=st.date_input('End Date')
print(df1.head())

if ticker:
    # query = f"SELECT * FROM `{ticker}`"
    # df_from_sql = pd.read_sql(query, engine)
    symbol, name = ticker.split(":")
    data = fetch_ticker_data(symbol, start_date, end_date)
    #st.dataframe(data)
    if data.shape[0] > 0:
        fig1=px.line(data, x = data['Date'], y = ['High', 'Low'], title= ticker)
        fig2=px.line(data, x = data['Date'], y = ['Open', 'Close'], title= ticker)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.button("Track", on_click=add_to_portfolio, args=(symbol, name))
    else:
        st.write("No data found for this ticker, try another ticker or modify the date range")
            
