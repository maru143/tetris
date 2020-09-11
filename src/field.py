#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from enum import Enum

from src.mino import TetroMinoColor


class Block:
    filled: bool
    color: TetroMinoColor

    def __init__(self, filled: bool, color: TetroMinoColor):
        self.filled = filled
        self.color = color


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_rotation_times(self) -> int:
        """returns clockwise rotation times of block"""

        if self == Direction.NORTH:
            return 0
        elif self == Direction.EAST:
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
