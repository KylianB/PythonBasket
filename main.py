import pygame
import math


pygame.init()


GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

SCREENWIDTH = 1280
SCREENHEIGHT = 720

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Basket Game")

t = 0
# Classes


class BasketBall(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Basketball.png")

        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 500

    def update(self):
        global t
        pass
        t += 0.5
        V0 = 1
        alpha = 2
        h = self.rect.y
        self.rect.x += V0 * math.cos(alpha) * t
        self.rect.y += (-10 * t**2)/(2 + (V0 + math.sin(alpha) * t) + h )


class Panier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/panier_basket.png")

        self.rect = self.image.get_rect()
        self.rect.x = -40
        self.rect.y = 100


# References aux classes
ball = BasketBall()
panier = Panier()

# Les sprites du jeu
balls_group = pygame.sprite.Group()
balls_group.add(ball)

panier_group = pygame.sprite.Group()
panier_group.add(panier)

all_sprite_group = pygame.sprite.Group()
all_sprite_group.add(balls_group, panier_group)


###


playing = True
clock = pygame.time.Clock()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # X pour fermer le jeu
                playing = False

    ball.update()
    # Couleurs fond
    screen.fill(WHITE)
    all_sprite_group.draw(screen)

    # Refresh
    pygame.display.flip()

    # 60FPS
    clock.tick(60)

pygame.quit()