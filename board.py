#!/usr/bin/env python

import os

occupied = 'o'
empty = ' '
border = 'x'
upper_border = '-'

class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.hmargin = 3

        board = []
        for _ in range(self.height + self.hmargin):
            line = []
            for _ in range(self.width):
                line.append(False)
            board.append(line)
        self.board = board

    def fill_line(self, i):
        actual_i = self.height + self.hmargin - i - 1
        for j in range(self.width):
            self.board[actual_i][j] = True

    def setup_tst(self):
        self.set_state(21, 3, '=')
        self.set_state(21, 2, '=')
        self.set_state(20, 2, '=')
        self.set_state(19, 2, '=')
        self.set_state(19, 4, '=')
        self.set_state(19, 5, '=')
        self.set_state(19, 6, '=')
        self.set_state(18, 2, '=')
        self.set_state(18, 5, '=')
        self.set_state(18, 6, '=')
        self.set_state(17, 2, '=')
        self.set_state(17, 4, '=')
        self.set_state(17, 5, '=')
        self.set_state(17, 6, '=')
        self.set_state(16, 2, '=')
        self.set_state(16, 3, '=')
        self.set_state(16, 4, '=')
        self.set_state(16, 5, '=')
        self.set_state(16, 6, '=')

    def get_state(self, i, j):
        return self.board[self.height + self.hmargin - i - 1][j]

    def set_state(self, i, j, s):
        self.board[self.height + self.hmargin - i - 1][j] = s

    def get_as_str(self, show_margin = False):
        s = ''
        if show_margin:
            for i in range(self.hmargin):
                actual_i = self.height + self.hmargin - i - 1
                s += border
                for j in range(self.width):
                    if self.get_state(actual_i, j) == '=':
                        s += '='
                    else:
                        s += occupied if self.get_state(actual_i, j) else empty
                s += border + '\n'
        s += upper_border
        s += empty * self.width
        s += upper_border + '\n'
        for i in range(self.height):
            s += border
            actual_i = self.height - i - 1
            for j in range(self.width):
                if self.get_state(actual_i, j) == '=':
                    s += '='
                else:
                    s += occupied if self.get_state(actual_i, j) else empty
            s += border + '\n'
        for _ in range(self.width + 2):
            s += border
        return s

    def print_board(self, clear = False, show_margin = False):
        if clear:
            clear_console()
        print(self.get_as_str(show_margin))

def clear_console():
    _ = os.system('clear' if os.name == 'posix' else 'cls')
