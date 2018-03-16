import pygame

pygame.init()


GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

SCREENWIDTH = 400
SCREENHEIGHT = 500

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Basket Game")

# Allowing the user to close the window...
playing = True
clock = pygame.time.Clock()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # X pour fermer le jeu
                playing = False

    # Couleurs fond
    screen.fill(WHITE)

    # Refresh
    pygame.display.flip()

    # 60FPS
    clock.tick(60)

pygame.quit()
