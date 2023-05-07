import pygame
import time


window = pygame.display.set_mode((800, 800))

# Classes


class Pawn:
    # init
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, args):
        # Pravo napred (args[0] je vrsta kretanja. args je lista dodatmih informacija (smer itd))
        if args[0] == 0:
            if self.color == 0:
                if spotOccupied(self.x, self.y - 1)[0] == False:
                    self.y -= 1
            if self.color == 1:
                if spotOccupied(self.x, self.y + 1)[0] == False:
                    self.y += 1

            pass  # u sred synca sam

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

    def move(self, args):
        if args[0] == 0:
            if self.color == 0:
                if spotOccupied(self.x, self.y - 1) == False:
                    self.y -= 1

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

    def move(self, args):
        if args[0] == 0:
            if self.color == 0:
                if spotOccupied(self.x, self.y - 1) == False:
                    self.y -= 1

    def draw(self, prozor):
        if self.color == 0:
            col = pygame.Color("Black")

        else:
            col = pygame.Color("Red")
        pygame.draw.rect(prozor, col, (40 + self.x * 100, 20 + self.y * 100, 20, 50))


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
MojRook = Rook(4, 4, pygame.Color("red"))
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
    if type(entity) == Pawn:
        if entity.color == 0:
            direction = 1
        if entity.color == 1:
            direction = -1
        spots = []
        if spotOccupied(entity.x, entity.y + direction)[0] == False:
            spots.append([entity.x, entity.y])
        if (
            spotOccupied(entity.x + 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x + 1, entity.y + direction)[1] != None
        ):
            spots.append([entity.x + 1, entity.y])
        if (
            spotOccupied(entity.x - 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction)[1] != None
        ):
            spots.append([entity.x - 1, entity.y])


# Main
def main():
    program_radi = True
    while program_radi:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_radi = False
        mouseB = pygame.mouse.get_pressed()

        if mouseB[0] == True:
            mousePos = pygame.mouse.get_pos()
            tilePos = getTileClickedOn(mousePos)
            entityClickedOn = spotOccupied(tilePos[0], tilePos[1])[1]
            print("got clicked")
            if entityClickedOn == None:
                print("none tzpe")
                pass
            else:
                entityClickedOn.move([0])
                print("moved")
        crtaj_tablu()
        for entity in entityList:
            entity.draw(window)
        pygame.display.flip()


main()
