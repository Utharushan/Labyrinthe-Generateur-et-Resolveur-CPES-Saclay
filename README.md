# **Labyrinthe Générateur et Résolveur**
Ce projet est un générateur de labyrinthes utilisant des algorithmes aléatoires et des algorithmes de recherche de chemin pour trouver des solutions optimales. Il comprend une interface graphique développée avec Pygame permettant de visualiser le labyrinthe et les différentes solutions (par exemple, Dijkstra et A*).

---

## **Fonctionnalités**

1. **Génération de labyrinthe :**
   - Le labyrinthe est généré aléatoirement en utilisant un algorithme de génération garantissant qu'il est **résolvable** avec un unique chemin de l'entrée à la sortie.
   - Les dimensions du labyrinthe (longueur et hauteur) peuvent être personnalisées.

2. **Visualisation graphique :**
   - Le labyrinthe est affiché avec des murs et des cases, et les entrées/sorties sont marquées.
   - L'interface graphique inclut des boutons pour interagir avec le labyrinthe :
     - Afficher/masquer un chemin.
     - Voir les étapes des algorithmes de recherche de chemin (Dijkstra, A*).
     - Comparer les algorithmes en parallèle.
     - Modifier la taille du labyrinthe.

3. **Algorithmes de recherche :**
   - **Dijkstra :** Explore les chemins en minimisant la distance totale.
   - **A*** : Utilise une heuristique pour trouver des chemins rapidement.
   - **Comparaison parallèle :** Permet de visualiser les deux algorithmes simultanément.

4. **Mode joueur :**
   - Les utilisateurs peuvent résoudre le labyrinthe eux-mêmes à l'aide des touches fléchées du clavier.

---

## **Prérequis**
- **Python 3.x** 
- **Modules nécessaires** :
  - `pygame` : Interface graphique pour l'affichage et l'interaction.

### Installation des dépendances
Pour installer Pygame, utilisez la commande suivante :
```bash
pip install pygame
```

---

## **Utilisation**

### **Lancement**
Exécutez le script principal pour démarrer l'interface graphique :
```bash
python main.py
```

### **Contrôles**
1. **Souris** :
   - Cliquez sur les boutons pour :
     - Générer un chemin, voir les étapes ou changer la taille du labyrinthe.
   - Boutons disponibles :
     - `Afficher Chemin / Masquer Chemin`
     - `Afficher Dijkstra`
     - `Afficher A*`
     - `Afficher Synchro`
     - `Taille (console)`
     - `Jouer / Arrêter`

2. **Clavier** :
   - **Touche Entrée :** Afficher/Masquer le chemin.
   - **Touche `D` :** Activer/masquer l'algorithme de Dijkstra.
   - **Touche `A` :** Activer/masquer l'algorithme A*.
   - **Flèches directionnelles :** Déplacer le joueur (mode Joueur activé).

---

## **Structure du projet**

- **`main.py`** : Point d'entrée principal du programme. Définit l'interface graphique et les interactions.
- **`class_graphe.py`** : Classes et méthodes pour représenter les graphes.
- **`labyrinthe.py`** : Génération du labyrinthe et algorithmes associés.
- **`algorithmes.py`** : Implémentations des algorithmes Dijkstra et A*.
- **`pile.py`** : Classes et méthodes pour représenter les piles.

---

## **Personnalisation**
1. **Modifier la taille par défaut du labyrinthe :**
   Modifiez les dimensions dans le fichier `interface.py` :
   ```python
   laby = generer_laby(50, 50)  # Exemple de labyrinthe 50x50
   ```

2. **Délai d'animation :**
   Ajustez le délai pour visualiser les étapes des algorithmes :
   ```python
   pygame.time.wait(10)  # Modifier la valeur en millisecondes.
   ```

---

## **Exemples de capture d'écran**

1. **Génération et visualisation du labyrinthe :**
   ![image](https://github.com/user-attachments/assets/8416eee0-1e75-49f9-80f4-56c5f0fa0831)
   Entrée (en vert) et sortie (en rouge).

2. **Recherche de chemin :**
   ![image](https://github.com/user-attachments/assets/54868a27-f985-4c79-bf4a-1e5e93e78f8a)
   - Chemin en jaune (utilisateur/joueur).

---

## **Problèmes connus**
- Les labyrinthes très grands (par exemple, 200x200) peuvent ralentir l'interface graphique.
- La résolution parallèle des algorithmes peut être lente sur des machines avec des ressources limitées.

## Auteurs

- **MALAPERT Rémi**  
  [remi.malapert@hec.edu](mailto:remi.malapert@hec.edu)
- **NAMMOUS Othmane**  
  [othmane.nammous@hec.edu](mailto:othmane.nammous@hec.edu)  
- **UTHAYAKUMAR Tharushan**  
  [tharushan.uthayakumar@hec.edu](mailto:tharushan.uthayakumar@hec.edu)  

---

## Support

Pour toute question ou suggestion, contactez les auteurs via les emails ci-dessus. 
