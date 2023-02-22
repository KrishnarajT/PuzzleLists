# Creating Tetris. The aim of this is to make a simple Tetris game using pygame. That we can then later integrate to our Puzzlelist Arcades.

import sys
from settings import *
from tetris import Tetris
import pathlib

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("TETRIS - From the Puzzlelist")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.running = True
        self.tetris = Tetris(self)
        
    
    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob("*.png") if item.is_file()]
        images = [pg.image.load(filename).convert_alpha() for filename in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images


    def set_timer(self):
        # normal
        self.user_event = pg.USEREVENT + 0
        self.anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)

        # fast
        self.fast_user_event = pg.USEREVENT + 1
        self.fast_anim_trigger = False
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.tetris.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.running = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
                
            # gets triggered by our timer we created above in set_timer()
            elif event.type == self.user_event:
                self.anim_trigger = True
                
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True    
            
            elif event.type == pg.KEYUP:
                if(event.key == pg.K_DOWN or event.key == pg.K_s):
                    self.tetris.speed_up = False

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
