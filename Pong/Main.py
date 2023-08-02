import pygame
import random
pygame.init()
SPEED = 10
class Platform:
    dy = 0
    height = 200
    width = 20
    def __init__(self,x,y, typeI) -> None:
        self.x = x
        self.y = y
        self.typeI = typeI
    
    def update(self, ballY, keys):
        self.dy = 0
        if self.typeI == "AI":
            if self.y+self.height//2 > ballY and self.y>SPEED:
                self.dy = -SPEED
            else:
                if (self.y + self.height) < 800-SPEED:
                    self.dy = SPEED
            if self.y+self.height//2 == ballY :
                self.dy = 0
        else:
            if keys[pygame.K_w] and self.y>SPEED:
                self.dy = -SPEED
            if keys[pygame.K_s] and (self.y + self.height) < 800-SPEED:
                self.dy = SPEED
        
        self.y += self.dy

    def draw(self,window):
        pygame.draw.rect(window, pygame.Color("White"), pygame.Rect(self.x,self.y,self.width,self.height))


def collisionCheck(ballX,ballY, platform : Platform):
    if ballX > platform.x and ballX<platform.x+platform.width:
        if ballY+30 > platform.y and ballY+30 < platform.y + platform.height:
            return True
        if ballY > platform.y and ballY < platform.y + platform.height:
            return True
    if ballX +30> platform.x and ballX+30<platform.x+platform.width:
        if ballY+30 > platform.y and ballY+30 < platform.y + platform.height:
            return True
        if ballY > platform.y and ballY < platform.y + platform.height:
            return True
    return False


window = pygame.display.set_mode((800,800))

playerPlatform = Platform(100,300,"Player")
AIPlatform = Platform(680,300, "AI")
AIPlatform2 = Platform(100,300, "AI")
ballY = 400
ballX = 300
ballDY = SPEED
ballDX = SPEED
mode = "AI"
BALL_ACCELERATION = 0.1
clock = pygame.time.Clock()
while True:
    
    ballX += ballDX
    ballY += ballDY
    if SPEED > 10:
        SPEED = 8
    if ballY <= 0:
        ballDY = SPEED
        SPEED += BALL_ACCELERATION
    if ballY+30>=800:
        ballDY = -SPEED
        SPEED += BALL_ACCELERATION
    if mode == "Player":
        if collisionCheck(ballX,ballY, playerPlatform) == True:
            ballDX = SPEED
            SPEED += BALL_ACCELERATION
    if collisionCheck(ballX,ballY, AIPlatform) == True:
        ballDX = -SPEED
        SPEED += BALL_ACCELERATION
    if mode == "AI":
        if collisionCheck(ballX,ballY, AIPlatform2) == True:
            ballDX = SPEED
            print("Gottem")
            SPEED += BALL_ACCELERATION
    
    
    window.fill("Black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if mode == "Player":
        playerPlatform.update(0,keys)
        playerPlatform.draw(window)
    AIPlatform.update(ballY, 0)
    AIPlatform.draw(window)
    if mode == "AI":
        AIPlatform2.update(ballY, 0)
        AIPlatform2.draw(window)
    
    pygame.draw.circle(window,pygame.Color("White"), (ballX+15, ballY+15), 15)
    pygame.display.update()
    clock.tick(60)