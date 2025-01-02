from random import randint, choice
from class_graphe import *
from pile import *


def liste_voisins(case, vus, g):
    """
    Renvoie la liste des cases voisines de `case` non visitées dans une matrice de taille n x n.
    """
    l = g.l
    h = g.h
    i, j = case
    voisins = []
    if i > 0:
        voisins.append((i - 1, j))
    if i < h - 1:
        voisins.append((i + 1, j))
    if j > 0:
        voisins.append((i, j - 1))
    if j < l - 1:
        voisins.append((i, j + 1))
    return [v for v in voisins if v not in vus]


def ajoute(g, pos, direction):
    """
    Ajoute un sommet au graphe g en fonction du sommet désigné par la position actuelle pos
    et du sommet suivant désigné par la direction 
    """
    i1, j1 = pos
    i2, j2 = direction
    s1 = g.l * i1 + j1 
    s2 = g.l * i2 + j2 
    g.ajouter_arc(s1, s2)
    

def generer_laby(l, h):
    """
    génère un labyrinthe de longueur l et de hauteur h
    """
    g = GrapheM(l, h)
    i, j = randint(0, h-1), randint(0, l-1)
    #assert i < l and j < h
    pos = (i, j)

    p = Pile()
    p.empile(pos)
    
    vus = {pos}
    voisins = liste_voisins(pos, vus, g)

    while not p.est_vide():
        pos = p.sommet()
        voisins = liste_voisins(pos, vus, g)
        if len(voisins) == 0:
            p.depile()
        else:
            if len(voisins) == 1:
                p.depile()
            
            direction = choice(voisins)
            vus.add(direction)
            ajoute(g, pos, direction)
            p.empile(direction)
    return g

