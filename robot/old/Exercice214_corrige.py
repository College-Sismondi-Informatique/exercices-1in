from robot import *

initExoRobot(3, 7, # taille de la grille
             # positions des obstacles
             [[0],[0,2],[0,2],[0,2],[0,2],[2],[0,1,2]],
             [0,5], # position du drapeau
             [2,0]  # position du robot au départ
             )
init("Exercice 214")

gauche(1)
bas(5)
gauche(1)

fin_robot()
