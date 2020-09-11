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


