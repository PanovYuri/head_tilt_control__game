import pygame
from api.opencv_api import OcvApi

#test api
test_api = OcvApi()
#end init

WIN_W = 500
WIN_H = WIN_W

pygame.init()
win = pygame.display.set_mode((WIN_W, WIN_H))

pygame.display.set_caption('Cubes game')

walkRight = [pygame.image.load(
    'sprites/pygame_right_{}.png'.format(i)) for i in range(1, 7)]
walkLeft = [pygame.image.load(
    'sprites/pygame_left_{}.png'.format(i)) for i in range(1, 7)]

playerStand = pygame.image.load('sprites/pygame_idle.png')
bg = pygame.image.load('sprites/pygame_bg.jpg')

clock = pygame.time.Clock()

width = 60
height = 71
x_pers = 50
y_pers = WIN_H - 75
speed = 5

isJump = False
jumpCount = 10

left = False
right = False
animCount = 0
lastMove = "right"

class Snaryad():
    def __init__(self, x, y, raduis, color, facing):
        self.x = x
        self.y = y
        self.raduis = raduis
        self.color = color
        self.facing = facing
        self.vel = 8 * self.facing
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.raduis)

def drawWindow():
    global animCount
    win.blit(bg, (0, 0))

    if animCount + 1 >= 30:
        animCount = 0
    if left:
        win.blit(walkLeft[animCount // 5], (x_pers, y_pers))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x_pers, y_pers))
        animCount += 1
    else:
        win.blit(playerStand, (x_pers, y_pers))

    for b in bullets:
        b.draw(win)
    
    pygame.display.update()


run = True
bullets = []
while run:
    clock.tick(30)

    face_pos = test_api.get_direction()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bul in bullets:
        if bul.x < WIN_W and bul.x > 0:
            bul.x += bul.vel
        else:
            bullets.pop(bullets.index(bul))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f] or test_api.is_smile:

        if not left:
            facing = 1
        else:
            facing = -1
        pos_x = round(x_pers + width // 2)
        if len(bullets) < 5:
            bullets.append(Snaryad(
                pos_x, 
                round(y_pers + height // 2), 5, 
                (255, 0, 0), facing
                ))
    
    if keys[pygame.K_LEFT] or face_pos[1]:
        if x_pers > 5:
            x_pers -= speed
            left = True
            right = False
    elif keys[pygame.K_RIGHT] or face_pos[0]:
        if x_pers < WIN_W - width - 5:
            x_pers += speed
            left = False
            right = True
    else:
        left = False
        right = False
        animCount = 0

    if not isJump:
        if keys[pygame.K_SPACE] or face_pos[2]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y_pers += (jumpCount ** 2) / 2
            else:
                y_pers -= jumpCount ** 2 / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    drawWindow()

pygame.quit()
