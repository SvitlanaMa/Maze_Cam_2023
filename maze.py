#створи гру "Лабіринт"!
import pygame
from levels import *
from time import time
from random import choice

pygame.init()

wind_width, wind_height = 700, 500
level_width = 860

window = pygame.display.set_mode((wind_width, wind_height))

FPS = 40

clock = pygame.time.Clock()

back = pygame.image.load("background.jpg")
back = pygame.transform.scale(back, (wind_width, wind_height))

# pygame.mixer_music.load("jungles.ogg")
# pygame.mixer_music.set_volume(0.1)
# pygame.mixer_music.play(-1)

class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player):
        if self.rect.right < level_width:
            if player.rect.x > self.rect.x + int(0.7*self.rect.w):
                self.rect.x += self.speed

camera = Camera(0 ,0, wind_width, wind_height, 5)

class GameSprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    def draw(self):
        window.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y))

class Player(GameSprite): 
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, down, up, left, right):
        k = pygame.key.get_pressed()
        if k[down]:
            if self.rect.bottom <= wind_height:
                self.rect.y += self.speed
        if k[up]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
        if k[right]:
            if self.rect.x <= level_width - self.rect.width:
                self.rect.x += self.speed
        if k[left]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False
bots = []            
class Bot(GameSprite):
    def __init__(self, x, y, w, h, image, speed, x_finish):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        if x > x_finish:
            self.direction = "left"
            self.x_start = x_finish
            self.x_finish = x
        else: 
            self.direction = "right"
            self.x_start = x
            self.x_finish = x_finish
        bots.append(self)
    
    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= self.x_start:
                self.direction = "right"
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x >= self.x_finish:
                self.direction = "left"

player_img = pygame.image.load("hero.png")
player1 = Player(25, 25, 25, 25, player_img, 2)

bot_img = pygame.image.load("cyborg.png")
bot1 = Bot(50, 25, 25, 25, bot_img, 2, 200)
bot2 = Bot(500, 250, 25, 25, bot_img, 2, 100)

block_img = pygame.image.load("brik.png")

cherry_img = pygame.image.load("cherry.png")
lemon_img = pygame.image.load("lemon.png")
plum_img = pygame.image.load("plum.png")

fr_imgs = [cherry_img, lemon_img, plum_img]

fruits = []
blocks = []
block_size = 20
x, y = 0, 0

for stroka in map1:
    for bl in stroka:
        if bl == "1":
            block = GameSprite(x, y, block_size, block_size, block_img)
            blocks.append(block)
        if bl == "2":
            apple = GameSprite(x, y, block_size, block_size, choice(fr_imgs))
            fruits.append(apple)
        x += block_size
    x = 0
    y += block_size

gold_img = pygame.image.load("treasure.png")
gold = GameSprite(650, 450, block_size, block_size, gold_img)

font = pygame.font.SysFont("Arial", 30)
font1 = pygame.font.SysFont("Arial", 20)
new_game_lb = font1.render("Щоб розпочати нову гру, натисніть Пробіл", True, (20, 20, 20))

points = 0

game = True
finish = False
start_time = time()


while game:
    if not finish:
        camera.move(player1)
        game_time = int(time() - start_time)
        time_lb = font1.render("Time: " + str(game_time), True, (250, 250, 250))
        window.blit(back, (0, 0))
        
        player1.draw()
        player1.move(pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d)
        gold.draw()

        for bot in bots:
            bot.draw()
            bot.move()
            if player1.collide(bot):
                game_over = font.render("Game Over!", True, (20, 20, 20))
                finish = True
                color = (255, 0, 0)

        for fruit in fruits:
            fruit.draw()
            if player1.collide(fruit):
                fruits.remove(fruit)
                points += 1
                print(points)

        for block in blocks:
            block.draw()
            if player1.collide(block):
                game_over = font.render("Game Over!", True, (20, 20, 20))
                finish = True
                color = (255, 0, 0)
        window.blit(time_lb, (0, 0))
        if player1.collide(gold):
            game_over = font.render("You Win!", True, (20, 20, 20))
            finish = True
            color = (0, 255, 0)

                
    else:
        window.fill(color)
        window.blit(game_over, (200, 200))
        window.blit(new_game_lb, (100, wind_height - 100))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            finish = False
            player1 = Player(25, 25, 25, 25, player_img, 2)
            start_time = time()
            points = 0
            fruits.clear()
            x, y = 0, 0
            for stroka in map1:
                for bl in stroka:
                    if bl == "2":
                        apple = GameSprite(x, y, block_size, block_size, choice(fr_imgs))
                        fruits.append(apple)
                    x += block_size
                x = 0
                y += block_size



    pygame.display.update()
    clock.tick(FPS)
