import pygame
import math
import Item
from Globals import *
print(Globals.items_dict)
BLOCK_SIZE = 32
class Player:
    img = pygame.image.load("Textures\\Player.png")
    img = pygame.transform.scale(img, (BLOCK_SIZE,BLOCK_SIZE))
    img_copy = img.copy()
    img_with_flip = pygame.transform.flip(img_copy, True, False)
    img_with_flip = pygame.transform.scale(img_with_flip, (BLOCK_SIZE, BLOCK_SIZE))
    current_img = img
    accuracy = 1
    ddy = 0.1
    dx = 0
    dy = 5
    reach = 15
    inventory = []
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def update(self,keys,world, cameraX, cameraY):
        i = 0
        while i < (len(self.inventory)):
            if self.inventory[i][1] <= 0:
                del self.inventory[i]
                i -=1
            i +=1
        self.dx = 0
        self.dy += self.ddy
        if self.dy > -0.3 and self.dy < 1:
            self.dy = 1
        if self.dy > 2:
            self.dy = 2
        if keys[pygame.K_a]:
            self.dx = -1*self.accuracy
        if keys[pygame.K_d]:
            self.dx = 1*self.accuracy
        if keys[pygame.K_SPACE] and world[int(self.y+1)][int(self.x)] != 0:
            self.dy = -1.8*self.accuracy
        else:
            if self.y > 29 and self.y < 30:
                self.y = 30
        for i in range(self.accuracy):
            try:
                if self.x+self.dx/self.accuracy>=0:
                    if world[int(self.y)][math.ceil(self.x+self.dx/self.accuracy)] == 0 and self.dx != 0:
                        self.x += self.dx/self.accuracy
                        cameraX += self.dx/self.accuracy
                        print(f"Moved x {self.x}")
            except:
                pass
            for i in range(abs(int(self.dy))):
                if world[math.ceil(self.y+self.dy/abs(self.dy))][int(self.x)] == 0 and self.dy != 0:
                    self.y +=  self.dy/abs(self.dy)
                    cameraY += self.dy/abs(self.dy)
                    print(f"Moved y {self.y}")
            """""
            try:
                if self.y + self.dy/self.accuracy > 0:
                    if world[math.ceil(self.y+self.dy/self.accuracy)][int(self.x)] == 0 and self.dy != 0:
                        self.y += self.dy / self.accuracy
                        cameraY += self.dy / self.accuracy
                        print(f"Moved y {self.y}")
            except:
                pass
            """
            return [cameraX,cameraY]
    
    
    def sortInv(self):
        self.inventory.sort(reverse=True)
    
    
    def addToInventory(self,itemInfo):
        leftToGive = itemInfo[1]
        flag = 1
        for item in self.inventory:
            if item[0] == itemInfo[0]:
                flag = 0
                if item[1] != itemInfo[0].maxStack:
                    if leftToGive + item[1] <= itemInfo[0].maxStack:
                        item[1] += leftToGive
                        return
                    else:
                        ogHad = item[1]
                        item[1] += itemInfo[0].maxStack-item[1]
                        leftToGive -= itemInfo[0].maxStack-ogHad
        if leftToGive != 0:
            while leftToGive>0:
                if itemInfo[0].maxStack == leftToGive:
                    self.inventory.append([itemInfo[0], leftToGive])
                    leftToGive = 0
                    break
                self.inventory.append([itemInfo[0], leftToGive%itemInfo[0].maxStack])
                leftToGive -= leftToGive%itemInfo[0].maxStack
        self.sortInv()
    
    def build(self, mouseState, mousePos, world, Camera_X, Camera_Y, l):
        if mouseState[0]:
            x = int(int(mousePos[0]+Camera_X*BLOCK_SIZE)//BLOCK_SIZE)
            y = int(int(mousePos[1]+Camera_Y*BLOCK_SIZE)//BLOCK_SIZE)
            if abs(x-self.x) + abs(y-self.y) > self.reach:
                return [world,l]
            try:
                if world[y][x] == 0:
                    for i in range(0,len(self.inventory)+1):
                        item = self.inventory[len(self.inventory)-(i+1)]
                        if item[0] == Item.WoodPlatform and item[1] > 0:
                            flag = 0
                            world[y][x] = 4
                            l.append([x,y])
                            item[1] -=1
                        break
            except:
                print("Tried to build out of bounds")
        if mouseState[2]:
            x = int(int(mousePos[0]+Camera_X*BLOCK_SIZE)//BLOCK_SIZE)
            y = int(int(mousePos[1]+Camera_Y*BLOCK_SIZE)//BLOCK_SIZE)
            if abs(x-self.x) + abs(y-self.y) > self.reach:
                return [world,l]
            try:
                self.addToInventory([Globals.items_dict[world[y][x]], 1])
                self.sortInv()
                world[y][x] = 0
                print("Deleted")
                print(len(l))
                for i in range(len(l)):
                    if l[i] == [x,y]:
                        del l[i]
                        print(len(l))
                        break
            except:
                print("Tried to delete out of bounds")
        return [world,l]
            
    
    def draw(self,window : pygame.surface, CAMERA_X, CAMERA_Y):
        
        if self.dx < 0:
            self.current_img = self.img_with_flip
        elif self.dx > 0:
            self.current_img = self.img
        window.blit(self.current_img, pygame.Rect((self.x-CAMERA_X)*BLOCK_SIZE,(self.y-CAMERA_Y)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))