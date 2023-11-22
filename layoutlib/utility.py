import math
import pygame as pg

#calculate the distance between two points using the formula
def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


# give the result of conversion from radians to degrees
def rad2deg(rad):
    return math.degrees(rad)

# give the result of conversion from degress to radians
def deg2rad(deg):
    return math.radians(deg)

# Rotate a point (x, y) around the origin (0, 0) by the specified angle
def rotate(x, y, angle):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle
    return new_x, new_y

# Rotate a point (x1, y1) around a given point (x0, y0) by the specified angle
def rotate2p(x1, y1, x0, y0, angle):
    dx = x1 - x0
    dy = y1 - y0
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_dx = dx * cos_angle - dy * sin_angle
    new_dy = dx * sin_angle + dy * cos_angle
    new_x = new_dx + x0
    new_y = new_dy + y0
    return new_x, new_y

# Get the current time in milliseconds or seconds
def getTime(type='ms'):
    ticks = pg.time.get_ticks()
    if type == 's':
        return ticks / 1000.0
    else:
        return ticks

# Rotate an image by the specified angle while keeping its center and size
def rotateDeg(image, angle):
    angle %= 360.0
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    orig_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(orig_rect).copy()
    return rot_image

# Check if two bodies intersect along the x-axis
def xIntersection(body1, body2):
    return (body1.x + body1.w) < (body2.x + body2.w) * 0.5 or \
           (body1.x + body1.w) >= (body2.x + body2.w) * 0.5
# Check if two bodies intersect along the y-axis
def yIntersection(body1, body2):
    return (body1.y + body1.h) < (body2.y + body2.h) or \
           (body1.y + body1.h) >= (body2.y + body2.h)






























