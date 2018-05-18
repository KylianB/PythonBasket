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

class BasketBall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Basketball.png")

        self.rect = self.image.get_rect()
        self.life = 1000
        self.position = [random.randint(10, 600), random.randint(50, 620)]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.pos = [0, 0]
        self.pos[0] = self.position[0]
        self.pos[1] = self.position[1]

    def update(self):
        global start
        self.collide()
        # self.preview()
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
        if self.rect.y >= 720:
            self.rect.y = 720

    def preview(self):
        global pts_list, force, alpha

        pts_list = [[self.position[0], self.position[1]]]
        alphaEnRad = math.radians(alpha)
        vitesse_prev = [math.cos(alphaEnRad) * force, -math.sin(alphaEnRad) * force]
        nb_points = 20

        for i in range(nb_points):
            self.pos[0] += vitesse_prev[0]
            self.pos[1] += vitesse_prev[1]

            vitesse_prev[1] += 4
            vitesse_prev[0] *= 0.99
            vitesse_prev[1] *= 0.99

            pts_list += [[self.pos[0], self.pos[1]]]

    def reset(self):

        self.pos[0] = self.position[0]
        self.pos[1] = self.position[1]

    def collide(self):
        global vitesse, force
        ball_collide = pygame.sprite.spritecollide(self, collide_group, False)
        if ball_collide:
            coeff_rebondy = 0.9
            coeff_rebondx = 0.9
            vitesse = [vitesse[0] * coeff_rebondy, -vitesse[1] * coeff_rebondx]
            force = force * 0.9
            vitesse = [math.cos(alphaRad) * force, -math.sin(alphaRad) * force]


class Panier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = 250


class Panier2(Panier):
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base2.png")
        self.rect.x = 1060
        self.rect.y = 255


class Panier3(Panier):
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base3.png")
        self.rect.x = 1019
        self.rect.y = 255


class Panier4(Panier):
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base4.png")
        self.rect.x = 1009
        self.rect.y = 255


class Panier5(Panier):
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_pannel.png")
        self.rect.x = 1094
        self.rect.y = 149


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Sol.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 700  # References aux classes


# References aux classes
ball = BasketBall()
panier = Panier()
panier2 = Panier2()
panier3 = Panier3()
panier4 = Panier4()
panier5 = Panier5()
sol = Sol()

# Les sprites du jeu
balls_group = pygame.sprite.Group()
balls_group.add(ball)

collide_group = pygame.sprite.Group()
collide_group.add(sol, panier, panier2, panier4, panier5)

collide_score = pygame.sprite.Group()
collide_score.add(panier3)

all_sprite_group = pygame.sprite.Group()
all_sprite_group.add(balls_group, collide_group, collide_score)

force = 30
alpha = 20
alphaRad = math.radians(alpha)

###
start = False
show_line = True
playing = True
clock = pygame.time.Clock()
ball.preview()

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
                show_line = False

            if event.key == pygame.K_r:
                start = False
                show_line = True
                ball.rect.x = 10
                ball.rect.y = 600
                ball.reset()
                ball.position = [ball.rect.x, ball.rect.y]

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        force -= 1
        ball.reset()
        ball.preview()
    if key[pygame.K_RIGHT]:
        force += 1
        ball.reset()
        ball.preview()
    if key[pygame.K_UP]:
        alpha += 1
        ball.reset()
        ball.preview()
    if key[pygame.K_DOWN]:
        alpha -= 1
        ball.reset()
        ball.preview()

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
    fond = pygame.image.load("images/plage.png")
    screen.blit(fond, (0, 0))
    all_sprite_group.draw(screen)
    print_text(str(format(force, '.2f')), 900, 10, 20, WHITE)
    print_text(str(format(alpha, '.2f')), 900, 30, 20, WHITE)
    if show_line:
        pygame.draw.lines(screen, WHITE, False, pts_list)

    # Refresh
    pygame.display.flip()

    # 60FPS
    clock.tick(60)

pygame.quit()
