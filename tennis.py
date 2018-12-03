import pygame
import random


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dy = 0
        self.score = 0


class Ball:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.dx = random.randint(-3,3)
        self.dy = random.randint(-3,3)
        while self.dx == 0 or self.dy == 0:
            self.dx = random.randint(-3, 3)
            self.dy = random.randint(-3, 3)
        self.img = pygame.image.load('ball.png')
        self.img = pygame.transform.scale(self.img, (self.size, self.size))


size = (540, 500)

player1 = Player(5, 100, 20, 100)
player2 = Player(size[0]-5-20, 100, 20, 100)
ball = Ball(size[0]/2-20, size[1]/2-20, 40)

pygame.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

c = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player1.dy = 5
            if event.key == pygame.K_w:
                player1.dy = -5
            if event.key == pygame.K_DOWN:
                player2.dy = 5
            if event.key == pygame.K_UP:
                player2.dy = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player1.dy = 0
            if event.key == pygame.K_w:
                player1.dy = 0
            if event.key == pygame.K_DOWN:
                player2.dy = 0
            if event.key == pygame.K_UP:
                player2.dy = 0

    player1.y += player1.dy
    player2.y += player2.dy

    if player1.y < 1:
        player1.y = 1
    if player2.y < 1:
        player2.y = 1
    if player1.y > size[1] - 1 - player1.height:
        player1.y = size[1] - 1 - player1.height
    if player2.y > size[1] - 1 - player2.height:
        player2.y = size[1] - 1 - player2.height

    ball.x += ball.dx
    ball.y += ball.dy

    # Bounce

    if ball.x > size[0] - ball.size - player2.width:
        if (ball.y + ball.size/2 > player2.y) and (ball.y + ball.size/2 < player2.y + player2.height):
            ball.dx = -abs(ball.dx)
        else:
            ball = Ball(size[0] / 2 - 20, size[1] / 2 - 20, 40)
            player1.score += 1
            c = 0

    if ball.y > size[1] - ball.size:
        ball.dy = -abs(ball.dy)

    if ball.x < player1.x + player1.width:
        if (ball.y + ball.size/2 > player1.y) and (ball.y + ball.size/2 < player1.y + player1.height):
            ball.dx = abs(ball.dx)
        else:
            ball = Ball(size[0] / 2 - 20, size[1] / 2 - 20, 40)
            player2.score += 1
            c = 0

    if ball.y < 1:
        ball.dy = abs(ball.dy)

    c += 10
    if c > 255:
        c = 255

    screen.fill((255,c,c))

    pygame.draw.rect(screen, (25, 224, 10), [
        player1.x, player1.y, player1.width, player1.height
    ], 0)

    pygame.draw.rect(screen, (25, 224, 10), [
        player2.x, player2.y, player2.width, player2.height
    ], 0)

    screen.blit(ball.img, (ball.x, ball.y))

    text_surface = myfont.render(str(player1.score),False,(20,20,250))
    screen.blit(text_surface, (size[0]/3, 10))

    text_surface = myfont.render(str(player2.score),False,(20,20,250))
    screen.blit(text_surface, (size[0]*2/3, 10))

    pygame.display.flip()
    clock.tick(80)

pygame.quit()
