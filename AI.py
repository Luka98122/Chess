import pygame
import time
import json
import threading
from copy import *


from Pawn import *
from Rook import *
from Bishop import *
from Knight import *
from Queen import *
from King import *
from globals import *
from HelperFunctions import *
from Trees import *


def is_check(king, entityList):
    for entity in entityList:
        if entity.color != king.color:
            if [king.x, king.y] in possibleSpots(entity, entityList):
                return True
    return False


def is_checkmate(king, entityList):
    for move in getAllMoves(entityList, king.color):
        entityList1 = changeStateFromList(entityList, move)
        if is_check(king, entityList1) == False:
            return False
    return True


def scoreBoard(gameState, color, weights: list):
    # 0                1                 2   3   4   5   6   7   8   9
    # [ourKingInCheck, theirKingInCheck, y1, y2, y3, y4, y5, y6, y7, y8]
    entityList = jsonDecoderBig(gameState)
    score = 0
    tScore = 0
    for entity in entityList:
        if entity.color == color:
            if type(entity) != King:
                if color == 0:
                    tScore += entity.value * weights[2 + entity.y]
                else:
                    tScore += entity.value * weights[-entity.y]
        else:
            if type(entity) != King:
                if color == 0:
                    tScore += entity.value * weights[2 + entity.y]
                else:
                    tScore += entity.value * weights[-entity.y]

        # If our king is in check
        if type(entity) == King and entity.color == color:
            if is_checkmate(entity, entityList):
                score -= weights[0]
                tScore += weights[0]

        # If their king is in check
        if type(entity) == King and entity.color != color:
            if is_checkmate(entity, entityList):
                score += weights[1]
                tScore -= weights[1]
    return score - tScore
    pass


# Collapse1
def canKingGoHere(x, y, king, entityList):
    spotOc = spotOccupied(x, y, entityList)
    if spotOc[0] == True:
        if spotOc[1] != None:
            if spotOc[1].color == king.color:
                return False
    for entity in entityList:
        if entity.color != king.color:
            if type(entity) == King:
                if [x, y] in kingSpots(entity, entityList):
                    return False
                continue
            if type(entity) == Pawn:
                if [x, y] in pawnSpots(entity, entityList):
                    return False
                continue
            if [x, y] in possibleSpots(entity, entityList):
                return False
    return True


# Collapse2
def possibleSpots(entity, entityList):
    spots = []
    if type(entity) == Pawn:
        if entity.color == 0:
            direction = 1
        if entity.color == 1:
            direction = -1
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


def jsonSerializer(object):
    resList = {
        "type": object.strType,
        "x": object.x,
        "y": object.y,
        "color": object.color,
        "moves": object.moves,
    }
    return resList


# Collapse3
def createObject(strType, pos, color, moves):
    if strType == "None":
        return "Error"
    if strType == "Remove":
        return "Error"
    if strType == "pawn":
        obj = Pawn(pos[0], pos[1], color)
    if strType == "bishop":
        obj = Bishop(pos[0], pos[1], color)
    if strType == "knight":
        obj = Knight(pos[0], pos[1], color)
    if strType == "rook":
        obj = Rook(pos[0], pos[1], color)
    if strType == "queen":
        obj = Queen(pos[0], pos[1], color)
    if strType == "king":
        obj = King(pos[0], pos[1], color)
    obj.moves = moves
    return obj


def jsonDecoder(data):
    obj = createObject(
        data["type"], [data["x"], data["y"]], data["color"], data["moves"]
    )
    return obj


def jsonDecoderBig(data):
    # print(data.decode())
    data = json.loads(data)
    gamestate = data["GameState"]
    if gamestate == None:
        return None
    rL = []
    for item in gamestate:
        obj = jsonDecoder(item)
        rL.append(obj)
    return rL


def getAllMoves(entityList, color):
    allMoves = []
    for entity in entityList:
        if type(entity) == King:
            a = 2
        if entity.color != color:
            continue
        spots = possibleSpots(entity, entityList)
        for move in spots:
            allMoves.append([[entity.x, entity.y], move])
    return allMoves


def changeStateFromList(entityList, move):
    for entity in entityList:
        if [entity.x, entity.y] == move[1]:
            del entity
    for entity in entityList:
        if [entity.x, entity.y] == move[0]:
            entity.x = move[1][0]
            entity.y = move[1][1]
    return entityList


def changeState(gameState, move, purp):
    entityList = jsonDecoderBig(gameState)
    for entity in entityList:
        if [entity.x, entity.y] == move[0]:
            entity.x = move[1][0]
            entity.y = move[1][1]
            if purp == "AI":
                print(f"Moved {type(entity)} to {entity.x} {entity.y}")
            break

    dataList = []
    turnNo = json.loads(gameState)["TurnNo"]
    for entity in entityList:
        data = jsonSerializer(entity)
        dataList.append(data)
    info = {"GameState": dataList, "TurnNo": turnNo, "Validity": True}
    json_object = json.dumps(info, indent=4)
    return json_object


def populate(tree: Tree, gameState, color):
    res = jsonDecoderBig(gameState)
    for move in getAllMoves(res, color):
        tree.insert(move)
    pass


def populateWithList(tree: Tree, entityList, color):
    for move in getAllMoves(entityList, color):
        tree.insert(move)
    pass


def drawSpots(spots, window):
    # Spot 0 je x, spot 1 je y
    for spot in spots:
        pygame.draw.circle(
            window, pygame.Color("Gray"), (spot[0] * 100 + 50, spot[1] * 100 + 50), 20
        )


def populateFull(tree: Tree, gameState, color):
    colors = [0, 1]
    populate(tree, gameState, color)
    for branch in tree.branches:
        gameState2 = changeState(gameState, branch.data, "pop")
        populate(branch, gameState2, colors[colors.index(color) - 1])
        """
        for subBranch in branch.branches:
            gameState3 = changeState(gameState2, subBranch.data)
            populate(subBranch, gameState3, color)
            for subSubBranch in subBranch.branches:
                gameState4 = changeState(gameState3, subSubBranch.data)
                populate(subSubBranch, gameState4, colors[colors.index(color) - 1])
            """


def bestMove(gameState, color, weights):
    tree = Tree(None)
    populateFull(tree, gameState, color)
    bestSoFar = [0, [[0, 0], [0, 0]]]
    for branch in tree.branches:
        game1 = changeState(gameState, branch.data, "pop2")
        score = scoreBoard(game1, color, weights)
        if score == 606.78:
            a = 2
        if score > bestSoFar[0]:
            bestSoFar[1] = branch.data
            bestSoFar[0] = score

    return bestSoFar


def chooseAMove(gameState, color, weights):
    otherColor = 1 - color
    move1 = bestMove(gameState, color, weights)

    game1 = changeState(gameState, move1[1], "none")
    move = bestMove(game1, otherColor, weights)
    game2 = changeState(game1, move[1], "none")
    move = bestMove(game2, color, weights)
    return move1


def makeMove(move, eList, turnNo):
    dataList = []
    for entity in entityList:
        if entity.x == move[1][0][0] and entity.y == move[1][0][1]:
            entity.x = move[1][1][0]
            entity.y = move[1][1][1]
        data = jsonSerializer(entity)
        dataList.append(data)
    info = {"GameState": dataList, "TurnNo": turnNo, "Validity": True}
    json_object = json.dumps(info, indent=4)
    f = open("testt.json", "w")
    f.write(json_object)
    f.close()

    for entity in eList:
        data = jsonSerializer(entity)
        dataList.append(data)
    state = changeState(json_object, move[1], "AI")
    res = jsonDecoderBig(state)
    return res


f = open("JSONDATA.json", "r")
contents = f.read()
f.close()


weights = [-20, 20, 1.03, 1.05, 1.08, 1.12, 1.15, 1.18, 1.21, 1.24]

window = pygame.display.set_mode((800, 800))

lastEntity = None
program_radi = True
spots = None
cooldownInit = 30
cooldown = cooldownInit
turnNo = 0
entityList = jsonDecoderBig(contents)
while True:
    if turnNo % 2 == 1:
        dataList = []
        for entity in entityList:
            data = jsonSerializer(entity)
            dataList.append(data)
        info = {"GameState": dataList, "TurnNo": turnNo, "Validity": True}
        json_object = json.dumps(info, indent=4)

        move = chooseAMove(json_object, 1, weights)
        moveX1 = move[1][0][0]
        moveX2 = move[1][1][0]
        moveY1 = move[1][0][1]
        moveY2 = move[1][1][1]

        print(move)
        entityList = makeMove(move, entityList, 0)
        turnNo += 1
        continue

    crtaj_tablu(window)
    events = pygame.event.get()
    for event in events:
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
                if 0 == lastEntity.color:
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
                                    spots = None
                                    mouseB = False

                                    continue
                    else:
                        if tilePos in spots:
                            lastEntity.move(tilePos)
                            change = 1
                            turnNo += 1
                            spots = None

            else:
                pass

        if entityClickedOn == None:
            pass
        else:
            lastEntity = entityClickedOn
            if 0 == lastEntity.color:
                spots = possibleSpots(entityClickedOn, entityList)
    flagVar = 0

    # Drawing
    for entity in entityList:
        entity.draw(window)
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

print(chooseAMove(contents, 0, weights))

# f = open("Log.txt", "w")
# print(f"Root branches {len(root.branches)}")
# f.write(f"{len(root.branches)}\n")
# for branch in root.branches:
#    f.write(f"Move: {branch.data}, Branchs branches: {len(branch.branches)}\n")
# f.close()
