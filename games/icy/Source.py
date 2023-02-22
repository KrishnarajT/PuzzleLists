# Game to see if you can identify all the colors and their variants.
# made from 21-5-2020 to 23-5-2020
# uses the basic pygame library, and other dependencies like os, time and stuff

# Game concept stolen from an android game called ColorSense

# Concept:

# basic idea is the print a matrix on the screen, of some random color, and have a single anomaly that is termed here as a 'weirdo'
# player has to click on the weirdo, and he succeedes the level, the level advances, and the shade of the weirdo keeps getting lighter.
# eventually the eye cannot differentiate between the different colors, and the player fails to select the weirdo, and the game ends.

# the playing mode is divided into 2 different types, one of them is based on time limit and the other one is based on the click limit.


from math import floor
import pygame
from Ky_Game import *
import pyautogui
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = pyautogui.size()

# IMAGES THAT ARE SCALED TO THE SCREEN DIMENSIONS.
# THESE ARE BACKGROUND IMAGES FOR EVERY PLAY MODE.
BG_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "BG_IMAGE.png" ) ), (WIDTH, HEIGHT) )
LOST_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "LOST_IMAGE.png" ) ), (WIDTH, HEIGHT) )
PLAY_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "PLAY_IMAGE.png" ) ), (WIDTH, HEIGHT) )
PLAY_IMAGE_TIME = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "PLAY_IMAGE_TIME.png" ) ),
                                          (WIDTH, HEIGHT) )
MENU_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "MENU_IMAGE.png" ) ), (WIDTH, HEIGHT) )


WIN = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.RESIZABLE )
pygame.display.set_caption( "ICY" )

# X AND Y COORDINATES OF THE BUTTONS ON SCREEN, TO BE DETECTED BY THE MOUSE POSITION
START_BTN_LOWER = (WIDTH - floor( WIDTH / 4.5 ),
                   HEIGHT - floor( HEIGHT / 2.3 ))
START_BTN_UPPER = (WIDTH - floor( WIDTH / 13.2 ),
                   HEIGHT - floor( HEIGHT / 3.2 ))

EXIT_BTN_LOWER = (WIDTH - floor( WIDTH / 4.5 ),
                  HEIGHT - floor( HEIGHT / 4.32 ))
EXIT_BTN_UPPER = (WIDTH - floor( WIDTH / 13.2 ),
                  HEIGHT - floor( HEIGHT / 10.8 ))

TIME_LIM_BTN_LOWER = (WIDTH - floor( WIDTH / 1.46 ),
                      HEIGHT - floor( HEIGHT / 1.6 ))
TIME_LIM_BTN_UPPER = (WIDTH - floor( WIDTH / 3.14 ),
                      HEIGHT - floor( HEIGHT / 2.51 ))

CLICK_LIM_BTN_LOWER = (WIDTH - floor( WIDTH / 1.46 ),
                       HEIGHT - floor( HEIGHT / 3.2 ))
CLICK_LIM_BTN_UPPER = (WIDTH - floor( WIDTH / 3.14 ),
                       HEIGHT - floor( HEIGHT / 10.8 ))

# BGM AND CLICK SOUNC EFFECT
BGM = pygame.mixer.music.load( "assets/BGM.mp3" )
pygame.mixer.music.play( -1 )
CLICK_SOUND = pygame.mixer.Sound( "assets/SELECT1.ogg" )

# DIMENSIONS OF THE BOX TO BE DRAWN IN THE BACKGROUND ON PLAY SCREEN
BG_BOX_SIDE = 700
BG_BOX_X = 100
BG_BOX_Y = 100
DRAW_BUFFER = 50 # HOW FAR IN THIS BOX TO DRAW THE BOXES

# DIMENSIOONS OF THE WEIRDO, SUBJECT TO CHANGE
WEIRD_X = 0
WEIRD_Y = 0
# POSITION IN ARRAY OF THE WEIRDO
i_val, j_val = 0, 0

TAP = 0
# LEVELS FOR DIFFERENT TYPES
click_level = 1
time_level = 1

# GET THE HIGHSCORES RESPECTIVELY
fin = open( "assets/click_highscore.txt", "r" )
click_highscore = int( fin.read() )
fin.close()
fin = open( "assets/time_highscore.txt", 'r' )
time_highscore = int( fin.read() )
fin.close()

# FOR INITIALIZING ALL THE BOXES IN THE GAME
class Box_:
    def __init__( self, X, Y, Box_Side, Box_Color = (255, 255, 255), Is_Weirdo = False ):
        self.X = X
        self.Y = Y
        self.Box_Color = Box_Color
        self.Box_Side = Box_Side
        self.Surface = pygame.Surface( (self.Box_Side, self.Box_Side) )
        self.Is_Weirdo = Is_Weirdo
        self.Reveal_Surface_Color = (255, 255, 255)
        
        if Is_Weirdo:
            global WEIRD_X, WEIRD_Y
            WEIRD_X = self.X
            WEIRD_Y = self.Y
    
    def Draw_( self ):
        self.Surface.fill( self.Box_Color )
        WIN.blit( self.Surface, (self.X, self.Y) )

# MAIN 2 DIMENTIONAL LIST, CONTAINING ALL THE CLASS OBJECTS BY DEFAULT, WITH DEFAULT VALUES
#Boxes = [[Box_( 0, 0, 50, color.get( "White" ) )] * 25] * 25
Boxes = [[Box_( 0, 0, 50, color.get( "White" ) ) for i in range(25)] for j in range(25)]

# RETURNS A RANDOM COLOR
def AssignRandomColor( ):
    rand_X = random.randrange( 10, 255 )
    rand_Y = random.randrange( 10, 255 )
    rand_Z = random.randrange( 10, 255 )
    rand_Color = (rand_X, rand_Y, rand_Z)
    
    return rand_Color

# REVEALS THE BLACK RECTANGLE TO SHOW THE WEIRDO
def ShowRevealer( box_Side ):
    # reveal the box
    Reveal_Surface_Color = color.get( "Black" )
    pygame.draw.rect( WIN, Reveal_Surface_Color,
                      (WEIRD_X - 2, WEIRD_Y - 2, box_Side + 2, box_Side + 2), 2 )
    
    pygame.display.update()
    pygame.time.wait( 2000 )
    
    Reveal_Surface_Color = color.get( "White" )
    pygame.draw.rect( WIN, Reveal_Surface_Color,
                      (WEIRD_X - 2, WEIRD_Y - 2, box_Side + 2, box_Side + 2), 2 )
    
    pygame.display.update()

# RETURNS TRUE IF PLAYER PRESSES LEFT MOUSE BUTTON IN THE DESIRED COORDINATES, FALSE IF NOT
def checkMouse( lower_x, lower_Y, upper_X, upper_Y, event ):
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        CLICK_SOUND.play()
        
        if lower_x <= x <= upper_X:
            if lower_Y <= y <= upper_Y:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# DRAWS THE BACKGROUND IMAGE ON THE SCREEN FOR PLAYING
def drawAndAssignBG_BOX( BG_Color, BG_Size = 10 ):

    global BG_BOX_SIDE
    global BG_BOX_X
    global BG_BOX_Y
    
    BG_BOX_SIDE = floor( HEIGHT - 2 * HEIGHT / BG_Size ) # SIDE OF THE BACKGROUND BOX
    BG_BOX_X, BG_BOX_Y = floor( WIDTH / BG_Size ), floor( HEIGHT / BG_Size ) # COORDINATES OF THE BACKGROUND BOX
    BG_SURFACE = pygame.Surface( (BG_BOX_SIDE, BG_BOX_SIDE) )
    BG_SURFACE.fill( BG_Color )
    
    # BG IMAGE IS BLITTED FIRST, THEN THE BG BOX
    WIN.blit( PLAY_IMAGE, ORIGIN )
    WIN.blit( BG_SURFACE, (BG_BOX_X, BG_BOX_Y) )

# RETURNS TRUE IF PLAYER WANTS TO CONTINUE, ELSE FALSE
def lostGame( ):
    WIN.blit( LOST_IMAGE, ORIGIN )
    pygame.display.update()
    
    loop_Lost_Game = True
    play_Again = False
    
    while loop_Lost_Game:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_Lost_Game = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
                if event.key == pygame.K_p:
                    play_Again = True
                    loop_Lost_Game = False
                elif event.key == pygame.K_q:
                    loop_Lost_Game = False
                    
            # CHECK IF MOUSE IS PRESSED ON THE BUTTONS
            if checkMouse( START_BTN_LOWER[0], START_BTN_LOWER[1], START_BTN_UPPER[0],
                           START_BTN_UPPER[1], event ):
                play_Again = True
                loop_Lost_Game = False
                
            if checkMouse( EXIT_BTN_LOWER[0], EXIT_BTN_LOWER[1], EXIT_BTN_UPPER[0],
                           EXIT_BTN_UPPER[1], event ):
                loop_Lost_Game = False
                
    return play_Again

# RETURNS THE SIZE OF THE GRID DEPENDING ON THE LEVEL
def AssignMatrix( level ):
    
    gridSize = 4
    if level <= 5:
        gridSize = 5
    elif level <= 10:
        gridSize = 6
    elif level <= 15:
        gridSize = 7
    elif level <= 25:
        gridSize = 8
    elif level <= 30:
        gridSize = 9
    elif level <= 35:
        gridSize = 10
    elif level <= 40:
        gridSize = 12
    elif level <= 45:
        gridSize = 13
    elif level <= 50:
        gridSize = 14
    elif level <= 55:
        gridSize = 15
    elif level <= 60:
        gridSize = 16
    elif level <= 65:
        gridSize = 17
    elif level <= 70:
        gridSize = 18
    elif level <= 80:
        gridSize = 19
    elif level <= 90:
        gridSize = 20
    elif level >= 100:
        gridSize = 21
    return gridSize

# RETURNS THE DIFFICULTY OF THE LEVEL DEPENDING ON THE LEVEL
def AssignDifficulty( level ):
    
    difficulty = 50
    if level <= 5:
        difficulty = 55
    elif level <= 10:
        difficulty = 50
    elif level <= 20:
        difficulty = 40
    elif level <= 30:
        difficulty = 30
    elif level <= 40:
        difficulty = 20
    elif level <= 50:
        difficulty = 10
    elif level <= 60:
        difficulty = 5
    elif level <= 70:
        difficulty = 5
    elif level >= 70:
        difficulty = 4
    return difficulty

# RETURNS THE SIDE OF THE INDIVIDUAL BOXES DEPENDING ON THE GRID SIZE
def AssignBoxSide( matrix, BG_BOX_Side, BOX_Gap ):
    box_Side = floor( (BG_BOX_Side - ((matrix - 1) * BOX_Gap)) / matrix )
    
    return box_Side

# CHECKS IF THE COORDINATES OF THE MOUSE MATCH THE GIVEN ONE, RETURNS TRUE IF THEY DO, ELSE FALSE.
def CheckFoundWeirdo( x, y, Box_Side ):
    global WEIRD_X, WEIRD_Y
    
    if WEIRD_X < x < WEIRD_X + Box_Side:
        if WEIRD_Y < y < WEIRD_Y + Box_Side:
            return True
        else:
            return False
    else:
        return False

# DRAWS ALL THE TEXT ON THE SCREEN FOR THE CLICK FUNCTION
def drawStatsClick( cur_level, highscore ):
    font = pygame.font.Font( "assets/KEL.ttf", floor( HEIGHT / 7 ) )
    level_label = font.render( f"{cur_level}", True, color.get( "Blue" ) )
    score_label = font.render( f"{highscore}", True, color.get( "Green" ) )
    
    WIN.blit( level_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 4.32 )) )
    WIN.blit( score_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 2.0 )) )
    
    tap_label = font.render( f"{5 - TAP}", True, color.get( "Green" ) )
    # THIS IS FOR THE TAP THING, AS IT OVERWRITES FOR SOME REASON, WHILE OTHER DON'T
    SUBSURFACE = PLAY_IMAGE.subsurface(
        (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 ), tap_label.get_width(), tap_label.get_height()) )
    
    WIN.blit( SUBSURFACE, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
    WIN.blit( tap_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
    pygame.display.update()

# DRAWS ALL THE TEXT ON THE SCREEN FOR THE TIME FUNCTION
def drawStatsTime( cur_level, time_passed, highscore ):
    font = pygame.font.Font( "assets/KEL.ttf", floor( HEIGHT / 7 ) )
    level_label = font.render( f"{cur_level}", True, color.get( "Blue" ) )
    score_label = font.render( f"{highscore}", True, color.get( "Green" ) )
    
    WIN.blit( level_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 4.32 )) )
    WIN.blit( score_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 2.0 )) )
    
    time_label = font.render( f"{time_passed}", True, color.get( "Green" ) )
    SUBSURFACE = PLAY_IMAGE_TIME.subsurface(
        (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 ), time_label.get_width(), time_label.get_height()) )
    WIN.blit( SUBSURFACE, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
    WIN.blit( time_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
    pygame.display.update()

# RETURNS THE DECIMAL VALUE FROM THE INTEGER VALUE OF THE DIFFICULTY, TO DARKEN
def modDifficulty( wat_to_do, difficulty ):
    if wat_to_do == 'darken':
        difficulty = 1 - (difficulty / 100)
        modified_Difficulty = difficulty
        return modified_Difficulty

# ASSIGNS THE NEW VALUES TO THE MAIN ARRAY, AND RETURNS THE SIDE OF THE BOXES AFTER CALCULATING. ALSO ASSIGNS WEIRDO
def updateTime( level ):
    global Boxes, i_val, j_val, DRAW_BUFFER
    
    Box_Gap = 4
    
    drawAndAssignBG_BOX( color.get( "White" ), 10 )
    matrix = AssignMatrix( level )
    difficulty = AssignDifficulty( level )
    box_Side = AssignBoxSide( matrix, BG_BOX_SIDE - (DRAW_BUFFER * 2), Box_Gap )
    box_Color = AssignRandomColor()
    
    i_val, j_val = random.randrange( matrix ), random.randrange( matrix )
    
    for i in range( len( Boxes ) ):
        if i < matrix:
            for j in range( len( Boxes[i] ) ):
                if j < matrix:
                    # ASSIGN GENERALLY FOR ALL BOXES
                    x = DRAW_BUFFER + BG_BOX_X + j * (Box_Gap + box_Side)
                    y = DRAW_BUFFER + BG_BOX_Y + i * (Box_Gap + box_Side)
                    
                    # SELECT DIFFERENT SET OF COLORS FOR THE WEIRDO
                    if i == i_val and j == j_val:
                        rand_X = box_Color[0]
                        rand_Y = box_Color[1]
                        rand_Z = box_Color[2]
                        what_to_do = random.choice( ["darken", "lighten"] )
                        
                        if what_to_do == 'darken':
                            modified_Difficulty = modDifficulty( 'darken', difficulty )
                            rand_X *= modified_Difficulty
                            rand_Y *= modified_Difficulty
                            rand_Z *= modified_Difficulty
                            
                        elif what_to_do == 'lighten':
                            dif_Rand_X = 255 - rand_X
                            dif_Rand_Y = 255 - rand_Y
                            dif_Rand_Z = 255 - rand_Z
                            dif_Perc = difficulty / 100
                            dif_Rand_X *= dif_Perc
                            dif_Rand_Y *= dif_Perc
                            dif_Rand_Z *= dif_Perc
                            rand_X += dif_Rand_X
                            rand_Y += dif_Rand_Y
                            rand_Z += dif_Rand_Z
                        
                        rand_Color = (rand_X, rand_Y, rand_Z)
                        Box = Box_( x, y, box_Side, rand_Color, True )
                        Boxes[i][j] = Box
                        Boxes[i][j].Draw_()
                    # ASSIGN TO THE ARRAY
                    else:
                        Box = Box_( x, y, box_Side, box_Color )
                        Boxes[i][j] = Box
                        Boxes[i][j].Draw_()
    pygame.display.update()
    return box_Side

# ASSIGNS THE NEW VALUES TO THE MAIN ARRAY, AND RETURNS THE SIDE OF THE BOXES AFTER CALCULATING. ALSO ASSIGNS WEIRDO
def updateClick( level ):
    global Boxes, i_val, j_val, DRAW_BUFFER
    
    Box_Gap = 5
    
    drawAndAssignBG_BOX( color.get( "White" ), 10 )
    matrix = AssignMatrix( level )
    difficulty = AssignDifficulty( level )
    box_Side = AssignBoxSide( matrix, BG_BOX_SIDE - (DRAW_BUFFER * 2), Box_Gap )
    box_Color = AssignRandomColor()
    
    i_val, j_val = random.randrange( matrix ), random.randrange( matrix )
    
    for i in range( len( Boxes ) ):
        if i < matrix:
            for j in range( len( Boxes[i] ) ):
                if j < matrix:
                    x = DRAW_BUFFER + BG_BOX_X + j * (Box_Gap + box_Side)
                    y = DRAW_BUFFER + BG_BOX_Y + i * (Box_Gap + box_Side)
                    
                    if i == i_val and j == j_val:
                        print(i_val, j_val)	
                        rand_X = box_Color[0]
                        rand_Y = box_Color[1]
                        rand_Z = box_Color[2]
                        what_to_do = random.choice( ["darken", "lighten"] )
                        
                        if what_to_do == 'darken':
                            modified_Difficulty = modDifficulty( 'darken', difficulty )
                            rand_X *= modified_Difficulty
                            rand_Y *= modified_Difficulty
                            rand_Z *= modified_Difficulty
                            
                        elif what_to_do == 'lighten':
                            dif_Rand_X = 255 - rand_X
                            dif_Rand_Y = 255 - rand_Y
                            dif_Rand_Z = 255 - rand_Z
                            dif_Perc = difficulty / 100
                            dif_Rand_X *= dif_Perc
                            dif_Rand_Y *= dif_Perc
                            dif_Rand_Z *= dif_Perc
                            rand_X += dif_Rand_X
                            rand_Y += dif_Rand_Y
                            rand_Z += dif_Rand_Z
                            
                        rand_Color = (rand_X, rand_Y, rand_Z)
                        Box = Box_( x, y, box_Side, rand_Color, True )
                        Boxes[i][j] = Box
                        Boxes[i][j].Draw_()
                    else:
                        Box = Box_( x, y, box_Side, box_Color )
                        Boxes[i][j] = Box
                        Boxes[i][j].Draw_()
    
    pygame.display.update()
    return box_Side

# RETURNS 1 IF THE USER WINS THE LEVEL, 2 IF THE PLAYER LOSES, IS THE MAIN FUNCTION FOR CLICKING LIMIT.
def clickLimit( ):
    global BG_BOX_SIDE, DRAW_BUFFER, TAP, click_level, click_highscore
    
    loop_Click = True
    play_Again_Click = 0
    won_Level = False
    
    box_Side = updateClick( click_level )
    
    while loop_Click:
        
        if click_level >= click_highscore:
            click_highscore = click_level
            
        drawStatsClick( click_level, click_highscore )
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                loop_Click = False
                fout = open( "assets/click_highscore.txt", "w" )
                fout.write( click_highscore.__str__() )
                fout.close()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
                    
            if checkMouse( BG_BOX_X + DRAW_BUFFER, BG_BOX_Y + DRAW_BUFFER, (BG_BOX_X + BG_BOX_SIDE - DRAW_BUFFER),
                           (BG_BOX_Y + BG_BOX_SIDE - DRAW_BUFFER), event ):
                TAP += 1
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    won_Level = CheckFoundWeirdo( x, y, box_Side )
                    
        if won_Level:
            loop_Click = False
            play_Again_Click = 2
            click_level += 1
            TAP -= 1
        
        if TAP >= 5:
            font = pygame.font.Font( "assets/KEL.ttf", floor( HEIGHT / 7 ) )
            tap_label = font.render( f"{5 - TAP}", True, color.get( "Green" ) )
            
            SUBSURFACE = PLAY_IMAGE.subsurface(
                (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 ), tap_label.get_width(), tap_label.get_height()) )
            
            WIN.blit( SUBSURFACE, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
            WIN.blit( tap_label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
            
            pygame.display.update()
            
            ShowRevealer( box_Side )
            pygame.time.wait( 3000 )
            loop_Click = False
            
            play_Again_Click = lostGame()  # returns true if you wanna continue, else it returns false
            
            fout = open( "assets/click_highscore.txt", "w" )
            fout.write( click_highscore.__str__() )
            fout.close()
        
        pygame.display.update()
    
    return play_Again_Click

# RETURNS 1 IF THE USER WINS THE LEVEL, 2 IF THE PLAYER LOSES, IS THE MAIN FUNCTION FOR CLICKING LIMIT.
def timeLimit( ):
    global BG_BOX_SIDE, DRAW_BUFFER, time_level, time_highscore
    
    loop_Time = True
    play_Again_Time = 0
    won_Level = False
    
    box_Side = updateTime( time_level )
    
    clock = pygame.time.Clock()
    clock.tick()
    time1 = pygame.time.get_ticks()
    
    while loop_Time:
        
        time2 = pygame.time.get_ticks()
        time_passed = 5 - round( time2 / 1000 - time1 / 1000 )
        
        if time_level >= time_highscore:
            time_highscore = time_level
            
        drawStatsTime( time_level, time_passed, time_highscore )
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                loop_Time = False
                fout = open( "assets/time_highscore.txt", "w" )
                fout.write( time_highscore.__str__() )
                fout.close()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
                    
            if checkMouse( BG_BOX_X + DRAW_BUFFER, BG_BOX_Y + DRAW_BUFFER, (BG_BOX_X + BG_BOX_SIDE - DRAW_BUFFER),
                           (BG_BOX_Y + BG_BOX_SIDE - DRAW_BUFFER), event ):
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    won_Level = CheckFoundWeirdo( x, y, box_Side )
        if won_Level:
            loop_Time = False
            play_Again_Time = 3
            time_level += 1
            
        if time_passed <= 0:
            font = pygame.font.Font( "assets/KEL.ttf", floor( HEIGHT / 7 ) )
            time_Label = font.render( f"{5 - time_passed}", True, color.get( "Green" ) )
            
            SUBSURFACE = PLAY_IMAGE_TIME.subsurface(
                (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 ), time_Label.get_width(), time_Label.get_height()) )
            
            WIN.blit( SUBSURFACE, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
            WIN.blit( time_Label, (floor( WIDTH - WIDTH / 7.7 ), floor( HEIGHT / 1.4 )) )
            pygame.display.update()
            
            ShowRevealer( box_Side )
            pygame.time.wait( 3000 )
            loop_Time = False
            
            play_Again_Time = lostGame()  # returns ture if you wanna continue else returns false.
            
            fout = open( "assets/time_highscore.txt", "w" )
            fout.write( time_highscore.__str__() )
            fout.close()
        
        pygame.display.update()
    
    return play_Again_Time

# MAIN FUNCTION TO THEN COORDINATE THE 2 TYPES
def mainMenu( ):
    loop_Menu = 1
    global click_level, time_level, TAP
    
    while loop_Menu != 0:
        if loop_Menu == 1:
            TAP = 0
            time_level = 1
            click_level = 1
            WIN.blit( MENU_IMAGE, ORIGIN )
            pygame.display.update()
            
        if loop_Menu == 2:
            loop_Menu = clickLimit()
            
        if loop_Menu == 3:
            loop_Menu = timeLimit()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_Menu = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    loop_Menu = timeLimit()
                elif event.key == pygame.K_c:
                    loop_Menu = clickLimit()
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
                    
            if checkMouse( TIME_LIM_BTN_LOWER[0], TIME_LIM_BTN_LOWER[1], TIME_LIM_BTN_UPPER[0],
                           TIME_LIM_BTN_UPPER[1], event ):
                loop_Menu = timeLimit()
                
            if checkMouse( CLICK_LIM_BTN_LOWER[0], CLICK_LIM_BTN_LOWER[1], CLICK_LIM_BTN_UPPER[0],
                           CLICK_LIM_BTN_UPPER[1], event ):
                loop_Menu = clickLimit()
    
    pygame.quit()

# FUNCTION TO START THE GAME AND SHOW THE MAIN SCREEN.
def start( ):
    loop = True
    run_Menu = False
    while loop:
        WIN.blit( BG_IMAGE, ORIGIN )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    loop = False
                    run_Menu = True
                if event.key == pygame.K_e:
                    loop = False
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode( (event.w, event.h), pygame.RESIZABLE )
            if checkMouse( START_BTN_LOWER[0], START_BTN_LOWER[1], START_BTN_UPPER[0],
                           START_BTN_UPPER[1], event ):
                loop = False
                run_Menu = True
            if checkMouse( EXIT_BTN_LOWER[0], EXIT_BTN_LOWER[1], EXIT_BTN_UPPER[0],
                           EXIT_BTN_UPPER[1], event ):
                loop = False
    
    if run_Menu:
        mainMenu()
    pygame.quit()

start()
