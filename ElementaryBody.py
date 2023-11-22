from math import cos, sin
from random import uniform
import pygame as pg
from config import *

class Body:
    def __init__(self, type, x, y, color=WHITE):
        self.type = type
        self.Xpos, self.Ypos = x, y
        self.color = color
        self.thickness = 0
        self.screen = pg.display.get_surface()
        self.boundary = self.screen.get_rect()

        if self.type == TYPE_CIRCLE:
            self.init_circle()
        elif self.type == TYPE_PADDLE:
            self.init_paddle()
        elif self.type == TYPE_BRICK:
            self.init_brick()

    def init_circle(self):
        # Initialize properties for a circle body
        self.alive = False
        self.radius = CIRCLE_RADIUS
        self.Shape = pg.Rect(self.Xpos, self.Ypos, CIRCLE_RADIUS, CIRCLE_RADIUS)
        self.angle = MAX_ANGLE
        self.xvel = self.yvel = -CIRCLE_VEL

    def init_paddle(self):
        # Initialize properties for a paddle body
        self.Shape = pg.Rect(self.Xpos, self.Ypos, PAD_W, PAD_H)
        self.xvel = PADDLE_VEL
        self.side = 0

    def init_brick(self):
        # Initialize properties for a brick body
        self.Shape = pg.Rect(self.Xpos, self.Ypos, BRICK_W, BRICK_H)
        self.alive = True

        if self.color == NORMAL_BRICK:
            self.duration = 1
        elif self.color == SOLID_BRICK:
            self.duration = 2
        elif self.color == ROCK_BRICK:
            self.duration = 3
        elif self.color == BONUS_BRICK:
            self.duration = 1

    def draw(self):
        # Draw the body object on the screen
        if self.type == TYPE_CIRCLE:
            pg.draw.circle(self.screen, self.color, (self.Shape.x, self.Shape.y), self.radius, self.thickness)
        else:
            pg.draw.rect(self.screen, self.color, self.Shape, self.thickness)

    def update(self, dt):
        # Update the position of the body object
        if self.type == TYPE_CIRCLE:
            self.update_circle(dt)
        elif self.type == TYPE_PADDLE:
            self.update_paddle(dt)

    def update_circle(self, dt):
        # Update the position of a circle body
        self.Xpos += self.xvel * cos(self.angle) * dt
        self.Ypos += self.yvel * sin(self.angle) * dt

        if self.collide_x():
            self.xvel *= -1

        if self.collide_y() == 1:
            self.angle = uniform(MIN_ANGLE, MAX_ANGLE + 0.02)
            self.yvel *= -1

        self.Shape.x = int(self.Xpos)
        self.Shape.y = int(self.Ypos)

    def update_paddle(self, dt):
        # Update the position of a paddle body
        self.Xpos += self.side * self.xvel * dt
        self.collide_x()
        self.Shape.x = int(self.Xpos)

    def collide_x(self):
        # Check for collisions with the horizontal boundaries
        if self.Xpos <= 0:
            self.Xpos = 1.0
            return True
        elif self.Xpos + self.Shape.w >= self.boundary.w:
            self.Xpos = self.boundary.w - (self.Shape.w + 1)
            return True

    def collide_y(self):
        # Check for collisions with the vertical boundaries
        if self.Ypos <= 0:
            self.Ypos = 1.0
            return 1
        elif self.Ypos + self.Shape.h >= self.boundary.h:
            return 2

