import yfinance as yf  # Import the yfinance library as yf, used to fetch historical stock data from Yahoo Finance
import plotly.graph_objects as go  # Import Plotly's graph objects as go, used for creating interactive plots
import streamlit as st, pandas as pd  # Import Streamlit for building web apps and pandas as pd for data manipulation
import requests  # Import the requests library for making HTTP requests (though not used in the code)
import time  # Import the time module (also not used in this code)

# Function to fetch stock data and plot a line chart with moving averages
# Function to fetch stock data and plot candlestick chart with moving averages
def plot_stock(stock_symbol):  # Define a function 'plot_stock' that takes a stock symbol as input
    # Fetch stock data
    stock_data = yf.download(stock_symbol, start='2020-01-01', end='2025-01-01')  # Use yfinance to download stock data from 2020-01-01 to 2025-01-01 for the given stock symbol

    # Calculate moving averages
    stock_data['MA_10'] = stock_data['Close'].rolling(window=10).mean()  # Calculate the 10-day moving average of the 'Close' price
    stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()  # Calculate the 20-day moving average of the 'Close' price

    # Create candlestick chart
    fig = go.Figure(data=[  # Create a figure object using Plotly
        go.Candlestick(  # Create a candlestick chart
            x=stock_data.index,  # Use the stock data index (dates) for the x-axis
            open=stock_data['Open'],  # Use the 'Open' prices for the candlestick chart
            high=stock_data['High'],  # Use the 'High' prices for the candlestick chart
            low=stock_data['Low'],  # Use the 'Low' prices for the candlestick chart
            close=stock_data['Close'],  # Use the 'Close' prices for the candlestick chart
            name='Candlestick'  # Label the candlestick chart
        ),
        go.Scatter(  # Create a line plot for the 10-day moving average
            x=stock_data.index,  # Use the stock data index (dates) for the x-axis
            y=stock_data['MA_10'],  # Use the 10-day moving average values for the y-axis
            mode='lines',  # Display it as a line
            name='MA 10',  # Label the line as 'MA 10'
            line=dict(color='orange')  # Set the line color to orange
        ),
        go.Scatter(  # Create a line plot for the 20-day moving average
            x=stock_data.index,  # Use the stock data index (dates) for the x-axis
            y=stock_data['MA_20'],  # Use the 20-day moving average values for the y-axis
            mode='lines',  # Display it as a line
            name='MA 20',  # Label the line as 'MA 20'
            line=dict(color='green')  # Set the line color to green
        )
    ])

    # Update layout of the chart
    fig.update_layout(  # Customize the layout of the chart
        title=f'{stock_symbol} Stock Price and Moving Averages',  # Set the chart title
        xaxis_title='Date',  # Label the x-axis as 'Date'
        yaxis_title='Price (USD)',  # Label the y-axis as 'Price (USD)'
        xaxis_rangeslider_visible=False  # Disable the range slider at the bottom of the x-axis
    )

    fig.show()  # Display the interactive chart

# Call the function for MSFT (Microsoft)
plot_stock('MSFT')  # Call the 'plot_stock' function with 'MSFT' as the input to plot Microsoft's stock data
