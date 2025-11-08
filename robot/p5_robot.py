import p5
import time

# --- Configuration de la grille ---
cols = 10
rows = 10
cell_size = 50  # taille d'une case en pixels

# --- Position initiale du robot (col, row) ---
robot_col = 0
robot_row = rows - 1  # en bas à gauche

# Robot
x_robot = cell_size//10
y_robot = cell_size//1.5
vx = vy = 1
i = 0

events = []
event = None

def setup():
    p5.createCanvas(cell_size*cols, cell_size*rows)
    
def draw_grid():
    p5.background(255)
    p5.stroke(0)
    for i in range(cols + 1):
        p5.line(i * cell_size, 0, i * cell_size, cell_size*rows)
    for j in range(rows + 1):
        p5.line(0, j * cell_size, cell_size*cols, j * cell_size)


def draw():
    global x_robot, vx, y_robot, events,i, event
    draw_grid()

    
    # dessine la fleur statique
    p5.textSize(cell_size//1.5)
    
    # dessine le robot à la position variable
    p5.text("🤖", x_robot, y_robot)
    if event == "droite":
        if i < (cell_size):
            # mise à jour de la position du robot
            x_robot += vx
            i+=1 
        else:
            i = 0
            event = None
    elif event == "bas":
        if i < (cell_size):
            # mise à jour de la position du robot
            y_robot += vy
            i+=1 
        else:
            i = 0
            event = None
    elif event == "gauche":
        if i < (cell_size):
            # mise à jour de la position du robot
            x_robot -= vx
            i+=1 
        else:
            i = 0
            event = None
    elif event == "haut":
        if i < (cell_size):
            # mise à jour de la position du robot
            y_robot -= vy
            i+=1 
        else:
            i = 0
            event = None
    elif events:
        event = events.pop()

def droite():
    global events
    events.append("droite")
def bas():
    global events
    events.append("bas")
def gauche():
    global events
    events.append("gauche")
def haut():
    global events
    events.append("haut")
    
def demarrer():
    p5.run()

if __name__ == "__main__":
    droite()
    droite()
    bas()
    droite()
    demarrer()