BLOCK_SIZE = 32
import pygame
pygame.init()

class Item():
    maxStack = None
    placeable = False
    def __init__(self) -> None:
        pass


class Dirt(Item):
    maxStack = 64
    placeable = True
    img = pygame.image.load("Textures\\Dirt.png")
    img = pygame.transform.scale(img, (BLOCK_SIZE-4, BLOCK_SIZE-4))
    def __init__(self) -> None:
        super().__init__()
    
class WoodPlatform(Item):
    maxStack = 64
    placeable = True
    img = pygame.image.load("Textures\\Wood_Platform.png")
    img = pygame.transform.scale(img, (BLOCK_SIZE-4, BLOCK_SIZE-4))
    def __init__(self) -> None:
        super().__init__()
    
