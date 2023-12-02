from button import Button
from enemy import Enemy
from turret import Turret
from world import World
import pygame as pg
import constants as c

class Game:
    def __init__(self):
        # create clock
        self.clock = pg.time.Clock()

        # create game window
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.display.set_caption("Tower Defence")


    def setup(self):
        # game variables
        self.game_over = False
        self.game_outcome = 0  # -1 is loss & 1 is won
        self.level_started = False
        self.last_enemy_spawn = pg.time.get_ticks()
        self.placing_turrets = False
        self.selected_turret = None
        self.is_running = False

        # create world
        self.world = World(world_data, map_image)
        self.world.process_data()
        self.world.process_enemies()

        # create groups
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()

        # create buttons // TODO: В отдельное хранилище
        self.turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
        self.upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
        self.begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
        self.restart_button = Button(310, 300, restart_image, True)
        self.fast_forward_button = Button(c.SCREEN_WIDTH + 50, 300, fast_forward_image, False)

    # function for outputting text onto the screen
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def display_data(self):
        # draw panel
        pg.draw.rect(self.screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.draw.rect(self.screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
        self.screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
        # display data
        self.draw_text("LEVEL: " + str(self.world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
        self.screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35))
        self.draw_text(str(self.world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
        self.screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65))
        self.draw_text(str(self.world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        # calculate the sequential number of the tile
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        # check if that tile is grass
        if self.world.tile_map[mouse_tile_num] == 7:
            # check that there isn't already a turret there
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
            # if it is a free space then create turret
            if space_is_free:
                new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
                self.turret_group.add(new_turret)
                # deduct cost of turret
                self.world.money -= c.BUY_COST

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False

    def update_all(self):
        """
        Обновление всех компонентов
        :return:
        """
        if not self.game_over:
            # check if player has lost
            if self.world.health <= 0:
                self.game_over = True
                self.game_outcome = -1  # loss
            # check if player has won
            if self.world.level > c.TOTAL_LEVELS:
                self.game_over = True
                self.game_outcome = 1  # win

            # update groups
            self.enemy_group.update(self.world)
            self.turret_group.update(self.enemy_group, self.world)

            # highlight selected turret
            if self.selected_turret:
                self.selected_turret.selected = True

    def draw_all(self):
        #########################
        # DRAWING SECTION
        #########################
        world = self.world
        screen = self.screen

        # draw level
        world.draw(screen)

        # draw groups
        self.enemy_group.draw(screen)
        for turret in self.turret_group:
            turret.draw(screen)

        self.display_data()

        if not self.game_over:
            # check if the level has been started or not
            if not self.level_started:
                if self.begin_button.draw(screen):
                    self.level_started = True
            else:
                # fast forward option
                world.game_speed = 1
                if self.fast_forward_button.draw(screen):
                    world.game_speed = 2
                # spawn enemies
                if pg.time.get_ticks() - self.last_enemy_spawn > c.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        self.enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        self.last_enemy_spawn = pg.time.get_ticks()

            # check if the wave is finished
            if world.is_level_complete():
                world.money += c.LEVEL_COMPLETE_REWARD
                world.level += 1
                self.level_started = False
                self.last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()

            # draw buttons
            # button for placing turrets
            # for the "turret button" show cost of turret and draw the button
            self.draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
            screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))
            if self.turret_button.draw(screen):
                self.placing_turrets = True
            # if placing turrets then show the cancel button as well
            if self.placing_turrets:
                # show cursor turret
                cursor_rect = cursor_turret.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= c.SCREEN_WIDTH:
                    screen.blit(cursor_turret, cursor_rect)
                if self.cancel_button.draw(screen):
                    self.placing_turrets = False
            # if a turret is selected then show the upgrade button
            if self.selected_turret:
                # if a turret can be upgraded then show the upgrade button
                if self.selected_turret.upgrade_level < c.TURRET_LEVELS:
                    # show cost of upgrade and draw the button
                    self.draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
                    screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
                    if self.upgrade_button.draw(screen):
                        if world.money >= c.UPGRADE_COST:
                            self.selected_turret.upgrade()
                            world.money -= c.UPGRADE_COST
        else:
            pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
            if self.game_outcome == -1:
                self.draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif self.game_outcome == 1:
                self.draw_text("YOU WIN!", large_font, "grey0", 315, 230)
            # restart level
            if self.restart_button.draw(screen):
                self.game_over = False
                self.level_started = False
                self.placing_turrets = False
                self.selected_turret = None
                self.last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                # empty groups
                self.enemy_group.empty()
                self.turret_group.empty()

    def process_events(self):
        # event handler
        for event in pg.event.get():
            # quit program
            if event.type == pg.QUIT:
                self.is_running = False
            # mouse click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                # check if mouse is on the game area
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    # clear selected turrets
                    self.selected_turret = None
                    self.clear_selection()
                    if self.placing_turrets:
                        # check if there is enough money for a turret
                        if self.world.money >= c.BUY_COST:
                            self.create_turret(mouse_pos)
                    else:
                        self.selected_turret = self.select_turret(mouse_pos)

    def run(self):
        # game loop
        self.is_running = True
        while self.is_running:
            self.clock.tick(c.FPS)

            self.update_all()
            self.draw_all()
            self.process_events()

            # update display
            pg.display.flip()


if __name__ == "__main__":
    # initialise pygame
    pg.init()
    game = Game()
    from resources import *
    game.setup()
    game.run()
    pg.quit()
