# This file stores functions that are used by most classes
import pygame


def darkenScreen():
    s = pygame.Surface((800, 800))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((0, 0, 0))  # this fills the entire surface


def crtaj_tablu(window):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = pygame.Color((122, 149, 83))  # Taken from chess.com
            if (i + j) % 2 == 1:
                color = pygame.Color((235, 236, 207))  # Taken from chess.com)
            pygame.draw.rect(window, color, pygame.Rect(i * 100, j * 100, 100, 100))


def getTileClickedOn(mousePos):
    tileX = mousePos[0] // 100
    tileY = mousePos[1] // 100
    return [tileX, tileY]


# da li je okupirano mesto (zbog mrdanje pijuna u napred)
def spotOccupied(x, y, entityList):
    if x < 0 or x > 7:
        return [True, None]
    if y < 0 or y > 7:
        return [True, None]
    for entity in entityList:
        if entity.x == x and entity.y == y:
            return [True, entity]
    return [False, None]


def kingSpots(entity, entityList):
    spots = []
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
    return spots


def pawnSpots(entity, entityList):
    spots = []
    if entity.color == 0:
        direction = -1
    if entity.color == 1:
        direction = 1
    if spotOccupied(entity.x + 1, entity.y + direction, entityList)[0] == False:
        spots.append([entity.x + 1, entity.y + direction])
    if spotOccupied(entity.x + 1, entity.y + direction, entityList)[1] != None:
        if (
            spotOccupied(entity.x + 1, entity.y + direction, entityList)[0] == True
            and spotOccupied(entity.x + 1, entity.y + direction, entityList)[1].color
            == entity.color
        ):
            spots.append([entity.x + 1, entity.y + direction])

    if spotOccupied(entity.x - 1, entity.y + direction, entityList)[0] == False:
        spots.append([entity.x - 1, entity.y + direction])
    if spotOccupied(entity.x - 1, entity.y + direction, entityList)[1] != None:
        if (
            spotOccupied(entity.x - 1, entity.y + direction, entityList)[0] == True
            and spotOccupied(entity.x - 1, entity.y + direction, entityList)[1].color
            == entity.color
        ):
            spots.append([entity.x - 1, entity.y + direction])

    if entity.moves == 0:
        if spotOccupied(entity.x, entity.y + direction, entityList)[0] == False:
            if spotOccupied(entity.x, entity.y + direction * 2, entityList)[0] == False:
                spots.append([entity.x, entity.y + direction * 2])
    return spots


def isSpotProtected(entity1, entityList, possibleSpots):
    x = entity1.x
    y = entity1.y
    for entity in entityList:
        if entity.color != entity1.color:
            if entity.strType == "king":
                print("Made it")
                if [x, y] in kingSpots(entity, entityList):
                    print("Used kingSpots")
                    return True
                continue
            if entity.strType == "pawn":
                if [x, y] in pawnSpots(entity, entityList):
                    return True
                continue
            if [x, y] in possibleSpots(entity, entityList):
                return True
    return False
