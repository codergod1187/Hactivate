import pygame
import stock_data  
import importlib
import time
import os  # To check if files exist

pygame.init()

screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)  
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Stock Market Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
PURPLE = (120, 100, 200)
LIGHT_GREY = (200, 200, 200)  
HOVER_COLOR = (220, 220, 220)  
CLICK_LIGHTER = (230, 230, 230)  

title_font = pygame.font.SysFont("Arial", 40, bold=True)
stock_font = pygame.font.SysFont("Arial", 25)

# Function to load images safely
def load_image(filename, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        print(f"Warning: {filename} not found!")  # Debugging if an image is missing
        return None

# Load images
user_img = load_image("user.png")
trade_img = load_image("trade.png")
dashboard_img = load_image("dashboard.png")

# Load stock logos (Crypto logos NOT included)
stock_logo_size = (40, 40)
stock_images = {
    "AAPL": load_image("AAPL_STK.png", stock_logo_size),
    "NVDA": load_image("NVDA_STK.png", stock_logo_size),
    "GOOGL": load_image("GOOGL_STK.png", stock_logo_size),
    "INTC": load_image("INTC_STK.png", stock_logo_size),
    "Gold": load_image("GOLD_STK.png", stock_logo_size)
}

# Resize bottom buttons
if user_img: user_img = pygame.transform.scale(user_img, (50, 50))
if trade_img: trade_img = pygame.transform.scale(trade_img, (50, 50))
if dashboard_img: dashboard_img = pygame.transform.scale(dashboard_img, (50, 50))

def update_button_positions():
    global WIDTH, HEIGHT, button_y, user_button, trade_button, dashboard_button
    WIDTH, HEIGHT = screen.get_size()
    button_y = HEIGHT - 70  
    center_x = WIDTH // 2  
    user_button = pygame.Rect(center_x - 100, button_y, 50, 50)
    trade_button = pygame.Rect(center_x, button_y, 50, 50)
    dashboard_button = pygame.Rect(center_x + 100, button_y, 50, 50)

update_button_positions()

trade_clicked = False  

def get_stock_data():
    importlib.reload(stock_data)  
    return {
        "AAPL": stock_data.AAPL_VAL,
        "NVDA": stock_data.NVDA_VAL,
        "GOOGL": stock_data.GOOG_VAL,
        "BTC/USD": stock_data.BTC_VAL,
        "ETH/USD": stock_data.ETH_VAL,
        "Gold": stock_data.GOLD_VAL,
        "INTC": stock_data.INTC_VAL,
        "LTC/USD": stock_data.LTC_VAL
    }

stocks = get_stock_data()
prev_stocks = stocks.copy()
last_update = time.time()

change_display_time = {key: (0, BLACK) for key in stocks}

money = stock_data.money  

running = True
while running:
    screen.fill(WHITE)  
    mouse_x, mouse_y = pygame.mouse.get_pos()  

    if time.time() - last_update >= 3:
        prev_stocks = stocks.copy()  
        stocks = get_stock_data()  
        last_update = time.time()

        for key in stocks:
            if stocks[key] > prev_stocks[key]:  
                change_display_time[key] = (time.time() + 1, GREEN)  
            elif stocks[key] < prev_stocks[key]:  
                change_display_time[key] = (time.time() + 2, RED)    
            else:
                change_display_time[key] = (0, BLACK)

    pygame.draw.rect(screen, PURPLE, (0, 0, WIDTH, 180))

    money_text = title_font.render(f"Money: ${money}", True, WHITE)
    screen.blit(money_text, (50, 50))

    trending_text = title_font.render("Trending Stocks", True, BLACK)
    screen.blit(trending_text, (50, 120))

    watchlist_text = title_font.render("Watchlist", True, BLACK)
    screen.blit(watchlist_text, (WIDTH - 250, 120))

    # Semi-transparent grey line
    transparent_surface = pygame.Surface((WIDTH, 3), pygame.SRCALPHA)
    transparent_surface.fill((180, 180, 180, 150))
    screen.blit(transparent_surface, (0, 180))

    y_offset = 200
    for stock, value in stocks.items():
        stock_rect = pygame.Rect(50, y_offset, 200, 30)  

        if stock_rect.collidepoint(mouse_x, mouse_y):
            color = HOVER_COLOR  
        elif time.time() < change_display_time[stock][0]:  
            color = change_display_time[stock][1]  
        else:
            color = BLACK  

        stock_text = stock_font.render(f"{stock}: ${value:.2f}", True, color)
        screen.blit(stock_text, (100, y_offset))  

        if stock in stock_images and stock_images[stock]:  
            screen.blit(stock_images[stock], (50, y_offset - 5))  

        y_offset += 50

    # Bottom Buttons
    user_hover = user_button.collidepoint(mouse_x, mouse_y)
    trade_hover = trade_button.collidepoint(mouse_x, mouse_y)
    dashboard_hover = dashboard_button.collidepoint(mouse_x, mouse_y)

    if user_hover:
        pygame.draw.rect(screen, LIGHT_GREY, user_button, border_radius=5)
    if user_img:
        screen.blit(user_img, (user_button.x, user_button.y))

    if trade_hover or trade_clicked:
        pygame.draw.rect(screen, CLICK_LIGHTER if trade_clicked else LIGHT_GREY, trade_button, border_radius=5)
    if trade_img:
        screen.blit(trade_img, (trade_button.x, trade_button.y))

    if dashboard_hover:
        pygame.draw.rect(screen, LIGHT_GREY, dashboard_button, border_radius=5)
    if dashboard_img:
        screen.blit(dashboard_img, (dashboard_button.x, dashboard_button.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:  
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            update_button_positions()  

        if event.type == pygame.MOUSEBUTTONDOWN:
            for stock, value in stocks.items():
                stock_rect = pygame.Rect(50, 200 + list(stocks.keys()).index(stock) * 50, 200, 30)
                if stock_rect.collidepoint(event.pos):
                    print(f"{stock} clicked!")  

            if user_button.collidepoint(event.pos):
                print("User button clicked!")
            elif trade_button.collidepoint(event.pos):
                trade_clicked = True 
                print("Trade button clicked!")
            elif dashboard_button.collidepoint(event.pos):
                print("Dashboard button clicked!")

        if event.type == pygame.MOUSEBUTTONUP:
            trade_clicked = False

    pygame.display.update()

pygame.quit()
