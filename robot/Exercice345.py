from robot import *

initExoRobot(7, 7, # taille de la grille
             # positions des obstacles
             [[0],[0,2,3,4,5,6],[0,2,6],[2,4,6],[1,4],[1,3,4,5],[3,5]],
             [2,0], # position du drapeau
             [6,6]  # position du robot au départ
             )
init("Exercice 345")

# à compléter avec les instructions haut(n), bas(n), gauche(n),
# droite(n) qui permettent de déplacer le robot de n cases

# écrire votre code ici

fin_robot()
