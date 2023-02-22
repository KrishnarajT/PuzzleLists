# This file contains the Tetris class. We are following a structure similar to the one we did in java. Where each class instantiates another class used for a small part of the game.

import math
from settings import *
from tetromino import Tetromino


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(
            self.app.screen,
            (WIN_W * 0.595, WIN_H * 0.02),
            text="TETRIS",
            fgcolor=self.get_color(),
            size=TILE_SIZE * 1.65,
            bgcolor="black",
        )
        self.font.render_to(
            self.app.screen,
            (WIN_W * 0.65, WIN_H * 0.22),
            text="next",
            fgcolor="orange",
            size=TILE_SIZE * 1.4,
            bgcolor="black",
        )
        self.font.render_to(
            self.app.screen,
            (WIN_W * 0.64, WIN_H * 0.67),
            text="score",
            fgcolor="orange",
            size=TILE_SIZE * 1.4,
            bgcolor="black",
        )
        self.font.render_to(
            self.app.screen,
            (WIN_W * 0.64, WIN_H * 0.8),
            text=f"{self.app.tetris.score}",
            fgcolor="white",
            size=TILE_SIZE * 1.8,
        )


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.make_field_array()
        self.tetromino = Tetromino(self)
        self.speed_up = False

    def check_full_lines(self):
        row = FIELD_HEIGHT - 1
        for y in range(FIELD_HEIGHT - 1, -1, -1):
            for x in range(FIELD_WIDTH):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].position = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_WIDTH:
                row -= 1

            else:
                for x in range(FIELD_WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

    def is_game_over(self):
        if any(self.field_array[0]):
            pg.time.wait(1000)
            return True

    def make_field_array(self):
        return [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)]

    def put_tetromino_in_field_array(self):
        for block in self.tetromino.blocks:
            self.field_array[int(block.position.y)][int(block.position.x)] = block

    def check_tetromino_landing(self):
        if self.tetromino.landed:
            if self.is_game_over():
                self.__init__(app=self.app)
            self.put_tetromino_in_field_array()
            self.tetromino = Tetromino(self)
            self.speed_up = False

    def control(self, pressed_key):
        self.speed_up = False
        if pressed_key == pg.K_LEFT or pressed_key == pg.K_a:
            self.tetromino.move("left")
        elif pressed_key == pg.K_RIGHT or pressed_key == pg.K_d:
            self.tetromino.move("right")
        elif (
            pressed_key == pg.K_DOWN
            or pressed_key == pg.K_s
            or pressed_key == pg.K_SPACE
        ):
            self.speed_up = True
            # self.tetromino.move("down")
        elif pressed_key == pg.K_UP or pressed_key == pg.K_w:
            self.tetromino.rotate()
        else:
            self.speed_up = False

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                pg.draw.rect(
                    self.app.screen,
                    pg.Color("black"),
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    width=1,
                    border_radius=1,
                )

    def update(self):
        if self.app.anim_trigger or (self.speed_up and self.app.fast_anim_trigger):
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(surface=self.app.screen)
