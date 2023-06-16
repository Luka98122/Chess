import pygame

pygame.init()


class Settings:
    debug = False
    width = 900
    myChatColor = pygame.Color("Red")
    theirChatColor = pygame.Color("Blue")

    def __init__(self) -> None:
        pass
