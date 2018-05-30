import pygame
import math
import random
import time

pygame.mixer.pre_init()
pygame.init()

# Couleurs

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# Taille ecran
SCREENWIDTH = 1280
SCREENHEIGHT = 720

BAR_LENGHT = 100
BAR_HEIGHT = 10

force = 30
alpha = 20
alphaRad = math.radians(alpha)
son = pygame.mixer.Sound('son/sans_rebond.wav')
score = 0

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)  # Definition ecran
pygame.display.set_caption("Basket Game")  # Titre fenetre


#  Fonctions


def print_text(text, x, y, fontsize, color):
    """ Fonction afficher texte
    Permet l'affichage du texte (text ) a une position
    x et y avec une taille de police et une couleur
    """
    myfont = pygame.font.Font(None, fontsize)  # Police ecriture
    text_display = myfont.render(text, True, color)
    return screen.blit(text_display, (x, y))  # Affichage du texte sur ecran


def restart():
    """ Fonction pour relancer la balle.
    """
    global start, show_line, pts_list, restart, force, alpha
    start = False
    ball.position = [random.randint(10, 600), random.randint(50, 620)]  # Position de la balle au depart aleatoire
    ball.rect.x = ball.position[0]
    ball.rect.y = ball.position[1]
    ball.reset()
    ball.preview()
    show_line = True
    force = 50
    alpha = 45
    ball.left = False


def draw_force_bar(surf, x, y):
    global force, BAR_HEIGHT, BAR_LENGHT
    if force < 0:
        force = 0
    fill = (force / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_alpha_bar(surf, x, y):
    global alpha, BAR_HEIGHT, BAR_LENGHT
    if alpha < 0:
        alpha = 0
    fill = (alpha / 90) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


#  Classes


class BasketBall(pygame.sprite.Sprite):
    """Classe de la balle
    Contient les differente fonction de la balle
    """

    def __init__(self):
        """
        Parametre de base de la balle
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Basketball.png").convert_alpha()  # Image de la balle
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.position = [random.randint(10, 600), random.randint(50, 620)]  # Position de la balle au depart aleatoire
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.pos = [0, 0]  # Pour la previsualisation
        self.pos[0] = self.position[0]
        self.pos[1] = self.position[1]
        self.playing = True
        self.left = False

    def update(self):
        """Fonction d'appel des fonctions principales
        de la classe.
        """
        global start
        self.collide()
        self.marque()
        if start:
            self.evolution()

    def evolution(self):
        """Fonction pour l'evolution des positions de
        la balle.
        En fonction des frottements, apesanteur.
        """
        global vitesse
        time.sleep(0.026)  # Timer
        self.position[0] += vitesse[0]
        self.position[1] += vitesse[1]

        vitesse[1] += 4  # Apesanteur
        vitesse[0] *= 0.99  # Frottements
        vitesse[1] *= 0.99
        self.rect.x = self.position[0]  # Application au coordonnees de la balle
        self.rect.y = self.position[1]
        if self.rect.y >= 720 or self.rect.x >= 1280:  # Si la balle depasse le bas/cote de l'ecran => rejoue
            restart()

    def preview(self):
        """Creation d'une liste de points permettant le dessin
        d'une courbe de previsualisation de la trajectoire.
        """
        global pts_list, force, alpha

        alpha_rad = math.radians(alpha)  # convertion de l'angle en degree vers radian
        vitesse_prev = [math.cos(alpha_rad) * force, -math.sin(alpha_rad) * force]  # Vecteur vitesse independant
        nb_points = 20  # Nombre de points previsualiser
        pts_list = []  # Liste de points

        for i in range(nb_points):
            """Meme fonctionnement que la fonction evolution 
            """
            self.pos[0] += vitesse_prev[0]
            self.pos[1] += vitesse_prev[1]

            vitesse_prev[1] += 4
            vitesse_prev[0] *= 0.99
            vitesse_prev[1] *= 0.99

            pts_list += [[self.pos[0], self.pos[1]]]

    def reset(self):
        """Reset de la courbe de previsualisation
        """
        self.pos[0] = self.position[0]
        self.pos[1] = self.position[1]
        self.playing = True

    def collide(self):
        """ Classe pour gerer les collision de la balle et des objets
        => Sol, Panier
        """
        global vitesse, force
        # Si la balle entre en collision avec le groupe de sprite collide_group
        ball_collide = pygame.sprite.spritecollide(self, collide_group, False)
        ball_panel = pygame.sprite.spritecollide(self, collide_panel, False)

        if ball_panel:
            force *= 0.8
            vitesse = [-(math.cos(alphaRad) * force), -math.sin(alphaRad) * force]  # On modifie le vecteur vitesse
            self.left = True

        if ball_collide:
            force = force * 0.8  # On reduit la force
            if not self.left:
                vitesse = [math.cos(alphaRad) * force, -math.sin(alphaRad) * force]  # On modifie le vecteur vitesse
            else:
                vitesse = [-math.cos(alphaRad) * force, -math.sin(alphaRad) * force]  # On modifie le vecteur vitesse

    def marque(self):
        """ Fonction permet de savoir quand le joueur
        marque un panier.
        """
        global score, force
        ball_panier = pygame.sprite.collide_mask(self, panier3)
        if ball_panier and self.playing:
            force *= 0.5
            score += 2
            self.playing = False
            son.play()


class SolidEntity(pygame.sprite.Sprite):
    """ Classe des objets.
    Le definit comme un sprite pour une gestion des collision plus simple.
    Prend en paramètres une image, une position x et une position y.
    """

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


# Images
panierBase = pygame.image.load("images/panier_basket_base.png")
panierBase2 = pygame.image.load("images/panier_basket_base2.png")
panierBase3 = pygame.image.load("images/panier_basket_base3.png")
panierPanel = pygame.image.load("images/panier_basket_pannel.png")
sol_img = pygame.image.load("images/Sol.png")

# References aux classes

ball = BasketBall()
panier = SolidEntity(panierBase, 1100, 250)
panier2 = SolidEntity(panierBase2, 1073, 255)
panier3 = SolidEntity(panierBase3, 1011, 255)
panier4 = SolidEntity(panierPanel, 1094, 149)
sol = SolidEntity(sol_img, 0, 700)

# Les sprites du jeu
collide_group = pygame.sprite.Group()
collide_group.add(sol, panier)

collide_marque = pygame.sprite.Group()
collide_marque.add(panier3)

collide_panel = pygame.sprite.Group()
collide_panel.add(panier4, panier2)

all_sprite_group = pygame.sprite.Group()
all_sprite_group.add(ball, collide_group, collide_marque, collide_panel)

start = False
show_line = True
restarts = False
playing = True
clock = pygame.time.Clock()
ball.preview()

while playing:  # Boucle principale
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Echapp pour fermer le jeu
                playing = False
            if event.key == pygame.K_SPACE:
                alphaRad = math.radians(alpha)
                vitesse = [math.cos(alphaRad) * force, -math.sin(alphaRad) * force]
                start = True
                show_line = False

            if event.key == pygame.K_r:
                restart()

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
        force = 100
    if force < 0:
        force = 0
    if alpha > 90:
        alpha = 90
    if alpha < 0:
        alpha = 0

    ball.update()
    screen.fill(BLACK)
    all_sprite_group.draw(screen)
    print_text(str(format(force, '.2f')), 120, 10, 20, WHITE)
    print_text(str(format(alpha, '.2f')), 120, 30, 20, WHITE)
    print_text(str(score), 120, 50, 20, WHITE)
    print_text("Score", 80, 50, 20, WHITE)
    draw_force_bar(screen, 10, 10)
    draw_alpha_bar(screen, 10, 30)
    if show_line:
        pygame.draw.lines(screen, WHITE, False, pts_list)

    # Refresh
    pygame.display.flip()

    clock.tick(60)  # 60FPS

pygame.quit()
