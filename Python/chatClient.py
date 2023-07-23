import socket
import pygame
from Settings import *

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
        self.them.sendall(("<CHAT>" + text).encode())
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
                color = Settings.theirChatColor
            if text[0] == "SENT":
                color = Settings.myChatColor
            h = max(32, len(text) // 16 * 32)
            offset += h
            draw_box = pygame.Rect(800, 600 - offset, 200, h)
            txt_surface = self.font.render(text[1], True, color)
            window.blit(txt_surface, (draw_box.x + 5, draw_box.y + 5))
            pygame.draw.rect(window, color, draw_box, 2)
