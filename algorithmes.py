import heapq
import math

def dijkstra(laby, start, end):
    """
    Implémente l'algorithme de Dijkstra pour trouver le chemin le plus court.
    """
    tas = [(0, start, [])]
    deja_vu = set()
    minis = {start: 0}
    while tas:
        (cout, v1, chemin) = heapq.heappop(tas)
        if v1 in deja_vu:
            continue
        deja_vu.add(v1)
        chemin = chemin + [v1]
        if v1 == end:
            return chemin
        for v2 in laby.voisins(v1):
            if v2 in deja_vu:
                continue
            precedent = minis.get(v2, None)
            suivant = cout + 1  # Assuming all edges have weight 1
            if precedent is None or suivant < precedent:
                minis[v2] = suivant
                heapq.heappush(tas, (suivant, v2, chemin))
    return None

def heuristique(a, b, laby):
    """
    Heuristique pour l'algorithme A* (distance de Manhattan).
    """
    (x1, y1) = (a % laby.l, a // laby.l)
    (x2, y2) = (b % laby.l, b // laby.l)
    return abs(x1 - x2) + abs(y1 - y2)

def astar(laby, start, end):
    """
    Implémente l'algorithme A* pour trouver le chemin le plus court.
    """
    tas = [(0, start, [])]
    deja_vu = set()
    minis = {start: 0}
    while tas:
        (cout, v1, chemin) = heapq.heappop(tas)
        if v1 in deja_vu:
            continue
        deja_vu.add(v1)
        chemin = chemin + [v1]
        if v1 == end:
            return chemin
        for v2 in laby.voisins(v1):
            if v2 in deja_vu:
                continue
            precedent = minis.get(v2, None)
            suivant = cout + 1  # On suppose que toutes les arêtes ont un poids de 1
            if precedent is None or suivant < precedent:
                minis[v2] = suivant
                priorite = suivant + heuristique(v2, end, laby)
                heapq.heappush(tas, (priorite, v2, chemin))
    return None




def dijkstra_etapes(laby, start, end):
    """
    Implémente Dijkstra et retourne les étapes d'exploration.
    """
    tas = [(0, start, [])]
    deja_vu = set()
    minis = {start: 0}
    étapes = []  # Pour stocker les étapes explorées
    while tas:
        (cout, v1, chemin) = heapq.heappop(tas)
        if v1 in deja_vu:
            continue
        deja_vu.add(v1)
        étapes.append(v1)
        chemin = chemin + [v1]
        if v1 == end:
            return chemin, étapes
        for v2 in laby.voisins(v1):
            if v2 in deja_vu:
                continue
            precedent = minis.get(v2, None)
            suivant = cout + 1  # Assuming all edges have weight 1
            if precedent is None or suivant < precedent:
                minis[v2] = suivant
                heapq.heappush(tas, (suivant, v2, chemin))
    return None, étapes


def astar_etapes(laby, start, end):
    """
    Implémente A* et retourne les étapes d'exploration.
    """
    tas = [(0, start, [])]
    deja_vu = set()
    minis = {start: 0}
    étapes = []  # Pour stocker les étapes explorées
    while tas:
        (cout, v1, chemin) = heapq.heappop(tas)
        if v1 in deja_vu:
            continue
        deja_vu.add(v1)
        étapes.append(v1)
        chemin = chemin + [v1]
        if v1 == end:
            return chemin, étapes
        for v2 in laby.voisins(v1):
            if v2 in deja_vu:
                continue
            precedent = minis.get(v2, None)
            suivant = cout + 1  # Assuming all edges have weight 1
            if precedent is None or suivant < precedent:
                minis[v2] = suivant
                priorite = suivant + heuristique(v2, end, laby)
                heapq.heappush(tas, (priorite, v2, chemin))
    return None, étapes


