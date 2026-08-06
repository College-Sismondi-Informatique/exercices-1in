import p5
import time
from enum import Enum

# --- Globals ---
gameStatus = None
nbCasesX = 10
nbCasesY = 10
cell_size = 50
rocksPos = []       # list of [row, col]
flagPos = [0, 0]    # [row, col]
robotPos = [0, 0]   # [row, col]

robotGridX = 0      # colonne courante du robot
robotGridY = 0      # ligne courante du robot

x_robot = 0
y_robot = 0
vx = 0
vy = 0
anim_i = 0
current_event = None
events = []
event_index = 0


class GameStatus(Enum):
    RUNNING = 1
    COLLISION = 2
    WIN = 3

def initExoRobot(_nbCasesX, _nbCasesY, _rocksPos, _flagPos, _robotPos):
    global gameStatus, exoName, nbCasesX, nbCasesY, cell_size, rocksPos, flagPos, robotPos
    global robotGridX, robotGridY, x_robot, y_robot
    global current_event, events, event_index, anim_i, vx, vy

    gameStatus = GameStatus.RUNNING
    nbCasesX = _nbCasesX
    nbCasesY = _nbCasesY

    # Aplatit rocksPos du format [[cols row0], [cols row1], ...] vers [[row, col], ...]
    rocksPos = []
    for row_idx, cols in enumerate(_rocksPos):
        for col_idx in cols:
            rocksPos.append([row_idx, col_idx])

    flagPos = list(_flagPos)      # [row, col]
    robotPos = list(_robotPos)    # [row, col]
    robotGridX = robotPos[1]      # col
    robotGridY = robotPos[0]      # row

    # Taille de case auto (max 80 px)
    cell_size = min(800 // nbCasesX, 600 // nbCasesY, 80)

    offset_x = cell_size // 10
    offset_y = int(cell_size / 1.5)
    x_robot = robotGridX * cell_size + offset_x
    y_robot = robotGridY * cell_size + offset_y

    current_event = None
    events = []
    event_index = 0
    anim_i = 0
    vx = 0
    vy = 0
    
    p5.run()

def setup():
    p5.createCanvas(cell_size * nbCasesX, cell_size * nbCasesY)

def draw_grid():
    p5.background(250)
    p5.stroke(0)
    for i in range(nbCasesX + 1):
        p5.line(i * cell_size, 0, i * cell_size, cell_size * nbCasesY)
    for j in range(nbCasesY + 1):
        p5.line(0, j * cell_size, cell_size * nbCasesX, j * cell_size)

def draw():
    global x_robot, y_robot, vx, vy, anim_i, current_event, event_index, robotGridX, robotGridY, gameStatus

    draw_grid()

    emoji_size = int(cell_size / 1.5)
    p5.textSize(emoji_size)
    offset_x = cell_size // 10
    offset_y = int(cell_size / 1.5)

    # Dessine les rochers
    for rock in rocksPos:
        row, col = rock
        rx = col * cell_size + offset_x
        ry = row * cell_size + offset_y
        p5.text("🪨", rx, ry)

    # Dessine le drapeau
    fx = flagPos[1] * cell_size + offset_x
    fy = flagPos[0] * cell_size + offset_y
    p5.text("🚩", fx, fy)

    # Dessine le robot
    p5.text("🤖", x_robot, y_robot)

    # Affichage du statut (collision / victoire)
    if gameStatus == GameStatus.COLLISION:
        p5.stroke(0)
        p5.fill(255, 0, 0)
        # bandeau au centre
        p5.rect(0, nbCasesY * cell_size // 3, nbCasesX * cell_size, cell_size * 1.2)
        p5.fill(255)
        p5.textSize(emoji_size)
        p5.text("💥 Collision !", nbCasesX * cell_size // 10, nbCasesY * cell_size // 2 + emoji_size // 2)
    elif gameStatus == GameStatus.WIN:
        p5.stroke(0)
        p5.fill(0, 200, 0)
        p5.rect(0, nbCasesY * cell_size // 3, nbCasesX * cell_size, cell_size * 1.2)
        p5.fill(255)
        p5.textSize(emoji_size)
        p5.text("🏆 Victoire !", nbCasesX * cell_size // 10, nbCasesY * cell_size // 2 + emoji_size // 2)

    # Gestion des événements / animation
    if current_event is not None:
        if anim_i < cell_size:
            x_robot += vx
            y_robot += vy
            anim_i += 1
        else:
            # Fin du mouvement d'une case
            anim_i = 0
            current_event = None
            # Vérification collision / victoire
            if [robotGridY, robotGridX] in rocksPos:
                gameStatus = GameStatus.COLLISION
            if robotGridX == flagPos[1] and robotGridY == flagPos[0]:
                gameStatus = GameStatus.WIN
    elif event_index < len(events):
        if gameStatus == GameStatus.RUNNING:
            current_event = events[event_index]
            event_index += 1
            if current_event == "droite":
                robotGridX += 1
                vx = 1
                vy = 0
            elif current_event == "gauche":
                robotGridX -= 1
                vx = -1
                vy = 0
            elif current_event == "bas":
                robotGridY += 1
                vx = 0
                vy = 1
            elif current_event == "haut":
                robotGridY -= 1
                vx = 0
                vy = -1

def droite(n=1):
    global events
    events.extend(["droite"] * n)

def gauche(n=1):
    global events
    events.extend(["gauche"] * n)

def haut(n=1):
    global events
    events.extend(["haut"] * n)

def bas(n=1):
    global events
    events.extend(["bas"] * n)

def murDroite():
    for rock in rocksPos:
        if robotGridX + 1 == rock[1] and robotGridY == rock[0]:
            return True
    return False

def murGauche():
    for rock in rocksPos:
        if robotGridX - 1 == rock[1] and robotGridY == rock[0]:
            return True
    return False

def murHaut():
    for rock in rocksPos:
        if robotGridX == rock[1] and robotGridY - 1 == rock[0]:
            return True
    return False

def murBas():
    for rock in rocksPos:
        if robotGridX == rock[1] and robotGridY + 1 == rock[0]:
            return True
    return False


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    initExoRobot( 7, 4, [[3,4,5,6],[1,5,6],[1,2,3],[1,2,3,4,5]], [3,0], [3,6])

