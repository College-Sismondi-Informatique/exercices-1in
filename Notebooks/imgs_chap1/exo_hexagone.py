from svg_turtle import SvgTurtle

t = SvgTurtle(300, 300)
t.penup()
t.goto(-50,-50)
t.pendown()
for _ in range(6):
    a = 360 / 6
    t.forward(100)
    t.left(a)

t.save_as('exo_hexagone.svg')