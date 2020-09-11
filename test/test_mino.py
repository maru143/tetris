#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from src.mino import TetroMino, TetroMinoColor, DroppingMino, Direction


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
        self.assertEqual(TetroMinoColor.ORANGE, 0xFFAA00)
        self.assertEqual(TetroMinoColor.DARKBLUE, 0x0000FF)


class TestDroppingMino(unittest.TestCase):
    def test_spin(self):
        dropping_mino = DroppingMino(TetroMino.T)
        dropping_mino.spin_clockwise()
        self.assertEqual(dropping_mino.direction, Direction.EAST)

        dropping_mino.spin_anticlockwise()
        self.assertEqual(dropping_mino.direction, Direction.NORTH)

    def test_valid_place(self):
        pass

    def test_rend_mino(self):
        dropping_mino = DroppingMino(TetroMino.S)
        dropping_mino.spin_clockwise()
        desired_shape = np.array(
            [[0, 1, 0],
             [0, 1, 1],
             [0, 0, 1]], dtype=bool)
        self.assertTrue(np.allclose(dropping_mino.rend_mino(), desired_shape))

        dropping_mino.spin_anticlockwise()
        dropping_mino.spin_anticlockwise()
        desired_shape = np.array(
            [[1, 0, 0],
             [1, 1, 0],
             [0, 1, 0]], dtype=bool)
        self.assertTrue(np.allclose(dropping_mino.rend_mino(), desired_shape))

    def test_move_mino(self):
        dropping_mino = DroppingMino(TetroMino.I)
        dropping_mino.move_mino(1, 0)  # move down
        self.assertEqual(dropping_mino.position, (1, 4))
        dropping_mino.move_mino(0, 1)  # move right
        self.assertEqual(dropping_mino.position, (1, 5))
        dropping_mino.move_mino(0, -1)  # move left
        self.assertEqual(dropping_mino.position, (1, 4))


if __name__ == '__main__':
    unittest.main()
