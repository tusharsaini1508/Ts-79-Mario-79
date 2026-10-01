import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

from types import SimpleNamespace
import unittest

import pygame as pg

from source import constants as c
from source.components.info import Info
from source.states.level import Level
from source.states.load_screen import GameComplete


class FinalLevelTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()

    @staticmethod
    def make_completed_level(level_number):
        level = Level.__new__(Level)
        level.player = SimpleNamespace(dead=False)
        level.persist = {c.LIVES: 3, c.LEVEL_NUM: level_number}
        level.game_info = level.persist
        level.overhead_info = SimpleNamespace(time=c.GAME_TIME_OUT)
        return level

    def test_nonfinal_level_advances(self):
        level = self.make_completed_level(c.LEVEL_COUNT - 1)

        level.update_game_info()

        self.assertEqual(level.next, c.LOAD_SCREEN)
        self.assertEqual(level.game_info[c.LEVEL_NUM], c.LEVEL_COUNT)

    def test_final_level_enters_win_screen_without_incrementing(self):
        level = self.make_completed_level(c.LEVEL_COUNT)

        level.update_game_info()

        self.assertEqual(level.next, c.GAME_COMPLETE)
        self.assertEqual(level.game_info[c.LEVEL_NUM], c.LEVEL_COUNT)
        complete = GameComplete()
        self.assertEqual(complete.set_next_state(), c.MAIN_MENU)
        self.assertEqual(complete.set_info_state(), c.GAME_COMPLETE)

    def test_win_screen_displays_victory_label(self):
        info = Info.__new__(Info)
        info.image_dict = {
            character: pg.Surface((7, 7))
            for character in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'
        }
        info.info_labels = []

        info.create_game_complete_labels()

        label = info.state_labels[0]
        rendered = ''.join(
            next(character for character, image in info.image_dict.items()
                 if item.image is image)
            for item in label
        )
        self.assertEqual(rendered, 'YOU WIN')