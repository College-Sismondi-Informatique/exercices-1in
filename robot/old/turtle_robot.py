import turtle
_d = 40
def draw_grid(size, step):
    turtle.speed(0)
    turtle.hideturtle()
    turtle.color("gray")
    
    # Draw vertical lines
    for x in range(-size, size + 1, step):
        turtle.penup()
        turtle.goto(x, -size)
        turtle.pendown()
        turtle.goto(x, size)
    
    # Draw horizontal lines
    for y in range(-size, size + 1, step):
        turtle.penup()
        turtle.goto(-size, y)
        turtle.pendown()
        turtle.goto(size, y)
    
    turtle.pu()
    turtle.goto(_d//2,_d//2)
    turtle.color("orange")
    turtle.shape("circle")
    turtle.showturtle()
    turtle.speed(1)
    
def init():
    draw_grid(200, _d)

def fini():
    turtle.done()



def haut(x):
    turtle.setheading(90)
    turtle.fd(x*_d)
    

def bas(x):
    turtle.setheading(-90)
    turtle.fd(x*_d)
    
def gauche(x):
    turtle.setheading(180)
    turtle.fd(x*_d)
    
def droite(x):
    turtle.setheading(0)
    turtle.fd(x*_d)

if __name__ == "__main__":
    init()
    haut(2)
    droite(2)
    fini()
