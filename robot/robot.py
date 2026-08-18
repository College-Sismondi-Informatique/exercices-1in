import p5
import time
from enum import Enum
try:
    import js
except Exception:
    pass

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

canvas_w = 0
canvas_h = 0
grid_offset_x = 0
msg_zone_height = 0


class GameStatus(Enum):
    RUNNING = 1
    COLLISION = 2
    WIN = 3
    OUTSIDE = 4

def initExoRobot(_nbCasesX, _nbCasesY, _rocksPos, _flagPos, _robotPos):
    global gameStatus, exoName, nbCasesX, nbCasesY, cell_size, rocksPos, flagPos, robotPos
    global robotGridX, robotGridY, x_robot, y_robot
    global current_event, events, event_index, anim_i, vx, vy, speed

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
    robotGridX = robotPos[0]      # col
    robotGridY = robotPos[1]      # row

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
    speed = 1.5
    
    p5.run()

def setup():
    global canvas_w, canvas_h, grid_offset_x, msg_zone_height
    emoji_size = cell_size / 1.5
    # Largeur minimum pour que les messages ne soient pas tronqués
    min_canvas_width = int(14 * emoji_size * 0.6) + 20
    canvas_w = max(cell_size * nbCasesX, min_canvas_width)
    msg_zone_height = int(cell_size * 1.5)
    canvas_h = cell_size * nbCasesY + msg_zone_height
    grid_offset_x = (canvas_w - cell_size * nbCasesX) // 2
    p5.createCanvas(canvas_w, canvas_h)

def _prng(row, col, n, max_val=1.0):
    """Génère un float pseudo-aléatoire stable basé sur les coordonnées de la case."""
    h = hash((row, col, n))
    return (abs(h) % 10000) / 10000.0 * max_val

def _draw_grass_cell(x, y, size, row, col):
    p5.noStroke()
    # Fond vert herbe éclairci
    p5.fill(151, 230, 83)
    p5.rect(x, y, size, size)
    # Taches vert foncé
    for k in range(0):
        px = x + _prng(row, col, k * 2, size)
        py = y + _prng(row, col, k * 2 + 1, size)
        p5.fill(160, 200, 90, 220)
        el_w = _prng(row, col, k * 2 + 100, size * 0.4) + size * 0.1
        el_h = _prng(row, col, k * 2 + 101, size * 0.4) + size * 0.1
        p5.ellipse(px, py, el_w, el_h)
    # Taches vert clair
    for k in range(0):
        px = x + _prng(row, col, k * 2 + 200, size)
        py = y + _prng(row, col, k * 2 + 201, size)
        p5.fill(180, 240, 120, 220)
        el_w = _prng(row, col, k * 2 + 202, size * 0.3) + size * 0.05
        el_h = _prng(row, col, k * 2 + 203, size * 0.3) + size * 0.05
        p5.ellipse(px, py, el_w, el_h)
    # Trait d'herbe
    p5.stroke(110, 160, 50)
    p5.strokeWeight(2)
    for k in range(2):
        bx = x + _prng(row, col, k * 3 + 300, size)
        by = y + _prng(row, col, k * 3 + 301, size)
        ex = bx + _prng(row, col, k * 3 + 302, size * 0.3) - size * 0.15
        ey = by + _prng(row, col, k * 3 + 303, size * 0.3) - size * 0.15
        p5.line(bx, by, ex, ey)
    p5.noStroke()

def _draw_dirt_cell(x, y, size, row, col):
    p5.noStroke()
    # Fond ocre terreux
    p5.fill(170, 130, 85)
    p5.rect(x, y, size, size)
    # Petit labour : traits brisés courts
    p5.strokeWeight(1)
    for k in range(2):
        sx = x + _prng(row, col, k * 4, size)
        sy = y + _prng(row, col, k * 4 + 1, size)
        angle = _prng(row, col, k * 4 + 2, 3.14)
        length = _prng(row, col, k * 4 + 3, size * 0.25) + size * 0.1
        ex = sx + length * p5.cos(angle)
        ey = sy + length * p5.sin(angle)
        p5.stroke(130, 95, 55, 220)
        p5.line(sx, sy, ex, ey)
    # Gravillons / cailloux gris foncés
    p5.noStroke()
    for k in range(5):
        px = x + _prng(row, col, k * 2 + 400, size)
        py = y + _prng(row, col, k * 2 + 401, size)
        p5.fill(110, 95, 80, 220)
        p5.ellipse(px, py, size * 0.1, size * 0.08)
    # Poussière sable clair
    for k in range(4):
        px = x + _prng(row, col, k * 2 + 500, size)
        py = y + _prng(row, col, k * 2 + 501, size)
        p5.fill(200, 175, 140, 220)
        p5.ellipse(px, py, size * 0.08, size * 0.08)
    p5.noStroke()

def draw_grid():
    for j in range(nbCasesY):
        for i in range(nbCasesX):
            x = i * cell_size
            y = j * cell_size
            if (i + j) % 2 == 0:
                _draw_grass_cell(x, y, cell_size, j, i)
            else:
                _draw_dirt_cell(x, y, cell_size, j, i)

    # Grille fine
    p5.strokeWeight(1)
    p5.stroke(0, 30)
    for i in range(nbCasesX + 1):
        p5.line(i * cell_size, 0, i * cell_size, cell_size * nbCasesY)
    for j in range(nbCasesY + 1):
        p5.line(0, j * cell_size, cell_size * nbCasesX, j * cell_size)
    p5.noStroke()

def draw():
    global x_robot, y_robot, vx, vy, anim_i, current_event, event_index, robotGridX, robotGridY, gameStatus

    p5.push()
    p5.translate(grid_offset_x, 0)

    draw_grid()

    # Voile léger sur le fond pour faire ressortir les emojis
    p5.noStroke()
    p5.fill(255, 255, 255, 40)
    p5.rect(0, 0, cell_size * nbCasesX, cell_size * nbCasesY)

    emoji_size = int(cell_size / 1.5)
    p5.textSize(emoji_size)
    offset_x = cell_size // 10
    offset_y = int(cell_size / 1.5)

    # Réinitialise l'état graphique pour les emojis
    p5.noStroke()
    p5.fill(0)

    def _draw_emoji(txt, cx, cy):
        p5.fill(0)
        p5.text(txt, cx, cy)

    # Dessine les rochers
    for rock in rocksPos:
        row, col = rock
        rx = col * cell_size + offset_x
        ry = row * cell_size + offset_y
        _draw_emoji("🪨", rx, ry)

    # Dessine le drapeau
    fx = flagPos[0] * cell_size + offset_x
    fy = flagPos[1] * cell_size + offset_y
    _draw_emoji("🚩", fx, fy)

    # Dessine le robot
    _draw_emoji("🤖", x_robot, y_robot)

    p5.pop()

    # Affichage du statut (collision / victoire / hors-plateau)
    if gameStatus in (GameStatus.COLLISION, GameStatus.WIN, GameStatus.OUTSIDE):
        msg_y = nbCasesY * cell_size + msg_zone_height // 2
        p5.textAlign(p5.CENTER, p5.CENTER)
        p5.textSize(emoji_size)
        if gameStatus == GameStatus.COLLISION:
            p5.fill(255, 0, 0)
            p5.text("💥 Collision !", canvas_w // 2, msg_y)
        elif gameStatus == GameStatus.WIN:
            p5.fill(0, 200, 0)
            p5.text("🏆 Victoire !", canvas_w // 2, msg_y)
            if 'js' in globals():
                js.basthon.breakpointMoveOn()
        elif gameStatus == GameStatus.OUTSIDE:
            p5.fill(255, 188, 59)
            p5.text("🪂 Revieeens !", canvas_w // 2, msg_y)
        p5.textAlign(p5.LEFT, p5.BASELINE)

    # Gestion des événements / animation
    if current_event is not None:
        if anim_i < cell_size:
            step = min(speed, cell_size - anim_i)
            x_robot += vx * step
            y_robot += vy * step
            anim_i += step
        else:
            # Fin du mouvement d'une case
            anim_i = 0
            current_event = None
            # Vérification collision / victoire
            if [robotGridY, robotGridX] in rocksPos :
                gameStatus = GameStatus.COLLISION
            if (robotGridX < 0 or robotGridX >= nbCasesX or robotGridY < 0 or robotGridY >= nbCasesY) :
                gameStatus = GameStatus.OUTSIDE
            if robotGridX == flagPos[0] and robotGridY == flagPos[1]:
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

def vitesse(n):
    global speed
    speed = n

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


#### Exercices prêts à être utilisés

# Lecon 1
def exoRobot1_0():
    initExoRobot( 3, 2, [[]], [0,0], [2,0])
    
def exoRobot1_1():
    initExoRobot( 3, 3, [[],[1],[1]], [0,2], [2,1])
    
def exoRobot1_2():
    initExoRobot(3, 7, # taille de la grille
             # positions des obstacles
             [[0],[0,2],[0,2],[0,2],[0,2],[2],[0,1,2]],
             [0,5], # position du drapeau
             [2,0]  # position du robot au départ
             )
    
def exoRobot1_3():
    initExoRobot( 7, 4, [[3,4,5,6],[1,5,6],[1,2,3],[1,2,3,4,5]], [0,3], [6,3])

    
# Lecon 2
def exoRobot2_1():
    initExoRobot(7, 6, # taille de la grille
             # positions des obstacles
             [[],[1,2,3,4,5,6],[],[2,3,4,5],[2],[2]],
             [2,0], # position du drapeau
             [4,4]  # position du robot au départ
             )
    
def exoRobot2_2():
    initExoRobot(7, 7, # taille de la grille
             # positions des obstacles
             [[2],[0,3],[1,4],[2,5],[3,6],[4],[5]],
             [0,0], # position du drapeau
             [6,6]  # position du robot au départ
             )
    
def exoRobot2_3():
    initExoRobot(7, 7, # taille de la grille
             # positions des obstacles
             [[0],[0,2,3,4,5,6],[0,2,6],[2,4,6],[1,4],[1,3,4,5],[3,5]],
             [2,0], # position du drapeau
             [6,6]  # position du robot au départ
             )

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    exoRobot2_3()

