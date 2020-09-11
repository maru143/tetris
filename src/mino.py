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
                [[0, 1, 1],
                 [1, 1, 0],
                 [0, 0, 0]]

        elif self == TetroMino.S:
            shape = \
                [[1, 1, 0],
                 [0, 1, 1],
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

