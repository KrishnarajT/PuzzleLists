# 2048, THE IDEA OF THE GAME IS THAT YOU HAVE TO COMBINE DIFERENT BLOCKS TO MAKE A BLOCK THAT IS OF 2 TIMES THE VALUE
# OF THE PREVIOUS BLOCK. AND THIS IS DONE BY PRESSING THE ARROW KEYS TO MOVE ALL THE MOVABLE BLOCKS IN THE DIRECTION OF
# THE ARROW KEY PRESSED. UPON MOVING, A RANDOM TILE OF VALUE 2 IS SPAWNED SOMEWHERE IN THE GRID, YOU LOSE WHEN YOUR GRID
# IS FULL
# THE LOGIC FOR THIS GAME IS THAT WE CREATE A MAIN 3 DIMENTIONAL LIST OF DIFFERENT NUMBER OF ELEMENTS, AND ALL THE
# CALCULATIONS OF THE LIST ARE DONE IN THAT 3D LIST, THE TILES ARE DRAWN ONLY IN FUNCTION, WHERE THEIR OBJECTS ARE
# GENERATED FOR THE TIME BEING AND THEN BLITTED.

import pygame
import random
from math import floor
import os

from pathlib import Path

PUZZLE_LIST_DIR = str(Path(__file__).parent.parent.parent)
BGM = None
color = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "DarkGreen": (0, 128, 0),
    "NavyBlue": (0, 0, 128),
    "Grey": (128, 128, 128),
    "Lavender": (230, 230, 250),
    "Orange": (255, 165, 0),
    "DarkOrange": (255, 70, 0),
    "Brown": (165, 42, 42),
    "Pink": (255, 192, 203),
}
ORIGIN = (0, 0)


def checkMouse(lower_x, lower_Y, upper_X, upper_Y, event):
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        # print(lower_x, lower_Y, upper_X, upper_Y, x, y)
        if lower_x <= x <= upper_X:
            if lower_Y <= y <= upper_Y:
                # print("You got it bro!")
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def printList(arr):
    if isinstance(arr[0], list):
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                print(arr[i][j], end=" ")

            print()
    else:
        for i in arr:
            print(i)
    print()


# RETURNS TRUE IF A AND B ARE IN PROXIMITY OF S FROM EACH OTHER


def isClostTo(a, b, s):
    rng = [b - s, b + s]
    if rng[0] <= a <= rng[1]:
        return True
    else:
        return False


# CUSTOM HEADER PYTHON MODULE MADY BY KPT


# function to leave spaces
def gimmi_Some_Space_pybro(Sure_how_Many_Lines_bro):
    print((Sure_how_Many_Lines_bro - 1) * "\n")


# function to check if a number is even
def check_Even(number):
    if number % 2 == 0:
        return True


# function to return the extension of a file.
def file_Extension_Return(File_Name):
    return File_Name[File_Name.index(".") :]


def count_Character_In_File(File_Name, Char_To_Check):
    fin = open(File_Name, "r")
    stuffInFile = fin.read()

    count = 0
    for i in stuffInFile:
        if i == Char_To_Check:
            count += 1
    fin.close()
    return count


def count_Characters_In_File(File_Name):
    fin = open(File_Name, "r")
    stuffInFile = fin.read()
    count = stuffInFile.__len__()
    fin.close()
    return count


pygame.font.init()
pygame.mixer.init()

# INTITIALIZING THE WIDTH AND THE HEIGHT OF THE WINDOW.
# THIS GAME WILL BE MADE WITH RESPECT TO THE HEGHT AND THE WIDTH OF THE MONITOR, AND WILL BE HALF OF THAT./

WIDTH, HEIGHT = 1280, 720
# WIDTH, HEIGHT = floor(WIDTH * 0.75), floor(HEIGHT * 0.75)

# INITIALIZING THE DIMENSIONS OF THE BG_BOX OF THE 2048 THING, AND THE SIDE OF THE TILES

BG_BOX_SIZE = floor(HEIGHT / 1.35)
BG_BOX_X = floor(WIDTH / 6.4)
BG_BOX_Y = floor(HEIGHT / 7.7)
BG_BOX_GAP_X = floor(BG_BOX_SIZE / 35)
BG_BOX_GAP_Y = floor(BG_BOX_SIZE / 35)
TILE_SIDE = floor(BG_BOX_SIZE / 4.6511)

# INITIALIZING THE WINDOW.

WIN = None
# INITIALIZING THE FONTS.

GAME_FONT = pygame.font.Font(
    os.path.join(PUZZLE_LIST_DIR, "resources/fonts/", "kel.ttf"), 70
)

# INTITIALIZING THE IMAGES.

BG_IMAGE = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "BG_IMAGE.png")
    ),
    (WIDTH, HEIGHT),
)
LOST_IMAGE = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "LOST_IMAGE.png")
    ),
    (WIDTH, HEIGHT),
)
PLAY_IMAGE = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "PLAY_IMAGE.png")
    ),
    (WIDTH, HEIGHT),
)
BG_BOX_IMAGE = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "BG_BOX_IMAGE.png")
    ),
    (BG_BOX_SIZE, BG_BOX_SIZE),
)

# INITIALIZING THE VALUED TILES.
IMAGE_2 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "2.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_4 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "4.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_8 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "8.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_16 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "16.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_32 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "32.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_64 = pygame.transform.scale(
    pygame.image.load(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "64.png")),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_128 = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "128.png")
    ),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_256 = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "256.png")
    ),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_512 = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "512.png")
    ),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_1024 = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "1024.png")
    ),
    (TILE_SIDE, TILE_SIDE),
)
IMAGE_2048 = pygame.transform.scale(
    pygame.image.load(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "2048.png")
    ),
    (TILE_SIDE, TILE_SIDE),
)

# INITIALIZING THE POSITIONS OF THE BUTTONS.

START_BTN_LOWER = (floor(WIDTH / 3.67), floor(HEIGHT / 1.75))
START_BTN_UPPER = (floor(WIDTH / 2.1), floor(HEIGHT / 1.43))

EXIT_BTN_LOWER = (floor(WIDTH / 1.9), floor(HEIGHT / 1.73))
EXIT_BTN_UPPER = (floor(WIDTH / 1.41), floor(HEIGHT / 1.43))

# INITIALIZING THE GLOBAL LIST THAT CONTAINS ALL THE STUFF (BASED ON THE WIDTH AND THE HEIGHT)

Coordees = []
for I in range(4):
    rows = []
    for J in range(4):
        rows.append([0, 0, 0, 0, 0])  # (x, y, tileExists?, tile_value, tile_Merged?)
    Coordees.append(rows)

# INITIALIZING THE SCORE

score = 0
fin = open(os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"), "r")
high_score = fin.read()
fin.close()


# INITIALIZING THE CLASS TILE
class Tile:
    def __init__(self, X, Y, Tile_Side, Value=2):
        self.X = X
        self.Y = Y
        self.Tile_Side = Tile_Side
        self.Value = Value
        self.Image = IMAGE_2
        self.SetImage_()

    def SetImage_(self):
        if self.Value == 2:
            self.Image = IMAGE_2
        elif self.Value == 4:
            self.Image = IMAGE_4
        elif self.Value == 8:
            self.Image = IMAGE_8
        elif self.Value == 16:
            self.Image = IMAGE_16
        elif self.Value == 32:
            self.Image = IMAGE_32
        elif self.Value == 64:
            self.Image = IMAGE_64
        elif self.Value == 128:
            self.Image = IMAGE_128
        elif self.Value == 256:
            self.Image = IMAGE_256
        elif self.Value == 512:
            self.Image = IMAGE_512
        elif self.Value == 1024:
            self.Image = IMAGE_1024
        elif self.Value == 2048:
            self.Image = IMAGE_2048

    def Draw_(self):
        WIN.blit(self.Image, (self.X, self.Y))


Tiles = []

""" ONE TIME RUN METHODS """


# DRAWS THE BACKGROUND OF THE TILES.
def drawBG_BOX():
    WIN.blit(BG_BOX_IMAGE, (BG_BOX_X, BG_BOX_Y))


# METHOD TO ASSIGN CORDEES
def assignCordees():
    for k in range(len(Coordees)):
        y = floor((BG_BOX_Y + BG_BOX_GAP_Y) + (k * (TILE_SIDE + BG_BOX_GAP_Y)))
        for l in range(len(Coordees[k])):
            x = floor((BG_BOX_X + BG_BOX_GAP_X) + (l * (TILE_SIDE + BG_BOX_GAP_X)))
            Coordees[k][l][0] = x
            Coordees[k][l][1] = y
            Coordees[k][l][2] = 0
            Coordees[k][l][3] = 0
            Coordees[k][l][4] = 0


# ASSIGNS THE FIRST 2 RANDOM TILES, AND DRAWS THEM ON THE SCREEN
def AssignFirstTwo():
    ran_I, ran_J = random.randrange(4), random.randrange(4)
    Coordees[ran_I][ran_J][2] = 1
    Coordees[ran_I][ran_J][3] = 2
    ran_I = random.choice([e for e in range(0, 4) if e not in [ran_I]])
    ran_J = random.choice([r for r in range(0, 4) if r not in [ran_J]])
    Coordees[ran_I][ran_J][2] = 1
    Coordees[ran_I][ran_J][3] = 2


""" MANY TIME RUN METHODS """


# RETURNS TRUE IF IT IS POSSIBLE TO MOVE ANYTHING, ELSE RETURNS FALSE
def isMovable():
    if (
        not rightMovable()
        and not leftMovable()
        and not upMovable()
        and not downMovable()
    ):
        return False
    else:
        return True


# DRAWS THE TILES BASED ON THE COORDEES
def drawTiles():
    gameTiles = []
    WIN.blit(PLAY_IMAGE, ORIGIN)
    drawBG_BOX()
    for i in range(4):
        for j in range(4):
            if Coordees[i][j][2] == 1:
                tileObj = Tile(
                    Coordees[i][j][0], Coordees[i][j][1], TILE_SIDE, Coordees[i][j][3]
                )
                gameTiles.append(tileObj)
                tileObj.SetImage_()
                tileObj.Draw_()
    pygame.display.update()


# METHOD TO REFRESH COORDEES, AND UPDATE ALL THE PLACES WHERE IT MAY BE DIFFERENT FROM THE ACTUAL VALUES
def refreshCoordees():
    for k in range(4):
        for l in range(4):
            itsThere = False
            for m in range(len(Tiles)):
                if isClostTo(Tiles[m].X, Coordees[k][l][0], 5) and isClostTo(
                    Tiles[m].Y, Coordees[k][l][1], 5
                ):
                    Coordees[k][l][2] = 1
                    itsThere = True
            if not itsThere:
                Coordees[k][l][2] = 0


# RETURNS THE TILE OBJ THAT HAS THE SAME X AND Y VALUES AS THE INDICES GIVEN IN THE PARAMETERS
def GetTileFrmCoordees(i, j):
    for t in Tiles:
        if isClostTo(t.X, Coordees[i][j][0], 10) and isClostTo(
            t.Y, Coordees[i][j][1], 10
        ):
            return t


# ASSIGNS A RANDOM TILE SOMEWHERE, EXCLUDING ALL THE PLACES WHERE THE TILES EXIST.
def assignRandom():
    exceptList = []
    for i in range(4):
        for j in range(4):
            exceptList.append([i, j])
    for i in range(len(Coordees)):
        for j in range(len(Coordees)):
            if Coordees[i][j][2] == 1:
                for g in range(len(exceptList)):
                    if exceptList[g][0] == i and exceptList[g][1] == j:
                        exceptList.remove(exceptList[g])
                        break
    randomList = random.choice(exceptList)

    for i in range(4):
        for j in range(4):
            if i == randomList[0] and j == randomList[1]:
                Coordees[randomList[0]][randomList[1]][2] = 1
                Coordees[randomList[0]][randomList[1]][3] = 2


# RESETS THE MERGED VALUE OF ALL THE TILES
def resetMergeVal():
    for i in range(4):
        for j in range(4):
            Coordees[i][j][4] = 0


# DRAWS THE SCORE AND THE HIGHSCORE ON THE SCREEN
def drawStuff():
    global high_score, score
    if score > int(high_score):
        high_score = score
    font = pygame.font.Font(
        os.path.join(PUZZLE_LIST_DIR, "resources/fonts", "kel.ttf"), floor(HEIGHT / 9)
    )
    score_str_Label = font.render("Score", True, color.get("White"))
    score_Label = font.render(f"{score}", True, color.get("White"))
    high_Score_str_Label = font.render("Highscore", True, color.get("White"))
    high_Score_Label = font.render(f"{high_score}", True, color.get("White"))
    WIN.blit(score_str_Label, (floor(WIDTH / 1.6), floor(HEIGHT / 5.4)))
    WIN.blit(score_Label, (floor(WIDTH / 1.47), floor(HEIGHT / 3)))
    WIN.blit(high_Score_str_Label, (floor(WIDTH / 1.6), floor(HEIGHT / 1.8)))
    WIN.blit(high_Score_Label, (floor(WIDTH / 1.47), floor(HEIGHT / 1.5)))


""" FUNCTIONS TO CHECK IF THE TILES ARE MOVABLE IN THAT SPECIFIC DIRECTION """


# RETURNS TRUE IF ANY TILE IS MOVABLE OR MERGABLE IN RIGHT DIRECTION, FALSE IF NOT.
def rightMovable():
    for i in range(4):
        for j in range(2, 5):
            if Coordees[i][-j][2] == 1:
                if Coordees[i][-j + 1][2] == 0:
                    return True
                else:
                    if Coordees[i][-j + 1][3] == Coordees[i][-j][3]:
                        if Coordees[i][-j + 1][4] == 0 and Coordees[i][-j][4] == 0:
                            return True
    return False


# RETURNS TRUE IF ANY TILE IS MOVABLE OR MERGABLE IN LEFT DIRECTION, FALSE IF NOT.
def leftMovable():
    for i in range(4):
        for j in range(1, 4):
            if Coordees[i][j][2] == 1:
                if Coordees[i][j - 1][2] == 0:
                    return True
                else:
                    if Coordees[i][j - 1][3] == Coordees[i][j][3]:
                        if Coordees[i][j - 1][4] == 0 and Coordees[i][j][4] == 0:
                            return True
    return False


# RETURNS TRUE IF ANY TILE IS MOVABLE OR MERGABLE IN DOWN DIRECTION, FALSE IF NOT.
def downMovable():
    for i in range(2, 5):
        for j in range(4):
            if Coordees[-i][j][2] == 1:
                if Coordees[-i + 1][j][2] == 0:
                    return True
                else:
                    if Coordees[-i + 1][j][3] == Coordees[-i][j][3]:
                        if Coordees[-i + 1][j][4] == 0 and Coordees[-i][j][4] == 0:
                            return True
    return False


# RETURNS TRUE IF ANY TILE IS MOVABLE OR MERGABLE IN UP DIRECTION, FALSE IF NOT.
def upMovable():
    for i in range(1, 4):
        for j in range(4):
            if Coordees[i][j][2] == 1:
                if Coordees[i - 1][j][2] == 0:
                    return True
                else:
                    if Coordees[i - 1][j][3] == Coordees[i][j][3]:
                        if Coordees[i - 1][j][4] == 0 and Coordees[i][j][4] == 0:
                            return True
    return False


""" THE FUNCTIONS TO MOVE THE TILES """

""" CHANGES THE POSITION OF THE ELEMENTS OF THE LISTS IN COORDEES, AND THEN PRINTS THEM """


def moveUp():
    global score
    for i in range(1, 4):
        for j in range(4):
            if Coordees[i][j][2] == 1:
                if Coordees[i - 1][j][2] == 0:
                    Coordees[i][j][2] = 0
                    Coordees[i - 1][j][2] = 1
                    Coordees[i - 1][j][3] = Coordees[i][j][3]
                    Coordees[i][j][3] = 0
                elif (
                    Coordees[i - 1][j][2] == 1
                    and Coordees[i][j][3] == Coordees[i - 1][j][3]
                ):
                    if Coordees[i - 1][j][4] == 0 and Coordees[i][j][4] == 0:
                        Coordees[i][j][2] = 0
                        Coordees[i][j][3] = 0
                        Coordees[i - 1][j][3] *= 2
                        score += Coordees[i - 1][j][3]
                        Coordees[i - 1][j][4] = 1

    drawTiles()
    pygame.time.wait(100)


def moveDown():
    global score
    for i in range(2, 5):
        for j in range(4):
            if Coordees[-i][j][2] == 1:
                if Coordees[-i + 1][j][2] == 0:
                    Coordees[-i][j][2] = 0
                    Coordees[-i + 1][j][2] = 1
                    Coordees[-i + 1][j][3] = Coordees[-i][j][3]
                    Coordees[-i][j][3] = 0
                elif (
                    Coordees[-i + 1][j][2] == 1
                    and Coordees[-i + 1][j][3] == Coordees[-i][j][3]
                ):
                    if Coordees[-i + 1][j][4] == 0 and Coordees[-i + 1][j][4] == 0:
                        Coordees[-i][j][2] = 0
                        Coordees[-i][j][3] = 0
                        Coordees[-i + 1][j][3] *= 2
                        score += Coordees[-i + 1][j][3]
                        Coordees[-i + 1][j][4] = 1

    drawTiles()
    pygame.time.wait(100)


def moveLeft():
    global score
    for i in range(4):
        for j in range(1, 4):
            if Coordees[i][j][2] == 1:
                if Coordees[i][j - 1][2] == 0:
                    Coordees[i][j][2] = 0
                    Coordees[i][j - 1][2] = 1
                    Coordees[i][j - 1][3] = Coordees[i][j][3]
                    Coordees[i][j][3] = 0
                elif (
                    Coordees[i][j - 1][2] == 1
                    and Coordees[i][j][3] == Coordees[i][j - 1][3]
                ):
                    if Coordees[i][j - 1][4] == 0 and Coordees[i][j][4] == 0:
                        Coordees[i][j][2] = 0
                        Coordees[i][j][3] = 0
                        Coordees[i][j - 1][3] *= 2
                        score += Coordees[i][-j + 1][3]
                        Coordees[i][j - 1][4] = 1
    drawTiles()
    pygame.time.wait(100)


def moveRight():
    global score
    for i in range(4):
        for j in range(2, 5):
            if Coordees[i][-j][2] == 1:
                if Coordees[i][-j + 1][2] == 0:
                    Coordees[i][-j][2] = 0
                    Coordees[i][-j + 1][2] = 1
                    Coordees[i][-j + 1][3] = Coordees[i][-j][3]
                    Coordees[i][-j][3] = 0
                elif (
                    Coordees[i][-j + 1][2] == 1
                    and Coordees[i][-j][3] == Coordees[i][-j + 1][3]
                ):
                    if Coordees[i][-j + 1][4] == 0 and Coordees[i][-j][4] == 0:
                        Coordees[i][-j][2] = 0
                        Coordees[i][-j][3] = 0
                        Coordees[i][-j + 1][3] *= 2
                        Coordees[i][-j + 1][4] = 1
                        score += Coordees[i][-j + 1][3]
    drawTiles()
    pygame.time.wait(100)


# CHECKS FOR USER IMPUT AND RUNS THE FUNCTIONS THAT ARE USED TO MOVE THE TILES
def moveTiles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        moved = False
        while upMovable():
            moveUp()
            moved = True
        if moved:
            assignRandom()
            resetMergeVal()
            drawTiles()
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        moved = False
        while downMovable():
            moveDown()
            moved = True
        if moved:
            assignRandom()
            resetMergeVal()
            drawTiles()
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        moved = False
        while leftMovable():
            moveLeft()
            moved = True
        if moved:
            assignRandom()
            resetMergeVal()
            drawTiles()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        moved = False
        while rightMovable():
            moveRight()
            moved = True
        if moved:
            assignRandom()
            resetMergeVal()
            drawTiles()


# METHOD TO DO THE STUFF INSIDE THE PLAY GAME FUNCTION
def runPlay():
    WIN.blit(PLAY_IMAGE, ORIGIN)
    drawBG_BOX()
    assignCordees()
    AssignFirstTwo()
    drawTiles()
    pygame.display.update()


# RUNS THOSE FUNCTIONS IN THE LOOP THAT REQUIRE BEING CALLED EVERY FRAME.
def updatePlayInLoop():
    moveTiles()
    drawStuff()
    pygame.display.update()


# DEFINING THE PLAY GAME FUNCTION
def playGame():
    play_Loop = True
    result = False
    clock = pygame.time.Clock()
    runPlay()
    while play_Loop:
        clock.tick(60)
        updatePlayInLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fout = open(
                    os.path.join(
                        PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"
                    ),
                    "w",
                )
                fout.write(high_score.__str__())
                fout.close()
                play_Loop = False
        if not isMovable():
            pygame.time.wait(3000)
            result = lostGame()
            fout = open(
                os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"),
                "w",
            )
            fout.write(high_score.__str__())
            fout.close()
            play_Loop = False
    return result


# DEFINING THE LOST GAME FUNCTION, RETURNS FALSE IF YOU WANNA QUIT, TRUE IF YOU WANNA CONTINUE
def lostGame():
    lost_Loop = True
    result = False
    while lost_Loop:
        WIN.blit(LOST_IMAGE, ORIGIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fout = open(
                    os.path.join(
                        PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"
                    ),
                    "w",
                )
                fout.write(high_score.__str__())
                fout.close()
                lost_Loop = False
            if checkMouse(
                START_BTN_LOWER[0],
                START_BTN_LOWER[1],
                START_BTN_UPPER[0],
                START_BTN_UPPER[1],
                event,
            ):
                lost_Loop = False
                result = True
            if checkMouse(
                EXIT_BTN_LOWER[0],
                EXIT_BTN_LOWER[1],
                EXIT_BTN_UPPER[0],
                EXIT_BTN_UPPER[1],
                event,
            ):
                lost_Loop = False
                result = False
        pygame.display.update()
    return result


# DEFINING THE START FUNCTION
def start_2048():
    global score, high_score, fin, WIN, CLICK_SOUND, BGM

    # INITIALIZING THE WINDOW
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("2048")

    # INITIALIZING THE BG MUSIC

    pygame.mixer.music.load(os.path.join(PUZZLE_LIST_DIR, "resources/audio", "BGM.ogg"))
    pygame.mixer.music.play()
    CLICK_SOUND = pygame.mixer.Sound(
        os.path.join(PUZZLE_LIST_DIR, "resources/audio", "SELECT1.ogg")
    )

    start_Loop = True
    while start_Loop:
        WIN.blit(BG_IMAGE, ORIGIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_Loop = False
            if checkMouse(
                START_BTN_LOWER[0],
                START_BTN_LOWER[1],
                START_BTN_UPPER[0],
                START_BTN_UPPER[1],
                event,
            ):
                start_Loop = playGame()
                if start_Loop:
                    score = 0
                    fin = open(
                        os.path.join(
                            PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"
                        ),
                        "r",
                    )
                    high_score = fin.read()
                    fin.close()

            if checkMouse(
                EXIT_BTN_LOWER[0],
                EXIT_BTN_LOWER[1],
                EXIT_BTN_UPPER[0],
                EXIT_BTN_UPPER[1],
                event,
            ):
                start_Loop = False
        pygame.display.update()

    fout = open(
        os.path.join(PUZZLE_LIST_DIR, "resources/images/2048", "highscore.txt"), "w"
    )
    fout.write(high_score.__str__())
    fout.close()
    pygame.quit()
    return floor(score / 50)


# print(start_2048())
