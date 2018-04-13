import pygame
import math
import random
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


def print_text(text, x, y, fontsize, color):
    myfont = pygame.font.Font(None, fontsize)
    text_display = myfont.render(text, True, color)
    return screen.blit(text_display, (x, y))


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


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Basketball.png")

        self.rect = self.image.get_rect()
        self.life = 1000
        self.position = [10, 600]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.last_pos = (self.position[0], self.position[1])


    def update(self):
        global start
        self.collide()
        if start:
            self.evolution()

    def evolution(self):
        global vitesse
        self.position[0] += vitesse[0]
        self.position[1] += vitesse[1]

        vitesse[1] += 4
        vitesse[0] *= 0.99
        vitesse[1] *= 0.99
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def collide(self):
        global vitesse, force
        ball_collide = pygame.sprite.spritecollide(self, collide_group, False)
        if ball_collide:
            CoeffRebond = 0.7
            #vitesse = [int(math.cos(alphaRad) * force) * CoeffRebond, int(-math.sin(alphaRad) * force) * CoeffRebond]
            vitesse = [int(vitesse[0]*CoeffRebond),-int(vitesse[1]*CoeffRebond)]

class Panier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/panier_basket.png")

        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 100


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Sol.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 700


# References aux classes
ball = Ball()
panier = Panier()
sol = Sol()

# Les sprites du jeu
balls_group = pygame.sprite.Group()
balls_group.add(ball)

collide_group = pygame.sprite.Group()
collide_group.add(sol, panier)

all_sprite_group = pygame.sprite.Group()
all_sprite_group.add(balls_group, collide_group)

force = 10
alpha = 45

###
start = False


playing = True
clock = pygame.time.Clock()
vitesse = 0

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_x:  # X pour fermer le jeu
                playing = False
            if event.key == pygame.K_SPACE:
                alphaRad = math.radians(alpha)
                vitesse = [math.cos(alphaRad) * force, -math.sin(alphaRad) * force]
                start = True

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        force -= 1
    if key[pygame.K_RIGHT]:
        force += 1
    if key[pygame.K_UP]:
        alpha += 1
    if key[pygame.K_DOWN]:
        alpha -= 1

    if force > 100:
        force = 1
    if force < 0:
        force = 0
    if alpha > 90:
        alpha = 90
    if alpha < 0:
        alpha = 0

    ball.update()

    # Couleurs fond
    screen.fill(BLACK)
    all_sprite_group.draw(screen)
    print_text(str(force), 900, 10, 20, WHITE)
    print_text(str(alpha), 900, 30, 20, WHITE)
    print_text(str(vitesse), 900, 50, 20, WHITE)

    # Refresh
    pygame.display.flip()

    # 60FPS
    clock.tick(60)


pygame.quit()


