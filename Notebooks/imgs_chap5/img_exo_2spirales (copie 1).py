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

goto(0, -100)
pendown()
width(5)


color("blue")
right(90)

x = 50
for _ in range(3):
    forward(x)
    right(90)
    x = x + 100

color("red")
x = x - 100
for _ in range(5):
    forward(x)
    right(90)
    x = x - 50

shape('turtle')
color("black")
left(90)
penup()
goto(0, -100)

ts = getscreen()
ts.getcanvas().postscript(file="img_exo_2spirales.eps")

done()