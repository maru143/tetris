#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest
import sys

from src.tetris import Tetris

class TestTetris(unittest.TestCase):
    def test_rend_field_color(self):
        # print("from test_tetris.TestTetris", file=sys.stderr)
        tetris = Tetris()
        tetris.field.set_default()
        # print(tetris.dropping_mino.mino, file=sys.stderr)
        field_color = tetris.rend_field_color()

if __name__ == '__main__':
    unittest.main()
