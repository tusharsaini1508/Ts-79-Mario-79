import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import mock_open, patch

import pygame as pg

from source import constants as c
from source import setup
from source.components.info import Character, Info
from source.components.player import Player
from source.states.level import Level
from source.states.main_menu import Menu


class GameplayRegressionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()

    @staticmethod
    def make_image_dict():
        return {
            character: pg.Surface((7, 7))
            for character in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'
        }

    @staticmethod
    def rendered_text(info, characters):
        return ''.join(
            next(
                character
                for character, image in info.image_dict.items()
                if item.image is image
            )
            for item in characters
        )

    def test_hud_grows_to_show_large_scores(self):
        info = Info.__new__(Info)
        info.image_dict = self.make_image_dict()
        score_text = [Character(info.image_dict['0']) for _ in range(6)]
        for index, character in enumerate(score_text):
            character.rect.topleft = (75 + index * 10, 55)

        info.update_text(score_text, 1_000_000)

        self.assertEqual(self.rendered_text(info, score_text), '1000000')
        self.assertEqual([item.rect.x for item in score_text], list(range(65, 126, 10)))

    def test_high_score_tracks_maximum_and_appears_in_menu(self):
        level = Level.__new__(Level)
        level.game_info = {c.SCORE: 0, c.TOP_SCORE: 100, c.COIN_TOTAL: 0}
        level.moving_score_list = []
        sprite = SimpleNamespace(rect=pg.Rect(10, 20, 1, 1))

        with patch('source.states.level.stuff.Score', return_value=object()):
            level.update_score(50, sprite)
            level.update_score(200, sprite)

        self.assertEqual(level.game_info[c.TOP_SCORE], 250)
        info = Info.__new__(Info)
        info.image_dict = self.make_image_dict()
        info.state = c.MAIN_MENU
        info.create_info_labels()
        info.create_main_menu_labels()
        info.flashing_coin = SimpleNamespace(update=lambda current_time: None)
        info.handle_level_state({
            c.SCORE: level.game_info[c.SCORE],
            c.TOP_SCORE: level.game_info[c.TOP_SCORE],
            c.COIN_TOTAL: 0,
            c.LEVEL_NUM: 1,
            c.CURRENT_TIME: 0,
        })

        self.assertEqual(self.rendered_text(info, info.top_score_text), '000250')

    def test_second_menu_option_selects_luigi(self):
        menu = Menu()
        keys = type(
            'Keys', (), {'__getitem__': lambda self, key: key == pg.K_DOWN}
        )()

        menu.update_cursor(keys)

        self.assertEqual(menu.game_info[c.PLAYER_NAME], c.PLAYER_LUIGI)
        self.assertEqual(c.PLAYER2, 'LUIGI GAME')

    def test_game_data_loads_from_project_root(self):
        self.assertEqual(Path(setup.PROJECT_ROOT), Path(__file__).resolve().parents[1])

        level = Level.__new__(Level)
        level.game_info = {c.LEVEL_NUM: 1}
        level.load_map()
        self.assertIn(c.MAP_IMAGE, level.map_data)

        player = Player.__new__(Player)
        player.player_name = c.PLAYER_MARIO
        player_data_path = Path(setup.PROJECT_ROOT) / 'source' / 'data' / 'player' / 'mario.json'
        player_data_file = mock_open(read_data='{}')
        with patch('builtins.open', player_data_file):
            player.load_data()
        player_data_file.assert_called_once_with(str(player_data_path))
        self.assertEqual(player.player_data, {})