# Developer - Bad 6666

import pygame as pg

class Enemy(pg.sprite.Sprite):
  def __init__(self, pos, image):
    pg.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.center = pos

  def update(self):
    self.move()

  def move(self):
    self.rect.x += 1


class Swordsmen:
    def __init__(self, x, y):
        self.x = x #получаем данные от карты
        self.y = y #получаем данные от карты
        self.hp = 30
        self.image = pg.image.load("swordsman.png")
        self.speed = 4
        self.damage = 3
        self.distance = 1
        self.rect = pg.Rect()
        self.rect.center = self.image.get_center()
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.hit_sound = pg.mixer.Sound("hit.mp3")
        self.hit_sound.set_volume(0.4)


class Archer:
    def __init__(self, x, y):
        self.x = x #получаем данные от карты
        self.y = y #получаем данные от карты
        self.hp = 20
        self.image = pg.image.load("archer.png")
        self.speed = 5
        self.damage = 2
        self.distance = 6
        self.rect = pg.Rect()
        self.rect.center = self.image.get_center()
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.hit_sound = pg.mixer.Sound("hitarrow.mp3")
        self.hit_sound.set_volume(0.5)


class HeavySwordsmen:
    def __init__(self, x, y):
        self.x = x #получаем данные от карты
        self.y = y #получаем данные от карты
        self.hp = 60
        self.image = pg.image.load("heavyswordsman.png")
        self.speed = 2
        self.damage = 5
        self.distance = 1
        self.rect = pg.Rect()
        self.rect.center = self.image.get_center()
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.hit_sound = pg.mixer.Sound("hit.mp3")
        self.hit_sound.set_volume(0.4)

  class Cavalery:
    def __init__(self, x, y):
        self.x = x #получаем данные от карты
        self.y = y #получаем данные от карты
        self.hp = 20
        self.image = pg.image.load("cavalery.png")
        self.speed = 10
        self.damage = 3
        self.distance = 2
        self.rect = pg.Rect()
        self.rect.center = self.image.get_center()
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.hit_sound = pg.mixer.Sound("horse.mp3")
        self.hit_sound.set_volume(0.6)
