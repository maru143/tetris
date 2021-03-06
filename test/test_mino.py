#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from src.mino import TetroMino, TetroMinoColor, DroppingMino, Direction, \
    Field, TetroMinoGenerator


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


class TestDroppingMino(unittest.TestCase):
    def test_spin(self):
        field = Field()
        dropping_mino = DroppingMino(TetroMino.T, field)
        dropping_mino.spin_clockwise(field)
        self.assertEqual(dropping_mino.direction, Direction.EAST)

        dropping_mino.spin_anticlockwise(field)
        self.assertEqual(dropping_mino.direction, Direction.NORTH)

    def test_valid_place(self):
        field = Field()
        dropping_mino = DroppingMino(TetroMino.Z, field)
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

        dropping_mino.position = (10, 4)  # 安全地帯に戻る
        dropping_mino.spin_anticlockwise(field)
        dropping_mino.position = (10, 8)  # 回転した状態で右端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (10, 4)  # 安全地帯に戻る
        dropping_mino.spin_anticlockwise(field)
        dropping_mino.spin_anticlockwise(field)
        dropping_mino.position = (10, -1)  # 回転した状態で左端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))

        dropping_mino = DroppingMino(TetroMino.I, field)
        dropping_mino.position = (3, 0)  # 真横状態で左端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (3, -1)  # 真横状態で左端ギリギリout
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.spin_clockwise(field)
        dropping_mino.position = (3, -2)  # I minoが縦に左端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (3, -3)  # I minoが縦に左端ギリギリout
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.position = (3, 7)  # I minoが縦に右端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (3, 8)  # I minoが縦に右端ギリギリout
        self.assertFalse(dropping_mino.valid_place(field))

        dropping_mino.position = (3, 5)  # 安全地帯に戻る
        dropping_mino.spin_clockwise(field)
        dropping_mino.spin_clockwise(field)
        dropping_mino.position = (3, -1)  # I minoが縦に左端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (3, -2)  # I minoが縦に左端ギリギリout
        self.assertFalse(dropping_mino.valid_place(field))
        dropping_mino.position = (3, 8)  # I minoが縦に右端ギリギリ
        self.assertTrue(dropping_mino.valid_place(field))
        dropping_mino.position = (3, 9)  # I minoが縦に右端ギリギリout
        self.assertFalse(dropping_mino.valid_place(field))

    def test_rend_mino(self):
        field = Field()
        dropping_mino = DroppingMino(TetroMino.S, field)
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
        field = Field()
        dropping_mino = DroppingMino(TetroMino.I, field)
        dropping_mino.move_mino(1, 0, field)  # move down
        self.assertEqual(dropping_mino.position, (3, 3))
        dropping_mino.move_mino(0, 1, field)  # move right
        self.assertEqual(dropping_mino.position, (3, 4))
        dropping_mino.move_mino(0, -1, field)  # move left
        self.assertEqual(dropping_mino.position, (3, 3))

        dropping_mino = DroppingMino(TetroMino.O, field)
        dropping_mino.move_mino(1, 0, field)  # move down
        self.assertEqual(dropping_mino.position, (3, 4))
        dropping_mino.move_mino(0, 1, field)  # move right
        self.assertEqual(dropping_mino.position, (3, 5))
        dropping_mino.move_mino(0, -1, field)  # move left
        self.assertEqual(dropping_mino.position, (3, 4))


class TestTetroMinoGenerator(unittest.TestCase):
    def test_gen(self):
        generator = TetroMinoGenerator()
        test_count = {
            TetroMino.O: 0,
            TetroMino.I: 0,
            TetroMino.T: 0,
            TetroMino.L: 0,
            TetroMino.J: 0,
            TetroMino.Z: 0,
            TetroMino.S: 0
        }
        max_iter = 100
        length = len(test_count)
        for i in range(length * max_iter):
            if i % length == 0:
                for count in test_count.values():
                    self.assertEqual(count, i / length)
            mino = generator.gen()
            test_count[mino] += 1


if __name__ == '__main__':
    unittest.main()
