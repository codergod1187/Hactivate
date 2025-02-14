import yfinance as yf

# Define stock symbols
stocks = {
    "AAPL": "AAPL",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "GOLD": "GC=F",
    "INTC": "INTC",
    "LTC": "LTC-USD"
}

# Fetch real-time prices
def get_stock_price(symbol):
    try:
        return round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2)
    except:
        return 0  # Default value if fetching fails

# Assign stock values
AAPL_VAL = get_stock_price(stocks["AAPL"])
BTC_VAL = get_stock_price(stocks["BTC"])
ETH_VAL = get_stock_price(stocks["ETH"])
GOLD_VAL = get_stock_price(stocks["GOLD"])
INTC_VAL = get_stock_price(stocks["INTC"])
LTC_VAL = get_stock_price(stocks["LTC"])

# Money variable (can be changed dynamically in the game)
money = 5000
