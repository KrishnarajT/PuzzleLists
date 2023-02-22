import pygame

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

def checkMouse( lower_x, lower_Y, upper_X, upper_Y, event ):
    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        #print(lower_x, lower_Y, upper_X, upper_Y, x, y)
        if lower_x <= x <= upper_X:
            if lower_Y <= y <= upper_Y:
                #print("You got it bro!")
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
                print(arr[i][j], end = ' ')
                
            print()
    else:
        for i in arr:
            print(i)
    print()
    
# RETURNS TRUE IF A AND B ARE IN PROXIMITY OF S FROM EACH OTHER

def isClostTo( a, b, s ):
    rng = [b - s, b + s]
    if rng[0] <= a <= rng[1]:
        return True
    else:
        return False
    
# CUSTOM HEADER PYTHON MODULE MADY BY KPT

# function to leave spaces
def gimmi_Some_Space_pybro( Sure_how_Many_Lines_bro ):
    print( (Sure_how_Many_Lines_bro - 1) * "\n" )

# function to check if a number is even
def check_Even(number):
    if number % 2 == 0:
        return True

# function to return the extension of a file.
def file_Extension_Return(File_Name):
    return File_Name[File_Name.index("."):]

def count_Character_In_File(File_Name, Char_To_Check):
    fin = open( File_Name, "r" )
    stuffInFile = fin.read()
    
    count = 0
    for i in stuffInFile:
        if i == Char_To_Check:
            count += 1
    fin.close()
    return count

def count_Characters_In_File(File_Name):
    fin = open( File_Name, "r" )
    stuffInFile = fin.read()
    count = stuffInFile.__len__()
    fin.close()
    return count
	
'''
COPY MATERIAL

    lost_Loop = False
    while lost_Loop:
        WIN.blit( PLAY_IMAGE, ORIGIN )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_Loop = False
'''