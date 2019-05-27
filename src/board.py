#!/usr/bin/env python

import os

occupied = 'o'
empty = ' '
border = 'x'
upper_border = '-'
ghost = '~'
#piece_list = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

cyan = (0, 159, 218)
light_cyan = (127, 255, 255)
yellow = (254, 203, 0)
light_yellow = (255, 255, 127)
blue = (0, 101, 189)
light_blue = (100, 200, 255)
orange = (255, 121, 0)
light_orange = (255, 180, 142)
green = (105, 190, 40)
light_green = (127, 255, 127)
red = (237, 41, 57)
light_red = (255, 145, 145)
purple = (149, 45, 152)
light_purple = (215, 142, 255)
white = (255, 255, 255)

color_from_board_val = {
    0: cyan,
    1: blue,
    2: orange,
    3: yellow,
    4: green,
    5: purple,
    6: red,
    -1: light_cyan,
    -2: light_blue,
    -3: light_orange,
    -4: light_yellow,
    -5: light_green,
    -6: light_purple,
    -7: light_red
}

#for the board:
#None is an empty cell
#val >= 0 (max is 6 inclusive) <=> actual piece
#val < 0 (max is -7 inclusive) <=> ghost piece
#~ is ignored (current ghost)
#val is self.board[i][j] and represents the mino in the cell
#later used for color ?

class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.hmargin = 3

        board = []
        for _ in range(self.height + self.hmargin):
            line = []
            for _ in range(self.width):
                line.append(None)
            board.append(line)
        self.board = board

    def get_state(self, i, j):
        state = self.board[self.height + self.hmargin - i - 1][j]
        return state is not None and state >= 0

    def set_state(self, i, j, s):
        self.board[self.height + self.hmargin - i - 1][j] = s

    def cell_as_str(self, i, j):
        state = self.board[self.height + self.hmargin - i - 1][j]
        if state is None:
            return empty
        if state >= 0:
            return occupied
        return ghost

    def get_as_str(self, show_margin = False):
        s = ''
        if show_margin:
            for i in range(self.hmargin):
                actual_i = self.height + self.hmargin - i - 1
                s += border
                for j in range(self.width):
                    s += self.cell_as_str(actual_i, j)
                s += border + '\n'
        s += upper_border
        s += empty * self.width
        s += upper_border + '\n'
        for i in range(self.height):
            s += border
            actual_i = self.height - i - 1
            for j in range(self.width):
                s += self.cell_as_str(actual_i, j)
            s += border + '\n'
        for _ in range(self.width + 2):
            s += border
        return s

    def print_board(self, clear = False, show_margin = False):
        if clear:
            clear_console()
        print(self.get_as_str(show_margin))

    def remove_ghost(self):
        for i in range(self.hmargin):
            actual_i = self.height + self.hmargin - i - 1
            for j in range(self.width):
                if self.cell_as_str(actual_i, j) == ghost:
                    self.set_state(actual_i, j, None)
        for i in range(self.height):
            actual_i = self.height - i - 1
            for j in range(self.width):
                if self.cell_as_str(actual_i, j) == ghost:
                    self.set_state(actual_i, j, None)

    def setup_tsd(self):
        self.set_state(19, 3, 8)
        self.set_state(18, 3, 8)
        self.set_state(18, 6, 8)
        self.set_state(18, 7, 8)
        self.set_state(17, 3, 8)
        self.set_state(17, 7, 8)
        self.set_state(16, 3, 8)
        self.set_state(16, 4, 8)
        self.set_state(16, 6, 8)
        self.set_state(16, 7, 8)
        self.set_state(15, 3, 8)
        self.set_state(15, 4, 8)
        self.set_state(15, 5, 8)
        self.set_state(15, 6, 8)
        self.set_state(15, 7, 8)

    def setup_tst(self):
        self.set_state(21, 3, 8)
        self.set_state(21, 2, 8)
        self.set_state(20, 2, 8)
        self.set_state(19, 2, 8)
        self.set_state(19, 4, 8)
        self.set_state(19, 5, 8)
        self.set_state(19, 6, 8)
        self.set_state(18, 2, 8)
        self.set_state(18, 5, 8)
        self.set_state(18, 6, 8)
        self.set_state(17, 2, 8)
        self.set_state(17, 4, 8)
        self.set_state(17, 5, 8)
        self.set_state(17, 6, 8)
        self.set_state(16, 2, 8)
        self.set_state(16, 3, 8)
        self.set_state(16, 4, 8)
        self.set_state(16, 5, 8)
        self.set_state(16, 6, 8)

def clear_console():
    _ = os.system('clear' if os.name == 'posix' else 'cls')
