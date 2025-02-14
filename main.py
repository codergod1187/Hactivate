import yfinance as yf  # Import the yfinance library to fetch financial data from Yahoo Finance
import plotly.graph_objects as go  # Import the Plotly graph_objects library to create interactive visualizations

# Fetch data for Microsoft (MSFT) for the last month
data = yf.download("RELIANCE", period="1mo", interval="1d")  # Download the RELIANCE stock data for the last 1 month with daily intervals

# Print first few rows to verify data is fetched
print(data.head())  # Print the first 5 rows of the downloaded data to verify

# Create a candlestick chart using Plotly
fig = go.Figure(data=[go.Candlestick(  # Create a new figure and add a candlestick chart trace
    x=data.index,  # x-axis: Use the dates from the index of the DataFrame
    open=data['Open'],  # Open prices: Use the 'Open' column for each day's opening price
    high=data['High'],  # High prices: Use the 'High' column for each day's highest price
    low=data['Low'],  # Low prices: Use the 'Low' column for each day's lowest price
    close=data['Close'],  # Close prices: Use the 'Close' column for each day's closing price
    name="MSFT"  # Label for the chart trace (Microsoft)
)])

# Update chart layout
fig.update_layout(  # Modify the layout of the figure
    title="MSFT Stock Price",  # Set the title of the chart
    xaxis_title="Date",  # Label for the x-axis
    yaxis_title="Price (USD)",  # Label for the y-axis
    template="plotly_dark",  # Set the theme to 'plotly_dark' (dark mode)
)

# Show the chart
fig.show()  # Display the interactive candlestick chart
