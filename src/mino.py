#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List
import numpy as np


class TetroMino(Enum):
    """defines tetromino types"""

    Empty = 0
    O = 1
    I = 2
    T = 3
    L = 4
    J = 5
    Z = 6
    S = 7

    def get_shape(self) -> np.ndarray:

        shape: List[List[int]]

        if self == TetroMino.O:
            shape = \
                [[1, 1],
                 [1, 1]]

        elif self == TetroMino.I:
            shape = \
                [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

        elif self == TetroMino.T:
            shape = \
                [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.L:
            shape = \
                [[0, 0, 1],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.J:
            shape = \
                [[1, 0, 0],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.Z:
            shape = \
                [[1, 1, 0],
                 [0, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.S:
            shape = \
                [[0, 1, 1],
                 [1, 1, 0],
                 [0, 0, 0]]

        else:
            shape = [[0]]

        return np.array(shape, dtype=bool)


class TetroMinoColor:
    """defines tetromino colors"""

    YELLOW = 0xFFFF00
    LIGHTBLUE = 0x00FFFF
    PURPLE = 0x880088
    ORANGE = 0xFFAA00
    DARKBLUE = 0x0000FF
    GREEN = 0x00FF00
    RED = 0xFF0000


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

    def get_rotation_times(self) -> int:
        """returns clockwise rotation times of block"""

        if self == Direction.NORTH:
            return 0
        elif self == Direction.WEST:
            return 1
        elif self == Direction.SOUTH:
            return 2
        else:
            return 3

    def next_dir_clockwise(self):
        """returns next cw-direction"""

        if self == Direction.NORTH:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.WEST
        else:
            return Direction.NORTH

    def next_dir_anticlockwise(self):
        """returns next ccw-direction"""

        if self == Direction.NORTH:
            return Direction.WEST
        elif self == Direction.EAST:
            return Direction.NORTH
        elif self == Direction.SOUTH:
            return Direction.EAST
        else:
            return Direction.SOUTH


class DroppingMino:
    position: (int, int)
    mino: TetroMino
    direction: Direction

    def __init__(self, mino: TetroMino):
        self.position = (0, 4)
        self.mino = mino
        self.direction = Direction.NORTH

    def rend_mino(self) -> np.ndarray:
        """現在のdirectionに合わせたminoの形を返す"""

        shape = self.mino.get_shape()
        rotation = self.direction.get_rotation_times()
        shape = np.rot90(shape, rotation)
        return shape

    def valid_place(self) -> bool:
        """現在のminoがちゃんとした場所にいるかどうかを判定する"""
        # TODO: フィールドを実装して参照を受け取るようにする
        return True

    def move_mino(self, i: int, j: int) -> bool:
        """
        y方向にi, x方向にjだけminoを動かす
        もしだめだったらもとに戻してfalseを返す
        """

        prev_position = self.position
        y, x = self.position
        self.position = (y + i, x + j)
        if self.valid_place():
            return True
        else:
            self.position = prev_position
            return False

    def spin_clockwise(self) -> bool:
        """
        minoを時計回りに90度回転
        もしだめだったらもとに戻してfalseを返す
        """

        self.direction = self.direction.next_dir_clockwise()
        if self.valid_place():
            return True
        else:
            self.direction = self.direction.next_dir_anticlockwise()
            return False

    def spin_anticlockwise(self) -> bool:
        """
        minoを反時計回りに90度回転
        もしだめだったらもとに戻してfalseを返す
        """

        self.direction = self.direction.next_dir_anticlockwise()
        if self.valid_place():
            return True
        else:
            self.direction = self.direction.next_dir_clockwise()
            return False
