import pygame
import traceback
from pygame.locals import *
import sys
from algorithmes import *
from labyrinthe import generer_laby


TAILLE_FENETRE = 700
BUTTON_CHEMIN = pygame.Rect(TAILLE_FENETRE + 10, 10, 220, 50)
BUTTON_JOUER = pygame.Rect(TAILLE_FENETRE + 10, 80, 220, 50)
BUTTON_TAILLE = pygame.Rect(TAILLE_FENETRE + 10, 150, 220, 50) 
BUTTON_DIJKSTRA = pygame.Rect(TAILLE_FENETRE + 10, 220, 220, 50)
BUTTON_ASTAR = pygame.Rect(TAILLE_FENETRE + 10, 290, 220, 50)
BUTTON_SYNCHRO = pygame.Rect(TAILLE_FENETRE + 10, 360, 220, 50)


def afficher_entree_sortie(fenetre, laby):
    """
    Affiche l'entrée (en vert) et la sortie (en rouge) du labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe sous forme de graphe.
    ------------------------------------------------------------------------------------------------
    Dessine des cercles représentant l'entrée et la sortie du labyrinthe sur la surface donnée.
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h
    # coordonnées de l'entrée (0, 0)
    x_entree, y_entree = 0, 0
    # coordonnées de la sortie (h-1, l-1)
    x_sortie, y_sortie = (laby.l - 1) * TAILLE_CASE_X, (laby.h - 1) * TAILLE_CASE_Y

    # Dessine l'entrée en vert
    pygame.draw.circle(fenetre, (0, 255, 0), (TAILLE_CASE_X // 2, TAILLE_CASE_Y // 2), min(TAILLE_CASE_X, TAILLE_CASE_Y) // 4)
    # Dessine la sortie en rouge
    pygame.draw.circle(fenetre, (255, 0, 0), (x_sortie + TAILLE_CASE_X // 2, y_sortie + TAILLE_CASE_Y // 2), min(TAILLE_CASE_X, TAILLE_CASE_Y) // 4)


def afficher_laby(fenetre, laby):
    """
    Trace le labyrinthe à partir du graphe donné
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe sous forme de graphe avec une matrice d'adjacence.
    ------------------------------------------------------------------------------------------------
    Trace les murs en blanc pour chaque case en fonction de la matrice d'adjacence du labyrinthe.
    """
    TAILLE_CASE_X = (TAILLE_FENETRE - 3) / laby.l # décalage pour pouvoir voir les bords
    TAILLE_CASE_Y = (TAILLE_FENETRE - 3) / laby.h

    for i in range(len(laby.adj)):
        x_dep = (i % laby.l) * TAILLE_CASE_X
        y_dep = (i // laby.l) * TAILLE_CASE_Y
        
        # si mur extérieur
        if i % laby.l == 0:  # gauche
            pygame.draw.line(fenetre, (255, 255, 255), (x_dep, y_dep), (x_dep, y_dep + TAILLE_CASE_Y), 1)
        if i % laby.l == laby.l - 1:  # droite
            if i != len(laby.adj) - 1:  # sauf la sortie
                pygame.draw.line(fenetre, (255, 255, 255), (x_dep + TAILLE_CASE_X, y_dep), (x_dep + TAILLE_CASE_X, y_dep + TAILLE_CASE_Y), 1)
        if i // laby.l == 0:  # haut
            pygame.draw.line(fenetre, (255, 255, 255), (x_dep, y_dep), (x_dep + TAILLE_CASE_X, y_dep), 1)
        if i // laby.l == laby.h - 1:  # bas
            if i != len(laby.adj) - 1:  # sauf la sortie
                pygame.draw.line(fenetre, (255, 255, 255), (x_dep, y_dep + TAILLE_CASE_Y), (x_dep + TAILLE_CASE_X, y_dep + TAILLE_CASE_Y), 1)

        # parcours uniquement la diagonale supérieure pour les arcs internes
        for j in range(i + 1, len(laby.adj[i])):
            if not laby.adj[i][j]:
                # coordonnées des sommets
                if j == i + 1:  # Mur à droite
                    dep = (x_dep + TAILLE_CASE_X, y_dep)
                    fin = (x_dep + TAILLE_CASE_X, y_dep + TAILLE_CASE_Y)
                elif j == i + laby.l:  # Mur en bas
                    dep = (x_dep, y_dep + TAILLE_CASE_Y)
                    fin = (x_dep + TAILLE_CASE_X, y_dep + TAILLE_CASE_Y)
                else:
                    continue # ne trace pas de mur si i et j ne sont pas voisins

                # trace le mur
                pygame.draw.line(fenetre, (255, 255, 255), dep, fin, 1)


def trouver_chemin(laby, début, fin):
    """
    Trouve un chemin reliant une position de départ à une position finale dans le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - laby : Le labyrinthe représenté sous forme de graphe.
    - début : Le sommet de départ.
    - fin : Le sommet de fin.
    ------------------------------------------------------------------------------------------------
    Renvoie un chemin sous forme de liste de sommets allant de début à fin, ou None si aucun chemin n'existe.
    """
    pile = [(début, [début])]
    deja_visite = set()

    while pile:
        (sommet, chemin) = pile.pop()
        if sommet in deja_visite:
            continue

        if sommet == fin:
            return chemin

        deja_visite.add(sommet)
        for voisin in laby.voisins(sommet):
            if voisin not in deja_visite:
                pile.append((voisin, chemin + [voisin]))
    return None


def afficher_chemin(fenetre, laby, chemin, couleur, jouer):
    """
    Affiche un chemin donné sur le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe sous forme de graphe.
    - chemin : Une liste de sommets représentant le chemin.
    - couleur : La couleur utilisée pour dessiner le chemin.
    - jouer : Booléen indiquant si le mode joueur est activé.
    ------------------------------------------------------------------------------------------------
    Trace le chemin sur le labyrinthe. Si jouer est activé, dessine aussi la position actuelle du joueur.
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h

    for i in range(len(chemin) - 1):
        x1 = (chemin[i] % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1 = (chemin[i] // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        x2 = (chemin[i + 1] % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y2 = (chemin[i + 1] // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.line(fenetre, couleur, (x1, y1), (x2, y2), 3)
    if jouer:
        if len(chemin) <= 1:
            (x2, y2) = (TAILLE_CASE_X // 2, TAILLE_CASE_Y // 2)
        pygame.draw.circle(fenetre, (255, 255, 255), (x2, y2), TAILLE_CASE_X / 3)


def dessiner_boutons(fenetre, afficher, jouer):
    """
    Dessine les boutons d'interaction de l'interface graphique.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - afficher : Booléen indiquant si le chemin doit être affiché.
    - jouer : Booléen indiquant si le mode joueur est activé.
    ------------------------------------------------------------------------------------------------
    Affiche les boutons pour activer les fonctionnalités :
    - Afficher/masquer le chemin.
    - Jouer/arrêter de jouer.
    - Changer la taille du labyrinthe.
    - Voir les algorithmes Dijkstra et A*.
    """
    couleur = (50, 230, 50) if afficher else (255, 0, 0)
    pygame.draw.rect(fenetre, couleur, BUTTON_CHEMIN)
    font = pygame.font.Font(None, 36)
    text = font.render('Afficher Chemin' if not afficher else 'Masquer Chemin', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_CHEMIN.x + 13, BUTTON_CHEMIN.y + 12))

    couleur = (255, 0, 0) if jouer else (0, 0, 225)
    pygame.draw.rect(fenetre, couleur, BUTTON_JOUER)
    font = pygame.font.Font(None, 36)
    text = font.render('Jouer' if not jouer else 'Arrêter', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_JOUER.x + 13, BUTTON_JOUER.y + 12))

    couleur = (255, 0, 0) 
    pygame.draw.rect(fenetre, couleur, BUTTON_TAILLE)
    font = pygame.font.Font(None, 36)
    text = font.render('Taille (console)', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_TAILLE.x + 13, BUTTON_TAILLE.y + 12))

    pygame.draw.rect(fenetre, (0, 255, 0), BUTTON_DIJKSTRA)
    text = font.render('Afficher Dijkstra', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_DIJKSTRA.x + 10, BUTTON_DIJKSTRA.y + 10))

    pygame.draw.rect(fenetre, (255, 0, 0), BUTTON_ASTAR)
    text = font.render('Afficher A*', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_ASTAR.x + 10, BUTTON_ASTAR.y + 10))

    pygame.draw.rect(fenetre, (0, 0, 255), BUTTON_SYNCHRO)
    text = font.render('Afficher Synchro', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_SYNCHRO.x + 10, BUTTON_SYNCHRO.y + 10))


def afficher_etapes(fenetre, laby, chemin, couleur):
    """
    Affiche les étapes d'un algorithme sur le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe représenté sous forme de graphe.
    - chemin : Une liste de sommets représentant le chemin parcouru par l'algorithme.
    - couleur : La couleur utilisée pour afficher les lignes représentant le chemin.
    ------------------------------------------------------------------------------------------------
    Affiche les étapes du chemin sur le labyrinthe en traçant les segments entre chaque paire 
    de sommets consécutifs. Ajoute un délai pour visualiser la progression.
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h

    for i in range(len(chemin) - 1):
        x1 = (chemin[i] % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1 = (chemin[i] // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        x2 = (chemin[i + 1] % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y2 = (chemin[i + 1] // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.line(fenetre, couleur, (x1, y1), (x2, y2), 3)
        pygame.display.flip()
        pygame.time.wait(10) 


def afficher_etapes_dijkstra(fenetre, laby, étapes_dijkstra):
    """
    Affiche les étapes de l'algorithme de Dijkstra sur le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe représenté sous forme de graphe.
    - étapes_dijkstra : Une liste de sommets représentant les étapes du parcours de Dijkstra.
    ------------------------------------------------------------------------------------------------
    Affiche chaque étape de Dijkstra en dessinant des cercles verts sur le labyrinthe. 
    Le chemin final trouvé par Dijkstra est ensuite affiché.
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h

    for dijkstra_pos in étapes_dijkstra:
        # Afficher les étapes de Dijkstra en vert
        x1_d = (dijkstra_pos % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1_d = (dijkstra_pos // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.circle(fenetre, (0, 255, 0), (x1_d + 1, y1_d + 1), TAILLE_CASE_X / 4)

        pygame.display.flip()
        pygame.time.wait(10)  # Délai pour observer la progression
    afficher_chemin(fenetre, laby, dijkstra(laby, 0, laby.l * laby.h - 1), (0, 255, 0), False)
    pygame.time.wait(1000)
    afficher = False


def afficher_etapes_astar(fenetre, laby, étapes_astar):
    """
    Affiche les étapes de l'algorithme A* sur le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe représenté sous forme de graphe.
    - étapes_astar : Une liste de sommets représentant les étapes du parcours de A*.
    ------------------------------------------------------------------------------------------------
    Affiche chaque étape de A* en dessinant des cercles rouges sur le labyrinthe.
    Le chemin final trouvé par A* est ensuite affiché.
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h

    for astar_pos in étapes_astar:
        # Afficher les étapes de A* en rouge
        x1_a = (astar_pos % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1_a = (astar_pos // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.circle(fenetre, (255, 0, 0), (x1_a - 1, y1_a - 1), TAILLE_CASE_X / 4)
        
        pygame.display.flip()
        pygame.time.wait(10)  # Délai pour observer la progression
    afficher_chemin(fenetre, laby, astar(laby, 0, laby.l * laby.h - 1), (255, 0, 0), False)
    pygame.time.wait(1000)  

            
def afficher_etapes_paralleles(fenetre, laby, étapes_dijkstra, étapes_astar):
    """
    Affiche les étapes des algorithmes de Dijkstra et A* en parallèle sur le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - fenetre : La surface Pygame où dessiner.
    - laby : Le labyrinthe représenté sous forme de graphe.
    - étapes_dijkstra : Une liste de sommets représentant les étapes du parcours de Dijkstra.
    - étapes_astar : Une liste de sommets représentant les étapes du parcours de A*.
    ------------------------------------------------------------------------------------------------
    Affiche simultanément les étapes de Dijkstra (cercles verts) et de A* (cercles rouges).
    Le chemin final trouvé est ensuite affiché avec une couleur différente (cyan).
    """
    TAILLE_CASE_X = TAILLE_FENETRE / laby.l
    TAILLE_CASE_Y = TAILLE_FENETRE / laby.h

    for dijkstra_pos, astar_pos in zip(étapes_dijkstra, étapes_astar):
        # Afficher les étapes de Dijkstra en vert
        x1_d = (dijkstra_pos % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1_d = (dijkstra_pos // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.circle(fenetre, (0, 255, 0), (x1_d + 1, y1_d + 1), TAILLE_CASE_X / 4)
        
        # Afficher les étapes de A* en rouge
        x1_a = (astar_pos % laby.l) * TAILLE_CASE_X + TAILLE_CASE_X // 2
        y1_a = (astar_pos // laby.l) * TAILLE_CASE_Y + TAILLE_CASE_Y // 2
        pygame.draw.circle(fenetre, (255, 0, 0), (x1_a - 1, y1_a - 1), TAILLE_CASE_X / 4)
        
        pygame.display.flip()
        pygame.time.wait(10)  # Délai pour observer la progression
    afficher_chemin(fenetre, laby, trouver_chemin(laby, 0, laby.l * laby.h - 1), (0, 255, 255), False)
    pygame.time.wait(1000)


def calcul_sommet(laby, sommet, nouveau_sommet):
    """
    Vérifie si le sommet voisin est atteignable et retourne le sommet correspondant.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - laby : Le labyrinthe représenté sous forme de graphe.
    - sommet : Le sommet actuel.
    - nouveau_sommet : Le sommet proposé pour le déplacement.
    ------------------------------------------------------------------------------------------------
    Renvoie :
    - Le nouveau sommet si le déplacement est possible (sommet voisin).
    - Le sommet actuel si le déplacement est impossible.
    """
    for v in laby.voisins(sommet):
        if nouveau_sommet == v:
            return v
    return sommet


def interface():
    """
    Initialise et gère l'interface graphique Pygame.
    ------------------------------------------------------------------------------------------------
    Fonction principale du programme, permettant :
    - De générer un labyrinthe aléatoire.
    - D'afficher et interagir avec le labyrinthe via des boutons et le clavier.
    - De visualiser les étapes des algorithmes (Dijkstra, A*) et de comparer leurs résultats.
    ------------------------------------------------------------------------------------------------
    Lancement automatique de l'interface utilisateur avec Pygame.
    """
    pygame.init()
    try:
        fenetre = pygame.display.set_mode((TAILLE_FENETRE + 250, TAILLE_FENETRE))
        laby = generer_laby(50, 50)
        pygame.display.set_caption(f"Labyrinthe {laby.l}×{laby.h}")
        afficher_laby(fenetre, laby)
        afficher_entree_sortie(fenetre, laby)

        sommet = 0
        début = 0
        fin = laby.l * laby.h - 1

        _, étapes_dijkstra = dijkstra_etapes(laby, début, fin)
        _, étapes_astar = astar_etapes(laby, début, fin)
        
        chemin = trouver_chemin(laby, début, fin)
        chemin_dijkstra = dijkstra(laby, début, fin)
        chemin_astar = astar(laby, début, fin)
        chemin_joueur = [0]
        
        afficher = False
        afficher_dijkstra = False
        afficher_astar = False
        afficher_synchro = False
        jouer = False

        continuer = True
        ok = True

        while continuer:
            fenetre.fill((0, 0, 0))
            afficher_laby(fenetre, laby)
            afficher_entree_sortie(fenetre, laby)
            dessiner_boutons(fenetre, afficher, jouer)
            if afficher and chemin:
                afficher_chemin(fenetre, laby, chemin, (255, 255, 0), jouer)
            if afficher_dijkstra and chemin_dijkstra:
                afficher_etapes_dijkstra(fenetre, laby, étapes_dijkstra)
            if afficher_astar and chemin_astar:
                afficher_etapes_astar(fenetre, laby, étapes_astar)
            if afficher_synchro:
                afficher_etapes_paralleles(fenetre, laby, étapes_dijkstra, étapes_astar)
            if jouer:
                afficher_chemin(fenetre, laby, chemin_joueur, (33, 130, 42), jouer)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if BUTTON_CHEMIN.collidepoint(event.pos):
                        afficher = not afficher
                        afficher_astar = False
                        afficher_dijkstra = False
                        afficher_synchro = False
                        
                    if BUTTON_DIJKSTRA.collidepoint(event.pos):
                        afficher_dijkstra = not afficher_dijkstra
                        afficher = False
                        afficher_astar = False
                        afficher_synchro = False

                    if BUTTON_ASTAR.collidepoint(event.pos):                        
                        afficher_astar = not afficher_astar
                        afficher = False
                        afficher_dijkstra = False
                        afficher_synchro = False

                    if BUTTON_SYNCHRO.collidepoint(event.pos):
                        afficher = True
                        afficher_synchro = not afficher_synchro
                        afficher_astar = False
                        afficher_dijkstra = False
                    
                    if BUTTON_JOUER.collidepoint(event.pos):
                        chemin_joueur = [0]
                        sommet = 0
                        jouer = not jouer
                        afficher = False
                        afficher_astar = False
                        afficher_dijkstra = False
                        afficher_synchro = False

                    if BUTTON_TAILLE.collidepoint(event.pos):
                        longueur = int(input("Quelle longueur ? "))
                        hauteur = int(input("Quelle hauteur ? "))
                        print()
                        laby = generer_laby(longueur, hauteur)
                        pygame.display.set_caption(f"Labyrinthe {laby.l}×{laby.h}")
                        fin = laby.l * laby.h - 1
                        chemin = trouver_chemin(laby, début, fin)
                        chemin_dijkstra = dijkstra(laby, début, fin)
                        chemin_astar = astar(laby, début, fin)
                        chemin_joueur = [0]
                        sommet = 0
                        _, étapes_dijkstra = dijkstra_etapes(laby, début, fin)
                        _, étapes_astar = astar_etapes(laby, début, fin)
                        
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key==pygame.K_RETURN:
                        afficher = not afficher
                    if event.key==pygame.K_d:
                        afficher_dijkstra = not afficher_dijkstra
                    if event.key==pygame.K_a:
                        afficher_astar = not afficher_astar

                    # Joueur
                    if jouer:
                        ancien = sommet
                        # récupération des instructions
                        if event.key == pygame.K_LEFT:
                            sommet = calcul_sommet(laby, sommet, sommet - 1)
                        elif event.key == pygame.K_RIGHT:
                            sommet = calcul_sommet(laby, sommet, sommet + 1)
                        elif event.key == pygame.K_UP:
                            sommet = calcul_sommet(laby, sommet, sommet - laby.l)
                        elif event.key == pygame.K_DOWN:
                            sommet = calcul_sommet(laby, sommet, sommet + laby.l)

                        # mise à jour du chemin
                        if sommet != ancien:
                            if len(chemin_joueur) < 2:
                                chemin_joueur.append(sommet)
                            else:
                                if chemin_joueur[-2] == sommet:
                                    chemin_joueur.pop()
                                else:
                                    chemin_joueur.append(sommet)
                        if sommet == fin:
                            print("Félicitations !!!")
                            jouer = False
                            afficher = True
                            
            pygame.display.flip()

    except:
        traceback.print_exc()

    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
	from class_graphe import *
	from labyrinthe import *


	interface()
