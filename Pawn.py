import pygame
from Button import *
from HelperFunctions import *
from Bishop import *
from Rook import *
from Knight import *
from Queen import *


class Pawn:
    # init
    BlackPawn = pygame.image.load("Textures\\BlackPawn.png")
    WhitePawn = pygame.image.load("Textures\\WhitePawn.png")
    strType = "pawn"

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
            self.pawnPromotion(window, pawnIndex, EntityList)

    def pawnPromotion(self, window, pawnIndex, listOfEntities):
        s = pygame.Surface((800, 800))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        buttons = []
        bishopButton = Button(pygame.Rect(15, 100, 175, 75), "Bishop", 25)
        buttons.append(bishopButton)
        knightButton = Button(pygame.Rect(215, 100, 175, 75), "Knight", 25)
        buttons.append(knightButton)
        rookButton = Button(pygame.Rect(415, 100, 175, 75), "Rook", 25)
        buttons.append(rookButton)
        queenButton = Button(pygame.Rect(615, 100, 175, 75), "Queen", 25)
        buttons.append(queenButton)

        while True:
            crtaj_tablu(window)
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
