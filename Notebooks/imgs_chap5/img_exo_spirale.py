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

goto(-200, -200)
pendown()
width(5)

color("red")

x = 400
for _ in range(8):
    forward(x)
    left(90)
    x = x - 50

shape('turtle')
penup()
goto(-200, -200)

ts = getscreen()
ts.getcanvas().postscript(file="img_exo_spirale.png")

done()