import pygame
import Item
pygame.init()

class Globals:
    # Blocks
    AIR = 0
    DIRT = 1
    GRASS = 2
    STONE = 3
    WOOD_PLATFORM = 4
    BLOCK_SIZE = 32
    colors_dict = {
    AIR : pygame.Color("Cyan"),
    DIRT : pygame.Color("Brown"),
    GRASS : pygame.Color("chartreuse2"),
    STONE : pygame.Color("Grey"),
    WOOD_PLATFORM : None 
    }

    img_dict = {
        WOOD_PLATFORM :  pygame.transform.scale(pygame.image.load("Textures\\Wood_Platform.png"), (BLOCK_SIZE, BLOCK_SIZE/2))
    }
    
    items_dict = {
        DIRT : Item.Dirt,
        WOOD_PLATFORM : Item.WoodPlatform
    }
    