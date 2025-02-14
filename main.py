import yfinance as yf
import matplotlib.pyplot as plt

# Example: Fetching stock data
stock_data = yf.download('AAPL', start='2020-01-01', end='2025-01-01')

# Calculate moving averages
stock_data['MA_10'] = stock_data['Close'].rolling(window=10).mean()
stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()

# Plot the stock data along with moving averages
plt.figure(figsize=(10,6))
plt.plot(stock_data['Close'], label='AAPL Close Price')
plt.plot(stock_data['MA_10'], label='MA 10', color='orange')
plt.plot(stock_data['MA_20'], label='MA 20', color='green')

plt.title('AAPL Stock Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()

plt.show()
