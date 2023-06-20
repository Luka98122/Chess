import pygame


class Bishop:
    BlackBishop = pygame.image.load("Textures\\BlackBishop.png")
    WhiteBishop = pygame.image.load("Textures\\WhiteBishop.png")
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
            img = self.BlackBishop
        else:
            img = self.WhiteBishop
        img = pygame.transform.scale(img, (80, 100))
        window.blit(img, pygame.Rect(self.x * 100 + 10, self.y * 100, 100, 100))

    def update(self):
        pass
