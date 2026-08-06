#### Import librairie
from crepes import *
N = 7
init(N)


#### Découverte de l'environnement
# 1) Afficher la taille de la 3ème crêpe en partant du haut (attention, on commence à compter à 0).
print(taille(2))

# 2) Retourner sous la 4ème crêpe en partant du haut (attention, on commence à compter à 0).
retourner(3) 

# 3) Afficher la taille de toutes les crêpes avec une boucle for.
for k in range(7):
    print(taille(k))

# 4) Afficher la position de la plus grande crêpe parmi les 3 premières crêpes.
print(plusGrande(3))

# 5) Afficher si le tas est trié.
print(tasTrié())
  

#### Solution algorithme

i = N
while tasTrié() == False:
    
    tasDeCrepes = retourner(plusGrande(i))    
    
    if bruleeEnBas(0):
        retourner(0)
    
    tasDeCrepes = retourner(i-1)
    
    i = i - 1

