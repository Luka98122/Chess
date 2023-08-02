import pygame

pygame.init()


class Button:
    def __init__(self, rect, text, textSize) -> None:
        self.rect = rect
        self.text = text
        self.textSize = textSize

    def update(self, mouseB, mousePos):
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

        pygame.draw.rect(window, pygame.Color("White"), self.rect)
        pygame.draw.rect(window, pygame.Color("Black"), self.rect, 2)
        font = pygame.font.Font(None, self.textSize)
        text1 = font.render(self.text, True, pygame.Color("Black"))
        text_rect = text1.get_rect(
            center=(
                self.rect.x + self.rect.width / 2,
                self.rect.y + self.rect.height / 2,
            )
        )
        window.blit(text1, text_rect)