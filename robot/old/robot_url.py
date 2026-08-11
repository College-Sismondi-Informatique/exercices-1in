import pygame
import time
import requests
from enum import Enum
from io import BytesIO

############## Constants ############## 
gameStatus = nbCasesX = nbCasesY = rocksPos =flagPos=robotPos = WIDTH = HEIGHT = caseSizeX = caseSizeY = screen = box = grass = grass2 = robot = rocks = flag = None

RED = 200, 0, 0
BLACK = 0, 0, 0
GREEN = 0, 200, 0
DARKGREEN = 0, 100, 0
DARKBLUE = (0, 0, 128)


class GameStatus(Enum):
    RUNNING = 1
    COLLISION = 2
    WIN = 3
    NOTFOUND = 4

############## Exercices ############## 


############## Objects ##############

all_sprites_list = pygame.sprite.Group()

class ObjectSprite(pygame.sprite.Sprite):
    def __init__(self, imgPath, x=0, y=0, factor=1):
        super().__init__()
        self.imagePath = imgPath
#         self.image = pygame.image.load(imgPath)
        self.image = pygame.image.load(BytesIO(requests.get('https://github.com/College-Sismondi-Informatique/exercices-1in/blob/main/robot/images/'+imgPath+'?raw=true').content))
        self.image = pygame.transform.scale(self.image, (caseSizeX*factor, caseSizeY*factor))
        self.rect = pygame.Rect((box[x][y].left, box[x][y].top), (caseSizeX*factor, caseSizeY*factor))
        all_sprites_list.add(self)
        self.updatePosition(x,y)
 
    def updatePosition(self, x, y):
        if (x < nbCasesX) & (y < nbCasesY):
            if(int(x) == x) & (int(y) == y):
                self.x = int(x)
                self.y = int(y)
            self.rect.centerx = box[self.x][self.y].centerx +caseSizeX*(x-self.x)
            self.rect.centery = box[self.x][self.y].centery +caseSizeY*(y-self.y)

def initObjects(exoName):
    global gameStatus, nbCasesX, nbCasesY,rocksPos ,flagPos,robotPos , WIDTH , HEIGHT , caseSizeX , caseSizeY , screen , box, grass, grass2, robot, rocks, flag
#     initExo(exoName)
    #### Constants #####
    WIDTH = nbCasesX*100
    HEIGHT = nbCasesY*100
    caseSizeX = WIDTH//nbCasesX
    caseSizeY = HEIGHT//nbCasesY
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    
    # Load boxes
    box = [[0 for y in range(nbCasesY)] for x in range(nbCasesX)]
    for x in range(nbCasesX):
        for y in range(nbCasesY):
            box[x][y] = pygame.Rect((caseSizeX*x, caseSizeY*y), ((caseSizeX), (caseSizeY)))
            
    # Load grass

    grass = pygame.image.load(BytesIO(requests.get('https://github.com/College-Sismondi-Informatique/exercices-1in/blob/main/robot/images/grass.png?raw=true').content))
    grass = pygame.transform.scale(grass, (caseSizeX, caseSizeY))
#     grass2 = pygame.image.load('images/dirt.png')
    grass2 = pygame.image.load(BytesIO(requests.get('https://github.com/College-Sismondi-Informatique/exercices-1in/blob/main/robot/images/dirt.png?raw=true').content))
    grass2 = pygame.transform.scale(grass2, (caseSizeX, caseSizeY))

    # Load rock
    rocksPos2 = [0 for x in range(sum(len(x) for x in rocksPos))]
    nRocks = 0
    for i in range(len(rocksPos)):
        for j in range(len(rocksPos[i])):
            rocksPos2[nRocks] = [i, rocksPos[i][j]]
            nRocks = nRocks+1

    rocks = [0 for x in (rocksPos2)]
    for rockPos, i in zip(rocksPos2, range(len(rocksPos2))):
        rocks[i] = ObjectSprite('stone.png', rockPos[1], rockPos[0],0.8)
#         rocks[i] = ObjectSprite('images/stone.png', rockPos[1], rockPos[0],0.8)

    # Load flag
#     flag = ObjectSprite("images/flag2.png",flagPos[0], flagPos[1])
    flag = ObjectSprite("flag2.png",flagPos[0], flagPos[1])

    # Load robot
    robot = ObjectSprite("robot.png",robotPos[0], robotPos[1],0.95)
#     robot = ObjectSprite("images/robot.png",robotPos[0], robotPos[1],0.95)
    
    gameStatus = GameStatus.RUNNING

############## Functions ############## 
def init(exoName):
    initObjects(exoName)
    pygame.init()
    pygame.display.set_caption(exoName)
    disp()
    
def initExoRobot(_nbCasesX, _nbCasesY,_rocksPos ,_flagPos,_robotPos):
    global gameStatus, nbCasesX, nbCasesY,rocksPos ,flagPos,robotPos , WIDTH , HEIGHT , caseSizeX , caseSizeY , screen , box, grass, grass2, robot, rocks, flag
    nbCasesX = _nbCasesX
    nbCasesY = _nbCasesY
    rocksPos = _rocksPos
    flagPos = _flagPos
    robotPos = _robotPos

    
def exercice_robot(exoName):
    init(exoName)
    
def isCollisionObj(sprite1, sprite2):
    return (sprite1.x == sprite2.x) & (sprite1.y == sprite2.y)
    
def isCollisionGroup(sprite1, spriteGroup):
    for sprite in spriteGroup:
        if isCollisionObj(sprite1, sprite):
            return True
    return False

def disp():
    # Display map
    for x in range(nbCasesX):
        for y in range(nbCasesY):
            if (x+y)%2 == 0:
                screen.blit(grass, box[x][y])
            else:
                screen.blit(grass2, box[x][y])
    # Draw sprites
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    dispText()
    pygame.display.flip()
 
stepsNb = 1
pauseLength = 0.5
def moveRobot(dx, dy):
    global gameStatus
    for i in range(1, stepsNb+1):
        if gameStatus == GameStatus.RUNNING:
            time.sleep(pauseLength/2/stepsNb)
            robot.updatePosition(robot.x+dx*i/stepsNb, robot.y+dy*i/stepsNb)   
            if isCollisionGroup(robot, rocks):
                gameStatus = GameStatus.COLLISION
            if isCollisionObj(robot, flag):
                gameStatus = GameStatus.WIN
        disp()
    time.sleep(pauseLength/2)
        
def droite(n):
    for i in range(n):
        moveRobot(1, 0)
        
def gauche(n):
    for i in range(n):
        moveRobot(-1, 0)
        
def haut(n):
    for i in range(n):
        moveRobot(0, -1)
        
def bas(n):
    for i in range(n):
        moveRobot(0, 1)
     
def murDroite():
    for sprite in rocks:
        if (robot.x+1 == sprite.x) & (robot.y == sprite.y):
            return True
    return False
     
def murGauche():
    for sprite in rocks:
        if (robot.x-1 == sprite.x) & (robot.y == sprite.y):
            return True
    return False
     
def murHaut():
    for sprite in rocks:
        if (robot.x == sprite.x) & (robot.y-1 == sprite.y):
            return True
    return False
     
def murBas():
    for sprite in rocks:
        if (robot.x == sprite.x) & (robot.y+1 == sprite.y):
            return True
    return False
        
def dispText():
    font = pygame.font.Font('freesansbold.ttf', 64)
    if gameStatus == GameStatus.COLLISION:
        text = font.render("Collision !!", True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, textRect)
    elif gameStatus == GameStatus.WIN:
        text = font.render("Victoire !!!", True, GREEN, BLACK)
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, textRect)
        
def fin_robot():
    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
            elif (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif (__name__ == "__main__") & (event.key == pygame.K_UP):
                    haut(1)
                elif (__name__ == "__main__") & (event.key == pygame.K_DOWN):
                    bas(1)
                elif (__name__ == "__main__") & (event.key == pygame.K_RIGHT):
                    droite(1)
                elif (__name__ == "__main__") & (event.key == pygame.K_LEFT):
                    gauche(1)

    # Done! Time to quit
    pygame.quit()
        

############## Program ##############
    

############## Exit ############## 
if __name__ == "__main__":
    initExoRobot(12, 5, [[1,2,5],[1,5],[1,5,6,7,8,9],[3,9,10,11],[0,1,2,3,4,5,6,7]], [0,2], [11,4])
    init("test")

    fin_robot()