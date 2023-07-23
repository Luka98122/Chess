import pygame
from globals import *


class Queen:
    # BlackQueen = globals.BlackQueen
    # WhiteQueen = globals.WhiteQueen
    strType = "queen"
    value = 9

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.moves = 0

    def move(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.moves += 1

    def draw(self, window):
        if self.color == 1:
            img = globals.BlackQueen
        else:
            img = globals.WhiteQueen
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass
