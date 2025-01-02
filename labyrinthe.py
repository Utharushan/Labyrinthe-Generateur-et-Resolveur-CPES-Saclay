from random import randint, choice
from class_graphe import *
from pile import *


def liste_voisins(case, vus, g):
    """
    Renvoie la liste des cases voisines non visitées pour une case donnée dans une matrice.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - case : Tuple représentant la position actuelle sous la forme (i, j).
    - vus : Ensemble des cases déjà visitées.
    - g : Objet du type GrapheM représentant le labyrinthe.
    ------------------------------------------------------------------------------------------------
    Détermine les voisins potentiels de la case en tenant compte des limites du labyrinthe
    et retourne uniquement les voisins qui n'ont pas encore été visités.
    ------------------------------------------------------------------------------------------------
    Renvoie :
    - Une liste des coordonnées des cases voisines non visitées.
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
    Ajoute un arc dans le graphe pour relier deux sommets adjacents.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - g : Objet du type GrapheM représentant le labyrinthe.
    - pos : Tuple représentant la position actuelle sous la forme (i, j).
    - direction : Tuple représentant la case voisine à connecter.
    ------------------------------------------------------------------------------------------------
    Traduit les coordonnées matricielles (i, j) en indices de sommets pour le graphe
    et crée un arc entre ces deux sommets dans le graphe.
    ------------------------------------------------------------------------------------------------
    Ne renvoie rien (modifie le graphe en place).
    """
    i1, j1 = pos
    i2, j2 = direction
    s1 = g.l * i1 + j1 
    s2 = g.l * i2 + j2 
    g.ajouter_arc(s1, s2)
    

def generer_laby(l, h):
    """
    Génère un labyrinthe aléatoire représenté sous forme de graphe.
    ------------------------------------------------------------------------------------------------
    Prend en entrée :
    - l : Entier représentant la largeur du labyrinthe (nombre de colonnes).
    - h : Entier représentant la hauteur du labyrinthe (nombre de lignes).
    ------------------------------------------------------------------------------------------------
    Utilise une approche par backtracking avec une pile pour générer un labyrinthe connexe.
    Chaque case est représentée comme un sommet dans un graphe. Les arcs du graphe
    correspondent aux passages entre cases (destruction des murs).
    ------------------------------------------------------------------------------------------------
    Renvoie :
    - Un objet GrapheM représentant le labyrinthe généré.
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

