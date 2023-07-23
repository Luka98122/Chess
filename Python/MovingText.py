import pygame

pygame.init()


class MovingText:
    def __init__(self, text, textSize, textColor, x, y, params, xSpeed, ySpeed) -> None:
        self.text = text
        self.textSize = textSize
        self.textColor = textColor
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.width = params[0]
        self.height = params[1]

    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

    def draw(self, window):
        font = pygame.font.Font(None, self.textSize)
        text1 = font.render(self.text, True, pygame.Color(self.textColor))
        text_rect = text1.get_rect(center=(self.x + self.width, self.y + self.height))
        window.blit(text1, text_rect)
