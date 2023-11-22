import random
import pygame as pg
from layoutlib.resources import Resources
from layoutlib.utility import xIntersection
from ElementaryBody import Body
from config import *
from player_data import load_player_name, save_player_name
from database import send_score_to_website


class Core(object):
    def __init__(self):
        self.left = self.right = False
        self.screen = pg.display.get_surface()
        self.boundary = self.screen.get_rect()
        self.gameDone = False
        self.restart = False
        self.clock = pg.time.Clock()
        self.dt = 0.05
        self.fps = 0.0
        self.res = None
        self.snd = list()

    def build_level(self):

        # There are 7 levels, reset to the first level if level exceeds 7
        self.level %= 7

        # Get configuration of current level
        level_config = self.levels[self.level]['cnf']
        this_level_map = self.levels[self.level]['map']
        start_x, start_y = level_config[0:2]  # Start positions of the first brick
        this_thickness = level_config[2]  # Thickness of drawable stuff
        this_pad_w = level_config[3]  # Paddle width
        this_pad_vel = level_config[4]  # Paddle velocity
        this_ball_vel = level_config[5]  # Ball velocity
        self.level_title = level_config[6]  # Level title

        # Create the pad
        for i in range(PAD_SIZE):
            x_pos = self.boundary.w / 2 - (PAD_W / 2)
            y_pos = self.boundary.h - (PAD_H + 5)
            self.pad.append(Body(TYPE_PADDLE, x_pos, y_pos, BALL_COL))
            self.pad[i].Shape.w = this_pad_w
            self.pad[i].thickness = this_thickness
            self.pad[i].xvel = this_pad_vel

        # Create the ball and start it from the center of the pad
        for i in range(BALL_SIZE):
            x_pos = self.pad[0].Shape.x + (PAD_W / 2)
            y_pos = self.pad[0].Shape.y - (CIRCLE_RADIUS + 1)
            self.ball.append(Body(TYPE_CIRCLE, x_pos, y_pos, BALL_COL))
            self.ball[i].xvel = self.ball[i].yvel = -this_ball_vel
            self.ball[i].thickness = this_thickness

        # Build the level by creating bricks
        x_pos = start_x
        y_pos = start_y
        i = 0
        for row in this_level_map:
            for brick in row:
                if brick == 'n':  # Normal brick
                    self.color = NORMAL_BRICK
                elif brick == 's':  # Solid brick
                    self.color = SOLID_BRICK
                elif brick == 'r':  # Rock brick
                    self.color = ROCK_BRICK
                elif brick == 'b':  # Bonus brick
                    self.color = BONUS_BRICK
                elif brick == ' ':  # Empty space
                    x_pos += BRICK_W + 3
                    continue
                self.bricks.append(Body(TYPE_BRICK, x_pos, y_pos, self.color))
                self.bricks[i].thickness = this_thickness
                i += 1
                x_pos += BRICK_W + 3
            y_pos += BRICK_H + 1
            x_pos = start_x

    def key_up(self, key):

        if key == pg.K_LEFT:
            self.left = False
        elif key == pg.K_RIGHT:
            self.right = False
        elif key == pg.K_SPACE:
            self.restart = False
        elif key == pg.K_ESCAPE:
            self.gameDone = True

    def key_down(self, key):

        if key == pg.K_LEFT:
            self.left = True
        elif key == pg.K_RIGHT:
            self.right = True
        elif key == pg.K_SPACE:
            if not self.gameOver:
                self.restart = True
        elif key == pg.K_RETURN:
            if self.gameOver:
                self.new_game()

    def event_listener(self):

        ev = pg.event.poll()
        if ev.type == pg.QUIT:
            self.gameDone = True
        elif ev.type == pg.KEYDOWN:
            self.key_down(ev.key)
        elif ev.type == pg.KEYUP:
            self.key_up(ev.key)

    def new_game(self):

        self.lives = 3
        self.score = 0
        self.gameOver = False
        self.level = 0
        self.gameDone = False
        self.restart = False
        self.next_level()  # Go to level 1

    def next_level(self):

        self.pad = []
        self.ball = []
        self.bricks = []

        # Create bricks for the next level
        self.build_level()

        # Prepare next level
        self.level += 1

        # Play random background music
        this_music = random.choice(self.music_titles)
        pg.mixer.music.load(this_music)
        pg.mixer.music.play()

    def draw(self):

        if not self.gameOver:
            self.screen.fill(BACK_COL)

            # Draw the pad list
            for pd in self.pad:
                pd.draw()

            # Draw the ball list
            for bl in self.ball:
                bl.draw()

            # Draw the bricks list
            for br in self.bricks:
                br.draw()
        else:  # Game over
            self.screen.fill(WHITE)
            self.res.print_font(self.fnt[2], 'Game is over now want a second try ? ', (260, 250), DARK)
            self.res.print_font(self.fnt[1], 'press Enter to play', (440, 500), DARK)

        # Draw all text elements
        self.res.print_font(self.fnt[0], str("{0:.2f} FPS".format(self.fps)), (1005, 2), DARK)
        self.res.print_font(self.fnt[0], self.level_title, (5, 2), DARK)
        self.res.print_font(self.fnt[0], str("{} X Points".format(self.score)), (560, 2), DARK)
        self.res.print_font(self.fnt[0], str("{} X Balls".format(self.lives)), (465, 2), DARK)

        pg.display.update()

    def update(self, dt):

        if not self.gameOver:
            # Update the pad
            for pd in self.pad:
                pd.side = int(self.right) - int(self.left)
                pd.update(dt)

            # Update ball/bricks
            for bl in self.ball:
                if bl.alive:
                    if bl.Ypos > self.boundary.h:
                        self.death(bl)
                        break

                    for pd in self.pad:
                        # Check for ball/pad collision
                        if pd.Shape.colliderect(bl.Shape):
                            bl.yvel *= -1
                            bl.Ypos = pd.Shape.y - (bl.Shape.h + 1)
                            self.snd[0].play()

                    for br in self.bricks:
                        # Check for ball/bricks collision and update state
                        if br.Shape.colliderect(bl.Shape):
                            bl.yvel *= -1
                            if xIntersection(bl.Shape, br.Shape):
                                bl.xvel *= -1
                            bl.angle = random.uniform(MIN_ANGLE, MAX_ANGLE)
                            self.snd[random.randint(1, 6)].play()
                            # Check brick type
                            self.kill_bricks_type(br)
                            self.score += 1

                else:
                    # Ball has fallen down, reset it if game is not over
                    bl.Xpos = pd.Xpos + pd.Shape.w / 2
                    bl.Ypos = pd.Ypos - (bl.Shape.w + 1)
                    bl.alive = self.restart

                bl.update(dt)

            # Check for win and proceed to next level
            if not self.bricks:
                self.snd[8].play()
                self.next_level()

    def kill_bricks_type(self, brick):

        if brick.duration > 0:
            if brick.color is NORMAL_BRICK:
                brick.alive = False
            elif brick.color is SOLID_BRICK:
                brick.color = NORMAL_BRICK
            elif brick.color is ROCK_BRICK:
                brick.color = SOLID_BRICK
            elif brick.color is BONUS_BRICK:
                brick.alive = False
                self.snd[7].play()
                self.lives += 1

            brick.duration -= 1

        self.bricks = [br for br in self.bricks if br.alive]

    def death(self, body):

        if not self.lives:
            self.gameOver = True
        else:
            self.lives -= 1
            body.alive = False

    def load_game(self, dataFolder, persistenceLayer):

        self.res = Resources(dataFolder)
        data = self.res.get_res_info(persistenceLayer)
        self.img = self.res.load_img_list(data['imgList'])
        self.snd = self.res.load_snd_list(data['sndList'])
        self.fnt = self.res.load_fnt_list(data['fntList'])
        self.music_titles = self.res.get_music_list(data['mscList'])
        print(self.res.__dict__)

    def load_levels(self, dataFolder, fileLevels):

        res = Resources(dataFolder)
        self.levels = res.get_res_info(fileLevels)
        del res

    def destroy_game(self):
        print('Destroying game')

        try :
            if self.img:
                del self.img
            if self.snd:
                del self.snd
            if self.fnt:
                del self.fnt
            if self.res:
                del self.res
        except Exception as e:
            pass

    def main_loop(self):

        self.new_game()

        while not self.gameDone:
            self.event_listener()
            self.update(self.dt)
            self.draw()
            self.clock.tick(DEFAULT_FPS)
            self.fps = self.clock.get_fps()

        self.destroy_game()
        return self.score


