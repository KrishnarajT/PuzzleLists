# This file contains constants relating to the entire game. 
import pygame as pg

vec = pg.math.Vector2

# Constants
WIDTH = 1280
HEIGHT = 720
FPS = 30

# Tetris Constants
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20
TILE_SIZE = HEIGHT // FIELD_HEIGHT
FIELD_RES = FIELD_WIDTH * TILE_SIZE, FIELD_HEIGHT * TILE_SIZE

# Design Constants
BG_COLOR = pg.Color("#FFDDE0")
FIELD_BG_COLOR = pg.Color("#000000")

# Vector Constants
INITIAL_OFFSET = vec(FIELD_WIDTH // 2, -1)

MOVE_DIRECTIONS = {
    'left': vec(-1, 0),
    'right': vec(1, 0),
    'down': vec(0, 1),
}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
}

# Animation Constants
ANIM_TIME_INTERVAL = 500 # milliseconds
FAST_ANIM_INTERVAL = 50 # milliseconds

# Sprite Constants
SPRITE_DIR_PATH = 'design/sprites'