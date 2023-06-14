import pygame
import time
import tkinter as tk
from tkinter import filedialog
import json
import socket
import threading

from copy import *
from Pawn import *
from Button import *
from Rook import *
from Bishop import *
from Knight import *
from Queen import *
from King import *
from globals import *
from HelperFunctions import *
from MovingText import *
from textTest import *
from chatClient import *

pygame.init()


window = pygame.display.set_mode((globals.windowLength, globals.windowHeight))


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
        pawn = Pawn(i, 1, 0)
        entityList.append(pawn)
    for i in range(8):
        pawn = Pawn(i, 6, 1)
        entityList.append(pawn)
    return entityList


def setUpBoard(entityList):
    entityList = setUpPawns(entityList)
    # Rooks
    rook1 = Rook(0, 0, 0)
    rook2 = Rook(7, 0, 0)
    rook3 = Rook(0, 7, 1)
    rook4 = Rook(7, 7, 1)
    entityList.append(rook1)
    entityList.append(rook2)
    entityList.append(rook3)
    entityList.append(rook4)
    # Bishops
    b1 = Knight(1, 0, 0)
    b2 = Knight(6, 0, 0)
    b3 = Knight(1, 7, 1)
    b4 = Knight(6, 7, 1)
    entityList.append(b1)
    entityList.append(b2)
    entityList.append(b3)
    entityList.append(b4)
    # Queens
    q1 = Queen(3, 0, 0)
    q2 = Queen(3, 7, 1)
    entityList.append(q1)
    entityList.append(q2)
    # Kings
    k1 = King(4, 0, 0)
    k2 = King(4, 7, 1)
    entityList.append(k1)
    entityList.append(k2)
    # Knights
    kn1 = Bishop(2, 0, 0)
    kn2 = Bishop(5, 0, 0)
    kn3 = Bishop(5, 7, 1)
    kn4 = Bishop(2, 7, 1)
    entityList.append(kn1)
    entityList.append(kn2)
    entityList.append(kn3)
    entityList.append(kn4)
    return entityList


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


def select_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Chess Save", ".chess")], defaultextension=".chess"
    )
    print(filepath)
    return filepath


def jsonDecoder(data):
    obj = createObject(
        data["type"], [data["x"], data["y"]], data["color"], data["moves"]
    )
    return obj


def jsonDecoderBig(data):
    print(data.decode())
    data = json.loads(data.decode())
    gamestate = data["GameState"]
    if gamestate == None:
        return None
    rL = []
    for item in gamestate:
        obj = jsonDecoder(item)
        rL.append(obj)
    return rL


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


# Player 0
# receiver 60292

# sendto 60293


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
    pressedOnEntry = False
    allowClicks = True
    if pygame.mouse.get_pressed()[0] == True:
        pressedOnEntry = True
        allowClicks = False
    while True:
        window.fill("Black")
        if pressedOnEntry == True:
            if pygame.mouse.get_pressed()[0] == False:
                allowClicks = True
        for button in listOfButtons:
            if allowClicks == True:
                res = button.update()
                if res == True:
                    if button.text == "Play Shared Computer":
                        main(False, None)
                    if button.text == "Credits":
                        doScreen("credits", window)
                    if button.text == "Lan Multiplayer":
                        buttons = []
                        white = Button(pygame.Rect(50, 250, 250, 100), "White", 35)
                        black = Button(pygame.Rect(500, 250, 250, 100), "Black", 35)
                        server = Button(pygame.Rect(275, 450, 250, 100), "Server", 35)
                        buttons.append(server)
                        buttons.append(white)
                        buttons.append(black)
                        while True:
                            crtaj_tablu(window)
                            for button in buttons:
                                button.draw(window)
                                if button.update() == True:
                                    if button.text == "White":
                                        main_online_client(0)
                                    if button.text == "Black":
                                        main_online_client(1)
                                    if button.text == "Server":
                                        pygame.display.quit()
                                        main_server_mode()
                            pygame.display.flip()

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
    if json_data == "":
        return "WHY"
    data = json.loads(json_data)

    x = data["x"]
    y = data["y"]
    x1 = data["x1"]
    y1 = data["y1"]

    return x, y, x1, y1


def takeCareOfChat(chatObj: inputBox, chatBoxObj: chatClient, window):
    while True:
        chatRes = chatObj.update(pygame.mouse.get_pressed(), pygame.event.get())
        if chatRes != None:
            chatBoxObj.send(chatRes)
        chatBoxObj.draw(window)
        chatObj.draw(window)


class Globals:
    data = None


def receive_messages(sock):
    while True:
        data, addr = sock.recvfrom(20000)
        Globals.data = data


def main_online_client(playerID):
    freeMove = False
    serverIp = "127.0.0.1"
    entityList = []
    entityList = setUpBoard(entityList)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((serverIp, 61292))
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 30
    cooldown = cooldownInit
    window = pygame.display.set_mode((950, 800))
    turnNo = 0
    chatBox = inputBox(pygame.Rect(800, 650, 200, 150))
    string = ""
    # if playerID == 0:
    #    me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    me.bind(("127.0.0.1", 62292))
    #    print("binded")
    #    me.listen(10)
    #    them, adr = me.accept()
    #    print("received")
    #    chat = chatClient(them)
    # else:
    #    them = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    them.bind(("127.0.0.1", 62293))
    #    print("bouta connect")
    #    them.connect(("127.0.0.1", 62292))
    #    print("connected")
    #    chat = chatClient(them)
    chat = chatClient(serverSocket)
    if playerID == 0:
        string = "WHITE"
        print(
            " __      __.__    .__  __           _________ .____    .______________ __________________"
        )
        print(
            "/  \    /  \  |__ |__|/  |_  ____   \_   ___ \|    |   |   \_   _____/ \      \__    ___/"
        )
        print(
            "\   \/\/   /  |  \|  \   __\/ __ \  /    \  \/|    |   |   ||    __)_  /   |   \|    |   "
        )
        print(
            " \        /|   Y  \  ||  | \  ___/  \     \___|    |___|   ||        \/    |    \    |   "
        )
        print(
            "  \__/\  / |___|  /__||__|  \___  >  \______  /_______ \___/_______  /\____|__  /____|   "
        )
        print(
            "       \/       \/              \/          \/        \/           \/         \/        "
        )

    else:
        string = "BLACK"
        print(
            "__________.__                 __        _________ .____    .______________ __________________"
        )
        print(
            "\______   \  | _____    ____ |  | __    \_   ___ \|    |   |   \_   _____/ \      \__    ___/"
        )
        print(
            " |    |  _/  | \__  \ _/ ___\|  |/ /    /    \  \/|    |   |   ||    __)_  /   |   \|    |   "
        )
        print(
            " |    |   \  |__/ __ \\  \___|    <     \     \___|    |___|   ||        \/    |    \    |   "
        )
        print(
            " |______  /____(____  /\___  >__|_ \     \______  /_______ \___/_______  /\____|__  /____|   "
        )
        print(
            "        \/          \/     \/     \/            \/        \/           \/         \/       "
        )
    pygame.display.set_caption(f"Online client {string}")
    print(f"{string} is COLOR {playerID}")
    # serverSocket.settimeout(2.0)
    t = threading.Thread(target=receive_messages, args=[serverSocket])
    t.start()
    lastRecv = None
    while program_radi:
        window.fill("Black")
        if turnNo % 2 != playerID:
            print("In limbo")
            crtaj_tablu(window)
            events = pygame.event.get()
            mouseB = pygame.mouse.get_pressed()
            for entity in entityList:
                entity.draw(window)
            chatRes = chatBox.update(mouseB, events)
            if chatRes != None:
                chat.send(chatRes)
            chatBox.draw(window)
            chat.draw(window)
            pygame.display.flip()
            try:
                if Globals.data != None:
                    if lastRecv != Globals.data:
                        rres = Globals.data
                        lastRecv = Globals.data
                    else:
                        continue
                else:
                    continue
            except:
                continue
            if rres.decode().startswith("CHAT"):
                chat.addRecv(rres.decode()[4:])
                continue
            res = rres.decode()
            print(rres[0])
            if len(res) == 1:
                a = 2
            if res[0] == str(playerID):
                serverSocket.close()
                buttons = []
                fakeButton = Button(pygame.Rect(300, 50, 200, 100), "YOU WON", 45)
                backToMenu = Button(
                    pygame.Rect(300, 500, 200, 100), "Back to Main Menu", 20
                )
                buttons.append(backToMenu)
                buttons.append(fakeButton)
                while True:
                    darkenScreen()
                    fakeButton.draw(window)
                    backToMenu.draw(window)
                    pygame.display.flip()
                    if backToMenu.update() == True:
                        main_menu()
            elif res[0] != str(playerID) and res[0] in ["0", "1"]:
                serverSocket.close()
                buttons = []
                fakeButton = Button(pygame.Rect(300, 50, 200, 100), "YOU LOST", 45)
                backToMenu = Button(
                    pygame.Rect(300, 500, 200, 100), "Back to Main Menu", 20
                )
                buttons.append(backToMenu)
                buttons.append(fakeButton)
                while True:
                    darkenScreen()
                    fakeButton.draw(window)
                    backToMenu.draw(window)
                    pygame.display.flip()
                    if backToMenu.update() == True:
                        main_menu()
            if jsonDecoderBig(rres) != None:
                entityList = jsonDecoderBig(rres)
            a = 2
            turnNo = json.loads(rres.decode())["TurnNo"]
            print("End of exception")

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
                print("Got something")
                cooldown = cooldownInit
                if lastEntity == None:
                    if playerID != entityClickedOn.color:
                        print("Got set to invalid")
                        entityClickedOn = None
            if entityClickedOn != None and lastEntity == entityClickedOn:
                print("Nulled out")
                entityClickedOn = None
                lastEntity = None
                spots = None
            res = spotOccupied(tilePos[0], tilePos[1], entityList)
            if spots != None:
                print("Clickeeeeeed")
                if lastEntity != None:
                    if res[0] == True:
                        if res[1] != None:
                            if tilePos in spots:
                                if lastEntity.color != playerID:
                                    continue
                                serverSocket.send(
                                    serialize_to_json(
                                        lastEntity.x,
                                        lastEntity.y,
                                        tilePos[0],
                                        tilePos[1],
                                    ).encode()
                                )

                                change = 1
                                turnNo += 1
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
                                ).encode()
                            )
                            print("Successfully sent")
                            change = 1
                            turnNo += 1
                            spots = None
                            continue
                else:
                    print("None")

            print("got clicked")
            if entityClickedOn == None:
                print("It was None?")
                pass
            else:
                lastEntity = entityClickedOn
                if playerID == entityClickedOn.color or freeMove:
                    spots = possibleSpots(entityClickedOn, entityList)
                    for i in range(10):
                        print("SPOTSSSSSSSSSSSSSSS")

        flagVar = 0
        try:
            if Globals.data != None:
                if lastRecv != Globals.data:
                    rres = Globals.data
                    lastRecv = Globals.data
                    if rres.decode().startswith("CHAT"):
                        chat.addRecv(rres.decode()[4:])
        except:
            pass
        chatRes = chatBox.update(mouseB, events)
        if chatRes != None:
            chat.send(chatRes)
        chatBox.draw(window)
        chat.draw(window)
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
        pygame.event.pump()
        pygame.display.flip()
        cooldown -= 1


def jsonSerializer(object):
    resList = {
        "type": object.strType,
        "x": object.x,
        "y": object.y,
        "color": object.color,
        "moves": object.moves,
    }
    return resList


def main_server_mode():
    offline = False
    if offline == False:
        server1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server1_socket.bind(("0.0.0.0", 61292))
        server1_socket.listen(10)

        client1_socket, client1_address = server1_socket.accept()
        print("got client 1")
        client2_socket, client2_address = server1_socket.accept()
        print("got client 2")

    entityList = setUpBoard([])

    turnNo = 0
    while True:
        print("in this loop")
        client1_socket.settimeout(1.0)
        client2_socket.settimeout(1.0)

        while True:
            try:
                player1Input = client1_socket.recvfrom(20000)[0].decode()
                if player1Input.startswith("CHAT"):
                    if len(player1Input) > 50:
                        print("Sent gamestate lol")
                    client2_socket.send(player1Input.encode())
                else:
                    if turnNo % 2 == 0:
                        playerInput = player1Input
                        break
            except:
                pass
            try:
                player2Input = client2_socket.recvfrom(20000)[0].decode()
                if player2Input.startswith("CHAT"):
                    client1_socket.send(player2Input.encode())
                    if len(player1Input) > 50:
                        print("Sent gamestate lol")
                else:
                    if turnNo % 2 == 1:
                        playerInput = player2Input
                        break
            except:
                pass

        print("Got stuff")
        b = deserialize_from_json(playerInput)
        if b == "WHY":
            print("got why")
            continue
        x = b[0]
        y = b[1]
        x1 = b[2]
        y1 = b[3]

        entityClickedOn = spotOccupied(x, y, entityList)[1]
        spots = possibleSpots(entityClickedOn, entityList)
        if [x1, y1] in spots:
            print("Valid move")
            if spotOccupied(x1, y1, entityList)[0] == True:
                del entityList[entityList.index(spotOccupied(x1, y1, entityList)[1])]
            entityClickedOn.move([x1, y1])
            foundKings = []
            for entity in entityList:
                if type(entity) == King:
                    foundKings.append(entity)
            print("Found kings")
            if len(foundKings) == 1:
                # Somebody won
                if foundKings[0].color == 0:
                    client1_socket.sendall("0".encode())
                    client2_socket.sendall("0".encode())
                    client1_socket.close()
                    client2_socket.close()
                    print("A winner has been found")
                    exit()

                else:
                    client1_socket.sendall("1".encode())
                    client2_socket.sendall("1".encode())
                    client1_socket.close()
                    client2_socket.close()

                    print("A winner has been found")
                    exit()
            print("Checked for winners")
            dataList = []
            for entity in entityList:
                data = jsonSerializer(entity)
                dataList.append(data)
            turnNo += 1
            info = {"GameState": dataList, "TurnNo": turnNo, "Validity": True}
            json_object = json.dumps(info, indent=4)
            print("Moved")
            if json_object.encode() == b"":
                print("OMG BUGGGGGGGGGGGGGGGG")
                a = 2
            client1_socket.sendall(json_object.encode())
            client2_socket.sendall(json_object.encode())

        else:
            print("Invalid move")
            info = {"GameState": None, "TurnNo": turnNo, "Validity": False}
            json_object = json.dumps(info, indent=4)
            print("Moved")
            if json_object.encode() == b"":
                print(" ILLEGAL MOVE BUG")
                a = 2
            if turnNo % 2 == 0:
                client1_socket.sendall(json_object.encode())
            else:
                client2_socket.sendall(json_object.encode())
            print("Illegal move")

        # crtaj_tablu(window)
        # for entity in entityList:
        #    entity.draw(window)
        # pygame.display.flip()


def main(freeMove, entityList):
    if entityList == None:
        entityList = []
        entityList = setUpBoard(entityList)
    lastEntity = None
    program_radi = True
    spots = None
    cooldownInit = 30
    cooldown = cooldownInit
    turnNo = 0
    while program_radi:
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


# Classes

pygame.display.set_caption("Chess.com")
main_menu()
main(True, entityList)
