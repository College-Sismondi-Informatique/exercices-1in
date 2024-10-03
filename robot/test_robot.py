from robot import *


initExoRobot("test", 12, 5, [[1,2,5],[1,5],[1,5,6,7,8,9],[3,9,10,11],[0,1,2,3,4,5,6,7]], [0,2], [11,4])
init("test")

gauche(3)
haut(1)
gauche(4)
haut(1)
gauche(2)
bas(1)
gauche(2)
haut(1)
fin_robot()
