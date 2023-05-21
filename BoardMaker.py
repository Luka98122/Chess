# Library imports
import pygame
import tkinter as tk
from tkinter import filedialog
import json

# Chess imports
from HelperFunctions import *
from Pawn import *
from Bishop import *
from Knight import *
from Rook import *
from King import *
from Queen import *
from Button import *


class GameState:
    def __init__(self, entityList) -> None:
        self.entityList = entityList


window = pygame.display.set_mode((1000, 925))
pygame.display.set_caption("Board Maker")

buttons = []

PawnButton = Button(pygame.Rect(850, 50, 100, 50), "Pawn", 25)
BishopButton = Button(pygame.Rect(850, 150, 100, 50), "Bishop", 25)
KnightButton = Button(pygame.Rect(850, 250, 100, 50), "Knight", 25)
RookButton = Button(pygame.Rect(850, 350, 100, 50), "Rook", 25)
QueenButton = Button(pygame.Rect(850, 450, 100, 50), "Queen", 25)
KingButton = Button(pygame.Rect(850, 550, 100, 50), "King", 25)


buttons.append(PawnButton)
buttons.append(BishopButton)
buttons.append(KnightButton)
buttons.append(RookButton)
buttons.append(QueenButton)
buttons.append(KingButton)

toggleBlackWhiteButton = Button(pygame.Rect(825, 700, 150, 75), "Toggle Color", 30)
loadFileButon = Button(pygame.Rect(100, 825, 150, 75), "Load File", 30)
saveFileButon = Button(pygame.Rect(300, 825, 150, 75), "Save File", 30)
removePieceButton = Button(pygame.Rect(600, 825, 150, 75), "Remove Piece", 30)

buttons.append(toggleBlackWhiteButton)
buttons.append(loadFileButon)
buttons.append(saveFileButon)
buttons.append(removePieceButton)

color = "White"
colors = [
    "Black",
    "White",
]
colorIndex = 0

toggleColorCooldownInit = 100
toggleColorCooldown = 30

selectedType = "None"

entityList = []


def jsonSerializer(object):
    resList = {
        "type": object.strType,
        "x": object.x,
        "y": object.y,
        "color": object.color,
    }
    return resList


def createObject(strType, pos, color):
    if strType == "None":
        return
    if strType == "Remove":
        exit()
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


def save_file(filepath, entityList):
    dataList = []
    for entity in entityList:
        data = jsonSerializer(entity)
        dataList.append(data)
    info = {"GameState": dataList}
    json_object = json.dumps(info, indent=4)
    with open(filepath, "w") as file:
        file.write(json_object)
    print("SAVEDDDDDDDDDD")


def select_save_file():
    filepath = filedialog.asksaveasfilename(
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
        entityList.append(entity)
    print("LOADED")
    return entityList


while True:
    toggleColorCooldown -= 1
    for button in buttons:
        res = button.update()
        if res == True:
            if button.text == "Toggle Color":
                if toggleColorCooldown <= 0:
                    if colorIndex == 0:
                        colorIndex = 1
                    elif colorIndex == 1:
                        colorIndex = 0
                    toggleColorCooldown = toggleColorCooldownInit
            elif button.text == "Load File":
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                path = select_file()
                if path != None:
                    entityList = load_file(path)
            elif button.text == "Save File":
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                path = select_save_file()
                if path != None:
                    save_file(path, entityList)
            elif button.text == "Remove Piece":
                selectedType = "Remove"
            else:
                selectedType = button.text.lower()

    mousePos = pygame.mouse.get_pos()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0] == True:
        tileCoords = getTileClickedOn(mousePos)
        if (
            tileCoords[0] > 7
            or tileCoords[0] < 0
            or tileCoords[1] < 0
            or tileCoords[1] > 7
        ):
            pass
        else:
            if (
                spotOccupied(tileCoords[0], tileCoords[1], entityList)[0] == False
                and selectedType != "Remove"
            ):
                entity = createObject(selectedType, tileCoords, colorIndex)
                entityList.append(entity)
            elif selectedType == "Remove":
                for entity in entityList:
                    if entity.x == tileCoords[0] and entity.y == tileCoords[1]:
                        del entityList[entityList.index(entity)]
                        print("Deleted")
                        break

    window.fill("Gray")
    pygame.draw.rect(window, pygame.Color(color), pygame.Rect(800, 0, 200, 800))
    crtaj_tablu(window)

    for entity in entityList:
        entity.draw(window)
    for button in buttons:
        button.draw(window)

    color = colors[colorIndex]
    pygame.display.flip()
