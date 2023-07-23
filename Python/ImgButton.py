import pygame

pygame.init()


class ImgButton:
    def __init__(self, rect, img) -> None:
        self.rect = rect
        self.img = img
        self.pos = pygame.Vector2(rect.x, rect.y)

    def update(self):
        mouseB = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if (
            mousePos[0] > self.rect.x
            and mousePos[0] < self.rect.x + self.rect.width
            and mousePos[1] > self.rect.y
            and mousePos[1] < self.rect.y + self.rect.height
            and mouseB[0] == True
        ):
            return True
        return False

    def draw(self, window):
        window.blit(self.img, (self.pos.x, self.pos.y))
