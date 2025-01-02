class Pile:
    "classe pile non bornée"
    
    def __init__(self, L = []):
        """initialisation d'une pile vide"""
        self.L = list(L)
    
    def est_vide(self):
        """teste si la pile est vide"""
        return self.L == []

    def depile(self):
        assert not self.est_vide(), 'Pile vide'
        return self.L.pop()

    def empile(self, x):
        "empile x sur la pile"
        self.L.append(x)

    def sommet(self):
        "renvoie le sommet de la pile"
        assert not self.est_vide(), 'Pile vide'
        return self.L[-1]

    def __repr__(self):
        """Pour l'affichage"""
        a_afficher = ['T                 T']
        for e in self.L[::-1]:
            chaine = str(e)
            if len(chaine) > 15:
                chaine = chaine[:10] + '[...]'
            a_afficher.append('| {:^15} |'.format(chaine))
        a_afficher.append('\_________________/')
        return "\n".join(a_afficher)

    def __del__(self) :
        del self.L
