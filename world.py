import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA


class World:
    level: int
    """Номер уровня"""
    game_speed: float
    """Сложность"""
    health: int
    """Здоровье"""
    money: int
    """Деньги"""
    tile_map: list
    """Список мест, на которые можно установить турель"""
    waypoints: list
    """Список точек пути"""
    level_data: None
    """Данные уровня"""
    image: pg.surface.Surface
    """Изображение карты"""
    enemy_list: list
    """Список врагов"""
    spawned_enemies: int
    """Кол-во врагов на карте"""
    killed_enemies: int
    """Кол-во убитых врагов"""
    missed_enemies: int
    """Кол-во пропущенных врагов"""

    def __init__(self, data: dict, map_image: pg.surface.Surface):
        """ Конструктор уровня - его соствляющие """
        self.level = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        """Извлечение информации из соответствующих данных"""
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data: list[dict]) -> None:
        """Составление пути из точек координат"""
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        """Спавн врагов"""
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def is_level_complete(self) -> bool:
        """Проверка завершён ли уровень"""
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True
        return False

    def reset_level(self):
        """Сброс уровня"""
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface: pg.surface.Surface) -> None:
        """Отрисовка карты"""
        surface.blit(self.image, (0, 0))
