import pygame
import random
import udp_socket

UDP_PORT_RX = 7070
UDP_PORT_TX = 7071
UDP_IP      = 'localhost' 

pygame.init()
win=pygame.display.set_mode((1000,500))
pygame.display.set_caption("NewGame")

walkRight = [pygame.image.load('img/right_1.png'),pygame.image.load('img/right_2.png'),pygame.image.load('img/right_3.png'),pygame.image.load('img/right_4.png'),pygame.image.load('img/right_5.png'),pygame.image.load('img/right_6.png'),]

walkLeft = [pygame.image.load('img/left_1.png'),pygame.image.load('img/left_2.png'),pygame.image.load('img/left_3.png'),pygame.image.load('img/left_4.png'),pygame.image.load('img/left_5.png'),pygame.image.load('img/left_6.png'),]

bg = pygame.image.load('img/m_bg2.jpg')
playerStand = pygame.image.load('img/idle.png')
ball = pygame.image.load('img/m_ball5.png')
ded = pygame.image.load('img/ded.jpg')

enemW =  pygame.image.load('img/m_general.png')
clock = pygame.time.Clock()

game_over =False
r=1
x = 5
y = 435
wight = 60
height = 71
wightE = 60
heightE = 71
speed = 10
speedE = 10
en = True
score = 0
die = 0
black     = (  0,   0,   0)
red = (213, 50, 80)
font = pygame.font.Font(None, 25)

isJump = False
jumpCount = 10

isJumpE = False
jumpCountE = 10

lastMoveE="left"

left  = False
right = False
animCount = 0
lastMove="right"


class enemy():
    def __init__(self, x, y, radius, color,speedE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speedE = speedE
        self.vel = speedE

    def draw(self,win):
        win.blit(enemW,(self.x,self.y))

    def move(self):
        global lastMoveE
        for enem in enemies:
            r = random.randint(1, 4)
            global isJumpE
            global jumpCountE
            if r==1 and enem.x > speedE:
                enem.x -= speedE
                lastMoveE = "left"
            elif r==2 and enem.x < 1000 - wightE - speedE:
                enem.x += speed
                lastMoveE = "right"
            elif r==3:
                if lastMoveE=="right":
                    facing = 1
                else:
                    facing = -1

                if len(bulletsE) < 1:
                    bulletsE.append(snaryadE(round(enem.x + wight // 2), round(enem.y + 
                    height // 2), 5,  (255, 0, 0), facing))
            if not(isJumpE):
                if r==4:
                    isJumpE = True
            else:
                if jumpCountE>= -10:
                    if jumpCountE <0:
                        enem.y += (jumpCountE ** 2)/2
                    else:
                        enem.y -= (jumpCountE ** 2)/2
                    jumpCountE -=1
                else:
                    isJumpE = False
                    jumpCountE = 10

    def goTo(self, x, y):
        self.x = x
        self.y = y
                    
                    

          
        

class snaryadE():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing
    def draw(self,win):
        win.blit(ball,(self.x,self.y))
    def goTo(self, x, y):
        self.x = x
        self.y = y


class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing
    def draw(self,win):
        win.blit(ball,(self.x,self.y))

def show_end():
    win.blit(ded,(0,0))
    over = font.render("GAME OVER!",True, red)
    win.blit(over ,[450,250] )
    Keys = font.render("Arrow keys move, Space to fire",True, red)
    win.blit( Keys,[450,300] )
    Key = font.render("Press any key to begin",True, red)
    win.blit( Key,[450,350] )
    pygame.display.update()
    runG =True
    while runG:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                runG = False
        
        


   
    
    
    
        
        


def drawWindow():
    global animCount
    win.blit(bg, (0, 0))

    if animCount + 3 >= 30:
        animCount =0
    if left:
        win.blit(walkLeft[animCount//5],(x,y))
        animCount +=3
    elif right:
        win.blit(walkRight[animCount//5],(x,y))
        animCount +=3
    else:
        win.blit(playerStand,(x,y))
    for bulletE in bulletsE:
        bulletE.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for enem in enemies:
        enem.draw(win)
    tex = font.render("Die: "+str(die),True, black)
    text = font.render("Score: "+str(score),True, black)
    win.blit(text, [900,0])
    win.blit(tex, [40,0])
    pygame.display.update()


bulletsE = []  
enemies = []
run = True 
bullets = []
enemySender = udp_socket.EnemySender(UDP_IP, UDP_PORT_RX, UDP_PORT_TX, enemies)

while run:
    clock.tick(30)
    if game_over:
        game_over=False
        for bullet in bullets:
             bullets.pop(bullets.index(bullet))
        for bulletE in bulletsE:
             bulletsE.pop(bulletsE.index(bulletE))
        x = 5
        y = 435
        isJump = False
        jumpCount = 10
        isJumpE = False
        jumpCountE = 10
        for enem in enemies:
            enem.y = 435
            enem.x = 800
        show_end()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x<1000 and bullet.x >0:
            bullet.x  +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    '''
    for bulletE in bulletsE:
        if bulletE.x<1000 and bulletE.x >0:
            bulletE.x  +=bulletE.vel
        else:
            bulletsE.pop(bulletsE.index(bulletE))   
        '''

    """ for enem in enemies:
     r = random.randint(1, 4)    


     if r==1:
         if enem.y>200:
                enem.y -=enem.vel
             
     elif r==2:
         if enem.x>20:
                enem.x -=enem.vel
             
     elif r==3:
         if enem.x<480:
                enem.x+=enem.vel
             
     else:
         if enem.y<480:
                enem.y+=enem.vel """
             

    for bullet in bullets:
        for enem in enemies:
            for i in range (70): 


                if bullet.x==enem.x+i :
                     
                            for g in range (60):
                                if bullet.y==enem.y+g:
                                    score +=1
                                    en=True
                                    for bullet in bullets:
                                        bullets.pop(bullets.index(bullet))
                                    for bulletE in bulletsE:
                                        bulletsE.pop(bulletsE.index(bulletE))
                                    enemies.pop(enemies.index(enem))    
                
                            """ elif bullet.x-i==enem.x :
                    
                            for j in range (60):
                                if bullet.y+j==enem.y:
                                    score +=1
                                    en=True
                                    enemies.pop(enemies.index(enem))
                                elif bullet.y-j==enem.y:
                                    score +=1
                                    en=True
                                    enemies.pop(enemies.index(enem)) """  
                
    for bulletE in bulletsE:        
        for i in range (70): 
            if bulletE.x==x+i :                     
                for g in range (60):
                    if bulletE.y==y+g:
                        die +=1
                        game_over =True
                                                                      
                

        




        #r = random.randint(1, 4)
        #if r==1:
         #   enem.x  +=enem.vel
         #   r+=1
       # elif r==2 :
          #  enem.x  -=enem.vel
          #  r+=1
       # elif r==3 :
       #     enem.y  +=enem.vel
         #   r+=1
       # elif r==4 :
        #    enem.y  -=enem.vel
        #    r = 1
    keys = pygame.key.get_pressed()
    if en:
        if len(enemies) < 1:
            enemies.append(enemy( 800,  435, 5,  (255, 0, 0),10))
            en = False 
    

    if keys[pygame.K_SPACE]:
        if lastMove=="right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 1:
            bullets.append(snaryad(round(x + wight // 2), round(y + 
            height // 2), 5,  (255, 0, 0), facing))


    if keys[pygame.K_LEFT] and x > speed:
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < 1000 - wight - speed:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        animCount = 0
    if not(isJump):
        if keys[pygame.K_UP]:
            isJump = True
    else:
        if jumpCount>= -10:
            if jumpCount <0:
                y += (jumpCount ** 2)/2
            else:
                y -= (jumpCount ** 2)/2
            jumpCount -=1
        else:
            isJump = False
            jumpCount = 10
    
    '''
    for enem in enemies:
        enem.move()
        '''
    
    if y>440:
        y =435
        '''
    for enem in enemies:
        if enem.y>440:
            enem.y =435 
            '''

    enemySender.send((x, y), bullets)
    drawWindow()
 



pygame.quit()