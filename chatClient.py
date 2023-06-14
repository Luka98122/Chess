import socket
import pygame

pygame.init()


class chatClient:
    def __init__(self, serverSocket):
        self.font = pygame.font.Font(None, 32)
        self.them = serverSocket
        self.recvs = []
        self.things = []
        self.color = pygame.Color("Red")
        pass

    def send(self, text):
        self.them.sendall(("CHAT" + text).encode())
        self.things.append(["SENT", text])
        pass

    def addRecv(self, text):
        self.recvs.append(text)
        self.things.append(["RECV", text])
        print(f"GOT {text}")

    def draw(self, window):
        offset = 0
        for text in reversed(self.things):
            color = None
            if text[0] == "RECV":
                color = pygame.Color("LightBlue")
            if text[0] == "SENT":
                color = pygame.Color("Purple")
            h = max(32, len(text) // 16 * 32)
            offset += h
            draw_box = pygame.Rect(800, 600 - offset, 200, h)
            txt_surface = self.font.render(text[1], True, color)
            window.blit(txt_surface, (draw_box.x + 5, draw_box.y + 5))
            pygame.draw.rect(window, color, draw_box, 2)
