import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import yfinance as yf
import io
import base64

# Function to fetch stock data and plot candlestick chart with moving averages
def plot_stock(stock_symbol):
    try:
        # Fetch stock data
        stock_data = yf.download(stock_symbol, start='2020-01-01', end='2025-01-01')

        # Calculate moving averages
        stock_data['MA_10'] = stock_data['Close'].rolling(window=10).mean()
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()

        # Create candlestick chart
        fig = plt.figure(figsize=(7, 5))
        ax1 = fig.add_subplot(111)

        # Candlestick plot
        ax1.plot(stock_data['Close'], label=f'{stock_symbol} Close', color='black')
        ax1.plot(stock_data['MA_10'], label='MA 10', color='orange')
        ax1.plot(stock_data['MA_20'], label='MA 20', color='green')
        
        ax1.set_title(f'{stock_symbol} Stock Price and Moving Averages')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price (USD)')
        ax1.legend()
        ax1.grid(True)

        # Save plot to a BytesIO object and encode as base64
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch stock data: {e}")
        return None

# Function to handle "Buy" action
def buy_stock(stock_symbol, price):
    messagebox.showinfo("Action", f"Bought 1 share of {stock_symbol} at ${price:.2f}")

# Function to handle "Sell" action
def sell_stock(stock_symbol, price):
    messagebox.showinfo("Action", f"Sold 1 share of {stock_symbol} at ${price:.2f}")

# Function to display the stock chart and details in the Tkinter window
def display_stock():
    stock_symbol = stock_symbol_entry.get().upper()  # Get stock symbol from entry widget
    
    if not stock_symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol")
        return
    
    # Plot the stock chart
    stock_chart = plot_stock(stock_symbol)
    
    if stock_chart:
        # Decode the base64 chart image
        stock_img_data = base64.b64decode(stock_chart)
        
        # Open image using PIL and convert to ImageTk format for Tkinter
        stock_img = Image.open(io.BytesIO(stock_img_data))
        stock_img_tk = ImageTk.PhotoImage(stock_img)

        # Create window to display chart
        stock_window = tk.Toplevel()
        stock_window.title(f"{stock_symbol} Stock Dashboard")
        
        # Add the stock chart to the window
        chart_label = Label(stock_window, image=stock_img_tk)
        chart_label.image = stock_img_tk  # Keep a reference to avoid garbage collection
        chart_label.pack(pady=20)

        # Optionally, display stock price and details (can add more details as needed)
        stock_data = yf.Ticker(stock_symbol).history(period="1d")
        latest_price = stock_data['Close'].iloc[-1]

        price_label = Label(stock_window, text=f"Latest Price: ${latest_price:.2f}", font=("Arial", 14))
        price_label.pack(pady=10)

        # Create Buy and Sell Buttons with images
        buy_button = Button(stock_window, text="Buy", image=img_buy, compound="left", command=lambda: buy_stock(stock_symbol, latest_price))
        buy_button.pack(side="left", padx=10, pady=10)

        sell_button = Button(stock_window, text="Sell", image=img_sell, compound="left", command=lambda: sell_stock(stock_symbol, latest_price))
        sell_button.pack(side="right", padx=10, pady=10)

# Set up the main Tkinter window
window = tk.Tk()
window.title("Stock Market Simulator Dashboard")

# Create the input field and button
input_label = Label(window, text="Enter Stock Symbol (e.g., MSFT, AAPL):", font=("Arial", 12))
input_label.pack(pady=20)

stock_symbol_entry = Entry(window, font=("Arial", 14), width=20)
stock_symbol_entry.pack(pady=10)

# Load images for the buttons (make sure the images are in the same directory or provide the full path)
img_buy = ImageTk.PhotoImage(Image.open("Buy.png").resize((30, 30)))  # Resizing image to fit the button
img_sell = ImageTk.PhotoImage(Image.open("Sell .png").resize((30, 30)))

# Button to fetch and display stock chart
fetch_button = Button(window, text="Fetch Stock Data", font=("Arial", 12), command=display_stock)
fetch_button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
