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

vitesse = [20, -30]


def draw_life_bar(surf, x, y, life):
    """
    Dessine la barre de vie
    :param surf: surface de dessin
    :param x: int
    :param y: int
    :param life: int
    :return:
    """
    if life < 0:
        life = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (life / 1000) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Classes


class BasketBall(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Basketball.png")

        self.rect = self.image.get_rect()
        self.life = 1000
        self.position = [0, SCREENHEIGHT -1]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def update(self):
        self.evolution()

    def evolution(self):
        global vitesse
        self.position[0] += vitesse[0]
        self.position[1] += vitesse[1]

        vitesse[1] += 0.5
        vitesse[0] *= 0.99
        vitesse[1] *= 0.99
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]


class Panier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/panier_basket.png")

        self.rect = self.image.get_rect()
        self.rect.x = 1000
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
    screen.fill(BLACK)
    all_sprite_group.draw(screen)

    # Refresh
    pygame.display.flip()

    # 60FPS
    clock.tick(60)

pygame.quit()
