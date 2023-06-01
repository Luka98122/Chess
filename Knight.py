import pygame


class Knight:
    BlackKnight = pygame.image.load("Textures\\BlackKnight.png")
    WhiteKnight = pygame.image.load("Textures\\WhiteKnight.png")
    strType = "knight"

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
        if self.color == 0:
            img = self.BlackKnight
        else:
            img = self.WhiteKnight
        img = pygame.transform.scale(img, (100, 100))
        window.blit(img, pygame.Rect(self.x * 100, self.y * 100, 100, 100))

    def update(self):
        pass
