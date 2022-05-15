import pygame as pg

pg.init()

screen_width = 1280
screen_height = 720

win = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Ourgame')

x = screen_width // 2
y = screen_height // 2
radius = 10
vel = 5

run = True
while run:  #main game loop
    win.fill((0,0,0))
    
    pg.draw.circle(win, (14, 88, 228), (int(x), int(y)), radius) 
    #(aaa,bbb,ccc) rgb notation
    
    for event in pg.event.get():    #event handling loop
        if event.type == pg.QUIT:
            run = False
            
    control = pg.key.get_pressed()
    
    #get teleported to center(test)
    if control[pg.K_f]:
        x = screen_width // 2
        y = screen_height // 2
    
    #normal movement controls
    if control[pg.K_a] and x>0:
        x -= vel
    if control[pg.K_d] and x<screen_width:
        x += vel
    if control[pg.K_w] and y>0:
        y -= vel
    if control[pg.K_s] and y<screen_height:
        y += vel
        
    #dash for evading enemy gunfire/meelee
    #dashing left/right
    dashing = False     #later to be used in evading attacks implementation
    if control[pg.K_SPACE]:
        dashing = True
        #horizontal
        if control[pg.K_a] and x>0:
            x -= vel*1.2
        if control[pg.K_d] and x<screen_width:
            x += vel*1.2
        #vertical
        if control[pg.K_w] and y>0:
            y -= vel*1.2
        if control[pg.K_s] and y<screen_height:
            y += vel*1.2
        #diagonal
        #left-up
        if control[pg.K_a] and control[pg.K_w]:
            if x>0:
                x -= vel*1.2
            if y>0:
                y -= vel*1.2
        #left-down
        if control[pg.K_a] and control[pg.K_s]:
            if x<screen_height:
                x += vel*1.2
            if y<screen_height:
                y += vel*1.2
        #right-up
        if control[pg.K_d] and control[pg.K_w]:
            if x<screen_width:
                x += vel*1.2
            if y>0:
                y -= vel*1.2
        #right-down
        if control[pg.K_d] and control[pg.K_s]:
            if x<screen_width:
                x += vel*1.2
            if y<screen_width:
                y += vel*1.2
    
    pg.time.delay(10)
    pg.display.update()