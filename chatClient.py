import socket
import pygame

pygame.init()


class chatClient:
    def __init__(self, serverSocket):
        self.font = pygame.font.Font(None, 32)
        self.them = serverSocket
        self.recvs = []
        self.color = pygame.Color("Red")
        pass

    def send(self, text):
        self.them.sendall(("CHAT" + text).encode())
        pass

    def addRecv(self, text):
        self.recvs.append(text)
        print(f"GOT {text}")

    def draw(self, window):
        offset = 0
        for text in self.recvs:
            h = max(32, len(text) // 16 * 32)
            offset += h
            draw_box = pygame.Rect(800, 600 - offset, 200, h)
            txt_surface = self.font.render(text, True, pygame.Color("Red"))
            window.blit(txt_surface, (draw_box.x + 5, draw_box.y + 5))
            pygame.draw.rect(window, self.color, draw_box, 2)
