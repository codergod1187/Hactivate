import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import yfinance as yf
import io
import base64
from datetime import datetime

# Function to load the saved balance from a file
def load_balance():
    try:
        with open("balance.txt", "r") as file:
            balance = float(file.read().strip())  # Read balance from file and convert to float
            return balance
    except FileNotFoundError:
        # If the file doesn't exist, return the default balance
        return 100000

# Function to save the balance to a file
def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(f"{balance:.2f}")  # Save balance to file with two decimal places

# Initial balance loaded from the file
balance = load_balance()

# Portfolio (inventory) - stores stock symbols and quantities
portfolio = {}

# Function to log actions (including balance and portfolio updates)
def log_balance(action, stock_symbol, price, balance, portfolio):
    with open("balance_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {action} {stock_symbol} at ${price:.2f}, Remaining Balance: ${balance:.2f}, Portfolio: {portfolio}\n")

# Function to fetch stock data and plot candlestick chart with moving averages
def plot_stock(stock_symbol):
    try:
        # Fetch stock data from Yahoo Finance
        stock_data = yf.download(stock_symbol, start='1995-01-01', end='2020-01-01')

        # Calculate moving averages
        stock_data['MA_10'] = stock_data['Close'].rolling(window=10).mean()
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()

        # Create candlestick chart
        fig = plt.figure(figsize=(7, 5))
        ax1 = fig.add_subplot(111)

        # Plot the closing price and moving averages
        ax1.plot(stock_data['Close'], label=f'{stock_symbol} Close', color='black')
        ax1.plot(stock_data['MA_10'], label='MA 10', color='orange')
        ax1.plot(stock_data['MA_20'], label='MA 20', color='green')
        
        # Add labels and legend
        ax1.set_title(f'{stock_symbol} Stock Price and Moving Averages')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price (USD)')
        ax1.legend()
        ax1.grid(True)

        # Save plot to a BytesIO object and encode as base64
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')  # Return base64-encoded image

    except Exception as e:
        # Show error message if fetching data fails
        messagebox.showerror("Error", f"Failed to fetch stock data: {e}")
        return None

# Function to handle the "Buy" action
def buy_stock(stock_symbol, price):
    global balance, portfolio
    if balance >= price:  # Check if there is enough balance
        balance -= price  # Deduct the price of the stock from the balance
        # Add stock to portfolio or increase quantity if already owned
        if stock_symbol in portfolio:
            portfolio[stock_symbol] += 1
        else:
            portfolio[stock_symbol] = 1
        
        # Log the action (buy)
        log_balance("Bought", stock_symbol, price, balance, portfolio)
        save_balance(balance)  # Save the updated balance to file
        messagebox.showinfo("Action", f"Bought 1 share of {stock_symbol} at ${price:.2f}. Remaining balance: ${balance:.2f}")
        update_balance_label()  # Update balance label in the main window
    else:
        messagebox.showwarning("Insufficient Funds", "You do not have enough balance to make this purchase.")  # Show warning if insufficient funds

# Function to handle the "Sell" action
def sell_stock(stock_symbol, price):
    global balance, portfolio
    if stock_symbol in portfolio and portfolio[stock_symbol] > 0:  # Check if stock is in portfolio and has a quantity > 0
        balance += price  # Add the selling price to balance
        portfolio[stock_symbol] -= 1  # Decrease stock quantity
        if portfolio[stock_symbol] == 0:
            del portfolio[stock_symbol]  # Remove stock from portfolio if quantity reaches 0
        
        # Log the action (sell)
        log_balance("Sold", stock_symbol, price, balance, portfolio)
        save_balance(balance)  # Save the updated balance to file
        messagebox.showinfo("Action", f"Sold 1 share of {stock_symbol} at ${price:.2f}. New balance: ${balance:.2f}")
        update_balance_label()  # Update balance label in the main window
    else:
        messagebox.showwarning("No Stock to Sell", f"You don't have any shares of {stock_symbol} to sell.")  # Show warning if no stock to sell

# Function to update balance label in the main window
def update_balance_label():
    balance_label.config(text=f"Balance: ${balance:.2f}")  # Update label with current balance

# Function to display the stock chart and details in the Tkinter window
def display_stock():
    stock_symbol = stock_symbol_entry.get().upper()  # Get stock symbol from entry widget and convert to uppercase
    
    if not stock_symbol:  # Show warning if no stock symbol is entered
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

        # Display latest price
        stock_data = yf.Ticker(stock_symbol).history(period="1d")
        latest_price = stock_data['Close'].iloc[-1]

        price_label = Label(stock_window, text=f"Latest Price: ${latest_price:.2f}", font=("Arial", 14))
        price_label.pack(pady=10)

        # Create Buy and Sell Buttons with images
        buy_button = Button(stock_window, text="Buy", image=img_buy, compound="left", command=lambda: buy_stock(stock_symbol, latest_price))
        buy_button.pack(side="left", padx=10, pady=10)

        sell_button = Button(stock_window, text="Sell", image=img_sell, compound="left", command=lambda: sell_stock(stock_symbol, latest_price))
        sell_button.pack(side="right", padx=10, pady=10)

# Function to display the portfolio (inventory) of owned stocks
def display_portfolio():
    portfolio_window = tk.Toplevel()
    portfolio_window.title("Your Stock Portfolio")
    
    # Display portfolio content
    portfolio_text = ""
    if portfolio:
        for stock, qty in portfolio.items():
            portfolio_text += f"{stock}: {qty} shares\n"
    else:
        portfolio_text = "Your portfolio is empty."
    
    portfolio_label = Label(portfolio_window, text=portfolio_text, font=("Arial", 14))
    portfolio_label.pack(pady=20)

# Set up the main Tkinter window
window = tk.Tk()
window.title("Stock Market Simulator Dashboard")

# Create the input field and button to enter stock symbol
input_label = Label(window, text="Enter Stock Symbol (e.g., MSFT, AAPL):", font=("Arial", 12))
input_label.pack(pady=20)

stock_symbol_entry = Entry(window, font=("Arial", 14), width=20)
stock_symbol_entry.pack(pady=10)

# Load images for the buttons (make sure the images are in the same directory or provide the full path)
img_buy = ImageTk.PhotoImage(Image.open("Buy.png").resize((30, 30)))  # Resizing image to fit the button
img_sell = ImageTk.PhotoImage(Image.open("Sell.png").resize((30, 30)))

# Create balance label
balance_label = Label(window, text=f"Balance: ${balance:.2f}", font=("Arial", 14))
balance_label.pack(pady=10)

# Button to fetch and display stock chart
fetch_button = Button(window, text="Fetch Stock Data", font=("Arial", 12), command=display_stock)
fetch_button.pack(pady=20)

# Button to display portfolio (inventory)
portfolio_button = Button(window, text="View Portfolio", font=("Arial", 12), command=display_portfolio)
portfolio_button.pack(pady=20)

# Run the Tkinter event loop to display the window
window.mainloop()
