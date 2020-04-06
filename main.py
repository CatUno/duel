import pygame as pygame

pygame.init()

WIN_X_SIZE          = 500
WIN_Y_SIZE          = 500
JUMP_SPEED_COEFF    = 2
JUMP_HEIGHT_COEFF   = 1


win = pygame.display.set_mode((WIN_X_SIZE, WIN_Y_SIZE))

pygame.display.set_caption("Podavilas")

walkRight = [pygame.image.load('pygame_right_1.png'), pygame.image.load('pygame_right_2.png'),
                pygame.image.load('pygame_right_3.png'), pygame.image.load('pygame_right_4.png'),
                pygame.image.load('pygame_right_5.png'), pygame.image.load('pygame_right_6.png')]
                
walkLeft = [pygame.image.load('pygame_left_1.png'), pygame.image.load('pygame_left_2.png'),
                pygame.image.load('pygame_left_3.png'), pygame.image.load('pygame_left_4.png'),
                pygame.image.load('pygame_left_5.png'), pygame.image.load('pygame_left_6.png')]

playerStand = pygame.image.load('pygame_idle.png')
background  = pygame.image.load('pygame_bg.jpg')

clock = pygame.time.Clock()

width   = 60
height  = 71
speed   = 5
x       = 10 
y       = WIN_Y_SIZE - height

isJump = False
jumpCnt = 10

left    = False
right   = False
animCnt = 0
lastMove = "right"

class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x  = x
        self.y  = y
        self.radius     = radius
        self.color      = color
        self.facing     = facing
        self.speed      = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def drawWindow():
    global animCnt
    
    win.blit(background, (0, 0))

    if (animCnt + 1 >= 30):
        animCnt = 0

    if left:
        win.blit(walkLeft[animCnt // 5], (x, y))  
        animCnt += 1      
    elif right:
        win.blit(walkRight[animCnt // 5], (x, y))  
        animCnt += 1            
    else:
        win.blit(playerStand, (x, y))

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()



bullets = []
run = True
while run:
    clock.tick(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < WIN_X_SIZE and bullet.x > 0:
            bullet.x += bullet.speed
        else: 
            bullets.pop(bullets.index((bullet)))


    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(snaryad(round(x + width // 2), round(y +  height // 2),
                                    5, (255, 0, 0), facing))

    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
        left    = True
        right   = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < WIN_X_SIZE - width:
        x += speed
        left    = False
        right   = True
        lastMove = "right"
    else:
        left    = False
        right   = False
        animCnt = 0


    if not isJump:
        if keys[pygame.K_UP] and y > 0:
            y -= speed
        if keys[pygame.K_DOWN] and y < WIN_Y_SIZE - height:
            y += speed
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCnt >= 0:
            y -= jumpCnt ** 2 * JUMP_HEIGHT_COEFF
            jumpCnt -= 1 * JUMP_SPEED_COEFF
        elif jumpCnt >= -10:
            y += jumpCnt ** 2 * JUMP_HEIGHT_COEFF
            jumpCnt -= 1 * JUMP_SPEED_COEFF
        else:
            jumpCnt = 10
            isJump = False

    drawWindow()

pygame.quit()