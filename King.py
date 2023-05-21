import pygame
from HelperFunctions import *
import time

class King:
    BlackKing = pygame.image.load("Textures\\BlackKing.png")
    WhiteKing = pygame.image.load("Textures\\WhiteKing.png")
    strType = "king"

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.timeChecked = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, window):
        self.window = window
        if self.color == 0:
            img = self.BlackKing
        else:
            img = self.WhiteKing
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self, EntityList, possibleSpots):
        if isSpotProtected(self, EntityList, possibleSpots) == True:
            self.checkedTime += 1
            if self.checkedTime == 2:
                rect = pygame.Rect(200, 200, 400, 300)
                darkenScreen()
                pygame.draw.rect(self.window, pygame.Color("White"), rect)
                pygame.draw.rect(self.window, pygame.Color("Black"), rect, 2)
                font = pygame.font.Font(None, 40)
                text1 = font.render(
                    f"Color {self.color} lost to a checkmate.",
                    True,
                    pygame.Color("Black"),
                )
                text_rect = text1.get_rect(
                    center=(
                        rect.x + rect.width / 2,
                        rect.y + rect.height / 2,
                    )
                )

                self.window.blit(text1, text_rect)
                pygame.display.flip()
                time.sleep(10)
            else:
                self.checkedTime = 0
            flagVar = 0
        if isSpotProtected(self,EntityList, possibleSpots) == False:
            for entity in EntityList:
                if entity.color == self.color:
                    if possibleSpots(entity) != []:
                        flagVar = 1
                        break
            if flagVar == 0:
                print(f"Stalemate, {self.color} is pinned!")
                exit()
