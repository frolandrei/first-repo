import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        """путевые точки"""
        self.pos = Vector2(self.waypoints[0])
        """позиция"""

        self.target_waypoint = 1
        """установка путевой точки 1(отправления)"""

        self.health = ENEMY_DATA.get(enemy_type)["health"]
        """здоровье врага"""

        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        """скорость врага"""
        self.angle = 0

        self.original_image = images.get(enemy_type)
        """создание картинки врага"""
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.target = Vector2(0, 0)
        self.movement = Vector2(0, 0)


    def update(self, world):
        """усложение врага обновление"""
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        # define a target waypoint
        """движение врага"""
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:

            # enemy has reached the end of the path
            self.kill()
            """также смерть врага"""
            world.health -= 1
            world.missed_enemies += 1

        # calculate distance to target

        dist = self.movement.length()
        # check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1



def rotate(self):
    """поворот врага"""
    # calculate distance to next waypoint
    dist = self.target - self.pos
    # use distance to calculate angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    # rotate image and update rectangle
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos


def check_alive(self, world):
    """ жив ли враг?"""
    if self.health <= 0:
        world.killed_enemies += 1
        world.money += c.KILL_REWARD
        """ прибавление  наград за смерть врага"""
        self.kill()
