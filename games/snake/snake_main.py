import pygame as pg
from pygame.locals import *
import random as rd
import os
import time as tm

#  variables for snake eyes
snake_eyes = pg.Color("#ffffff")

# Initializing colors for snake, background and food
snake_color = pg.Color("#d25062")
back_gd = pg.Color("#fedde0")
snake_food_color = (0, 255, 0)

# game over screen
game_over_mssg = pg.Color("#952735")
game_over_color = "#0C120C"


# length of snake
Size = 33

# Food Class


class Food:
    def __init__(self, parent_display):
        self.parent_display = parent_display
        self.apple_image = pg.image.load(
            os.path.join(os.getcwd(), "resources/images/snake/apple.png")
        ).convert_alpha()
        self.apple_image = pg.transform.scale(self.apple_image, (40, 40))
        self.pos_x = Size * 3
        self.pos_y = Size * 3
        # pg.draw.circle(self.parent_display,snake_color,[self.pos_x[i],self.pos_y[i]],20,20)

    def draw_food(self):
        # pg.draw.rect(self.parent_display,snake_food_color,[self.pos_x,self.pos_y,37,37])
        self.parent_display.blit(self.apple_image, (self.pos_x, self.pos_y))
        pg.display.flip()

    def change_position(self):
        self.pos_x = rd.randint(0, 27) * Size
        self.pos_y = rd.randint(0, 18) * Size


# snake class
class Snake:
    def __init__(self, parent_display):
        self.parent_display = parent_display
        self.snake_image = pg.image.load(
            os.path.join(os.getcwd(), "resources/images/snake/snakeu.png")
        )
        self.snake_image = pg.transform.scale(self.snake_image, (40, 40))
        self.snake_body = pg.image.load(
            os.path.join(os.getcwd(), "resources/images/snake/body.png")
        )
        self.snake_body = pg.transform.scale(self.snake_body, (40, 40))

        self.length = 1
        # snake position:
        self.pos_x = [Size]
        self.pos_y = [Size]

        self.direction_of_snake = "DOWN"
        self.changed_direction = self.direction_of_snake

    def draw_body(self):
        # we need display fill to clear previous blocks before moving to new co-ordinate
        self.parent_display.fill(back_gd)

        if self.direction_of_snake == "DOWN":
            self.snake_image = pg.image.load(
                os.path.join(os.getcwd(), "resources/images/snake/snaked.png")
            )
            self.snake_image = pg.transform.scale(self.snake_image, (40, 40))
        if self.direction_of_snake == "UP":
            self.snake_image = pg.image.load(
                os.path.join(os.getcwd(), "resources/images/snake/snakeu.png")
            )
            self.snake_image = pg.transform.scale(self.snake_image, (40, 40))

        self.parent_display.blit(self.snake_image, (self.pos_x[0], self.pos_y[0]))

        for i in range(1, self.length):
            self.parent_display.blit(self.snake_body, (self.pos_x[i], self.pos_y[i]))
        pg.display.flip()

    # Change snake direction
    def move_UP(self):
        self.direction_of_snake = "UP"

    def move_DOWN(self):
        self.direction_of_snake = "DOWN"

    def move_LEFT(self):
        self.direction_of_snake = "LEFT"
        self.snake_image = pg.image.load(
            os.path.join(os.getcwd(), "resources/images/snake/snakel.png")
        )
        self.snake_image = pg.transform.scale(self.snake_image, (40, 40))

    def move_RIGHT(self):
        self.direction_of_snake = "RIGHT"
        self.snake_image = pg.image.load(
            os.path.join(os.getcwd(), "resources/images/snake/snaker.png")
        )
        self.snake_image = pg.transform.scale(self.snake_image, (40, 40))

    # to check if two keys are pressed simultaneously
    def check_if_two_keys_pressed(self, changed_direction):
        if changed_direction == "UP" and self.direction_of_snake != "DOWN":
            self.move_UP()

        if changed_direction == "DOWN" and self.direction_of_snake != "UP":
            self.move_DOWN()

        if changed_direction == "LEFT" and self.direction_of_snake != "RIGHT":
            self.move_LEFT()

        if changed_direction == "RIGHT" and self.direction_of_snake != "LEFT":
            self.move_RIGHT()

    def snake_change_direction(self):
        for i in range(self.length - 1, 0, -1):
            self.pos_x[i] = self.pos_x[i - 1]
            self.pos_y[i] = self.pos_y[i - 1]

        if self.direction_of_snake == "UP":
            self.pos_y[0] -= Size

        if self.direction_of_snake == "DOWN":
            self.pos_y[0] += Size

        if self.direction_of_snake == "LEFT":
            self.pos_x[0] -= Size

        if self.direction_of_snake == "RIGHT":
            self.pos_x[0] += Size

        self.draw_body()

    # Increase body length
    def increase_body_length(self):
        self.length += 1
        self.pos_x.append(-1)
        self.pos_y.append(-1)


# game class
class snake_game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Snake BY Puzzlelists")

        self.display = pg.display.set_mode((1280, 720))
        self.display.fill(back_gd)
        self.snake = Snake(self.display)
        self.snake.draw_body()
        self.food = Food(self.display)
        self.food.draw_food()
        self.speed = 0.21

    # reset game
    def reset(self):
        self.snake = Snake(self.display)
        self.food = Food(self.display)

    # collision detection between apple and snake
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Size:
            if y1 >= y2 and y1 < y2 + Size:
                return True
        return False

    # render background
    def render_background(self):
        self.display.fill(back_gd)

    def play(self):
        self.render_background()
        self.snake.snake_change_direction()
        self.food.draw_food()
        self.display_score()
        pg.display.flip()

        # snake eating apple scenario
        if self.is_collision(
            self.snake.pos_x[0], self.snake.pos_y[0], self.food.pos_x, self.food.pos_y
        ):
            self.food.change_position()
            self.snake.increase_body_length()
            self.Increase_speed()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(
                self.snake.pos_x[0],
                self.snake.pos_y[0],
                self.snake.pos_x[i],
                self.snake.pos_y[i],
            ):
                raise "Collision Occurred"

        # snake colliding with wall
        if (
            self.snake.pos_x[0] >= 1280
            or self.snake.pos_x[0] < 0
            or self.snake.pos_y[0] >= 780
            or self.snake.pos_y[0] < 0
        ):
            raise "collision Occurred"

    # display score
    def display_score(self):
        font = pg.font.SysFont("arial", 30)
        score = font.render(f"SCORE:{self.snake.length}", True, (0, 0, 0))
        self.display.blit(score, (1000, 10))

    # game over screen

    def game_over_screen(self):
        self.render_background()
        font = pg.font.SysFont("arial", 30)
        line1 = font.render(
            f"Game Is Over! Your Score is {self.snake.length}", True, game_over_mssg
        )
        self.display.blit(line1, (200, 300))
        line2 = font.render(
            "To play again press Enter. To exit press Esc!", True, game_over_mssg
        )
        self.display.blit(line2, (200, 350))
        pg.display.flip()

    # increase snake speed after eating apple
    def Increase_speed(self):
        if self.is_collision:
            self.speed -= 0.009

    def run(self):
        game_running = True
        game_pause = False

        while game_running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_running = False

                    if event.key == K_RETURN:
                        game_pause = False

                    if not game_pause:
                        if event.key == pg.K_UP or event.key == pg.K_w:
                            self.snake.changed_direction = "UP"
                            self.snake.check_if_two_keys_pressed(
                                self.snake.changed_direction
                            )

                        if event.key == pg.K_DOWN or event.key == pg.K_s:
                            self.snake.changed_direction = "DOWN"
                            self.snake.check_if_two_keys_pressed(
                                self.snake.changed_direction
                            )

                        if event.key == pg.K_LEFT or event.key == pg.K_a:
                            self.snake.changed_direction = "LEFT"
                            self.snake.check_if_two_keys_pressed(
                                self.snake.changed_direction
                            )

                        if event.key == pg.K_RIGHT or event.key == pg.K_d:
                            self.snake.changed_direction = "RIGHT"
                            self.snake.check_if_two_keys_pressed(
                                self.snake.changed_direction
                            )

                elif event.type == QUIT:
                    game_running = False

            try:
                if not game_pause:
                    self.play()
            except Exception as e:
                self.game_over_screen()
                game_pause = True
                self.reset()

            tm.sleep(self.speed)


if __name__ == "__main__":
    game = snake_game()
    game.run()
