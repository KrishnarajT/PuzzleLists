import pygame as pg
import time as tm
import random as rd
pg.init()

# variables for snake eyes
snake_eyes =pg.Color("#ffffff")
# Initializing colors for snake, background and food
snake =pg.Color("#d25062")
back_gd= pg.Color("#fedde0")
snake_food_color = (0,255,0)
#game over screen
game_over_mssg = pg.Color("#952735")
game_over_color = ("#0C120C")
# boarder_color= pg.Color("#BE3114")
# display the screen
display_width = 1920
display_height = 1080
display =pg.display.set_mode((display_width,display_height)) #display size

pg.display.set_caption("Snake Game By Puzzlelists")  #Title

#snake food
# snake_food = pg.image.load("/home/parth/python/Python_Projects/Puzzlelists/snake/design/vecteezy_apple-icon-sign-symbol-design_10056053_139.png").convert()

snake_eye_x_offset = 7
snake_eye_y_offset = 13


snake_block = 20
snake_speed= 25
clck = pg.time.Clock()


font_style = pg.font.SysFont("bahnschrift",50)
score_font = pg.font.SysFont("comicsans",50)
def add_snake(snake_block,snake_list):
    for x in snake_list:
        pg.draw.circle(display,snake,[x[0],x[1]],20,0)

def message (messg):
    mesg = font_style.render(messg,True,game_over_mssg)
    display.blit(mesg,[display_width/2 - mesg.get_width()/2,display_height/2 - mesg.get_height()/2])

def gameLoop():
    
    game_over =False
    game_close =False
    
    #initial coordinates
    x1= display_width/2
    y1= display_height/2
    
    x1_change = 0
    y1_change = 0
    snake_List = [] # to keep track of snake size
    snake_length = 1

    #intializing food position
    foodx = round(rd.randrange(1,display_width//10.0)) * 10
    foody= round(rd.randrange(1,display_height//10.0)) *10

    while not game_over:
        # while game_close == True:
        #     display.fill(game_over_color)
        #     message("You Lost!! Press C-Play again or Q-Quit")
        #     pg.display.update()
        #     for event in pg.event.get():
        #         if event.type == pg.K_q:
        #             game_over = True
        #             game_close = False
        #         if event.type == pg.K_c:
        #             gameLoop()     
        for event in pg.event.get():
            if event.type == pg.QUIT:   # To quit game on clicking close button 
                game_over=True 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a :
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    x1_change= snake_block
                    y1_change = 0
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    y1_change = -snake_block
                    x1_change =0

                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    y1_change = snake_block
                    x1_change = 0
        

        if x1 >= display_width or x1<0 or y1 >= display_height or y1 < 0:
            game_over = True
        x1 += x1_change
        y1 += y1_change
        pg.draw.rect(display,snake_food_color,[foodx,foody,20,20]) # creating food
        display.fill(back_gd) # changing background color
        snake_head= []
        # pg.draw.circle(display,snake,[x1,y1],20,0) # creating snake
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List)>snake_length:
            del snake_List[0]
        
        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True
        add_snake(snake_block,snake_List)
        # Drawing snake eyes. 
        pg.draw.circle(display, snake_eyes, [x1 - snake_eye_x_offset, y1 + snake_eye_y_offset], 4, 0)
        pg.draw.circle(display, snake_eyes, [x1 + snake_eye_x_offset, y1 + snake_eye_y_offset], 4, 0)
        if x1 == foodx and y1 == foody:
            foodx = round(rd.randrange(0,display_width - snake_block)/ 10.0) *10.0
            foody= round (rd.randrange(0,display_height - snake_block)/10.0) *10.0
            snake_length +=1
        pg.display.update()

        clck.tick(snake_speed) 
    message("Game Over!!")
    pg.display.update()
    tm.sleep(3)
    pg.quit()
    quit()

gameLoop()