import pygame
import time
from copy import *

pygame.init()
window = pygame.display.set_mode((800, 800))

# Classes
pygame.display.set_caption("Chess.com")


class GameState:
    def __init__(self, entityList, turn) -> None:
        self.entityList = entityList
        self.turn = turn


class Pawn:
    # init
    BlackPawn = pygame.image.load("Textures\\BlackPawn.png")
    WhitePawn = pygame.image.load("Textures\\WhitePawn.png")

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
            img = self.BlackPawn
        else:
            img = self.WhitePawn
        img = pygame.transform.scale(img, (80, 100))
        window.blit(img, pygame.Rect(self.x * 100 + 10, self.y * 100, 100, 100))

    def update(self, window, pawnIndex, EntityList):
        if self.color == 1:
            promoPos = 7
        else:
            promoPos = 0
        if self.y == promoPos:
            pawnPromotion(window, pawnIndex, EntityList)


class Rook:
    BlackRook = pygame.image.load("Textures\\BlackRook.png")
    WhiteRook = pygame.image.load("Textures\\WhiteRook.png")

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.moves = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, window):
        if self.color == 0:
            img = self.BlackRook
        else:
            img = self.WhiteRook
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass


class Bishop:
    BlackBishop = pygame.image.load("Textures\\BlackBishop.png")
    WhiteBishop = pygame.image.load("Textures\\WhiteBishop.png")

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, window):
        if self.color == 0:
            img = self.BlackBishop
        else:
            img = self.WhiteBishop
        img = pygame.transform.scale(img, (80, 100))
        window.blit(img, pygame.Rect(self.x * 100 + 10, self.y * 100, 100, 100))

    def update(self):
        pass


class Queen:
    BlackQueen = pygame.image.load("Textures\\BlackQueen.png")
    WhiteQueen = pygame.image.load("Textures\\WhiteQueen.png")

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            img = self.BlackQueen
        else:
            img = self.WhiteQueen
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass


class King:
    BlackKing = pygame.image.load("Textures\\BlackKing.png")
    WhiteKing = pygame.image.load("Textures\\WhiteKing.png")

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.timeChecked = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            img = self.BlackKing
        else:
            img = self.WhiteKing
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self, EntityList):
        if isSpotProtected(self) == True:
            self.checkedTime += 1
            if self.checkedTime == 2:
                print(f"Color {self.color} lost to a checkmate.")
                exit()
            else:
                self.checkedTime = 0
            flagVar = 0
        if isSpotProtected(self) == False:
            for entity in EntityList:
                if entity.color == self.color:
                    if possibleSpots(entity) != []:
                        flagVar = 1
                        break
            if flagVar == 0:
                print(f"Stalemate, {self.color} is pinned!")
                exit()


class Knight:
    BlackKnight = pygame.image.load("Textures\\BlackKnight.png")
    WhiteKnight = pygame.image.load("Textures\\WhiteKnight.png")

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, prozor):
        if self.color == 0:
            img = self.BlackKnight
        else:
            img = self.WhiteKnight
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass


class Button:
    def __init__(self, rect, text) -> None:
        self.rect = rect
        self.text = text

    def update(self):
        pygame.event.pump()
        mouseB = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if (
            mousePos[0] > self.rect.x
            and mousePos[0] < self.rect.x + self.rect.width
            and mousePos[1] > self.rect.y
            and mousePos[1] < self.rect.y + self.rect.height
            and mouseB[0] == True
        ):
            return True
        return False

    def draw(self, window):

        pygame.draw.rect(window, pygame.Color("White"), self.rect)
        pygame.draw.rect(window, pygame.Color("Black"), self.rect, 2)
        font = pygame.font.Font(None, 25)
        text1 = font.render(self.text, True, pygame.Color("Black"))
        text_rect = text1.get_rect(
            center=(
                self.rect.x + self.rect.width / 2,
                self.rect.y + self.rect.height / 2,
            )
        )
        window.blit(text1, text_rect)


# Draw function


def crtaj_tablu():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = pygame.Color((122, 149, 83))  # Taken from chess.com
            if (i + j) % 2 == 1:
                color = pygame.Color((235, 236, 207))  # Taken from chess.com)
            pygame.draw.rect(window, color, pygame.Rect(i * 100, j * 100, 100, 100))


entityList = []


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


def kingSpots(entity):
    spots = []
    dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
    for i in range(8):
        dir = dirs[i]
        for j in range(1, 2):
            status = spotOccupied(entity.x + dir[0] * j, entity.y + dir[1] * j)
            if status[0] == False:
                spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
            elif status[0] == True:

                if status[1] == None:
                    break
                elif status[1] != None:
                    if status[1].color != entity.color:
                        spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                        break
                    else:
                        break
    return spots


def pawnSpots(entity):
    spots = []
    if entity.color == 0:
        direction = -1
    if entity.color == 1:
        direction = 1
    if spotOccupied(entity.x + 1, entity.y + direction)[0] == False:
        spots.append([entity.x + 1, entity.y + direction])
    if spotOccupied(entity.x + 1, entity.y + direction)[1] != None:
        if (
            spotOccupied(entity.x + 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x + 1, entity.y + direction)[1].color
            == entity.color
        ):
            spots.append([entity.x + 1, entity.y + direction])

    if spotOccupied(entity.x - 1, entity.y + direction)[0] == False:
        spots.append([entity.x - 1, entity.y + direction])
    if spotOccupied(entity.x - 1, entity.y + direction)[1] != None:
        if (
            spotOccupied(entity.x - 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction)[1].color
            == entity.color
        ):
            spots.append([entity.x - 1, entity.y + direction])

    if entity.moves == 0:
        if spotOccupied(entity.x, entity.y + direction)[0] == False:
            if spotOccupied(entity.x, entity.y + direction * 2)[0] == False:
                spots.append([entity.x, entity.y + direction * 2])
    return spots


def pawnPromotion(window, pawnIndex, listOfEntities):
    s = pygame.Surface((800, 800))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((0, 0, 0))  # this fills the entire surface
    buttons = []
    bishopButton = Button(pygame.Rect(15, 100, 175, 75), "Bishop")
    buttons.append(bishopButton)
    knightButton = Button(pygame.Rect(215, 100, 175, 75), "Knight")
    buttons.append(knightButton)
    rookButton = Button(pygame.Rect(415, 100, 175, 75), "Rook")
    buttons.append(rookButton)
    queenButton = Button(pygame.Rect(615, 100, 175, 75), "Queen")
    buttons.append(queenButton)

    while True:
        crtaj_tablu()
        for entity in listOfEntities:
            entity.draw(window)
        window.blit(s, (0, 0))  # (0,0) are the top-left coordinates
        for button in buttons:
            status = button.update()
            if status == True:
                print(button.text)
                if button.text == "Knight":
                    b = Knight(
                        listOfEntities[pawnIndex].x,
                        listOfEntities[pawnIndex].y,
                        listOfEntities[pawnIndex].color,
                    )
                    del listOfEntities[pawnIndex]
                    listOfEntities.append(b)
                    return
                if button.text == "Bishop":
                    b = Bishop(
                        listOfEntities[pawnIndex].x,
                        listOfEntities[pawnIndex].y,
                        listOfEntities[pawnIndex].color,
                    )
                    del listOfEntities[pawnIndex]
                    listOfEntities.append(b)
                    return
                if button.text == "Rook":
                    b = Rook(
                        listOfEntities[pawnIndex].x,
                        listOfEntities[pawnIndex].y,
                        listOfEntities[pawnIndex].color,
                    )
                    del listOfEntities[pawnIndex]
                    listOfEntities.append(b)
                    return
                if button.text == "Queen":
                    b = Queen(
                        listOfEntities[pawnIndex].x,
                        listOfEntities[pawnIndex].y,
                        listOfEntities[pawnIndex].color,
                    )
                    del listOfEntities[pawnIndex]
                    listOfEntities.append(b)
                    return

        for button in buttons:
            button.draw(window)

        pygame.display.flip()


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
            and spotOccupied(entity.x + 1, entity.y + direction)[1].color
            != entity.color
        ):
            spots.append([entity.x + 1, entity.y + direction])
        if (
            spotOccupied(entity.x - 1, entity.y + direction)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction)[1] != None
            and spotOccupied(entity.x - 1, entity.y + direction)[1].color
            != entity.color
        ):
            spots.append([entity.x - 1, entity.y + direction])
        if entity.moves == 0:
            if spotOccupied(entity.x, entity.y + direction)[0] == False:
                if spotOccupied(entity.x, entity.y + direction * 2)[0] == False:
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

                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([entity.x + dir[0] * j, entity.y + dir[1] * j])
                            break
                        else:
                            break
        drawSpots2(spots, window)
        pygame.display.flip()
        realSpots = []
        for spot in spots:
            res = canKingGoHere(spot[0], spot[1], entity, entityList)
            if res == True:
                realSpots.append(spot)
        return realSpots
    if type(entity) == Knight:
        dirs = [[-1, -2], [1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1]]
        for i in range(8):
            dir = dirs[i]
            status = spotOccupied(entity.x + dir[0], entity.y + dir[1])
            if status[0] == False:
                spots.append([entity.x + dir[0], entity.y + dir[1]])
            elif status[0] == True:

                if status[1] == None:
                    pass
                elif status[1] != None:
                    if status[1].color != entity.color:
                        spots.append([entity.x + dir[0], entity.y + dir[1]])
    return spots


def drawSpots(spots, window):
    # Spot 0 je x, spot 1 je y
    for spot in spots:
        pygame.draw.circle(
            window, pygame.Color("Gray"), (spot[0] * 100 + 50, spot[1] * 100 + 50), 20
        )


def drawSpots2(spots, window):
    # Spot 0 je x, spot 1 je y
    for spot in spots:
        pygame.draw.circle(
            window, pygame.Color("Red"), (spot[0] * 100 + 50, spot[1] * 100 + 50), 20
        )


def isSpotProtected(entity1):
    x = entity1.x
    y = entity1.y
    for entity in entityList:
        if entity.color != entity1.color:
            if type(entity) == King:
                print("Made it")
                if [x, y] in kingSpots(entity):
                    print("Used kingSpots")
                    return True
                continue
            if type(entity) == Pawn:
                if [x, y] in pawnSpots(entity):
                    return True
                continue
            if [x, y] in possibleSpots(entity):
                return True
    return False


def canKingGoHere(x, y, king, entityList):
    spotOc = spotOccupied(x, y)
    if spotOc[0] == True:
        if spotOc[1] != None:
            if spotOc[1].color == king.color:
                return False
    for entity in entityList:
        if entity.color != king.color:
            if type(entity) == King:
                print("Made it")
                if [x, y] in kingSpots(entity):
                    print("Used kingSpots")
                    return False
                continue
            if type(entity) == Pawn:
                if [x, y] in pawnSpots(entity):
                    return False
                continue
            if [x, y] in possibleSpots(entity):
                return False
    return True


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
    b1 = Knight(1, 0, 1)
    b2 = Knight(6, 0, 1)
    b3 = Knight(1, 7, 0)
    b4 = Knight(6, 7, 0)
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
    # Knights
    kn1 = Bishop(2, 0, 1)
    kn2 = Bishop(5, 0, 1)
    kn3 = Bishop(5, 7, 0)
    kn4 = Bishop(2, 7, 0)
    entityList.append(kn1)
    entityList.append(kn2)
    entityList.append(kn3)
    entityList.append(kn4)


def checkOnKing(king, entityList):
    # if isSpotProtected(king) == False:
    #    if possibleSpots(king) == []:
    #        print(f"Color {king.color} lost to a stalemate")
    if isSpotProtected(king) == True:
        king.checkedTime += 1
        if king.checkedTime == 2:
            print(f"Color {king.color} lost to a checkmate.")
            exit()
    else:
        king.checkedTime = 0
    flagVar = 0
    if isSpotProtected(king) == False:
        for entity in entityList:
            if entity.color == king.color:
                if possibleSpots(entity) != []:
                    flagVar = 1
                    break
        if flagVar == 0:
            print(f"Stalemate, {king.color} is pinned!")
            exit()


# COMMENt
setUpBoard()
# Main


def main():
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 30
    cooldown = cooldownInit
    turnNo = 1
    freeMove = True
    while program_radi:
        crtaj_tablu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_radi = False
        mouseB = pygame.mouse.get_pressed()
        change = 0
        if mouseB[0] == True and cooldown <= 0:
            mousePos = pygame.mouse.get_pos()
            tilePos = getTileClickedOn(mousePos)
            entityClickedOn = spotOccupied(tilePos[0], tilePos[1])[1]
            if entityClickedOn != None:
                cooldown = cooldownInit
            if entityClickedOn != None and lastEntity == entityClickedOn:
                entityClickedOn = None
                lastEntity = None
                spots = None
            res = spotOccupied(tilePos[0], tilePos[1])
            if spots != None:
                if lastEntity != None:
                    if turnNo % 2 == lastEntity.color or freeMove:
                        if res[0] == True:
                            if res[1] != None:
                                if res[1].color != lastEntity.color:
                                    if tilePos in spots:
                                        lastEntity.move(tilePos)
                                        change = 1
                                        turnNo += 1
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
                                change = 1
                                turnNo += 1
                                spots = None
                else:
                    print("None")

            print("got clicked")
            if entityClickedOn == None:
                print("none type")
                pass
            else:
                lastEntity = entityClickedOn
                if turnNo % 2 == lastEntity.color or freeMove:
                    spots = possibleSpots(entityClickedOn)
        flagVar = 0

        # Drawing
        for entity in entityList:
            entity.draw(window)
            if type(entity) == King and change == 1:
                checkOnKing(entity, entityList)
                flagVar = 1
        for entity in entityList:
            if type(entity) == King:
                if change != 1:
                    continue
                entity.update(entityList)
                flagVar = 1
                continue
            if type(entity) == Pawn:
                entity.update(window, entityList.index(entity), entityList)
                continue
            entity.update()
        # Updating
        if flagVar == 1:
            change = 0
        if spots != None:
            drawSpots(spots, window)
        pygame.display.flip()
        cooldown -= 1


main()
