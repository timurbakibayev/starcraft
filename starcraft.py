import pygame
import random

class Zerg():
    x = 0
    y = 0
    zx = 0
    zy = 0
    bullet = None
    attack = None
    fire = 5


def collide(zerg1, zerg2):
    cx1 = zerg1.x + zerg1.w/2
    cy1 = zerg1.y + zerg1.h/2
    cx2 = zerg2.x + zerg2.w/2
    cy2 = zerg2.y + zerg2.h/2
    if abs(cx2-cx1) < (zerg1.w + zerg2.w)/2:
        if abs(cy2-cy1) < (zerg1.h + zerg2.h)/2:
            return True
    return False


pygame.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
size = (400, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False
img1 = pygame.image.load('image1.png') #<---------upload png
img2 = pygame.image.load('image2.png') #<---------upload png
img3 = pygame.image.load('image3.png') #<---------upload png
img4 = pygame.image.load('image4.png') #<---------upload png
img5 = pygame.image.load('pacman.png') #<---------upload png

img1 = pygame.transform.scale(img1, (32, 32))
img2 = pygame.transform.scale(img2, (32, 32))
img3 = pygame.transform.scale(img3, (32, 32))
img4 = pygame.transform.scale(img4, (32, 32))
img5 = pygame.transform.scale(img5, (32, 32))

# w,h = img.get_rect().size

zergs = []

zerg = Zerg() #<------------ Create object of class zerg

zerg.x = 100
zerg.y = 100
zerg.zx = zerg.x
zerg.zy = zerg.y
zerg.img = img1
zerg.w, zerg.h = zerg.img.get_rect().size
zergs.append(zerg)

zerg = Zerg() #<------------ Create object of class zerg

zerg.x = 200
zerg.y = 100
zerg.zx = zerg.x
zerg.zy = zerg.y
zerg.img = img2
zerg.w, zerg.h = zerg.img.get_rect().size
zergs.append(zerg)

zerg = Zerg() #<------------ Create object of class zerg

zerg.x = 120
zerg.y = 300
zerg.zx = zerg.x
zerg.zy = zerg.y
zerg.img = img3
zerg.w, zerg.h = zerg.img.get_rect().size
zergs.append(zerg)

zerg = Zerg() #<------------ Create object of class zerg

zerg.x = 280
zerg.y = 300
zerg.zx = zerg.x
zerg.zy = zerg.y
zerg.img = img4
zerg.w, zerg.h = zerg.img.get_rect().size
zergs.append(zerg)


selected = None

stop = False

eaten = False
food_position_x = random.randrange(50, 351)
food_position_y = random.randrange(50, 451)
counter = 0;

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # if event.type == pygame.KEYDOWN:
        #     pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                 zerg = Zerg() #<------------ Create object of class zerg
                 zerg.x = random.randrange(100, 400, 1)
                 zerg.y = random.randrange(100, 400, 1)
                 zerg.zx = zerg.x
                 zerg.zy = zerg.y
                 zerg.img = img5
                 zerg.w, zerg.h = zerg.img.get_rect().size
                 for z in zergs:
                     if collide(z,zerg):
                         stop = True
                         
                 zergs.append(zerg)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                for zerg in zergs:
                    if x >= zerg.x and x <= zerg.x + zerg.w:
                        if y >= zerg.y and y <= zerg.y + zerg.h:
                            selected = zerg
                if selected is not None:
                    selected.zx, selected.zy = pygame.mouse.get_pos()
                    selected.zx = selected.zx - zerg.w/2
                    selected.zy = selected.zy - zerg.h/2
            else:
                if selected is not None:
                    selected.attack = pygame.mouse.get_pos()
                    selected.bullet = (selected.x + selected.w/2, selected.y + selected.h/2)
                    selected.fire = 5

    #logic
    for zerg in zergs:
        lx = zerg.x #<----remember last x
        if zerg.zx > zerg.x: zerg.x+=1
        if zerg.zx < zerg.x: zerg.x-=1
        # if zerg.zy > zerg.y: zerg.y+=1
        # if zerg.zy < zerg.y: zerg.y-=1
        intersection = False
        for other_zerg in zergs:
            if other_zerg != zerg:
                if collide(zerg, other_zerg):
                    intersection = True
        if intersection:
            zerg.x = lx
        ly = zerg.y #<----remember last y
        if zerg.zy > zerg.y: zerg.y+=1
        if zerg.zy < zerg.y: zerg.y-=1
        # if zerg.zy > zerg.y: zerg.y+=1
        # if zerg.zy < zerg.y: zerg.y-=1
        intersection = False
        for other_zerg in zergs:
            if other_zerg != zerg:
                if collide(zerg, other_zerg):
                    intersection = True
        if intersection:
            zerg.y = ly

        if (food_position_x-25<zerg.x+32<food_position_x+25) & (food_position_y-25<zerg.y+32<food_position_y+25):
            eaten = True
    #end of logic
    screen.fill((255, 255, 255))

    if not eaten:
        pygame.draw.rect(screen, (200, 100, 100), [food_position_x, food_position_y, 10, 10], 15)
    else:
        food_position_x = random.randrange(50, 351)
        food_position_y = random.randrange(50, 451)
        counter += 1
        eaten = False
        pygame.draw.rect(screen, (200, 100, 100), [food_position_x, food_position_y, 10, 10], 15)


    for zerg in zergs:
        if zerg.attack is not None:
            if zerg.bullet is not None:
                x, y = zerg.bullet
                x1, y1 = zerg.attack
                x = x + (x1-x)/20
                y = y + (y1-y)/20
                if abs(x-x1) < 3 and abs(y-y1) < 3:
                    zerg.fire -= 1
                    if zerg.fire > 0:
                        x = zerg.x + zerg.w/2
                        y = zerg.y + zerg.h/2
                    else:
                        zerg.bullet = None
                if zerg.bullet is not None:
                    zerg.bullet = x,y


    textsurface = myfont.render(str(counter), False, (0, 0, 0))
    for z in zergs:
        if z == selected:
            pygame.draw.rect(screen, (255, 224, 178), [z.x,z.y,z.w,z.h], 0)

    for z in zergs:
        screen.blit(z.img, (z.x, z.y))

    for z in zergs:
        if z.bullet is not None:
            x,y = z.bullet
            x = int(x)
            y = int(y)
            pygame.draw.circle(screen, (50, 50, 50), (x,y), 4)


    screen.blit(textsurface,(50, 50))
    pygame.display.flip()
    clock.tick(144)
pygame.quit()
