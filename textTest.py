import pygame

pygame.init()


def quickCollide(pos, rect):
    if (
        pos[0] > rect.x
        and pos[0] < rect.x + rect.w
        and pos[1] > rect.y
        and pos[1] < rect.y + rect.h
    ):
        return True
    return False


class inputBox:
    def __init__(self, rect) -> None:

        self.font = pygame.font.Font(None, 32)
        self.input_box = rect
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.active = False
        self.text = ""
        self.lines = [""]

    def update_text(self, text, font, box_width):
        words = text.split(" ")
        lines = [""]
        for word in words:
            temp_line = lines[-1] + " " + word if lines[-1] else word
            temp_text = font.render(temp_line, True, self.color)
            if temp_text.get_width() <= box_width:
                lines[-1] = temp_line
            else:
                lines.append(word)
        return lines

    def update(self, mouseState, events):
        if self.active == True:
            a = 2
        for event in events:
            if mouseState[0] == True:
                if quickCollide(pygame.mouse.get_pos(), self.input_box):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
            if event.type == pygame.KEYDOWN:
                print("KD")
                if self.active == True:
                    print("ACTIVE")
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        a = self.text
                        self.text = ""
                        self.lines = [""]
                        print(a)
                        return a

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        print("Text added")
                        self.text += event.unicode
                    self.lines = self.update_text(
                        self.text, self.font, self.input_box.width - 10
                    )

        return None

    def draw(self, window):
        for i, line in enumerate(self.lines):
            txt_surface = self.font.render(line, True, self.color)
            window.blit(
                txt_surface, (self.input_box.x + 5, self.input_box.y + 5 + i * 32)
            )
        self.input_box.h = max(32, len(self.lines) * 32)
        pygame.draw.rect(window, self.color, self.input_box, 2)
