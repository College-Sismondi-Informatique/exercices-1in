from robot import *

initExoRobot(3, 7, # taille de la grille
             # positions des obstacles
             [[0],[0,2],[0,2],[0,2],[0,2],[2],[0,1,2]],
             [0,5], # position du drapeau
             [2,0]  # position du robot au départ
             )
init("Exercice 214")

# à compléter avec les instructions haut(n), bas(n), gauche(n),
# droite(n) qui permettent de déplacer le robot de n cases

fin_robot()
