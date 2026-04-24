import pygame
import random
import time

BLACK = 0, 0, 0
WHITE = 200, 200,200
RED = 200, 0, 0
GREEN = 0, 200, 0
BLUE = 0, 0, 200
DARKGREEN = 0, 100, 0
DARKRED = 100, 0, 0
DARKBLUE = (0, 0, 128)
MAGENTA = (128, 0, 128)
CYAN = (0, 128, 128)
colors =  [RED, BLUE, GREEN, DARKBLUE, DARKGREEN, CYAN, MAGENTA, DARKRED]
nCrepes = burnedMode = tas = nbCasesY= nbCasesX= box= background=background= screen= None
print()

def init(n=7, brulees = False):
    global nCrepes, nbCasesY, nbCasesX, box, background,background, screen, tas, burnedMode
    nCrepes = n
    nbCasesY = n*4
    nbCasesX = n*2
    WIDTH = nbCasesX*75
    HEIGHT = nbCasesY*50/4
    caseSizeX = WIDTH//nbCasesX
    caseSizeY = HEIGHT//nbCasesY
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    burnedMode = brulees
    
    # Load boxes
    box = [[0 for x in range(nbCasesX)] for y in range(nbCasesY)]
    for x in range(nbCasesX):
        for y in range(nbCasesY):
            box[y][x] = pygame.Rect((caseSizeX*x, caseSizeY*y), ((caseSizeX), (caseSizeY)))
            
    # Load background
    background = pygame.Surface((caseSizeX, caseSizeY))
    
    pygame.init()
    pygame.display.set_caption("Grid")
    
    tas = generate_crepes(n)
    disp(tas)
    return tas
    
def generate_crepes(n=7):
    tas = []
    for i in range(n):
        newNumber = 0
        while (newNumber in tas) or (newNumber ==0):
            newNumber = random.randrange(n)+1
        tas.append(newNumber)
        
    return tas

def taille(n):
    return tas[n]

def retourner(n):
    global tas
    newTas = []
    negSiBrulee = burnedMode * -2 +1
    n = n+1
    for i in range(n,0,-1):
        newTas.append(tas[i-1]*negSiBrulee)
    for i in range(n, nCrepes):
        newTas.append(tas[i])
    tas = newTas
    pygame.time.wait(500)
    disp(tas)
    return newTas


def indexNiemePlusGrande(tasCrepes, n):
    absTas = [abs(x) for x in tasCrepes]
    indexPlusGrande = absTas.index(sorted(absTas)[-n]) 
    return indexPlusGrande


def triee(tasCrepes):
    absTas = [abs(x) for x in tasCrepes]
    return absTas == sorted(absTas)

    
def disp(tasCrepes = []):
    global nbCasesY, nbCasesX, box, background, screen, colors
    # Display map
    screen.blit(background, box[0][1])
    for crepe in range(nbCasesY//4): # each line
        for subY in range(4):
            y = crepe*4+subY
            for x in range(nbCasesX//2): # each box
                isCrepe = False
                if crepe<len(tasCrepes):
                    if x < abs(tasCrepes[crepe]):
                        isCrepe = True
                # Select color
                if isCrepe:
                    if burnedMode and ((subY == 0 and tasCrepes[crepe] < 0) or(subY == 3 and tasCrepes[crepe] > 0)):
                        background.fill(BLACK)
                    else:
                        background.fill(colors[abs(tasCrepes[crepe])])
                else :
                    background.fill(WHITE)
                # Fill both sides
                screen.blit(background, box[y][nbCasesX//2-x-1])
                screen.blit(background, box[y][nbCasesX//2+x])              
        
            
    pygame.display.flip()
    
def souris():
    running = True
    while running:
      # get all events
      ev = pygame.event.get()

      # proceed events
      for event in ev:
        if (event.type == pygame.QUIT):
            running = False
        elif (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                running = False
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
          pos = pygame.mouse.get_pos()
          for x in range(nbCasesX):
            for y in range(nbCasesY):
              if box[y][x].collidepoint(pos):
                  return (x,y)
    # Done! Time to quit
    pygame.quit()
    
def fin():
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

    # Done! Time to quit
    pygame.quit()
    
def tasTrié():
    estTrié = True
    for i in range(nCrepes-1):
        if taille(i)> taille(i+1):
            estTrié = False
    return estTrié

def plusGrande(nombreCrepes):
    idx = 0
    for i in range(nombreCrepes):
        if taille(i) > taille(idx):
            idx = i            
    return idx

if (__name__ == "__main__"):
    
    tasDeCrepes = init(7, True)
    while True:
        pos = souris()
        if pos:
            print(pos[1]//4)
            retourner(pos[1]//4)
        else:
            break
