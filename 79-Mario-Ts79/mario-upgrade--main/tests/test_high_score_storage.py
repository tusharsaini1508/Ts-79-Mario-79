import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import pygame as pg

from source import constants as c
from source.high_score import load_high_score, save_high_score
from source.states.level import Level


class HighScoreStorageTests(unittest.TestCase):
    def test_missing_or_invalid_score_file_returns_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            score_path = Path(directory) / 'nested' / 'high_score.json'
            self.assertEqual(load_high_score(score_path), 0)

            score_path.parent.mkdir(parents=True)
            score_path.write_text('{', encoding='utf-8')
            self.assertEqual(load_high_score(score_path), 0)

            score_path.write_text(json.dumps({'top_score': -1}), encoding='utf-8')
            self.assertEqual(load_high_score(score_path), 0)

    def test_save_creates_directory_and_loads_record(self):
        with tempfile.TemporaryDirectory() as directory:
            score_path = Path(directory) / 'profile' / 'high_score.json'

            self.assertTrue(save_high_score(1200, score_path))
            self.assertEqual(load_high_score(score_path), 1200)
            self.assertEqual(json.loads(score_path.read_text(encoding='utf-8')),
                             {'top_score': 1200})

    def test_score_updates_persist_only_new_records(self):
        level = Level.__new__(Level)
        level.game_info = {c.SCORE: 0, c.TOP_SCORE: 100, c.COIN_TOTAL: 0}
        level.moving_score_list = []
        sprite = SimpleNamespace(rect=pg.Rect(10, 20, 1, 1))

        with patch('source.states.level.stuff.Score', return_value=object()), \
             patch('source.states.level.save_high_score') as save_score:
            level.update_score(50, sprite)
            save_score.assert_not_called()
            level.update_score(100, sprite)

        self.assertEqual(level.game_info[c.TOP_SCORE], 150)
        save_score.assert_called_once_with(150)


if __name__ == '__main__':
    unittest.main()
