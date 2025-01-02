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
    Affiche l'entrée et la sortie du labyrinthe
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
    Trace le labyrinthe issu du graphe laby.
    Pour chaque mur (arc non existant dans la matrice d'adjacence), une ligne
    blanche est tracée entre les deux sommets.
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
    Trouve un chemin du début à la fin dans le labyrinthe en utilisant DFS.
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
    Affiche le chemin trouvé sur le labyrinthe.
    laby un graphe
    chemin une liste de sommets du graphe
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
    Dessine les boutons pour
        afficher/masquer le chemin.
        jouer/arrêter de jouer
        changer la taille du labyrinthe
        afficher la recherche du chemin par Dijkstra
        afficher la recherche du chemin par A*
        afficher la recherche du chemin par les deux algorithmes en même temps
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
    Affiche les étapes de l'algorithme sur le labyrinthe.
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
    Affiche les étapes de Dijkstra sur le labyrinthe.
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
    Affiche les étapes de A* sur le labyrinthe.
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
    Affiche les étapes de Dijkstra et A* en parallèle sur le labyrinthe.
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
    for v in laby.voisins(sommet):
        if nouveau_sommet == v:
            return v
    return sommet


def interface():
    """
    Lancement de l'interface graphique avec Pygame.
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
##                if ok:
##                    couleur = (randint(0, 255), randint(0, 255), randint(0, 255))
##                    #print(couleur)
##                    ok = False
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
