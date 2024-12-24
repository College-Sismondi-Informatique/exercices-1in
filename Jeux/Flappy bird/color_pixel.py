import turtle
import time
from PIL import Image
import io

img = LTurtle = HTurtle = LImg = HImg = None

def get_background():
    global img, LTurtle, HTurtle , LImg , HImg
    turtle.hideturtle()
    screen = turtle.Screen()
    LTurtle = screen.window_width()
    HTurtle = screen.window_height()
    screen_image = screen.getcanvas().postscript(colormode="color")
    img = Image.open(io.BytesIO(screen_image.encode('utf-8')))
    LImg = img.size[0]
    HImg = img.size[1]
    turtle.showturtle()


def get_pixel_color(x, y):
    X = (x+LTurtle//2)*LImg/LTurtle
    Y = HImg-(y+HTurtle//2)*HImg/HTurtle
    if 0<X<LImg and 0<Y<HImg:
        color = img.getpixel((int(X), int(Y)))
        return color
    else:
        return (0,0,0)
    
if __name__ == "__main__":
    # Créer une tortue
    t = turtle.Turtle()
    def rectangle(h, l):
        t.begin_fill()
        for _ in range(2):
            t.fd(l)
            t.left(90)
            t.fd(h)
            t.left(90)
        t.end_fill()
        
    rectangle(200,200)
    t.fd(100)
    t.left(90)
    t.fd(100)

    # Capturer l'écran à la position de la tortue
    get_background()
    
    t0 = time.time()
    print(get_pixel(-10,-10))
    print(get_pixel(10,10))
    print(get_pixel(210,210))

    print(time.time()-t0)



