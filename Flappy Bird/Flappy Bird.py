import pygame
import random
pygame.init()

class Obstacle:
    def __init__(self,x) -> None:
        self.x = x
        self.height = 150
        self.width = 50
        self.top = random.randint(0,800-self.height)
        self.bottom = self.top + self.height
        pass
    
    def draw(self,window, camX):
        pygame.draw.rect(window, pygame.Color("Green"), pygame.Rect(self.x-camX, 0, self.width, self.top))
        pygame.draw.rect(window, pygame.Color("Green"), pygame.Rect(self.x-camX, self.top+self.height, self.width, 800-(self.top+self.height)))

    def update(self,playerX,playerY):
        if playerX+25>self.x and playerX+25 < self.x+self.width:
            if playerY>self.top and playerY+25 < self.top+self.height:
                return False
            return True
        if playerX>self.x and playerX< self.x+self.width:
            if playerY>self.top and playerY+25 < self.top+self.height:
                return False

            return True
        return False





window = pygame.display.set_mode((800,800))
obs = []



def generateObs(lastPos,obs):
    for i in range(50):
        lastPos = lastPos+i*250
        obs.append(Obstacle(lastPos))
    return lastPos

lastPos = 500

generateObs(lastPos,obs)

cameraX = 0
playerX = 40
playerY = 300
dy = 0
ddy = 0.02
dx = 1
jumped = False
clock = pygame.time.Clock()
dyCap = 3
while True:
    score = (playerX-500)/250+1
    window.fill("Blue")
    
    cameraX += dx
    for ob in obs:
        if ob.update(playerX,playerY) == True:
            print("Collison")
            exit()
    
    for ob in obs:
        ob.draw(window, cameraX)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Choice")
            exit()
    # Movement
    if dy>dyCap:
        dy = dyCap
    playerX += dx
    dy += ddy
    playerY+=dy
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] :
        if jumped == False:
            dy = 0
            dy -= 1.7
            jumped = True
    else:
        jumped = False
    
    # Draw player
    pygame.draw.rect(window, pygame.Color("Yellow"), pygame.Rect(playerX-cameraX,playerY, 25, 25))
    clock.tick(60)
    
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(int(score)), True, pygame.Color("Black"))
    textRect = text.get_rect() 
    textRect.center = (40,40)
    window.blit(text,textRect)
    if playerY +20> 740:
        exit()
    pygame.draw.rect(window, pygame.Color("Brown"), pygame.Rect(0,750,800,50))
    pygame.draw.rect(window, pygame.Color("Green"), pygame.Rect(0,740,800,10))
    pygame.display.update()