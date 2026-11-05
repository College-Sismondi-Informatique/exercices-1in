# Crêpier psychorigide

## Introduction (10')
Retour sur le cours précédent sur devine mon nombre:

* Rappel de l'algorithme de résolution, 
* lien avec recherche dichotomique, par exemple dans un dictionnaire, 
* très rapidement la complexité en log2(N) en montrant démo pour N = 1e30


## Explication règles (5')

* On veut ordonner la pile
* On ne peut que retourner avec une spatule

## Activité débranchée(20')
Par groupes de 3 :

1) Ordonner 2-3 piles
2) 1 robot, 1 qui controle le robot à l'aveugle, 1 qui vérifie (5')
3) Proposer un algorithme (5')

Puis on met en commun, chaque groupe propose son algorithme, on essaie de formaliser un algorithme commun et d'identifier les instructions nécessaires : Position crepe plus grosse, Retourner, Tas trié, etc. (10')

## Activité branchée (40')

On a comme instructions à dispostion :

* `taille(n)` # Taille de la n-ème crêpe en partant du haut
* `retourner(n)` # Retourner sous la n-ème crêpe en partant du haut
* `plusGrande(n)` # Indique la position de la plus grande crêpe parmi les n premières
* `tasTrié()` # Indique si le tas est trié (True) ou pas (False).


### Découverte de l'environnement (15')

1) Afficher la taille de la 3ème crêpe en partant du haut (attention, on commence à compter à 0).
2) Retourner sous la 4ème crêpe en partant du haut (attention, on commence à compter à 0).
3) Afficher la taille de toutes les crêpes avec une boucle for.
4) Afficher la position de la plus grande crêpe parmi les 3 premières crêpes.
5) Afficher si le tas est trié.


### Implémentation de l'algorithme (15')

Implémentation de l'algorithme de tri.

## Conclusion (10')

* Correction au tableau de l'algo
* Discussion sur nombre d'étapes max


# Canevas élève

```python
#### Import librairie
from crepes import *
N = 7
init(N)


#### Découverte de l'environnement
# 1) Afficher la taille de la 3ème crêpe en partant du haut (attention, on commence à compter à 0).

# 2) Retourner sous la 4ème crêpe en partant du haut (attention, on commence à compter à 0).

# 3) Afficher la taille de toutes les crêpes avec une boucle for.

# 4) Afficher la position de la plus grande crêpe parmi les 3 premières crêpes.

# 5) Afficher si le tas est trié.



#### Implémentation de l'algorithme de tri


```
# Corrigé

```python
# Import librairie
from crepes import init, taille, retourner

N = 7
init(N)


# Instructions disponibles :
taille(3) # Taille de la 3e crêpe en partant du haut
retourner(3) # Retourner sous la 3e crêpe en partant du haut


# Fonctions nécessaires
def tasTrié():
    estTrié = True
    for i in range(N-1):
        if taille(i)> taille(i+1):
            estTrié = False
    return estTrié

def plusGrande(nombreCrepes=N):
    idx = 0
    for i in range(nombreCrepes):
        if taille(i) > taille(idx):
            idx = i            
    return idx
    

# Solution algorithme
idx = N
while tasTrié() == False:
    
    # On retourne sous la plus grande non triée
    tasDeCrepes = retourner(plusGrande(idx))
    
    # On retourne sous la 1ère non triée 
    tasDeCrepes = retourner(idx-1)
    
    idx = idx - 1
``` 
