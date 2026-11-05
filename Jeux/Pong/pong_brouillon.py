from turtle import *
from math import sqrt

# Constantes
XPalette = 10
YPalette = 100
xTerrain = 300
yTerrain = 200

# Formes
paletteShape = ((0, 0), (0, YPalette), (XPalette, YPalette), (XPalette, 0)) 
register_shape('palette', paletteShape)
carreShape = ((0, 0), (0, XPalette), (XPalette, XPalette), (XPalette, 0)) 
register_shape('carre', carreShape)
 

wn = Screen()
wn.bgcolor('lightblue')

 
ball = Turtle(shape='circle')
ball.penup()
ball.shapesize()
ball.speed(0)
ball.goto(xTerrain//2, yTerrain//2)
ball.pendown()
ball.width(5)
for _ in range(2):
    ball.right(90)
    ball.forward(yTerrain)
    ball.right(90)
    ball.forward(xTerrain)

ball.penup()
ball.goto(0,0)
ball.setheading(45)

# turtle object
p1 = Turtle(shape='palette')
p1.penup()
p1.setheading(90)
p1.speed(0)
# p1.goto(-100, -50)
 
p2 = Turtle(shape='palette')
p2.penup()
p2.setheading(90)
p2.speed(0)
p2.goto(100, -50)
 


def check_collision(t1, t2):
    x1, y1 = t1.position()
    x2, y2 = t2.position()
    print(abs(y1 - y2), abs(x1 - x2))
    return abs(x1 + XPalette/2 - x2) <= (XPalette/2 + XPalette/2 ) and abs(y1 - y2) <= (YPalette/2 + XPalette/2 )



def deplacement():
    ball.forward(10)
    if check_collision(ball, p2):
        print("coucou")
        ball.backward(10)
        if ball.heading<90:
            ball.left(90)
        else:
            ball.left(-90)
    elif check_collision(ball, p1):
        print("coucou")
        ball.backward(10)
        if ball.heading<90:
            ball.left(-90)
        else:
            ball.left(90)
        
    wn.ontimer(deplacement, 500)


wn.onkey(lambda: p1.forward(10), 'w')
wn.onkey(lambda: p1.backward(10), 's')

wn.onkey(lambda: p2.forward(10), 'Up')
wn.onkey(lambda: p2.backward(10), 'Down')
ball.dot()
 
#  
# wn.listen()
# deplacement()
# 
# wn.mainloop()

 
 
