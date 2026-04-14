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


