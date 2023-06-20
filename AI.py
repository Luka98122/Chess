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


def scoreBoard(entityList, color):
    score = 0
    for entity in entityList:
        if entity.color == color:
            score += entity.value

        # If our king is in check
        if type(entity) == King and entity.color == color:
            for entity2 in entityList:
                if entity2 != King:
                    if [entity.x, entity.y] in possibleSpots(entity2):
                        score -= 20

        # If their king is in check
        if type(entity) == King and entity.color != color:
            for entity2 in entityList:
                if entity2 != King:
                    if [entity.x, entity.y] in possibleSpots(entity2):
                        score += 20

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
        if entity.color != color:
            continue
        spots = possibleSpots(entity, entityList)
        for move in spots:
            allMoves.append([[entity.x, entity.y], move])
    return allMoves


def changeState(gameState, move):
    entityList = jsonDecoderBig(gameState)
    for entity in entityList:
        if [entity.x, entity.y] == move[1]:
            del entity
    for entity in entityList:
        if [entity.x, entity.y] == move[0]:
            entity.x = move[1][0]
            entity.y = move[1][1]

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


def populateFull(tree: Tree, gameState, color):
    colors = [0, 1]
    populate(tree, gameState, color)
    for branch in tree.branches:
        gameState2 = changeState(gameState, branch.data)
        populate(branch, gameState2, colors[colors.index(color) - 1])
        for subBranch in branch.branches:
            gameState3 = changeState(gameState2, subBranch.data)
            populate(subBranch, gameState3, color)
            for subSubBranch in subBranch.branches:
                gameState4 = changeState(gameState3, subSubBranch.data)
                populate(subSubBranch, gameState4, colors[colors.index(color) - 1])


a = Pawn(0, 0, 0)
jsonSerializer(a)
f = open("JSONDATA.json", "r")
contents = f.read()
f.close()
root = Tree(None)
populateFull(root, contents, 0)
print("Hi")
f = open("Log.txt", "w")
print(f"Root branches {len(root.branches)}")
f.write(f"{len(root.branches)}\n")
for branch in root.branches:
    f.write(f"Move: {branch.data}, Branchs branches: {len(branch.branches)}\n")
f.close()
