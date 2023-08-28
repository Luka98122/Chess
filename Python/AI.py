import pygame
import time
import json
import threading
from copy import *
from ctypes import cdll, c_char_p

#lib = cdll.LoadLibrary("ai_dll\\x64\\Debug\\ai_dll.dll")
#HelloWorld = lib.HelloWorld
#HelloWorld.restype = c_char_p

#print(HelloWorld("Pop").decode())


from Pawn import *
from Rook import *
from Bishop import *
from Knight import *
from Queen import *
from King import *
from globals import *
from HelperFunctions import *
from Trees import *

globals.counter = 0


def is_check(king, entityList):
    for entity in entityList:
        if entity.color != king.color:
            if [king.x, king.y] in possibleSpots(entity, entityList):
                return True
    return False


def is_checkmate(king, ENtityLIst):
    for move in getAllMoves(ENtityLIst, king.color):
        entityList1 = changeStateFromList(ENtityLIst, move)
        if is_check(king, entityList1) == False:
            return False
    return True


def scoreBoard(ENtityList, color, weights: list):
    globals.counter += 1
    # 0                1                 2   3   4   5   6   7   8   9
    # [ourKingInCheck, theirKingInCheck, y1, y2, y3, y4, y5, y6, y7, y8]
    score = 0
    tScore = 0
    for entity in ENtityList:
        if entity.color == color:
            if type(entity) != King:
                if color == 0:
                    score += (
                        entity.value * weights[10 + entity.y] * weights[2 + entity.x]
                    )

                else:
                    score += entity.value * weights[-entity.y] * weights[2 + entity.x]
        else:
            if type(entity) != King:
                if color == 0:
                    tScore += (
                        entity.value * weights[10 + entity.y] * weights[2 + entity.x]
                    )
                else:
                    tScore += entity.value * weights[-entity.y] * weights[2 + entity.x]

        # If our king is in check
        if type(entity) == King and entity.color == color:
            if is_checkmate(entity, ENtityList):
                score -= weights[0]
                tScore += weights[0]

        # If their king is in check
        if type(entity) == King and entity.color != color:
            if is_checkmate(entity, ENtityList):
                score += weights[1]
                tScore -= weights[1]
    return score - tScore


def scoreBoardEmoji():
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

def possibleSpotsEmoji(entity : str, x, y, entityList):
    spots = []
    if entity in "♙♟":
        if entity == "♙":
            direction = 1
        if entity == "♟":
            direction = -1
        if spotOccupied(x, y + direction, entityList)[0] == False:
            spots.append([x, y + direction])
        if (
            spotOccupied(x + 1, y + direction, entityList)[0] == True
            and spotOccupied(x + 1, y + direction, entityList)[1] != None
            and spotOccupied(x + 1, y + direction, entityList)[1].color
            != entity.color
        ):
            if direction == 1:
                if spotOccupied(x + 1, y + direction, entityList)[1] in "♚♛♝♜♟♞":
                    spots.append([x + 1, y + direction])
            if direction == -1:
                if spotOccupied(x + 1, y + direction, entityList)[1] not in "♚♛♝♜♟♞":
                    spots.append([x + 1, y + direction])
        if (
            spotOccupied(x - 1, y + direction, entityList)[0] == True
            and spotOccupied(x - 1, y + direction, entityList)[1] != None
            and spotOccupied(x - 1, y + direction, entityList)[1].color
            != entity.color
        ):
            if direction == 1:
                if spotOccupied(x - 1, y + direction, entityList)[1] in "♖♘♗♕♔♙":
                    spots.append([x - 1, y + direction])
            if direction == -1:
                if spotOccupied(x - 1, y + direction, entityList)[1] not in "♖♘♗♕♔♙":
                    spots.append([x - 1, y + direction])
        if entity.moves == 0:
            if spotOccupied(x, y + direction, entityList)[0] == False:
                if (
                    spotOccupied(x, y + direction * 2, entityList)[0]
                    == False
                ):
                    spots.append(
                        [
                            x,
                            y + direction * 2,
                        ]
                    )
    if type(entity) == Rook:
        spots = []
        dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(4):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(
                    x + dir[0] * j, y + dir[1] * j, entityList
                )
                if status[0] == False:
                    spots.append([x + dir[0] * j, y + dir[1] * j])
                elif status[0] == True:
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([x + dir[0] * j, y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == Bishop:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
        for i in range(4):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(
                    x + dir[0] * j, y + dir[1] * j, entityList
                )
                if status[0] == False:
                    spots.append([x + dir[0] * j, y + dir[1] * j])
                elif status[0] == True:
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([x + dir[0] * j, y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == Queen:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(8):
            dir = dirs[i]
            for j in range(1, 9):
                status = spotOccupied(
                    x + dir[0] * j, y + dir[1] * j, entityList
                )
                if status[0] == False:
                    spots.append([x + dir[0] * j, y + dir[1] * j])
                elif status[0] == True:
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([x + dir[0] * j, y + dir[1] * j])
                            break
                        else:
                            break
    if type(entity) == King:
        dirs = [[1, -1], [1, 1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(8):
            dir = dirs[i]
            for j in range(1, 2):
                status = spotOccupied(
                    x + dir[0] * j, y + dir[1] * j, entityList
                )
                if status[0] == False:
                    spots.append([x + dir[0] * j, y + dir[1] * j])
                elif status[0] == True:
                    if status[1] == None:
                        break
                    elif status[1] != None:
                        if status[1].color != entity.color:
                            spots.append([x + dir[0] * j, y + dir[1] * j])
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
            status = spotOccupied(x + dir[0], y + dir[1], entityList)
            if status[0] == False:
                spots.append([x + dir[0], y + dir[1]])
            elif status[0] == True:
                if status[1] == None:
                    pass
                elif status[1] != None:
                    if status[1].color != entity.color:
                        spots.append([x + dir[0], y + dir[1]])
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


def getAllMoves(ENTItyList, color):
    allMoves = []
    for entity in ENTItyList:
        if type(entity) == King:
            a = 2
        if entity.color != color:
            continue
        spots = possibleSpots(entity, ENTItyList)
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


def debugPrintBoard(ENTityList):
    boardList = []
    padder = 2
    for i in range(8):
        boardList.append([])
        for j in range(8):
            if (i + j) % 2 != 0:
                boardList[i].append("⬜ ")
            else:
                boardList[i].append("⬛ ")
    for entity in ENTityList:
        if entity.color == 0:
            if type(entity) == King:
                char = "♔" + " " * padder
            if type(entity) == Queen:
                char = "♕" + " " * padder
            if type(entity) == Rook:
                char = "♖" + " " * padder
            if type(entity) == Bishop:
                char = "♗" + " " * padder
            if type(entity) == Knight:
                char = "♘" + " " * padder
            if type(entity) == Pawn:
                char = "♙" + " " * padder
        if entity.color == 1:
            if type(entity) == King:
                char = "♚" + " " * padder
            if type(entity) == Queen:
                char = "♛" + " " * padder
            if type(entity) == Rook:
                char = "♜" + " " * padder
            if type(entity) == Bishop:
                char = "♝" + " " * padder
            if type(entity) == Knight:
                char = "♞" + " " * padder
            if type(entity) == Pawn:
                char = "♟" + " " * padder
        boardList[entity.y][entity.x] = char
    print("==============")
    for i in range(8):
        stri = ""
        for j in range(8):
            stri += boardList[i][j]
        print(stri)
    pass


def changeState(EntitYList, move, purp):
    EntitYList = deepcopy(EntitYList)
    for entity in EntitYList:
        if [entity.x, entity.y] == move[1]:
            del entity
    for entity in EntitYList:
        if [entity.x, entity.y] == move[0]:
            entity.x = move[1][0]
            entity.y = move[1][1]
            if purp == "AI":
                print(f"Moved {type(entity)} to {entity.x} {entity.y}")
            break
    return EntitYList

def changeStateEmoji(emojiBoard, move):
    emojiBoard2 = deepcopy(emojiBoard)
    emojiBoard2[move[1][1]][move[1][0]] = emojiBoard2[move[0][1]][move[0][0]]
    emojiBoard2[move[0][1]][move[0][0]] = "X"
    return emojiBoard2
    

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

    entityList = jsonDecoderBig(gameState)
    bestSoFar = 0
    BestMove = 0
    theStates = [0, 1, 2]
    for move in getAllMoves(entityList, color):
        game1 = changeState(gameState, move[1], "AIC")
        move1 = bestMove(game1, otherColor, weights)
        game2 = changeState(game1, move1[1], "AIC")
        move2 = bestMove(game2, color, weights)
        if move2[0] > bestSoFar:
            BestMove = move2[1]
            bestSoFar = move2[0]
            theStates[0] = game1
            theStates[1] = game2
            theStates[2] = changeState(game2, move2, "None")
    for state in theStates:
        debugPrintBoard(state)
    return [bestSoFar, BestMove]

# ♖♘♗♕♔♙ 
# ♜♞♝♛♚♟
def emojiToEList(emojiBoard):
    eList = []
    for i in range(8):
        for j in range(8):
            c = emojiBoard[i][j]
            if c == "♙":
                eList.append(Pawn(j,i,0))
            elif c == "♔":
                eList.append(King(j,i,0))
            elif c == "♕":
                eList.append(Queen(j,i,0))
            elif c == "♖":
                eList.append(Rook(j,i,0))
            elif c == "♘":
                eList.append(Knight(j,i,0))
            elif c == "♗":
                eList.append(Bishop(j,i,0))
            
            # black
            elif c == "♟":
                eList.append(Pawn(j,i,1))
            elif c == "♚":
                eList.append(King(j,i,1))
            elif c == "♛":
                eList.append(Queen(j,i,1))
            elif c == "♜":
                eList.append(Rook(j,i,1))
            elif c == "♞":
                eList.append(Knight(j,i,1))
            elif c == "♝":
                eList.append(Bishop(j,i,1))
            


def chooseAMove2(EntityList, color, weights, depthLeft):
    bestScore = -1000
    # bestmove = [[0, 6], [0, 4]]
    var = getAllMoves(EntityList, color)
    EmojiBoard = makeEmoji(EntityList)
    for move in var:
        if depthLeft != 0:
            newEntityList = changeState(EntityList, move)
            res = chooseAMove2(newEntityList, 1 - color, weights, depthLeft - 1)
            if res[0] > bestScore:
                bestScore = res[0]
                bestMove = move
        else:
            
            newEmojiBoard = changeStateEmoji(EmojiBoard, move, "None")
            score = scoreBoard(newEmojiBoard, color, weights)
            if score > bestScore:
                bestScore = score
                bestMove = move
    if depthLeft == 2:
        debugPrintBoard(changeState(EntityList, bestMove, "None"))
    return [bestScore, bestMove]
    pass


def makeMove(move, eList, turnNo):
    dataList = []
    for entity in eList:
        if entity.x == move[1][1][0] and entity.y == move[1][1][1]:
            del entity
    for entity in eList:
        if entity.x == move[1][0][0] and entity.y == move[1][0][1]:
            entity.x = move[1][1][0]
            entity.y = move[1][1][1]

    return eList

def makeEmoji(entityList):
    boardList = []
    for i in range(8):
        boardList.append([""])
        for j in range(8):
            if (i + j) % 2 != 0:
                boardList[i]+="⬜"
            else:
                boardList[i]+="⬛"
    for entity in entityList:
        if entity.color == 0:
            if type(entity) == King:
                char = "♔"
            if type(entity) == Queen:
                char = "♕"
            if type(entity) == Rook:
                char = "♖"
            if type(entity) == Bishop:
                char = "♗"
            if type(entity) == Knight:
                char = "♘"
            if type(entity) == Pawn:
                char = "♙"
        if entity.color == 1:
            if type(entity) == King:
                char = "♚"
            if type(entity) == Queen:
                char = "♛"
            if type(entity) == Rook:
                char = "♜"
            if type(entity) == Bishop:
                char = "♝"
            if type(entity) == Knight:
                char = "♞"
            if type(entity) == Pawn:
                char = "♟"
        boardList[entity.y][entity.x] = char
    return boardList


f = open("JSONDATA.json", "r")
contents = f.read()
f.close()

#   King    King    x1   x2    x3    x4    x5    x6    x7    x8
weights = [
    -20,
    20,
    1.0,
    1.02,
    1.03,
    1.07,
    1.07,
    1.03,
    1.02,
    1.01,
    1.03,
    1.05,
    1.08,
    1.12,
    1.15,
    1.18,
    1.21,
    1.24,
]

window = pygame.display.set_mode((800, 800))

lastEntity = None
program_radi = True
spots = None
cooldownInit = 30
cooldown = cooldownInit
turnNo = 0
entityList = jsonDecoderBig(contents)
# debugPrintBoard(contents)
emjiList = makeEmoji(entityList)
emjiList = changeStateEmoji(emjiList, [[0,1],[0,3]])
while True:
    if turnNo % 2 == 1:
        dataList = []
        for entity in entityList:
            data = jsonSerializer(entity)
            dataList.append(data)
        info = {"GameState": dataList, "TurnNo": turnNo, "Validity": True}
        json_object = json.dumps(info, indent=4)
        start = time.time()
        move = chooseAMove2(entityList, 1, weights, 2)
        end = time.time()
        print(
            f"{end-start} seconds. {globals.counter} considered. {globals.counter/int(end-start)} per second."
        )
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
