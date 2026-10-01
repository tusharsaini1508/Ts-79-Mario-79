import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import unittest

import pygame as pg

from source.tools import Control


class QuitShortcutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((1, 1))

    def setUp(self):
        pg.event.clear()

    def test_escape_key_exits_game(self):
        control = Control()
        pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE))

        control.event_loop()

        self.assertTrue(control.done)

    def test_window_close_still_exits_game(self):
        control = Control()
        pg.event.post(pg.event.Event(pg.QUIT))

        control.event_loop()

        self.assertTrue(control.done)