#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from collections import deque
from typing import Deque, List, Dict

sys.path.append("src/")
from mino import Field, DroppingMino, TetroMino, TetroMinoGenerator, \
    TetroMinoColor, Block


class Score:
    actions: Dict[int, int]
    t_spins: Dict[int, int]
    lines: int
    total: int

    def __init__(self):
        self.actions = {i: 0 for i in range(1, 5)}
        self.t_spins = {i: 0 for i in range(1, 4)}
        self.lines = 0
        self.total = 0


class Tetris:
    field: Field
    mino_generator: TetroMinoGenerator
    dropping_mino: DroppingMino
    holding_mino: TetroMino
    hold_just_now: bool
    next_mino_num: int
    next_minos: Deque[TetroMino]

    speed: int  # mino falls every {speed} ms
    score: Score
    is_paused: bool
    is_game_over: bool
    last_op_is_spin: bool

    def __init__(self):
        self.field = Field()
        self.mino_generator = TetroMinoGenerator()
        self.dropping_mino = DroppingMino(self.mino_generator.gen(),
                                          self.field)
        self.holding_mino = None
        self.hold_just_now = False
        self.next_mino_num = 5
        self.next_minos = deque()

        self.speed = 1000
        self.score = Score()
        self.is_paused = False
        self.is_game_over = False
        self.last_op_is_spin = False

        for i in range(self.next_mino_num):
            self.next_minos.append(self.mino_generator.gen())

    def generate_next_mino(self) -> TetroMino:
        next_mino = self.next_minos.popleft()
        self.next_minos.append(self.mino_generator.gen())
        return next_mino

    def rend_field_color(self) -> List[List[TetroMinoColor]]:
        """returns complete field color for painting"""

        field_color = [[TetroMinoColor.WHITE
                        for i in range(self.field.width)]
                       for j in range(self.field.height)]

        # copy field's color simply
        for i in range(self.field.height):
            for j in range(self.field.width):
                field_color[i][j] = self.field.grid[i][j].color

        size = self.dropping_mino.mino.size()
        shape = self.dropping_mino.rend_mino()

        # show dropping mino ghost
        position = self.dropping_mino.position
        ghost_mino = self.dropping_mino
        while ghost_mino.move_mino(1, 0, self.field):
            pass
        y, x = ghost_mino.position
        self.dropping_mino.position = position
        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                field_color[y + i][x + j] = TetroMinoColor.GRAY

        # show dropping mino
        y, x = self.dropping_mino.position
        color = self.dropping_mino.mino.get_color()
        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                field_color[y + i][x + j] = color

        # self.dump_field()

        return field_color

    def dump_field(self) -> None:
        """output field to stderr for debugging"""

        field_color = self.rend_field_color()
        for i in range(self.field.height):
            print(" {:<2}:".format(i), end=" ", file=sys.stderr)
            for j in range(self.field.width):
                value = field_color[i][j].value
                if value == 0:
                    value = '_'
                print(value, end="", file=sys.stderr)
            print(file=sys.stderr)

    def oneLineDown(self) -> bool:
        return self.dropping_mino.move_mino(1, 0, self.field)

    def dropped(self) -> None:
        """fixes the dropping mino's location and yield next mino"""

        size = self.dropping_mino.mino.size()
        shape = self.dropping_mino.rend_mino()
        color = self.dropping_mino.mino.get_color()
        y, x = self.dropping_mino.position

        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                self.field.grid[y + i][x + j] = Block(True, color)

        self.clear_lines()
        self.drop_next_mino()
        self.hold_just_now = False
        self.last_op_is_spin = False

    def drop_next_mino(self):
        """take out mino from next and restock it"""

        self.dropping_mino = DroppingMino(self.next_minos.popleft(),
                                          self.field)
        if self.check_game_over():
            self.is_game_over = True
        self.next_minos.append(self.mino_generator.gen())

    def is_t_spin(self) -> bool:
        """judges whether the t_spin condition is satisfied"""

        if not self.last_op_is_spin or \
                not self.dropping_mino.mino == TetroMino.T:
            return False

        y, x = self.dropping_mino.position
        size = self.dropping_mino.mino.size()
        count = 0
        for i in range(0, size, 2):
            for j in range(0, size, 2):
                if self.field.grid[y + i][x + j]:
                    count += 1

        if count >= 3:
            return True
        else:
            return False

    def clear_lines(self) -> None:
        """deletes completely filled lines"""

        # delete completed lines
        remained_lines = [line for line in self.field.grid
                          if len([block for block in line if block.filled])
                          < self.field.width]
        delete_count = self.field.height - len(remained_lines)

        if not delete_count:
            return None

        # calculate score
        self.score.actions[delete_count] += 1
        if self.is_t_spin():
            self.score.t_spins[delete_count] += 1
        self.score.lines += delete_count

        # push new lines
        new_lines = [[Block(False, TetroMinoColor.WHITE)
                      for j in range(self.field.width)]
                     for i in range(delete_count)]

        new_grid = new_lines + remained_lines

        self.field.grid = new_grid

    def check_game_over(self) -> bool:
        if not self.dropping_mino.valid_place(self.field):
            return True
        return False

    def move_right(self):
        if self.dropping_mino.move_mino(0, 1, self.field):
            self.last_op_is_spin = False

    def move_left(self):
        if self.dropping_mino.move_mino(0, -1, self.field):
            self.last_op_is_spin = False

    def move_down(self):
        if self.dropping_mino.move_mino(1, 0, self.field):
            self.last_op_is_spin = False

    def hard_drop(self):
        while self.dropping_mino.move_mino(1, 0, self.field):
            pass  # drop mino as much as possible
        self.dropped()

    def spin_clockwise(self):
        if self.dropping_mino.spin_clockwise(self.field):
            self.last_op_is_spin = True

    def spin_anticlockwise(self):
        if self.dropping_mino.spin_anticlockwise(self.field):
            self.last_op_is_spin = True

    def hold(self) -> bool:
        if self.hold_just_now:
            return False
        if not self.holding_mino:
            self.holding_mino = self.dropping_mino.mino
            self.dropping_mino = DroppingMino(self.generate_next_mino(),
                                              self.field)
        else:
            mino = self.holding_mino
            self.holding_mino = self.dropping_mino.mino
            self.dropping_mino = DroppingMino(mino, self.field)
        self.hold_just_now = True
        return True
