import pygame

pygame.init()


# Set up the screen
screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("TradeTactiX")

# Load images
start_img = pygame.image.load("Start_Trade.png").convert_alpha()
exit_img = pygame.image.load("Exit.png").convert_alpha()  # Make sure you have "exit.png"

class Button:
    def __init__(self, x, y, image, scale_factor=1.1):
        self.original_image = image  # Store the original image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scale_factor = scale_factor  # Scale factor for hover effect
        self.x, self.y = x, y  # Store original position

    def draw(self, surface):
        # Hover effect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            new_size = (int(self.original_image.get_width() * self.scale_factor),
                        int(self.original_image.get_height() * self.scale_factor))
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)  # Keep it centered
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Reset to original

        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Create buttons (Pass images, NOT strings)
start_button = Button(50,250, start_img)
exit_button = Button(400,240, exit_img)  # Added an exit button

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))  # Background color

    # Draw buttons
    start_button.draw(screen)
    exit_button.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if exit_button.is_clicked(event):
            running = False  # Exit the program when exit button is clicked

    pygame.display.update() 

pygame.quit()
