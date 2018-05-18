import pygame
import math
import random

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
    global start, show_line, pts_list
    start = False
    ball.reset()
    ball.position = [random.randint(10, 600), random.randint(50, 620)]  # Position de la balle au depart aleatoire
    ball.rect.x = ball.position[0]
    ball.rect.y = ball.position[1]
    show_line = True


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
        self.image = pygame.image.load("images/Basketball.png")  # Image de la balle
        self.rect = self.image.get_rect()
        self.position = [random.randint(10, 600), random.randint(50, 620)]  # Position de la balle au depart aleatoire
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.pos = [0, 0]  # Pour la previsualisation
        self.pos[0] = self.position[0]
        self.pos[1] = self.position[1]

    def update(self):
        """Fonction d'appel des fonctions principales
        de la classe.
        """
        global start
        self.collide()
        if start:
            self.evolution()

    def evolution(self):
        """Fonction pour l'evolution des positions de
        la balle.
        En fonction des frottements, apesanteur.
        """
        global vitesse
        self.position[0] += vitesse[0]
        self.position[1] += vitesse[1]

        vitesse[1] += 4  # Apesanteur
        vitesse[0] *= 0.99  # Frottements
        vitesse[1] *= 0.99
        self.rect.x = self.position[0]  # Application au coordonnees de la balle
        self.rect.y = self.position[1]
        if self.rect.y >= 720:  # Si la balle depasse le bas de l'ecran => rejoue
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

    def collide(self):
        """ Classe pour gerer les collision de la balle et des objets
        => Sol, Panier
        """
        global vitesse, force
        # Si la balle entre en collision avec le groupe de sprite collide_group
        ball_collide = pygame.sprite.spritecollide(self, collide_group, False)
        if ball_collide:
            force = force * 0.9  # On reduit la force
            vitesse = [math.cos(alphaRad) * force, -math.sin(alphaRad) * force]  # On modifie le vecteur vitesse


class Panier(pygame.sprite.Sprite):
    """ Classe du panier
    Le definit comme un sprite pour une gestion des collision plus simple.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = 250


class Panier2(Panier):
    """ Herite de Panier()
    """
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base2.png")
        self.rect.x = 1060
        self.rect.y = 255


class Panier3(Panier):
    """ Herite de Panier()
    """
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_base3.png")
        self.rect.x = 1019
        self.rect.y = 255


class PanierPanel(Panier):
    """ Herite de Panier()
    """
    def __init__(self):
        Panier.__init__(self)
        self.image = pygame.image.load("images/panier_basket_pannel.png")
        self.rect.x = 1094
        self.rect.y = 149


class Sol(pygame.sprite.Sprite):
    def __init__(self):
        """ Classse du sol
        Le definit comme un sprite pour les collisions.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Sol.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 700


# References aux classes

ball = BasketBall()
panier = Panier()
panier2 = Panier2()
panier3 = Panier3()
panier4 = PanierPanel()
sol = Sol()

# Les sprites du jeu
collide_group = pygame.sprite.Group()
collide_group.add(sol, panier, panier2)


all_sprite_group = pygame.sprite.Group()
all_sprite_group.add(ball, collide_group, panier3, panier4)

force = 30
alpha = 20
alphaRad = math.radians(alpha)

start = False
show_line = True
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
        force = 1
    if force < 0:
        force = 0
    if alpha > 90:
        alpha = 90
    if alpha < 0:
        alpha = 0

    ball.update()
    # Couleurs fond
    # fond = pygame.image.load("images/plage.png")
    # screen.blit(fond, (0, 0))
    screen.fill(BLACK)
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
