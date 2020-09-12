#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from src.mino import TetroMino, TetroMinoColor, DroppingMino, Direction, Field


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

        mino = TetroMino.T
        shape = \
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))

        mino = TetroMino.L
        shape = \
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))

        mino = TetroMino.J
        shape = \
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))

        mino = TetroMino.Z
        shape = \
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))

        mino = TetroMino.S
        shape = \
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]]
        desired_shape = np.array(shape, dtype=bool)
        self.assertTrue(np.allclose(mino.get_shape(), desired_shape))


class TestTetroMinoColor(unittest.TestCase):
    def test_color(self):
        self.assertEqual(TetroMinoColor.YELLOW.rend_RGB(), 0xFFFF00)
        self.assertEqual(TetroMinoColor.LIGHTBLUE.rend_RGB(), 0x00FFFF)
        self.assertEqual(TetroMinoColor.PURPLE.rend_RGB(), 0x880088)
        self.assertEqual(TetroMinoColor.ORANGE.rend_RGB(), 0xFFAA00)
        self.assertEqual(TetroMinoColor.DARKBLUE.rend_RGB(), 0x0000FF)
        self.assertEqual(TetroMinoColor.GREEN.rend_RGB(), 0x00FF00)
        self.assertEqual(TetroMinoColor.RED.rend_RGB(), 0xFF0000)
        self.assertEqual(TetroMinoColor.WHITE.rend_RGB(), 0xFFFFFF)


class TestDroppingMino(unittest.TestCase):
    def test_spin(self):
        dropping_mino = DroppingMino(TetroMino.T)
        field = Field()
        dropping_mino.spin_clockwise(field)
        self.assertEqual(dropping_mino.direction, Direction.EAST)

        dropping_mino.spin_anticlockwise(field)
        self.assertEqual(dropping_mino.direction, Direction.NORTH)

    def test_valid_place(self):
        dropping_mino = DroppingMino(TetroMino.Z)
        field = Field()
        field.set_default()
        # field.print_field()

        dropping_mino.position = (0, -1)  # 左端が範囲外
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.position = (0, 8)  # 右端が範囲外
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.position = (0, 7)  # 右端がギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (14, 4)  # 右下が重なる
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.position = (14, 3)  # うまく重ならないようになってる
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (15, 3)  # 左上が重なる
        self.assertFalse(dropping_mino.valid_place(field))

    def test_rend_mino(self):
        dropping_mino = DroppingMino(TetroMino.S)
        field = Field()
        dropping_mino.spin_clockwise(field)
        desired_shape = np.array(
            [[0, 1, 0],
             [0, 1, 1],
             [0, 0, 1]], dtype=bool)
        self.assertTrue(np.allclose(dropping_mino.rend_mino(), desired_shape))

        dropping_mino.spin_anticlockwise(field)
        dropping_mino.spin_anticlockwise(field)
        desired_shape = np.array(
            [[1, 0, 0],
             [1, 1, 0],
             [0, 1, 0]], dtype=bool)
        self.assertTrue(np.allclose(dropping_mino.rend_mino(), desired_shape))

    def test_move_mino(self):
        dropping_mino = DroppingMino(TetroMino.I)
        field = Field()
        dropping_mino.move_mino(1, 0, field)  # move down
        self.assertEqual(dropping_mino.position, (1, 4))
        dropping_mino.move_mino(0, 1, field)  # move right
        self.assertEqual(dropping_mino.position, (1, 5))
        dropping_mino.move_mino(0, -1, field)  # move left
        self.assertEqual(dropping_mino.position, (1, 4))


if __name__ == '__main__':
    unittest.main()
