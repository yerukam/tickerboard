import streamlit as st
from db import fetch_ticker_data
import plotly.express as px
import sqlalchemy
from sqlalchemy import create_engine
from db import fetch_portfolio
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
import mysql.connector 
from mysql.connector import Error
from db import delete_stock_procedure
st.title("Portfolio")

stocks = []

try:
    portfolios = fetch_portfolio()
    if portfolios is not None and portfolios.shape[0] > 0:
        for index, stock in portfolios.iterrows():
            stocks.append(f"{stock['ticker']}:{stock['name']}")
except Exception as e:
    st.error(f"An error occured while fetching the portfolio: {e}")

st.subheader("Stock Details:")
ticker=st.selectbox('Tracked Stocks', options=stocks)
start_date=st.date_input('Start Date')
end_date=st.date_input('End Date')
if ticker:
    try:
        symbol, name = ticker.split(":")
        data = fetch_ticker_data(symbol, start_date, end_date)
        if data.shape[0] > 0:
            fig1=px.line(data, x = data['Date'], y = ['High', 'Low'], title=symbol)
            fig2=px.line(data, x = data['Date'], y = ['Open', 'Close'], title=symbol)
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
        else:
            st.write("No data found for this ticker, try another ticker or modify the date range")

        if st.button("Delete Ticker"):
            delete_stock_procedure(symbol)

        fundamental_data,news=st.tabs(["Fundamental Data","Top 3 News"])

        with fundamental_data:
            engine = create_engine('mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_D', echo=False)

            # ticker_info=pd.read_sql("select * from fundamental_data",engine)
            try:
                # Connect to the database
                # mysql+mysqlconnector://root:WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu@junction.proxy.rlwy.net:13793/Stock_D
                host = "junction.proxy.rlwy.net"
                port = 13793
                user = "root"
                password = "WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu"
                database = "Stock_DB"
                connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
                
                if connection.is_connected():
                    cursor = connection.cursor()

                    # Call the stored procedure without parentheses
                    cursor.callproc("get_fundamental_data")

                    # Process the result set returned by the stored procedure
                    results = []
                    for result in cursor.stored_results():
                        result_set = result.fetchall()
                        for row in result_set:
                            results.append(row)

                    # Close cursor and connection
                    cursor.close()
                    connection.close()
                    print("Connection is closed")

                    # Convert the results list into a DataFrame
                    ticker_info = pd.DataFrame(results, columns=["ticker", "city", "state", "zip", "country", "website", "sector", "open", "dayLow", "dayHigh", "payoutRatio", "beta", "volume", "marketCap", "currentPrice", "targetHighPrice", "totalCash"])
                
            except Error as e:
                print("Error:", e)

            st.dataframe(ticker_info)
            
            color_map = {
                'Category1': 'blue',
                'Category2': 'green',
                'Category3': 'red'
            }
            fig3=px.bar(ticker_info, x='ticker', y='marketCap', title='Market Cap by Ticker')
            fig4 = px.histogram(ticker_info, x='payoutRatio', title='Histogram for Payout Ratio', color_discrete_sequence=['blue'])
            fig5 = px.histogram(ticker_info, x='beta', title='Histogram for Beta', color_discrete_sequence=['green'])
            fig6 = px.scatter(ticker_info, x='volume', y='currentPrice', title='Volume vs. Current Price Scatter Plot', color_discrete_sequence=['red'])
            fig7 = px.box(ticker_info, y='volume', title='Box Plot for Volume', color_discrete_sequence=['orange'])   
         
            query="""
                SELECT sector, AVG(currentprice) AS AvgCurrentPrice
                FROM fundamental_data
                GROUP BY sector
            """

            try:
                # Connect to the database
                host = "junction.proxy.rlwy.net"
                port = 13793
                user = "root"
                password = "WyUYyuPVISLqUKbJNvYxsQpYjpulGVwu"
                database = "Stock_DB"
                connection = mysql.connector.connect(host=host, port=, user=user, password=password, database=database)
                
                if connection.is_connected():
                    cursor = connection.cursor()

                    # Call the stored procedure without parentheses
                    cursor.execute("select sector, avg(currentprice) as AvgCurrentPrice from fundamental_data group by sector;")

                    # Process the result set returned by the stored procedure
                    results = cursor.fetchall()

                    # Close cursor and connection
                    cursor.close()
                    connection.close()
                    print("Connection is closed")

                    # Convert the results list into a DataFrame
                    sector_avg_price = pd.DataFrame(results, columns=["Sector", "Average Price"])
                    fig8 = px.pie(sector_avg_price, values="Average Price", names='Sector',title='Average Current Price by Sector')

            except Exception as e:
                print("Error:", e)
            #fig8 = px.pie(sector_avg_price, values='AvgCurrentPrice', names='sector',title='Average Current Price by Sector')
            
            col1, col2 = st.columns(2)
            st.plotly_chart(fig3)
            
            st.plotly_chart(fig4)
            
            st.plotly_chart(fig5) 
         
            st.plotly_chart(fig6)
            
            st.plotly_chart(fig7)

            st.plotly_chart(fig8)

        with news:
            tick = yf.Ticker(symbol)
            x = tick.news
            for i in range(min(3, len(x))):
                if  x[i] is not None:
                    st.write(f"\nNews {i+1}\n")
                    timestamp = x[i]['providerPublishTime']
                    datetime_obj = datetime.fromtimestamp(timestamp, timezone.utc)
                    formatted_date = datetime_obj.strftime("%Y-%m-%d")
                    st.write(f"Title: {x[i]['title']}")
                    st.write(f"Publisher: {x[i]['publisher']}")
                    st.write(f"Time: {formatted_date}")
                    st.write(f"Link: {x[i]['link']}")
                else:
                    st.write("No News Available...Sorry :(")
    except Exception as e:
        st.error(f"An error occured:")

    

    
    