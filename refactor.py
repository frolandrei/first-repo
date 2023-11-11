import pygame as pg
from src.enemies import Enemy
from area import World
import constants as c

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#load images

# map
map_image = pg.image.load('resources/images/level.png').convert_alpha()

enemy_image = pg.image.load('resources/images/Enemy1.png').convert_alpha()

# create world
world = World(map_image)

#create groups
enemy_group = pg.sprite.Group()

waypoints = [
  (100, 100),
  (400, 200),
  (400, 100),
  (200, 300)
]

enemy = Enemy((200, 300), enemy_image)
enemy_group.add(enemy)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  screen.fill("grey100")

  # draw level
  world.draw(screen)

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False

  #update display
  pg.display.flip()

pg.quit()
