import pygame
from HelperFunctions import *
import time
from globals import *


class King:
    # BlackKing = globals.BlackKing
    # WhiteKing = globals.WhiteKing
    strType = "king"
    value = 1000

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.timeChecked = 0
        self.moves = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, window):
        if self.color == 1:
            img = globals.BlackKing
        else:
            img = globals.WhiteKing
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self, EntityList, possibleSpots):
        pass
