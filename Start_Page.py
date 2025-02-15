import pygame
import subprocess
import os  # To handle file paths properly

pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("TradeTactiX")

# Load images from the "useless" folder
start_img = pygame.image.load(os.path.join("useless", "Start.png")).convert_alpha()
exit_img = pygame.image.load(os.path.join("useless", "Exit.png")).convert_alpha()

class Button:
    def __init__(self, x, y, image, scale_factor=1.1):
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scale_factor = scale_factor
        self.x, self.y = x, y

    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            new_size = (int(self.original_image.get_width() * self.scale_factor),
                        int(self.original_image.get_height() * self.scale_factor))
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Create buttons
start_button = Button(50, 250, start_img)
exit_button = Button(400, 240, exit_img)

running = True
while running:
    screen.fill((30, 30, 30))  # Background color

    # Draw buttons
    start_button.draw(screen)
    exit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if exit_button.is_clicked(event):
            running = False  # Close game

        if start_button.is_clicked(event):
            print("Starting Dashboard...")  
            pygame.quit()  # Close the menu before launching dashboard
            subprocess.run(["python", "dashboard.py"])  # Launch dashboard.py
            exit()

    pygame.display.update()

pygame.quit()
