class Pile:
    """
    Classe implémentant une pile (structure de données LIFO - Last In, First Out).
    ------------------------------------------------------------------------------------------------
    Attributs :
    - L : Liste contenant les éléments de la pile, avec le sommet de la pile à la fin de la liste.
    """
    
    def __init__(self, L = []):
        """
        Initialise une pile avec les éléments optionnels d'une liste donnée.
        ------------------------------------------------------------------------------------------------
        Paramètre :
        - L : Liste d'éléments optionnelle pour initialiser la pile (par défaut, une pile vide).
        """
        self.L = list(L)
    
    def est_vide(self):
        """
        Vérifie si la pile est vide.
        ------------------------------------------------------------------------------------------------
        Renvoie :
        - True si la pile est vide, False sinon.
        """
        return self.L == []

    def depile(self):
        """
        Retire et renvoie l'élément au sommet de la pile.
        ------------------------------------------------------------------------------------------------
        Renvoie :
        - L'élément au sommet de la pile.
        ------------------------------------------------------------------------------------------------
        Exceptions :
        - AssertionError si la pile est vide.
        """
        assert not self.est_vide(), 'Pile vide'
        return self.L.pop()

    def empile(self, x):
        """
        Ajoute un élément au sommet de la pile.
        ------------------------------------------------------------------------------------------------
        Paramètre :
        - x : L'élément à ajouter à la pile.
        """
        self.L.append(x)

    def sommet(self):
        """
        Renvoie l'élément au sommet de la pile sans le retirer.
        ------------------------------------------------------------------------------------------------
        Renvoie :
        - L'élément au sommet de la pile.
        ------------------------------------------------------------------------------------------------
        Exceptions :
        - AssertionError si la pile est vide.
        """
        assert not self.est_vide(), 'Pile vide'
        return self.L[-1]

    def __repr__(self):
        """
        Représentation en chaîne de caractères de la pile pour un affichage visuel.
        ------------------------------------------------------------------------------------------------
        Renvoie :
        - Une chaîne de caractères représentant visuellement la pile.
        """
        a_afficher = ["T                 T"]
        for e in self.L[::-1]:
            chaine = str(e)
            if len(chaine) > 15:
                chaine = chaine[:10] + "[...]"
            a_afficher.append("| {:^15} |".format(chaine))
        a_afficher.append("\_________________/")
        return "\n".join(a_afficher)

    def __del__(self) :
        """
        Détruit l'objet Pile et libère la mémoire associée.
        """
        del self.L
