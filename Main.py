import pygame
import time
from copy import *
from Pawn import *
from Button import *
from Rook import *
from Bishop import *
from Knight import *
from Queen import *
from King import *

from HelperFunctions import *

pygame.init()
window = pygame.display.set_mode((800, 800))

# Classes
pygame.display.set_caption("Chess.com")


class GameState:
    def __init__(self, entityList, turn) -> None:
        self.entityList = entityList
        self.turn = turn


# Draw function


entityList = []


# Helper functions


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


def possibleSpots(entity):
    spots = []
    if type(entity) == Pawn:
        if entity.color == 0:
            direction = -1
        if entity.color == 1:
            direction = 1
        if spotOccupied(entity.x, entity.y + direction, entityList)[0] == False:
            spots.append([entity.x, entity.y + direction])
        if (
            spotOccupied(entity.x + 1, entity.y + direction, entityList)[0] == True
            and spotOccupied(entity.x + 1, entity.y + direction, entityList)[1] != None
            and spotOccupied(entity.x + 1, entity.y + direction, entityList)[1].color
            != entity.color
        ):
            spots.append([entity.x + 1, entity.y + direction])
        if (
            spotOccupied(entity.x - 1, entity.y + direction, entityList)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction, entityList)[1] != None
            and spotOccupied(entity.x - 1, entity.y + direction, entityList)[1].color
            != entity.color
        ):
            spots.append([entity.x - 1, entity.y + direction])
        if entity.moves == 0:
            if spotOccupied(entity.x, entity.y + direction, entityList)[0] == False:
                if (
                    spotOccupied(entity.x, entity.y + direction * 2, entityList)[0]
                    == False
                ):
                    spots.append(
                        [
                            entity.x,
                            entity.y + direction * 2,
                        ]
                    )
    if type(entity) == Rook:
        spots = []
        dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(4):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(
                    entity.x + dir[0] * j, entity.y + dir[1] * j, entityList
                )
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
                status = spotOccupied(
                    entity.x + dir[0] * j, entity.y + dir[1] * j, entityList
                )
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
                status = spotOccupied(
                    entity.x + dir[0] * j, entity.y + dir[1] * j, entityList
                )
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
                status = spotOccupied(
                    entity.x + dir[0] * j, entity.y + dir[1] * j, entityList
                )
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
            status = spotOccupied(entity.x + dir[0], entity.y + dir[1], entityList)
            if status[0] == False:
                spots.append([entity.x + dir[0], entity.y + dir[1]])
            elif status[0] == True:

                if status[1] == None:
                    pass
                elif status[1] != None:
                    if status[1].color != entity.color:
                        spots.append([entity.x + dir[0], entity.y + dir[1]])
    return spots


def canKingGoHere(x, y, king, entityList):
    spotOc = spotOccupied(x, y, entityList)
    if spotOc[0] == True:
        if spotOc[1] != None:
            if spotOc[1].color == king.color:
                return False
    for entity in entityList:
        if entity.color != king.color:
            if type(entity) == King:
                print("Made it")
                if [x, y] in kingSpots(entity, entityList):
                    print("Used kingSpots")
                    return False
                continue
            if type(entity) == Pawn:
                if [x, y] in pawnSpots(entity, entityList):
                    return False
                continue
            if [x, y] in possibleSpots(entity):
                return False
    return True


def setUpPawns():
    for i in range(8):
        pawn = Pawn(i, 1, 1, crtaj_tablu)
        entityList.append(pawn)
    for i in range(8):
        pawn = Pawn(i, 6, 0, crtaj_tablu)
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
    if isSpotProtected(king, entityList, possibleSpots) == True:
        king.checkedTime += 1
        if king.checkedTime == 2:
            rect = pygame.Rect(200, 200, 400, 300)
            pygame.draw.rect(window, pygame.Color("White"), rect)
            pygame.draw.rect(window, pygame.Color("Black"), rect, 2)
            font = pygame.font.Font(None, 25)
            text1 = font.render(
                f"Color {king.color} lost to a checkmate.", True, pygame.Color("Black")
            )
            text_rect = text1.get_rect(
                center=(
                    rect.x + rect.width / 2,
                    rect.y + rect.height / 2,
                )
            )
            window.blit(text1, text_rect)
            pygame.display.flip()
            time.sleep(10)
    else:
        king.checkedTime = 0
    flagVar = 0
    if isSpotProtected(king, entityList, possibleSpots) == False:
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
        crtaj_tablu(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_radi = False
        mouseB = pygame.mouse.get_pressed()
        change = 0
        if mouseB[0] == True and cooldown <= 0:
            mousePos = pygame.mouse.get_pos()
            tilePos = getTileClickedOn(mousePos)
            entityClickedOn = spotOccupied(tilePos[0], tilePos[1], entityList)[1]
            if entityClickedOn != None:
                cooldown = cooldownInit
            if entityClickedOn != None and lastEntity == entityClickedOn:
                entityClickedOn = None
                lastEntity = None
                spots = None
            res = spotOccupied(tilePos[0], tilePos[1], entityList)
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
                entity.update(entityList, possibleSpots)
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
