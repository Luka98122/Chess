import pygame
import random



pygame.init()

window = pygame.display.set_mode((800,800))

def drawTable(window,width,height,size):
    for i in range(height):
        for j in range(width):
            if (i+j)%2==0:
                color = pygame.Color("green")
            else:
                color = pygame.Color("darkgreen")
            if state[i][j] in "U123456789":
                color = pygame.Color("antiquewhite2")
            pygame.draw.rect(window, color, pygame.Rect(j*size, i*size,size,size))
            if state[i][j] in "123456789":
                font = pygame.font.Font('freesansbold.ttf', 24)
                text = font.render(str(state[i][j]), True, pygame.Color("Black"))
                textRect = text.get_rect() 
                textRect.center = (j*size+size/2,i*size+size/2)
                window.blit(text,textRect)
                

state = []
GAME_WIDTH = 2
GAME_HEIGHT = 2
MINE_COUNT = 1
SIZE = 400

counter = 0

for i in range(GAME_WIDTH):
    state.append([])
    for j in range(GAME_HEIGHT):
        if random.randint(0,2) == 0 and counter != MINE_COUNT:
            state[i].append("X")
            counter +=1
            continue
        state[i].append("O")
        
def getTileClicked(tup):
    return pygame.Vector2(int(tup[0]//SIZE), int(tup[1]//SIZE))


def findAll(x,y, foundSoFar : list):
    dirs = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    res = 0
    for dir in dirs:
        try:
            if y+dir[1]<0 or x+dir[0]<0:
                continue
            if state[y+dir[1]][x+dir[0]] != "X":
                if getNumber(x+dir[0],y+dir[1]) == 0 and [x+dir[0],y+dir[1]] not in foundSoFar:
                    foundSoFar.append([x+dir[0],y+dir[1]])
                    foundSoFar = findAll(x+dir[0],y+dir[1], foundSoFar)
        except:
            pass
    return foundSoFar


def getNumber(x,y):
    dirs = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    res = 0
    for dir in dirs:
        try:
            if state[y+dir[1]][x+dir[0]] == "X":
                res +=1
        except:
            pass
    return res

while True:
    drawTable(window, GAME_WIDTH,GAME_HEIGHT, SIZE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    
    if pygame.mouse.get_pressed()[0]:
        tileCoords = getTileClicked(pygame.mouse.get_pos())
        if state[int(tileCoords.y)][int(tileCoords.x)] == "X":
            exit()
        else:
            state[int(tileCoords.y)][int(tileCoords.x)] = "U"
            if getNumber(int(tileCoords.y),int(tileCoords.x)) != 0:
                state[int(tileCoords.y)][int(tileCoords.x)] = str(getNumber(int(tileCoords.y),int(tileCoords.x)))
                for tileCoords in findAll(int(tileCoords.x),int(tileCoords.y),[]):
                    state[int(tileCoords[1])][int(tileCoords[0])] = "U"
            
    
    pygame.display.flip()