from turtle import *

speed(0)
WIDTH, HEIGHT = 500, 500
L_carre = 25

screen = Screen()
screen.setup(WIDTH + 4, HEIGHT + 8)  # fudge factors due to window borders & title bar


penup()
for k in range(2*WIDTH//L_carre + 1):
    goto(-WIDTH+k*L_carre,-HEIGHT)
    pendown()
    goto(-WIDTH+k*L_carre,HEIGHT)
    penup()
for k in range(2*HEIGHT//L_carre):
    goto(-WIDTH,-HEIGHT+k*L_carre)
    pendown()
    goto(WIDTH,-HEIGHT+k*L_carre)
    penup()

# pour positionner le curseur en bas à gauche
penup()
goto(0, 0)
pendown()

# mettre le bon style de trait
width(3)
color("red")

def triangle(longueur):
    for _ in range(3):
        forward(longueur)
        left(120)
# à compléter avec maximum 5 lignes
x = 200
for _ in range(6):
    triangle(x)
    left(60)
    x = x - 25

ts = getscreen()
ts.getcanvas().postscript(file="img_exo_triangles.eps")

done()