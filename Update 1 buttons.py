import pygame

pygame.init()

screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("TradeTactiX")

exit_img = pygame.image.load("Exit_btn.png").convert_alpha()
start_img = pygame.image.load("start_btn.png").convert_alpha()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

exit_button = Button(300, 400, exit_img)
start_button = Button(300, 300, start_img)

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))  # Background color


    start_button.draw(screen)
    exit_button.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if exit_button.is_clicked(event):
            running = False  # Quit game when exit button is clicked

    pygame.display.update()  # Update display

pygame.quit()
