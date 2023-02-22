import pygame as pg 
import time  as tm
import random as rd

#snake speed
snake_speed = 20

#snake eyes
snake_eye_x_offset = 7
snake_eye_y_offset = 13

#window size
display_width = 1280
display_height = 720

# defining colors
snake_eyes =pg.Color("#ffffff")
snake =pg.Color("#d25062")
back_gd= pg.Color("#fedde0")
snake_food_color = (0,0,0)
game_over_mssg = pg.Color("#952735")
game_over_color = ("#0C120C")

#initializing pygame
pg.init()

#initialise game window 
pg.display.set_caption("Snake By Puzzlelists")
display = pg.display.set_mode((display_width,display_height))

#fps controller 
fps = pg.time.Clock()

#defining snake default position
snake_position = [display_width/2, display_height/2]

#defining first two blocks of snake 
#body
snake_body = [ [200,100],
               [190,100],
             ]

#fruit position 
fruit_position = [rd.randrange(1,(display_width//10))*10,
                 rd.randrange(1,(display_height//10))*10]

fruit_spwan = True

#setting default direction of snake

direction_of_snake = 'Right'
changed_direction = direction_of_snake

#initial score
score =0
#display score 
def display_score(choice, color, font, size):

    #creating font object score_font
    score_font = pg.font.SysFont(font,size)

    #creating the display surface object 
    #score
    score_surface = score_font.render("Score : "+str(score),True,color)

    #create a rectangular object for the text 
    # surface object
    score_rect = score_surface.get_rect()

    #display Text
    display.blit(score_surface ,score_rect) 

# game over function

def game_over():
    #creating font object game_over_font
    game_over_font = pg.font.SysFont('comicsans',50)

    # creating a text surface on which text will be drawn
    game_over_surface = game_over_font.render('Your Score is: '+str(score),True,pg.Color("#952735"))

    #create a recutrangular object for the text 
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text 
    game_over_rect.midtop=(display_width/2 - game_over_surface.get_width()/2, display_height/2 -game_over_surface.get_width()/2)

    # blit will draw the text on screen
    display.blit(game_over_surface,game_over_rect)
    pg.display.flip()

    #after some seconds we will quite the program
    tm.sleep(1)

    #deactivating pygame library 
    pg.quit()

    #quit the program
    quit()
# game = True
# def Main():
while True:

        #handling key events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    changed_direction ='Up'
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    changed_direction = 'Down'
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    changed_direction = 'Left'
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    changed_direction = 'Right'

        #if two key pressed simultaneously 
        #two restrict movement of snake in two different direction

        if changed_direction == 'Up' and  direction_of_snake != 'Down':
            direction_of_snake = 'Up'
        if changed_direction == 'Down' and direction_of_snake != 'Up':
            direction_of_snake = 'Down'
        if changed_direction == 'Left' and direction_of_snake != 'Right':
            direction_of_snake = 'Left'
        if changed_direction == 'Right' and direction_of_snake != 'Left':
            direction_of_snake = 'Right'

        #moving the snake 

        if direction_of_snake == 'Up':
            snake_position[1] -= 10

        if direction_of_snake =='Down':
            snake_position[1] += 10

        if direction_of_snake =='Left':
            snake_position[0] -= 10

        if direction_of_snake =='Right':
            snake_position [0] += 10

        #snake body growing after eating food 
        #if food and snake comes in contact then player will score
        #score will be incremented by 1

        snake_body.insert(0,list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            fruit_spwan = False
        else:
            snake_body.pop()

        if not fruit_spwan:
            fruit_position = [rd.randrange(1,(display_width//10))*10,
                            rd.randrange(1,(display_height//10))*10]

        fruit_spwan = True 
        # filling background color
        display.fill(back_gd)

        #displaying fruit
        pg.draw.circle(display,snake_food_color,[fruit_position[0],fruit_position[1]],15,15)
        
        for pos in snake_body:
            pg.draw.circle(display,snake,[pos[0],pos[1]],20,20)
        
        
        #initializing snake eyes
        pg.draw.circle(display, snake_eyes, [snake_position[0] - snake_eye_x_offset, snake_position[1] + snake_eye_y_offset], 4, 0)
        pg.draw.circle(display, snake_eyes, [snake_position[0] + snake_eye_x_offset, snake_position[1] + snake_eye_y_offset], 4, 0)
        
        #game over conditions
        if snake_position[0] < 0 or snake_position[0] > display_width -10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > display_height-10:
            game_over()

        #touching the snake body 
        for block in snake_body[1:]:
            if snake_position[0] == block [0] and snake_position [1] == block[1]:
                game_over()

        #displaying score continuously 
        display_score(1,game_over_color,'times new roman',50)

        # refresh game screen
        pg.display.update()

        fps.tick(snake_speed)

# #calling main function
# Main()