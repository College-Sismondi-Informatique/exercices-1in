from turtle import *

speed(0)
WIDTH, HEIGHT = 500, 500

screen = Screen()
screen.setup(WIDTH + 4, HEIGHT + 8)  # fudge factors due to window borders & title bar


penup()
for k in range(21):
    goto(-500+k*50,-500)
    pendown()
    goto(-500+k*50,500)
    penup()
for k in range(20):
    goto(-500,-500+k*50)
    pendown()
    goto(500,-500+k*50)
    penup()

# pour positionner le curseur en bas à gauche
penup()
goto(-200, -200)
pendown()

# mettre le bon style de trait
width(5)
color("red")

def triangle(longueur):
    for _ in range(3):
        forward(longueur)
        left(120)
# à compléter avec maximum 5 lignes
x = 50
for _ in range(8):
    triangle(x)
    x = 50 + x

ts = getscreen()
ts.getcanvas().postscript(file="img_exo_triangles.eps")

done()