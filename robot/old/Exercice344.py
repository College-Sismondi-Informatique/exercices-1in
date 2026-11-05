from robot import *

initExoRobot(7, 7, # taille de la grille
             # positions des obstacles
             [[2],[0,3],[1,4],[2,5],[3,6],[4],[5]],
             [0,0], # position du drapeau
             [6,6]  # position du robot au départ
             )
init("Exercice 344")

# à compléter avec les instructions haut(n), bas(n), gauche(n),
# droite(n) qui permettent de déplacer le robot de n cases

# écrire votre code ici

fin_robot()
