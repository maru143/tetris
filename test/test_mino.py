#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from src.mino import TetroMino, TetroMinoColor


class TestTetroMino(unittest.TestCase):
    def test_get_shape(self):
        mino = TetroMino.O
        shape = \
            [[1, 1],
             [1, 1]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))

        mino = TetroMino.I
        shape = \
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))


class TestTetroMinoColor(unittest.TestCase):
    def test_color(self):
        self.assertEqual(TetroMinoColor.ORANGE, 0xFFAA00)
        self.assertEqual(TetroMinoColor.DARKBLUE, 0x0000FF)


if __name__ == '__main__':
    unittest.main()
