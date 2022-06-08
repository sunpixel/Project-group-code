import pygame as pg
import random

pg.init()

window = pg.display.set_mode((800, 600))

bg = random.randint(1,15)

score_value = 0
font = pg.font.SysFont('Comic Sans MS', 34)

if bg <= 5:
    BackGround = pg.transform.scale(pg.image.load('background1.png') , (800, 600))
elif 10 >= bg > 5:
    BackGround = pg.transform.scale(pg.image.load('background2.jpg') , (800, 600))
elif 15 >= bg > 10:
    BackGround = pg.transform.scale(pg.image.load('background3.jpg') , (800, 600))


entity = pg.image.load('SpaceShip.png')

hostile = pg.image.load('Enemy.png')



def show_score():
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    window.blit(score, (10, 10))

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.cool_down_counter = 0
        self.speed = 10

    def movement(self, userInput):
        if userInput[pg.K_a] and self.x >= 0:
            self.x -= self.speed
        if userInput[pg.K_d] and self.x <= 750:
            self.x += self.speed
    
    def draw_player(self, window):
        window.blit(entity, (self.x, self.y))

    def shooting(self):
        self.cool_down()
        self.deal_damage()
        if userInput[pg.K_SPACE] and self.cool_down_counter == 0:
            bullet = Bullet(self.x, self.y)
            self.bullets.append(bullet)
            self.cool_down_counter = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def cool_down(self):
        if self.cool_down_counter >= 15:
            self.cool_down_counter = 0
        if self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def deal_damage(self):
        global score_value
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hit_box[0]- 25 < bullet.x + 10 < enemy.hit_box[0] + 50 and enemy.hit_box[1] < bullet.y + 10 < enemy.hit_box[1] + 80:
                    self.bullets.remove(bullet)
                    enemies.remove(enemy)
                    score_value += 100


class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def off_screen(self):
        return not (self.y >= 0)

    def draw_bullet(self):
        pg.draw.circle(window, (255, 255, 255), (self.x + 25, self.y - 5), 10)


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.cool_down_counter = 0
        self.hit_box = (self.x, self.y, 50, 50)

    def draw(self, window):
        self.hit_box = (self.x, self.y, 50, 50)
        pg.draw.line(window, (4, 255, 4), (0, 500), (800, 500))
        window.blit(hostile, (self.x, self.y))

    def move(self):
        self.cool_down()
        if self.cool_down_counter == 0:
            self.y += random.randint(5,30)
            self.cool_down_counter = 1            
        
    def cool_down(self):
        if self.cool_down_counter > 0:
            self.cool_down_counter += 1
        if self.cool_down_counter >= 20:
            self.cool_down_counter = 0

    def win(self):
        return not (self.y <= 455)

def draw_game():
    if game_over:
        window.blit(over, (300, 200))
        pg.time.delay(30)
        pg.display.update()
    else:
        window.fill((0, 0, 0))
        window.blit(BackGround, (0, 0))
        player.draw_player(window)
        for bullet in player.bullets:
            bullet.draw_bullet()
        for enemy in enemies:
            enemy.draw(window)
        pg.time.delay(30)
        pg.display.update()


player = Player(225, 510)

enemies = []

game_over = False

over = font.render("Game Over", True, (255, 255, 255))

run = True

spawn_x = 25

spawn_y = 0

while run:

    spawn_x = 25

    spawn_y = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    userInput = pg.key.get_pressed()

    player.movement(userInput)
    player.shooting()

    if game_over and userInput[pg.K_r]:
        run = False

    if len(enemies) == 0:
        for i in range(8):
            enemy = Enemy(spawn_x, spawn_y)
            enemies.append(enemy)
            spawn_x += 100

    for enemy in enemies:
        enemy.move()
        if enemy.win():
            enemies.clear()
            game_over = True

    show_score()
    pg.display.update()

    draw_game()

        