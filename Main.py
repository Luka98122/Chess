import pygame
import time
from copy import *

window = pygame.display.set_mode((800, 800))

# Classes
pygame.display.set_caption("Chess.com")


class Pawn:
    # init
    def __init__(self, x, y, color):
        self.moves = 0
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, window):
        if self.color == 0:
            col = pygame.Color("Black")
        else:
            col = pygame.Color("White")
        pygame.draw.circle(window, col, (self.x * 100 + 50, self.y * 100 + 50), 40)


class Rook:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.moves = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, prozor):
        if self.color == 0:
            col = pygame.Color("Black")

        else:
            col = pygame.Color("Red")
        pygame.draw.rect(prozor, col, (15 + self.x * 100, 15 + self.y * 100, 70, 70))


class Bishop:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            col = pygame.Color("Black")
        else:
            col = pygame.Color("Red")
        pygame.draw.rect(prozor, col, (40 + self.x * 100, 20 + self.y * 100, 20, 50))


class Queen:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            col = pygame.Color("Black")
        else:
            col = pygame.Color("Red")
        pygame.draw.rect(prozor, col, (20 + self.x * 100, 20 + self.y * 100, 50, 50))


class King:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            col = pygame.Color("Blue")
        else:
            col = pygame.Color("Green")
        pygame.draw.rect(prozor, col, (20 + self.x * 100, 20 + self.y * 100, 50, 50))


# Draw function


def crtaj_tablu():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = pygame.Color((122, 149, 83))  # Taken from chess.com
            if (i + j) % 2 == 1:
                color = pygame.Color((235, 236, 207))  # Taken from chess.com)
            pygame.draw.rect(window, color, pygame.Rect(i * 100, j * 100, 100, 100))


# Init test pieces
entityList = []
MojRook = Rook(4, 4, 0)
entityList.append(MojRook)

mojPawn = Pawn(3, 3, 1)
entityList.append(mojPawn)

MojBishop = Bishop(5, 5, 0)
entityList.append(MojBishop)

# Helper functions
def getTileClickedOn(mousePos):
    tileX = mousePos[0] // 100
    tileY = mousePos[1] // 100
    return [tileX, tileY]


# da li je okupirano mesto (zbog mrdanje pijuna u napred)
def spotOccupied(x, y):
    if x < 0 or x > 7:
        return [True, None]
    if y < 0 or y > 7:
        return [True, None]
    for entity in entityList:
        if entity.x == x and entity.y == y:
            return [True, entity]
    return [False, None]


def possibleSpots(entity):
    spots = []
    if type(entity) == Pawn:
        if entity.color == 0:
            direction = -1
        if entity.color == 1:
            direction = 1
        if spotOccupied(entity.x, entity.y + direction)[0] == False:
            spots.append([entity.x, entity.y + direction])
        if (
            spotOccupied(entity.x + 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x + 1, entity.y + direction)[1] != None
        ):
            spots.append([entity.x + 1, entity.y + direction])
        if (
            spotOccupied(entity.x - 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction)[1] != None
        ):
            spots.append([entity.x - 1, entity.y + direction])
        if entity.moves == 0:
            spots.append([entity.x, entity.y + direction * 2])
    if type(entity) == Rook:
        spots = []
        dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(4):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(entity.x + dir[0] * j, entity.y + dir[1] * j)
                if status[0] == False:
                    spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                elif status[0] == True:
                    print("Usao")
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == Bishop:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
        for i in range(4):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(entity.x + dir[0] * j, entity.y + dir[1] * j)
                if status[0] == False:
                    spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                elif status[0] == True:
                    print("Usao")
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == Queen:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(8):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(entity.x + dir[0] * j, entity.y + dir[1] * j)
                if status[0] == False:
                    spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                elif status[0] == True:
                    print("Usao")
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == King:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(8):
            dir = dirs[i]
            for j in range(1, 2):
                status = spotOccupied(entity.x + dir[0] * j, entity.y + dir[1] * j)
                if status[0] == False:
                    spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                elif status[0] == True:
                    print("Usao")
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                            break
                        else:
                            break

    return spots


def drawSpots(spots, window):
    # Spot 0 je x, spot 1 je y
    for spot in spots:
        pygame.draw.circle(
            window, pygame.Color("Gray"), (spot[0] * 100 + 50, spot[1] * 100 + 50), 20
        )


def setUpPawns():
    for i in range(8):
        pawn = Pawn(i, 1, 1)
        entityList.append(pawn)
    for i in range(8):
        pawn = Pawn(i, 6, 0)
        entityList.append(pawn)


def setUpBoard():
    setUpPawns()
    # Rooks
    rook1 = Rook(0, 0, 1)
    rook2 = Rook(7, 0, 1)
    rook3 = Rook(0, 7, 0)
    rook4 = Rook(7, 7, 0)
    entityList.append(rook1)
    entityList.append(rook2)
    entityList.append(rook3)
    entityList.append(rook4)
    # Bishops
    b1 = Bishop(1, 0, 1)
    b2 = Bishop(6, 0, 1)
    b3 = Bishop(1, 7, 0)
    b4 = Bishop(6, 7, 0)
    entityList.append(b1)
    entityList.append(b2)
    entityList.append(b3)
    entityList.append(b4)
    # Queens
    q1 = Queen(3, 0, 1)
    q2 = Queen(3, 7, 0)
    entityList.append(q1)
    entityList.append(q2)
    # Kings
    k1 = King(4, 0, 1)
    k2 = King(4, 7, 0)
    entityList.append(k1)
    entityList.append(k2)


# COMMENt
a = 2

setUpBoard()
# Main
def main():
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 200
    cooldown = cooldownInit
    while program_radi:
        crtaj_tablu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_radi = False
        mouseB = pygame.mouse.get_pressed()

        if mouseB[0] == True and cooldown <= 0:
            cooldown = cooldownInit
            mousePos = pygame.mouse.get_pos()
            tilePos = getTileClickedOn(mousePos)
            entityClickedOn = spotOccupied(tilePos[0], tilePos[1])[1]
            if entityClickedOn != None and lastEntity == entityClickedOn:
                entityClickedOn = None
                lastEntity = None
                spots = None
            res = spotOccupied(tilePos[0], tilePos[1])
            if spots != None:
                if lastEntity != None:
                    if res[0] == True:
                        if res[1] != None:
                            if res[1].color != lastEntity.color:
                                if tilePos in spots:
                                    lastEntity.move(tilePos)
                                    entityList.remove(entityClickedOn)
                                    entityClickedOn = None
                                    lastEntity = None
                                    print("Moved")
                                    spots = None
                                    mouseB = False
                                    continue
                    else:
                        if tilePos in spots:
                            print("Moved 2")
                            lastEntity.move(tilePos)
                            spots = None
                else:
                    print("None")

            print("got clicked")
            if entityClickedOn == None:
                print("none type")
                pass
            else:
                spots = possibleSpots(entityClickedOn)
                lastEntity = entityClickedOn
                print("moved")
        for entity in entityList:
            entity.draw(window)
        if spots != None:
            drawSpots(spots, window)
        pygame.display.flip()
        cooldown -= 1


main()
