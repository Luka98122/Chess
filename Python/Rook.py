import pygame
from globals import *


class Rook:
    # BlackRook = globals.BlackRook
    # WhiteRook = globals.WhiteRook
    strType = "rook"
    value = 5

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
            img = globals.BlackRook
        else:
            img = globals.WhiteRook
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass
