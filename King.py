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
        self.moves = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, window):
        self.window = window
        if self.color == 1:
            img = self.BlackKing
        else:
            img = self.WhiteKing
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self, EntityList, possibleSpots):
        pass
