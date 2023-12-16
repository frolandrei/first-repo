import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        """фиксация значений основных переменных, для даного файла"""

        # position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        """Координаты турелей(башень)"""
        # calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        """ Координаты центра башень путём вычисления"""
        # shot sound effect
        self.shot_fx = shot_fx
        """ Звуковой эффект выстрела"""

        # animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        """Пошаговый изменения картинки через анимацию"""
        # update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        """Обновление изображения турели"""

        # create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        """Создание не видимого круга, который будет означать зону досягаемости снарядов с нашей турели(башни)"""

    def load_images(self, sprite_sheet):
        # extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world):
        # if target picked, play firing animation
        if self.target:
            self.play_animation()
            """Если цель для атаки определена, то атаковать её"""
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)
                """Как только турель "остынет" (зависит от скорости атаки турели) искать новую цель"""

    def pick_target(self, enemy_group):
        # find an enemy to target
        # check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # damage enemy
                    self.target.health -= c.DAMAGE
                    # play sound effect
                    self.shot_fx.play()
                    break
                    """ Найти цель для снарядов турели, а так проверка досягаемости врагов для данных турелей"""

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        """обновление изображения"""
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            """Проверка, прошло ли время с момента последнего обновления картинки"""
            # check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                """Проверка, совершилось ли изменение картинки и если да, то даём ей статус ожидания"""
                # record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None
            """ Если цель в виде врага определена, чтобы произошло обновление картинки турели"""

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        # upgrade turret image
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        """обновление изображения турели"""

        # upgrade range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        """обновление круга досягаемости, путём проверки расположения, целей и других параметров"""

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
            """Разворот башни на определённый угол, учитывая наводку на врага"""
