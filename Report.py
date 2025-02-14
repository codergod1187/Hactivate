import tkinter as tk


user_name = "John Doe"
total_score = total_score_val
total_trades = total_trade_val
profit_trades = profit_trade_val
loss_trades = loss_trade_val
win_rate = round((profit_trades / total_trades) * 100, 2) if total_trades > 0 else 0
average_profit = average_profit_val
average_loss = average_loss_val
best_trade = best_trade_val
worst_trade = worst_trade_val


show_page = 2  


def create_score_page():
    root = tk.Tk()
    root.title("User Score Page")
    root.geometry("400x400")  

   
    tk.Label(root, text="User Total Score", font=("Arial", 16, "bold")).pack(pady=10)

    
    stats = [
        f"User: {user_name}",
        f"Total Score: {total_score}",
        f"Total Trades: {total_trades}",
        f"Profitable Trades: {profit_trades}",
        f"Loss Trades: {loss_trades}",
        f"Win Rate: {win_rate}%",
        f"Avg Profit: ${average_profit}",
        f"Avg Loss: ${average_loss}",
        f"Best Trade: ${best_trade}",
        f"Worst Trade: ${worst_trade}"
    ]

    for stat in stats:
        tk.Label(root, text=stat, font=("Arial", 12)).pack(pady=3)

    root.mainloop()

if show_page > 1:
    create_score_page()
