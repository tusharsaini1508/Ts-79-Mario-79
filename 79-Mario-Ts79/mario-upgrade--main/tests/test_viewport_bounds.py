import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import unittest

import pygame as pg

from source.states.level import Level


class ViewportBoundsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()

    @staticmethod
    def make_level(viewport_x, start_x, end_x, player_center, velocity):
        level = Level.__new__(Level)
        level.start_x = start_x
        level.end_x = end_x
        level.viewport = pg.Rect(viewport_x, 0, 800, 600)
        level.player = type('Player', (), {})()
        level.player.x_vel = velocity
        level.player.rect = pg.Rect(player_center - 10, 0, 20, 20)
        return level

    def test_leftward_camera_step_stops_at_level_start(self):
        level = self.make_level(102, 100, 3000, 150, -5)

        level.update_viewport()

        self.assertEqual(level.viewport.x, level.start_x)

    def test_rightward_camera_step_stops_at_final_view(self):
        level = self.make_level(1249, 0, 2050, 1540, 5)

        level.update_viewport()

        self.assertEqual(level.viewport.x, 1250)
        self.assertEqual(level.viewport.right, level.end_x)
