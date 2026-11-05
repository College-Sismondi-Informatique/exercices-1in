from turtle import *
from random import randint

from color_pixel import *

### Constantes
LWorld = 1000
HWorld = 300
lObstacle = 10
ratioObstacleEspacement = 15
nObstacles = LWorld // (lObstacle*ratioObstacleEspacement)
hFenetre = lObstacle*5

### Background
def rectangle(h, l):
    begin_fill()
    for _ in range(2):
        fd(l)
        left(90)
        fd(h)
        left(90)
    end_fill()
    


def dessiner_obstacles():
    up();goto(-LWorld//2 + lObstacle*10, -HWorld//2);down() # Aller en bas à gauche
    speed(0)
    for _ in range(nObstacles):        
        hObstacle = randint(HWorld//5,(4*HWorld)//5)
        
        rectangle(hObstacle, lObstacle)
        
        up()
        left(90)
        fd(hObstacle+hFenetre)
        right(90)
        down()
        
        rectangle(HWorld- (hObstacle+hFenetre), lObstacle)
        
        up()
        right(90)        
        fd(hObstacle+hFenetre)
        left(90)
        fd(lObstacle*ratioObstacleEspacement)
        down()


#### Dessin
        
# Background
Screen().setup(width=LWorld, height=HWorld)

dessiner_obstacles()

up();goto(-LWorld//2 , 0); left(90) # Aller au début

# Init
shape('circle')
get_background()
onkey(lambda: fd(20), 'space') 
listen()


# Boucle principale du jeu
while True:
    update()
    setx(xcor() + 1)
    backward(1)
    if get_pixel_color(xcor(),ycor()) != (255,255,255):
        break;
print("Perdu")
    