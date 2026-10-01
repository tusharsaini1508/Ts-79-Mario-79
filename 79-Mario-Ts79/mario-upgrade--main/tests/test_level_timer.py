import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

from types import SimpleNamespace
import unittest

import pygame as pg

from source import constants as c
from source.components.info import Character, Info


class LevelTimerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()

    def make_info(self, start_time):
        info = Info.__new__(Info)
        info.image_dict = {
            character: pg.Surface((7, 7))
            for character in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'
        }
        info.state = c.LEVEL
        info.game_info = {c.CURRENT_TIME: start_time}
        info.create_info_labels()
        info.create_level_labels()
        info.flashing_coin = SimpleNamespace(update=lambda current_time: None)
        return info

    @staticmethod
    def level_info(current_time):
        return {
            c.SCORE: 0,
            c.COIN_TOTAL: 0,
            c.LEVEL_NUM: 1,
            c.CURRENT_TIME: current_time,
        }

    def test_timer_starts_at_level_entry_time(self):
        info = self.make_info(5000)

        info.handle_level_state(self.level_info(5000))

        self.assertEqual(info.time, c.GAME_TIME_OUT)
        self.assertEqual(info.current_time, 5000)

    def test_timer_catches_up_and_clears_digits_at_zero(self):
        info = self.make_info(5000)

        info.handle_level_state(self.level_info(7500))
        self.assertEqual(info.time, c.GAME_TIME_OUT - 2)
        self.assertEqual(info.current_time, 7000)

        info.handle_level_state(self.level_info(7050))
        self.assertEqual(info.time, c.GAME_TIME_OUT - 2)
        self.assertEqual(info.current_time, 7000)

        info.handle_level_state(self.level_info(400000))
        self.assertEqual(info.time, 0)
        self.assertEqual(len(info.clock_time_label), 1)
        zero = info.clock_time_label[0]
        self.assertIs(zero.image, info.image_dict['0'])
