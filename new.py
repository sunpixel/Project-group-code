import pygame as pg
import random
import os

pg.init()


window = pg.display.set_mode((800, 600))

bg = random.randint(1,15)

score_value = 0
font = pg.font.SysFont('Comic Sans MS', 34)

if bg <= 5:
    BackGround = pg.transform.scale(pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'background1.png')) , (800, 600))
elif 10 >= bg > 5:
    BackGround = pg.transform.scale(pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'background2.jpg')) , (800, 600))
elif 15 >= bg > 10:
    BackGround = pg.transform.scale(pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'background3.jpg')) , (800, 600))


entity = pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'SpaceShip.png'))

hostile = pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'Enemy.png'))

explode = pg.transform.scale(pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'explosion.png')), (60, 60))

menuBG = pg.transform.scale(pg.image.load(os.path.join(os.path.dirname(__file__), 'images', 'Menu-BG.jpg')), (800, 600))


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
        global score_value, enemy_x, enemy_y, hit
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hit_box[0]- 25 < bullet.x + 10 < enemy.hit_box[0] + 50 and enemy.hit_box[1] < bullet.y + 10 < enemy.hit_box[1] + 80:
                    score_value += 100
                    hit = 1
                    enemy_x = enemy.x
                    enemy_y = enemy.y
                    self.bullets.remove(bullet)
                    enemies.remove(enemy)

# Nikita

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

# Amir

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


class Spawn:
    def __init__(self, wave, spawn_rate):
        self.wave = wave
        self.spawn_rate = spawn_rate

def draw_game():
    if menu:
        window.blit(menuBG, (0, 0))
        window.blit(start1, (200, 200))
        window.blit(start2, (250, 300))
        window.blit(start3, (190, 400))
        pg.display.update()
    elif game_over:
        window.fill((0, 0, 0))
        window.blit(over, (300, 200))
        window.blit(restart, (200, 250))
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
        show_score()
        pg.time.delay(30)
        pg.display.update()

e_time = 0   # End time
hit = 0      # Hit

player = Player(225, 510)
enemies = []

game_over = False
menu = True


restart = font.render("To play again press 'R'.", False, (204, 0, 0))
over = font.render("Game Over", True, (255, 255, 255))
start1 = font.render("To start playing press 'R'.", False, (204, 0, 0))
start2 = font.render("Use 'A', 'D' to move..", False, (255, 255, 255))
start3 = font.render("Press 'SPACEBAR' to shoot.", False, (255, 255, 255))

run = True

enemy_x, enemy_y = 0, 0
spawn_x = 25
spawn_y = -50

while run:

    spawn_x = 25
    spawn_y = -25
    c_time = pg.time.get_ticks()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    userInput = pg.key.get_pressed()

    player.movement(userInput)
    player.shooting()

    if menu and userInput[pg.K_r]:
        menu = False

    if game_over and userInput[pg.K_r]:
        game_over = False

    if not game_over or not menu:
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

# Show explosion EFFECT

########################

    c_time = pg.time.get_ticks()
    if hit:
        e_time = c_time + 100
        hit = 0

    if c_time < e_time:
        window.blit(explode, (enemy_x, enemy_y))

#########################
    
    draw_game()
