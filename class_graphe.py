
class GrapheM:
    """
    Représente un graphe non pondéré à l'aide d'une matrice d'adjacence.
    Les sommets sont numérotés de 0 à n-1.
    """

    def __init__(self, l, h):
        """
        Initialise un graphe de dimensions l x h.
        Chaque case représente un sommet et est initialement déconnectée.
        """
        self.n = l*h
        self.l = l
        self.h = h
        self.adj=[[False]*self.n for i in range(self.n)]

    def ajouter_arc(self,s1,s2):
        """Ajoute un arc non orienté entre les sommets s1 et s2."""
        self.adj[s1][s2]=True
        self.adj[s2][s1]=True

    def arc(self,s1,s2):
        """Retourne True si un arc existe entre s1 et s2, sinon False."""
        return self.adj[s1][s2]

    def voisins(self, s):
        """Retourne une liste des sommets voisins de s."""
        return [i for i in range(self.n) if self.adj[s][i]]

    def afficher(self):
        """Affiche la liste d'adjacence du graphe."""
        for s in range(self.n):
            print(s,"->", end="")
            for v in range(self.n):
                if self.adj[s][v]:
                    print("",v,end="")
            print()

    def degre(self, s):
        """Retourne le degré (nombre d'arcs) du sommet s."""
        d=0
        for i in range(self.n):
            if self.adj[s][i]:
                d+=1
        return d

    def nb_arcs(self):
        """Retourne le nombre total d'arcs dans le graphe."""
        n=0
        for s in range(self.n):
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        """Supprime l'arc entre les sommets s1 et s2."""
        self.adj[s1][s2]=False
        self.adj[s2][s1]=False


class GrapheD:
    """
    Représente un graphe non pondéré à l'aide d'un dictionnaire d'adjacence.
    """

    def __init__(self):
        """Initialise un graphe vide."""
        self.adj={}

    def ajouter_sommet(self,s):
        """Ajoute un sommet s au graphe s'il n'existe pas déjà."""
        if s not in self.adj:
            self.adj[s]=set()

    def ajouter_arc(self,s1,s2):
        """Ajoute un arc non orienté entre les sommets s1 et s2."""
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].add(s2)

    def arc(self,s1,s2):
        """Retourne True si un arc existe entre s1 et s2, sinon False."""
        return s2 in self.adj[s1]

    def sommets(self):
        """Retourne la liste des sommets du graphe."""
        return list(self.adj)

    def voisins(self,s):
        """Retourne la liste des sommets voisins de s."""
        return self.adj[s]

    def afficher(self):
        """Affiche la liste d'adjacence du graphe."""
        for s in self.adj:
            if len(self.adj[s])==0:
                print(s,"{}")
            else:
                print(s,self.adj[s])

    def nb_sommets(self):
        """Retourne le nombre de sommets dans le graphe."""
        return len(self.adj)

    def degre(self,s):
        """Retourne le degré (nombre d'arcs) du sommet s."""
        return len(self.adj[s])

    def nb_arcs(self):
        """Retourne le nombre total d'arcs dans le graphe."""
        n=0
        for s in self.adj:
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        """Supprime l'arc entre les sommets s1 et s2."""
        self.adj[s1].remove(s2)


class GraphePondM:
    """"
    Représente un graphe pondéré à l'aide d'une matrice d'adjacence.
    """

    def __init__(self,n):
        """Initialise un graphe pondéré de n sommets."""
        self.n=n
        self.adj=[[float('inf') if i!=j else 0 for j in range(n)] for i in range(n)]

    def ajouter_arc(self,s1,s2,p):
        """Ajoute un arc pondéré entre les sommets s1 et s2 avec un poids p."""
        self.adj[s1][s2] = p
        self.adj[s2][s1] = p
        
    def arc(self,s1,s2):
        """Retourne le poids de l'arc entre s1 et s2."""
        return self.adj[s1][s2]

    def voisins(self,s):
        """Retourne la liste des sommets voisins de s."""
        v=[]
        for i in range(self.n):
            if self.adj[s][i]!=0 and self.adj[s][i]!=float('inf'):
                v.append(i)
        return v

    def afficher(self):
        """Affiche la matrice d'adjacence du graphe."""
        for s in range(self.n):
            print(s,"->", end="")
            for v in range(self.n):
                if self.adj[s][v]!=0 and self.adj[s][v]!=float('inf'):
                    print(" ",str(v)+", dist="+str(self.adj[s][v]),end="")
            print()

    def degre(self,s):
        """Retourne le degré (nombre d'arcs) du sommet s."""
        d=0
        for i in range(self.n):
            if self.adj[s][i]!=0 and self.adj[s][i]!=float('inf'):
                d+=1
        return d

    def nb_arcs(self):
        """Retourne le nombre total d'arcs dans le graphe."""
        n=0
        for s in range(self.n):
            n+=self.degre(s)
        return n

    def nb_sommets(self):
        """Retourne le nombre de sommets dans le graphe."""
        return len(self.adj)

    def supprimer_arc(self,s1,s2):
        """Supprime l'arc entre les sommets s1 et s2."""
        self.adj[s1][s2]=float('inf')
        self.adj[s2][s1]=float('inf')


class GraphePondD:
    """"
    Représente un graphe pondéré à l'aide d'un dictionnaire d'adjacence.
    """

    def __init__(self):
        """Initialise un graphe pondéré vide."""
        self.adj={}

    def ajouter_sommet(self,s):
        """Ajoute un sommet s au graphe s'il n'existe pas déjà."""
        if s not in self.adj:
            self.adj[s]=[]

    def ajouter_arc(self,s1,s2,p):
        """Ajoute un arc pondéré entre les sommets s1 et s2 avec un poids p."""
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].append([s2,p])

    def arc(self,s1,s2):
        """Retourne le poids de l'arc entre s1 et s2."""
        for s in self.adj[s1]:
            if s[0]==s2:
                return True
        return False

    def sommets(self):
        """Retourne la liste des sommets du graphe."""
        return list(self.adj)

    def voisins(self,s):
        """Retourne la liste des sommets voisins de s."""
        L=[]
        for som in self.adj[s]:
            L.append(som[0])
        return L

    def afficher(self):
        """Affiche la liste d'adjacence du graphe."""
        for s in self.adj:
            if len(self.adj[s])==0:
                print(s,"[]")
            else:
                print(s,self.adj[s])

    def nb_sommets(self):
        """Retourne le nombre de sommets dans le graphe."""
        return len(self.adj)

    def degre(self,s):
        """Retourne le degré (nombre d'arcs) du sommet s."""
        return len(self.adj[s])

    def nb_arcs(self):
        """Retourne le nombre total d'arcs dans le graphe."""
        n=0
        for s in self.adj:
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        """Supprime l'arc entre les sommets s1 et s2."""
        for i in range(len(self.adj[s1])):
            print("src",s1)
            if self.adj[s1][i][0]==s2:
                print("dest",self.adj[s1][i][0])
                del(self.adj[s1][i])
                break        
