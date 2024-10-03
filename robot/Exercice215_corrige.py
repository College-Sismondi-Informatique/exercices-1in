from robot import *

initExoRobot(7, 6, # taille de la grille
             # positions des obstacles
             [[],[1,2,3,4,5,6],[],[2,3,4,5],[2],[2]],
             [2,0], # position du drapeau
             [4,4]  # position du robot au départ
             )
init("Exercice 215")

# à compléter avec les instructions haut(n), bas(n), gauche(n),
# droite(n) qui permettent de déplacer le robot de n cases
droite(2)
haut(2)
gauche(6)
haut(2)
droite(2)

fin_robot()
