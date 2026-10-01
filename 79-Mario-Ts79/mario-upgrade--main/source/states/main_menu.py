"""
MIT License

Copyright (c) 2025 Tushar Saini 79

Developed by Tushar Saini, Computer Science Engineering student at Vaish College of Engineering, Rohtak, Haryana, India. 
This software project was created as a part of personal learning, open-source contribution, and portfolio development. 
For inquiries or collaborations, feel free to reach out via social media or email.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice, this permission notice, and the author details 
shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

__author__ = 'Tushar Saini 79'

import pygame as pg
from .. import tools
from .. import setup
from .. import constants as c
from .. components import info
from ..high_score import load_high_score

# Class representing the main menu of the game
class Menu(tools.State):
    def __init__(self):
        tools.State.__init__(self)
        # Initialize game information and state
        persist = {
            c.COIN_TOTAL: 0,
            c.SCORE: 0,
            c.LIVES: 3,
            c.TOP_SCORE: load_high_score(),
            c.CURRENT_TIME: 0.0,
            c.LEVEL_NUM: 1,
            c.PLAYER_NAME: c.PLAYER_MARIO
        }
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        # Initialize the menu state with the given game information
        self.next = c.LOAD_SCREEN
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.Info(self.game_info, c.MAIN_MENU)

        self.setup_background()
        self.setup_player()
        self.setup_cursor()

    def setup_background(self):
        # Set up the main menu background
        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(
            self.background,
            (int(self.background_rect.width * c.BACKGROUND_MULTIPLER),
            int(self.background_rect.height * c.BACKGROUND_MULTIPLER))
        )

        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)
        self.image_dict = {}
        image = tools.get_image(setup.GFX['title_screen'], 1, 60, 176, 88, (255, 0, 220), c.SIZE_MULTIPLIER)
        rect = image.get_rect()
        rect.x, rect.y = (170, 100)
        self.image_dict['GAME_NAME_BOX'] = (image, rect)

    def setup_player(self):
        # Set up the player character(s) on the main menu
        self.player_list = []
        player_rect_info = [(178, 32, 12, 16), (178, 128, 12, 16)]
        for rect in player_rect_info:
            image = tools.get_image(setup.GFX['mario_bros'], *rect, c.BLACK, 2.9)
            rect = image.get_rect()
            rect.x, rect.bottom = 110, c.GROUND_HEIGHT
            self.player_list.append((image, rect))
        self.player_index = 0

    def setup_cursor(self):
        # Set up the cursor for player selection in the main menu
        self.cursor = pg.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GFX[c.ITEM_SHEET], 24, 160, 8, 8, c.BLACK, 3)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (220, 358)
        self.cursor.rect = rect
        self.cursor.state = c.PLAYER1

    def update(self, surface, keys, current_time):
        # Update the main menu based on user input
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.player_image = self.player_list[self.player_index][0]
        self.player_rect = self.player_list[self.player_index][1]
        self.update_cursor(keys)
        self.overhead_info.update(self.game_info)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0], self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.player_image, self.player_rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)

    def update_cursor(self, keys):
        # Update the cursor position and player selection
        if self.cursor.state == c.PLAYER1:
            self.cursor.rect.y = 358
            if keys[pg.K_DOWN]:
                self.cursor.state = c.PLAYER2
                self.player_index = 1
                self.game_info[c.PLAYER_NAME] = c.PLAYER_LUIGI
        elif self.cursor.state == c.PLAYER2:
            self.cursor.rect.y = 403
            if keys[pg.K_UP]:
                self.cursor.state = c.PLAYER1
                self.player_index = 0
                self.game_info[c.PLAYER_NAME] = c.PLAYER_MARIO
        if keys[pg.K_RETURN]:
            self.reset_game_info()
            self.done = True

    def reset_game_info(self):
        # Reset game information to its initial state
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_NUM] = 1

        self.persist = self.game_info
