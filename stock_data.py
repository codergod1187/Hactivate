import yfinance as yf

stocks = {
    "AAPL": "AAPL",
    "NVDA": "NVDA",
    "GOOGL": "GOOGL",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "GOLD": "GC=F",
    "INTC": "INTC",
    "LTC": "LTC-USD"
}

def get_stock_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if not data.empty and 'Close' in data.columns:
            return round(data['Close'].iloc[-1], 2)
        else:
            return 0  
    except:
        return 0  

AAPL_VAL = get_stock_price(stocks["AAPL"])
NVDA_VAL = get_stock_price(stocks["NVDA"])
GOOG_VAL = get_stock_price(stocks["GOOGL"])
BTC_VAL = get_stock_price(stocks["BTC"])
ETH_VAL = get_stock_price(stocks["ETH"])
GOLD_VAL = get_stock_price(stocks["GOLD"])
INTC_VAL = get_stock_price(stocks["INTC"])
LTC_VAL = get_stock_price(stocks["LTC"])

money = 5000
