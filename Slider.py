import pygame

pygame.init()


class Slider:
    def __init__(self, rect, min_val, max_val, boxColor, sliderColor):
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        self.held = False
        self.boxColor = boxColor
        self.sliderColor = sliderColor
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(screen, self.boxColor, self.rect, 1)
        pos_x = self.rect.x + (
            self.rect.width
            * ((self.value - self.min_val) / (self.max_val - self.min_val))
        )
        pygame.draw.circle(
            screen,
            self.sliderColor,
            (int(pos_x), self.rect.y + self.rect.height // 2),
            self.rect.height // 2,
        )
        value_text = self.font.render(str(int(self.value)), True, pygame.Color("White"))
        screen.blit(value_text, (pos_x - 20, self.rect.y - 40))

    def handle_event(self):
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0]:

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.held = True
                print("HELD")
        if mouseState[0] == False:
            self.held = False
        if self.held:
            print("made it 2")
            x_pos = pygame.mouse.get_pos()[0] - self.rect.x
            self.value = (x_pos / self.rect.width) * (
                self.max_val - self.min_val
            ) + self.min_val
            self.value = max(min(self.value, self.max_val), self.min_val)
