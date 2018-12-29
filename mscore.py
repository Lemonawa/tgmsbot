#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from random import randint

# 0 - 8: means 0-8 mines, not opened
# opened block = the value of not opened block + 10
# 9 is mine, not opened
# 19 is flagged mine
# 20 is stepped mine

# default:
#  HEIGHT = 8
#  WIDTH = 8
#  MINES = 9

IS_MINE = 9
DEAD = 20

def check_params(height, width, mines):
    if height <= 0 or width <= 0:
        return (False, "地图太小!")
    elif mines > height * width:
        return (False, "放不下这么多雷嘛!")
    elif mines == height * width:
        return (False, "一点就爆炸，有意思吗？")
    elif mines < 0:
        return (False, "暂时还不会放负数颗雷呢。")
    elif mines <= height * width:
        return (True, "")
def get_row_col(width, index):
    row = index // width
    col = index - width * row
    return (row, col)
def get_index(width, row_col):
    (row, col) = row_col
    index = width * row + col
    return index
class Board():
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.mines = mines
        self.map = None
        self.moves = list()
        self.state = 0 # 0:not playing, 1:playing, 2:win, 3:dead
    def __gen_map(self, first_move):
        height = self.height
        width = self.width
        mines = self.mines
        if mines >= height * width:
            return
        elif mines < 0:
            return
        mines_1d = list(range(height * width))
        # first_move should't be a mine
        del mines_1d[get_index(width, first_move)]
        mines_index = list()
        self.map = np.zeros((height, width), dtype=np.int8)
        for i in range(mines):
            index = randint(1, len(mines_1d)) - 1
            mines_index.append(mines_1d[index])
            del mines_1d[index]
        for mine_index in mines_index:
            (row, col) = get_row_col(width, mine_index)
            self.map[row][col] = IS_MINE
        for row in range(height):
            for col in range(width):
                if self.map[row][col] != IS_MINE:
                    mine_count = 0
                    for nbr_value in self.__iter_neighbour(row, col, return_rc=False):
                        if nbr_value == IS_MINE:
                            mine_count += 1
                    self.map[row][col] = mine_count
    def __iter_neighbour(self, row, col, return_rc=True):
        height = self.height
        width = self.width
        for i in [a - 1 for a in range(3)]:
            for j in [b - 1 for b in range(3)]:
                if (i != 0 or j != 0) and row + i >= 0 and row + i <= height - 1 and \
                col + j >= 0 and col + j <= width - 1:
                    if return_rc:
                        yield (row + i, col + j)
                    else:
                        yield self.map[row + i][col + j]
    def __do_i_win(self):
        unopened = 0
        mines_opened = 0
        for x in np.nditer(self.map):
            if x <= 8:
                unopened += 1
            elif x == 19:
                mines_opened += 1
        if mines_opened == self.mines:
            return True
        elif unopened == 0:
            return True
        else:
            return False
    def __open(self, row, col, automatic=False):
        if self.state != 1:
            return
        if not automatic and self.map[row][col] == 9:
            self.map[row][col] = DEAD
            self.state = 3
        elif self.map[row][col] == 0:
            self.map[row][col] += 10 # open this block
            # open other blocks
            for nbr in self.__iter_neighbour(row, col):
                self.__open(nbr[0], nbr[1], automatic=True)
        elif self.map[row][col] >= 10:
            # already opened
            if automatic:
                return
            neighbour_mine_opened = 0
            neighbour_unopened = 0
            for neighbour in self.__iter_neighbour(row, col, return_rc=False):
                if neighbour == 19:
                    neighbour_mine_opened += 1
                if neighbour <= 9:
                    neighbour_unopened += 1
            if (neighbour_mine_opened == self.map[row][col] - 10) or \
            (neighbour_unopened == self.map[row][col] - 10 - neighbour_mine_opened):
                for nbr in self.__iter_neighbour(row, col):
                    self.__open(nbr[0], nbr[1], automatic=True)
        else:
            self.map[row][col] += 10
        if self.__do_i_win():
            self.state = 2

    def move(self, row_col):
        if self.state == 0:
            self.__gen_map(row_col)
            self.state = 1
        (row, col) = row_col
        self.__open(row, col)
