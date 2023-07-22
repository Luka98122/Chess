import pygame
from globals import *


class Bishop:
    # BlackBishop = globals.BlackBishop
    # WhiteBishop = globals.WhiteBishop
    strType = "bishop"
    value = 4

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
            img = globals.BlackBishop
        else:
            img = globals.WhiteBishop
        img = pygame.transform.scale(img, (80, 100))
        window.blit(img, pygame.Rect(self.x * 100 + 10, self.y * 100, 100, 100))

    def update(self):
        pass
