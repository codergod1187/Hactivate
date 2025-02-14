import pygame
import stock_data  
import importlib
import time

pygame.init()


WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stock Market Simulator")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
PURPLE = (120, 100, 200)
LIGHT_GREY = (200, 200, 200)  
HOVER_COLOR = (220, 220, 220)  
CLICK_LIGHTER = (230, 230, 230)  


title_font = pygame.font.SysFont("Arial", 40, bold=True)
stock_font = pygame.font.SysFont("Arial", 25)


user_img = pygame.image.load("user.png")
trade_img = pygame.image.load("trade.png")
dashboard_img = pygame.image.load("dashboard.png")


button_width, button_height = user_img.get_size()


button_y = HEIGHT - button_height - 20  
user_button = pygame.Rect(50, button_y, button_width, button_height)
trade_button = pygame.Rect(250, button_y, button_width, button_height)
dashboard_button = pygame.Rect(450, button_y, button_width, button_height)

trade_clicked = False  


def get_stock_data():
    importlib.reload(stock_data)
    return {
        "AAPL": stock_data.AAPL_VAL,
        "BTC/USD": stock_data.BTC_VAL,
        "ETH/USD": stock_data.ETH_VAL,
        "Gold": stock_data.GOLD_VAL,
        "INTC": stock_data.INTC_VAL,
        "LTC/USD": stock_data.LTC_VAL
    }


stocks = get_stock_data()
prev_stocks = stocks.copy()
last_update = time.time()
green_display_time = {key: 0 for key in stocks}


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
            if stocks[key] != prev_stocks[key]:  
                green_display_time[key] = time.time() + 2  

    
    pygame.draw.rect(screen, PURPLE, (0, 0, WIDTH, 180))

  
    money_text = title_font.render(f"Money: ${money}", True, WHITE)
    screen.blit(money_text, (50, 50))

    
    y_offset = 200
    for stock, value in stocks.items():
        stock_rect = pygame.Rect(50, y_offset, 200, 30)  

       
        if stock_rect.collidepoint(mouse_x, mouse_y): 
            color = HOVER_COLOR  
        elif time.time() < green_display_time[stock]: 
            color = GREEN
        else:
            color = BLACK 

      
        stock_text = stock_font.render(f"{stock}: ${value:.2f}", True, color)
        screen.blit(stock_text, (50, y_offset))

        y_offset += 50

   
    user_hover = user_button.collidepoint(mouse_x, mouse_y)
    trade_hover = trade_button.collidepoint(mouse_x, mouse_y)
    dashboard_hover = dashboard_button.collidepoint(mouse_x, mouse_y)

 
    if user_hover:
        pygame.draw.rect(screen, LIGHT_GREY, user_button, border_radius=5)
    screen.blit(user_img, (50, button_y))

    if trade_hover or trade_clicked:
        pygame.draw.rect(screen, CLICK_LIGHTER if trade_clicked else LIGHT_GREY, trade_button, border_radius=5)
    screen.blit(trade_img, (250, button_y))

    if dashboard_hover:
        pygame.draw.rect(screen, LIGHT_GREY, dashboard_button, border_radius=5)
    screen.blit(dashboard_img, (450, button_y))

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

      
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
