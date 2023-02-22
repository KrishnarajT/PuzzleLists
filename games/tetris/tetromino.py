from settings import *
import math
import random


class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, position):
        self.tetromino = tetromino
        super().__init__(self.tetromino.tetris.sprite_group)

        self.position = vec(position) + INITIAL_OFFSET
        self.image = self.tetromino.image
        # self.color = pg.Color("#BE3114")
        # self.image = pg.Surface((TILE_SIZE - 2, TILE_SIZE - 2))
        # self.image.fill(color=self.color)
        self.rect = self.image.get_rect()
        self.alive = True

    def is_Alive(self):
        if not self.alive:
            self.kill()

    def set_rect_position(self):
        self.rect.topleft = self.position * TILE_SIZE

    def rotate(self, pivot):
        translated = self.position - pivot
        rotated = translated.rotate(90)
        return rotated + pivot

    # overridden method
    def update(self):
        self.set_rect_position()
        self.is_Alive()

    def is_colliding(self, position):
        if (
            0 <= position.x < FIELD_WIDTH
            and -2 <= position.y < FIELD_HEIGHT
            and (
                position.y < 0
                or self.tetromino.tetris.field_array[int(position.y)][int(position.x)]
                == 0
            )
        ):
            return False
        else:
            return True


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.image = random.choice(self.tetris.app.images)
        self.blocks = [Block(self, position) for position in TETROMINOES[self.shape]]
        self.landed = False

    def rotate(self):
        pivot = self.blocks[0].position
        new_block_positions = [block.rotate(pivot) for block in self.blocks]
        if not self.is_colliding(new_block_positions):
            for _, block in enumerate(self.blocks):
                block.position = new_block_positions[_]

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.position + move_direction for block in self.blocks]
        gonna_collide = self.is_colliding(new_block_positions)
        if not gonna_collide:
            for block in self.blocks:
                block.position += move_direction
        elif direction == "down":
            self.landed = True

    def is_colliding(self, block_positions):
        return any(map(Block.is_colliding, self.blocks, block_positions))

    def update(self):
        self.move("down")
        pass
