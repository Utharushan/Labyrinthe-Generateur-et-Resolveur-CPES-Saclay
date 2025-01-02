
class GrapheM:
    """"graphe représenté par une matrice d'adjacence"""

    def __init__(self, l, h):
        self.n = l*h
        self.l = l
        self.h = h
        self.adj=[[False]*self.n for i in range(self.n)]

    def ajouter_arc(self,s1,s2):
        self.adj[s1][s2]=True
        self.adj[s2][s1]=True

    def arc(self,s1,s2):
        return self.adj[s1][s2]

    def voisins(self, s):
        v=[]
        for i in range(self.n):
            if self.adj[s][i]:
                v.append(i)
        return v

    def afficher(self):
        for s in range(self.n):
            print(s,"->", end="")
            for v in range(self.n):
                if self.adj[s][v]:
                    print("",v,end="")
            print()

    def degre(self, s):
        d=0
        for i in range(self.n):
            if self.adj[s][i]:
                d+=1
        return d

    def nb_arcs(self):
        n=0
        for s in range(self.n):
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        self.adj[s1][s2]=False
        self.adj[s2][s1]=False


class GrapheD:
    """"graphe représenté par un dictionnaire d'adjacence"""

    def __init__(self):
        self.adj={}

    def ajouter_sommet(self,s):
        if s not in self.adj:
            self.adj[s]=set()

    def ajouter_arc(self,s1,s2):
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].add(s2)

    def arc(self,s1,s2):
        return s2 in self.adj[s1]

    def sommets(self):
        return list(self.adj)

    def voisins(self,s):
        return self.adj[s]

    def afficher(self):
        for s in self.adj:
            if len(self.adj[s])==0:
                print(s,"{}")
            else:
                print(s,self.adj[s])

    def nb_sommets(self):
        return len(self.adj)

    def degre(self,s):
        return len(self.adj[s])

    def nb_arcs(self):
        n=0
        for s in self.adj:
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        self.adj[s1].remove(s2)


    
        



class GraphePondM:
    """"graphe pondéré représenté par une matrice d'adjacence"""

    def __init__(self,n):
        self.n=n
        self.adj=[[float('inf') if i!=j else 0 for j in range(n)] for i in range(n)]

    def ajouter_arc(self,s1,s2,p):
        self.adj[s1][s2] = p
        self.adj[s2][s1] = p
        
    def arc(self,s1,s2):
        return self.adj[s1][s2]

    def voisins(self,s):
        v=[]
        for i in range(self.n):
            if self.adj[s][i]!=0 and self.adj[s][i]!=float('inf'):
                v.append(i)
        return v

    def afficher(self):
        for s in range(self.n):
            print(s,"->", end="")
            for v in range(self.n):
                if self.adj[s][v]!=0 and self.adj[s][v]!=float('inf'):
                    print(" ",str(v)+", dist="+str(self.adj[s][v]),end="")
            print()

    def degre(self,s):
        d=0
        for i in range(self.n):
            if self.adj[s][i]!=0 and self.adj[s][i]!=float('inf'):
                d+=1
        return d

    def nb_arcs(self):
        n=0
        for s in range(self.n):
            n+=self.degre(s)
        return n

    def nb_sommets(self):
        return len(self.adj)

    def supprimer_arc(self,s1,s2):
        self.adj[s1][s2]=float('inf')
        self.adj[s2][s1]=float('inf')


class GraphePondD:
    """"graphe pondéré représenté par un dictionnaire d'adjacence"""

    def __init__(self):
        self.adj={}

    def ajouter_sommet(self,s):
        if s not in self.adj:
            self.adj[s]=[]

    def ajouter_arc(self,s1,s2,p):
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].append([s2,p])

    def arc(self,s1,s2):
        for s in self.adj[s1]:
            if s[0]==s2:
                return True
        return False

    def sommets(self):
        return list(self.adj)

    def voisins(self,s):
        L=[]
        for som in self.adj[s]:
            L.append(som[0])
        return L

    def afficher(self):
        for s in self.adj:
            if len(self.adj[s])==0:
                print(s,"[]")
            else:
                print(s,self.adj[s])

    def nb_sommets(self):
        return len(self.adj)

    def degre(self,s):
        return len(self.adj[s])

    def nb_arcs(self):
        n=0
        for s in self.adj:
            n+=self.degre(s)
        return n

    def supprimer_arc(self,s1,s2):
        for i in range(len(self.adj[s1])):
            print("src",s1)
            if self.adj[s1][i][0]==s2:
                print("dest",self.adj[s1][i][0])
                del(self.adj[s1][i])


    
        
