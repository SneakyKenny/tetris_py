#!/usr/bin/env python
from __future__ import print_function

import pieces
import board
import custom_tools
import random

#piece_list = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
piece_list = ['J', 'S', 'Z', 'O', 'I', 'L', 'T']

points_per_line = [0, 100, 300, 500, 800]

time_to_drop_per_level = [1.0, 1.0, 0.793, 0.618, 0.473, 0.355, 0.262, 0.190, 0.135, 0.094, 0.064, 0.043, 0.028, 0.018, 0.011, 0.007]

btb_bonus_factor = 1.5

class Tetris:
    def __init__(self):
        self.board = board.Board()
        self.bucket = piece_list[:]
        #random.shuffle(self.bucket)
        self.second_bucket = piece_list[:]
        #random.shuffle(self.second_bucket)
        #self.create_new_bucket()
        self.active_piece = None
        self.held_piece = None

        self.level = 5
        self.points = 0

        self.lines_cleared = 0

        self.is_back_to_back_bonus = False

    def check_for_tspin(self):
        #TODO
        #TODO: split as check_tspin and check_tspin_mini
        return self.active_piece.to_string() == 'T'

    def clear_completed_lines(self):
        if self.active_piece and self.active_piece.to_string() == 'T':
            for i in range(len(self.active_piece.shape)):
                for j in range(len(self.active_piece.shape[i])):
                    pass

        completed_lines = []
        for i in range(self.board.height):
            full = True
            j = 0
            while full and j < self.board.width:
                full &= self.board.get_state(i, j)
                if full:
                    j += 1
            if full:
                completed_lines.append(i)

        off_i = 0
        for comp in completed_lines:
            actual_i = self.board.height + self.board.hmargin - comp - 1 + off_i
            off_i += 1
            l = self.board.board.pop(actual_i)
            new_line = []
            for _ in range(self.board.width):
                new_line.append(False)
            self.board.board.insert(0, new_line)

        old_lc = self.lines_cleared % 10

        self.score(len(completed_lines))

        self.lines_cleared += len(completed_lines)

        if self.lines_cleared % 10 < old_lc and self.level < 15:
            self.level += 1

        return len(completed_lines)

    def score(self, lines_cleared):
        self.points += (self.level + 1) * points_per_line[lines_cleared]

    def spawn_next_piece(self, isFromHold = False):

        #TODO: REFACTOR THIS !!!
        self.clear_completed_lines()

        p = None

        if isFromHold == False:
            if len(self.bucket) == 0:
                self.bucket = self.second_bucket
                self.second_bucket = piece_list[:]
                random.shuffle(self.second_bucket)
            p = self.bucket.pop()
        else:
            p = self.held_piece
        new_piece = None

        if p == 'I':
            new_piece = pieces.I()
        elif p == 'J':
            new_piece = pieces.J()
        elif p == 'L':
            new_piece = pieces.L()
        elif p == 'O':
            new_piece = pieces.O()
        elif p == 'S':
            new_piece = pieces.S()
        elif p == 'T':
            new_piece = pieces.T()
        else:
            new_piece = pieces.Z()

        for i in range(len(new_piece.shape)):
            actual_i = len(new_piece.shape) - i - 1
            for j in range(len(new_piece.shape[i])):
                if new_piece.shape[i][j]:
                    if self.board.get_state(actual_i + new_piece.y, j + new_piece.x):
                        return False

        for i in range(len(new_piece.shape)):
            actual_i = len(new_piece.shape) - i - 1
            for j in range(len(new_piece.shape[i])):
                if new_piece.shape[i][j]:
                    self.board.set_state(actual_i + new_piece.y, j + new_piece.x, True)

        self.active_piece = new_piece
        return True

    def set_active_visibility(self, vis):
        for i in range(len(self.active_piece.shape)):
            actual_i = len(self.active_piece.shape) - i - 1
            for j in range(len(self.active_piece.shape[i])):
                if self.active_piece.shape[i][j]:
                    self.board.set_state(actual_i + self.active_piece.y, j + self.active_piece.x, vis)

    def move_active_piece(self):
        self.set_active_visibility(False)

        for i in range(len(self.active_piece.shape)):
            actual_i = len(self.active_piece.shape) - i - 1
            for j in range(len(self.active_piece.shape[i])):
                if self.active_piece.shape[i][j]:
                    if actual_i + self.active_piece.y - 1 < 0:
                        self.set_active_visibility(True)
                        return False
                    if self.board.get_state(actual_i + self.active_piece.y - 1, j + self.active_piece.x):
                        self.set_active_visibility(True)
                        return False

        self.active_piece.y -= 1

        self.set_active_visibility(True)

        return True

    def test_pos(self, mat, tests, k):
        off_x, off_y = tests[k]
        for i in range(len(mat)):
            actual_i = len(self.active_piece.shape) - i - 1
            for j in range(len(mat[i])):
                if mat[i][j]:
                    if i + self.active_piece.y + off_y < 0:
                        return False
                    if j + self.active_piece.x + off_x < 0 or j + self.active_piece.x + off_x >= self.board.width:
                        return False
                    if self.board.get_state(actual_i + self.active_piece.y + off_y, j + self.active_piece.x + off_x):
                        return False
        return True

    def rotate_piece_left(self):
        if self.active_piece.to_string() == 'O':
            return False

        self.set_active_visibility(False)

        left_rot_mat = custom_tools.matrix_left_rot(self.active_piece.shape)

        rot = self.active_piece.rot

        tests = None

        if self.active_piece.to_string() == 'I':
            if rot == '0':
                tests = pieces.iwk0_L
            elif rot == 'L':
                tests = pieces.iwkL_2
            elif rot == '2':
                tests = pieces.iwk2_R
            elif rot == 'R':
                tests = pieces.iwkR_0
            else:
                print('unknown rotation for I piece.')
                return False
        else:
            if rot == '0':
                tests = pieces.all0_L
            elif rot == 'L':
                tests = pieces.allL_2
            elif rot == '2':
                tests = pieces.all2_R
            elif rot == 'R':
                tests = pieces.allR_0
            else:
                print('unknown rotation for common piece.')
                return False

        for k in range(5):
            if self.test_pos(left_rot_mat, tests, k):
                self.active_piece.shape = left_rot_mat
                self.active_piece.x += tests[k][0]
                self.active_piece.y += tests[k][1]
                self.set_active_visibility(True)

                self.active_piece.rot_index = (self.active_piece.rot_index - 1) % 4
                self.active_piece.rot = pieces.rotations[self.active_piece.rot_index]

                return True

        self.set_active_visibility(True)
        return False

    def rotate_piece_right(self):
        if self.active_piece.to_string() == 'O':
            return False

        self.set_active_visibility(False)

        right_rot_mat = custom_tools.matrix_right_rot(self.active_piece.shape)

        rot = self.active_piece.rot

        tests = None

        if self.active_piece.to_string() == 'I':
            if rot == '0':
                tests = pieces.iwk0_R
            elif rot == 'L':
                tests = pieces.iwkL_0
            elif rot == '2':
                tests = pieces.iwk2_L
            elif rot == 'R':
                tests = pieces.iwkR_2
            else:
                print('unknown rotation for I piece to the right.')
                return False
        else:
            if rot == '0':
                tests = pieces.all0_R
            elif rot == 'L':
                tests = pieces.allL_0
            elif rot == '2':
                tests = pieces.all2_L
            elif rot == 'R':
                tests = pieces.allR_2
            else:
                print('unknown rotation for common piece to the right.')
                return False

        for k in range(5):
            if self.test_pos(right_rot_mat, tests, k):
                self.active_piece.shape = right_rot_mat
                self.active_piece.x += tests[k][0]
                self.active_piece.y += tests[k][1]
                self.set_active_visibility(True)

                self.active_piece.rot_index = (self.active_piece.rot_index + 1) % 4
                self.active_piece.rot = pieces.rotations[self.active_piece.rot_index]

                return True

        self.set_active_visibility(True)
        return False

    def rotate_piece_180(self):
        self.set_active_visibility(False)

        rot_mat_180 = custom_tools.matrix_180_rot(self.active_piece.shape)

        rot = self.active_piece.rot

        tests = None

        if self.active_piece.to_string() != 'O':
            if self.active_piece.to_string() == 'I':
                if rot == '0':
                    tests = pieces.iwk0_R
                elif rot == 'L':
                    tests = pieces.iwkL_0
                elif rot == '2':
                    tests = pieces.iwk2_L
                elif rot == 'R':
                    tests = pieces.iwkR_2
                else:
                    print('unknown rotation for I piece to the right.')
                    return False
            else:
                if rot == '0':
                    tests = pieces.all0_R
                elif rot == 'L':
                    tests = pieces.allL_0
                elif rot == '2':
                    tests = pieces.all2_L
                elif rot == 'R':
                    tests = pieces.allR_2
                else:
                    print('unknown rotation for common piece to the right.')
                    return False

            for k in range(5):
                if self.test_pos(rot_mat_180, tests, k):
                    self.active_piece.shape = rot_mat_180
                    self.active_piece.x += tests[k][0]
                    self.active_piece.y += tests[k][1]
                    self.set_active_visibility(True)
                    return True
            self.set_active_visibility(True)
            return False

        else:
            if self.test_pos(rot_mat_180, [(0, 0)], 0):
                self.active_piece.shape = rot_mat_180
                self.set_active_visibility(True)
                return True
            self.set_active_visibility(True)
            return False

    def rotate_piece(self, dir):
        if dir == 'R':
            return self.rotate_piece_right()
        elif dir == 'L':
            return self.rotate_piece_left()
        return self.rotate_piece_180()

    def move_piece_horizontal(self, xdir):
        for i in range(len(self.active_piece.shape)):
            for j in range(len(self.active_piece.shape[i])):
                if self.active_piece.shape[i][j]:
                    if j + self.active_piece.x + xdir < 0:
                        return False
                    if j + self.active_piece.x + xdir >= self.board.width:
                        return False

        test = [(xdir, 0)]
        self.set_active_visibility(False)

        if self.test_pos(self.active_piece.shape, test, 0):
            self.active_piece.x += xdir
            self.set_active_visibility(True)
            return True

        self.set_active_visibility(True)
        return False

    def move_piece(self, dir):
        if dir == 'R':
            return self.move_piece_horizontal(1)
        elif dir == 'L':
            return self.move_piece_horizontal(-1)
        return self.move_active_piece() # I should rename this to move piece down

    def tetris_as_str(self):
        l = self.second_bucket + self.bucket
        s = ''
        s += '[]' if self.held_piece == None else '[' + self.held_piece + ']'
        s += ' '
        for i in range(6):
            s += l[len(l) - i - 1] + ' '
        s += '\tScore: {}'.format(self.points)
        s += '\n'
        s += self.board.get_as_str(True)
        return s

    def hold_piece(self):
        if self.held_piece == None:
            self.held_piece = self.active_piece.to_string()
            self.set_active_visibility(False)
            self.spawn_next_piece()
            self.set_active_visibility(True)
        else:
            old_active = self.active_piece.to_string()
            self.set_active_visibility(False)
            self.spawn_next_piece(isFromHold = True)
            self.set_active_visibility(True)
            self.held_piece = old_active
