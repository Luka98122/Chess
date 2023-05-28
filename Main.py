import pygame
import time
import tkinter as tk
from tkinter import filedialog
import json
import socket


from copy import *
from Pawn import *
from Button import *
from Rook import *
from Bishop import *
from Knight import *
from Queen import *
from King import *

from HelperFunctions import *
from MovingText import *

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


def possibleSpots(entity, entityList):
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
            if [x, y] in possibleSpots(entity, entityList):
                return False
    return True


def setUpPawns(entityList):
    for i in range(8):
        pawn = Pawn(i, 1, 1)
        entityList.append(pawn)
    for i in range(8):
        pawn = Pawn(i, 6, 0)
        entityList.append(pawn)
    return entityList


def setUpBoard(entityList):
    entityList = setUpPawns(entityList)
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
    return entityList


def createObject(strType, pos, color):
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
    return obj


def select_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Chess Save", ".chess")], defaultextension=".chess"
    )
    print(filepath)
    return filepath


def jsonDecoder(data):
    obj = createObject(data["type"], [data["x"], data["y"]], data["color"])
    return obj


def load_file(filepath):
    entityList = []
    with open(filepath, "r") as file:
        gameState = json.load(file)
        entityListofDicts = gameState["GameState"]
    for dict in entityListofDicts:
        entity = jsonDecoder(dict)
        if entity not in ["Error", None]:
            entityList.append(entity)
    print("LOADED")
    return entityList


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
                if possibleSpots(entity, entityList) != []:
                    flagVar = 1
                    break
        if flagVar == 0:
            print(f"Stalemate, {king.color} is pinned!")
            exit()


# Main


def doScreen(screenCode, window):
    if screenCode == "credits":
        creditsSpeed = 0.2
        creditsText = MovingText("-Credits-", 40, "Red", 200, -100, [200, 100], 0, 0.2)
        LMText = MovingText("Luka Markovic", 40, "Red", 200, -150, [200, 100], 0, 0.2)
        DLText = MovingText("Dejan Livada", 40, "Red", 200, -200, [200, 100], 0, 0.2)
        texts = []
        texts.append(creditsText)
        texts.append(LMText)
        texts.append(DLText)
        while True:
            window.fill("Black")
            for text in texts:
                text.update()
                text.draw(window)
                if text.text == "Dejan Livada" and text.y > 810:
                    return
            pygame.display.flip()


def main_menu():
    listOfButtons = []
    playButton = Button(pygame.Rect(300, 50, 200, 100), "Play Shared Computer", 25)
    listOfButtons.append(playButton)
    playButton = Button(pygame.Rect(300, 200, 200, 100), "Lan Multiplayer", 25)
    listOfButtons.append(playButton)
    playButton = Button(pygame.Rect(300, 350, 200, 100), "Load Game", 25)
    listOfButtons.append(playButton)
    playButton = Button(pygame.Rect(300, 500, 200, 100), "Credits", 25)
    listOfButtons.append(playButton)
    playButton = Button(pygame.Rect(300, 650, 200, 100), "Quit", 25)
    listOfButtons.append(playButton)

    while True:
        window.fill("Black")

        for button in listOfButtons:
            res = button.update()
            if res == True:
                if button.text == "Play Shared Computer":
                    main(False, None)
                if button.text == "Credits":
                    doScreen("credits", window)
                if button.text == "Quit":
                    exit()
                if button.text == "Load Game":
                    root = tk.Tk()
                    root.withdraw()
                    path = select_file()
                    if path not in [None, ""]:
                        entityList = load_file(path)
                        main(False, entityList)
                    else:
                        return

        for button in listOfButtons:
            button.draw(window)

        pygame.display.flip()


def serialize_to_json(x, y, x1, y1):
    data = {"x": x, "y": y, "x1": x1, "y1": y1}
    json_data = json.dumps(data)
    return json_data


def deserialize_from_json(json_data):
    data = json.loads(json_data)

    x = data["x"]
    y = data["y"]
    x1 = data["x1"]
    y1 = data["y1"]

    return x, y, x1, y1


def main_online_client():
    serverIp = input()
    if entityList == None:
        entityList = []
        entityList = setUpBoard(entityList)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if input("1 or 2") == "1":
        serverSocket.connect(serverIp, 61292)
    if input("1 or 2") == "2":
        serverSocket.connect(serverIp, 61293)
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 30
    cooldown = cooldownInit
    turnNo = 1
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
                print("Clickeeeeeed")
                if lastEntity != None:
                    if turnNo % 2 == lastEntity.color:
                        if res[0] == True:
                            if res[1] != None:
                                if res[1].color != lastEntity.color:
                                    if tilePos in spots:
                                        serverSocket.send(
                                            serialize_to_json(
                                                lastEntity.x,
                                                lastEntity.y,
                                                tilePos[0],
                                                tilePos[1],
                                            )
                                        )

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
                                serverSocket.send(
                                    serialize_to_json(
                                        lastEntity.x,
                                        lastEntity.y,
                                        tilePos[0],
                                        tilePos[1],
                                    )
                                )
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
                    spots = possibleSpots(entityClickedOn, entityList)
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


def main(freeMove, entityList):
    if entityList == None:
        entityList = []
        entityList = setUpBoard(entityList)
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 30
    cooldown = cooldownInit
    turnNo = 1
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
                print("Clickeeeeeed")
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
                    spots = possibleSpots(entityClickedOn, entityList)
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


def main_server_mode():

    server1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player1IP = input("Enter player 1s ip address.")
    player2IP = input("Enter player 2s ip address.")
    server1_socket.bind("0.0.0.0", 61292)
    server2_socket.bind("0.0.0.0", 61293)
    client1_socket, client1_address = server1_socket.accept()
    client2_socket, client2_address = server2_socket.accept()

    entityList = setUpBoard([])
    turnNo = 1
    while True:
        if turnNo % 2 == 0:
            playerInput = input()  # [[x,y] to [x1,y1]]
        else:
            playerInput = input()
        x = int(playerInput.split(",")[0])
        y = int(playerInput.split(",")[1])
        x1 = int(playerInput.split(",")[2])
        y1 = int(playerInput.split(",")[3])

        entityClickedOn = spotOccupied(x, y, entityList)[1]
        spots = possibleSpots(entityClickedOn, entityList)
        if [x1, y1] in spots:
            entityClickedOn.move([x1, y1])
            print("Moved")
        else:
            print("Illegal move")


main_server_mode()

main_menu()
main(True, entityList)
