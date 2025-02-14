import pygame


pygame.init()


screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("Stock Market Simulator")


font = pygame.font.SysFont("Arial", 40)


money = 100,000 
show_money = False  
running = True
while running:

    if show_money:  
        text = font.render(f"Money: ${money}", True, (255, 255, 255))
        screen.blit(text, (50, 50))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()  # Update display

pygame.quit()
