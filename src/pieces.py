#!/usr/bin/env python

spawn_y = 19
spawn_x_3w = 3
spawn_x_4w = 3

all0_R = [( 0, 0), (-1, 0), (-1,+1), ( 0,-2), (-1,-2)]
allR_2 = [( 0, 0), (+1, 0), (+1,-1), ( 0,+2), (+1,+2)]
allR_0 = [( 0, 0), (+1, 0), (+1,-1), ( 0,+2), (+1,+2)]
all2_R = [( 0, 0), (-1, 0), (-1,+1), ( 0,-2), (-1,-2)]
all2_L = [( 0, 0), (+1, 0), (+1,+1), ( 0,-2), (+1,-2)]
allL_2 = [( 0, 0), (-1, 0), (-1,-1), ( 0,+2), (-1,+2)]
allL_0 = [( 0, 0), (-1, 0), (-1,-1), ( 0,+2), (-1,+2)]
all0_L = [( 0, 0), (+1, 0), (+1,+1), ( 0,-2), (+1,-2)]

iwk0_R = [( 0, 0), (-2, 0), (+1, 0), (-2,-1), (+1,+2)]
iwkR_0 = [( 0, 0), (+2, 0), (-1, 0), (+2,+1), (-1,-2)]
iwkR_2 = [( 0, 0), (-1, 0), (+2, 0), (-1,+2), (+2,-1)]
iwk2_R = [( 0, 0), (+1, 0), (-2, 0), (+1,-2), (-2,+1)]
iwk2_L = [( 0, 0), (+2, 0), (-1, 0), (+2,+1), (-1,-2)]
iwkL_2 = [( 0, 0), (-2, 0), (+1, 0), (-2,-1), (+1,+2)]
iwkL_0 = [( 0, 0), (+1, 0), (-2, 0), (+1,-2), (-2,+1)]
iwk0_L = [( 0, 0), (-1, 0), (+2, 0), (-1,+2), (+2,-1)]

rotations = ['0', 'R', '2', 'L']

tl = (-1,  1)
tr = ( 1,  1)
bl = (-1, -1)
br = ( 1, -1)

north = [tl, tr, bl, br]
east  = [tr, br, tl, bl]
south = [br, bl, tr, tl]
west  = [bl, tl, br, tr]

t_spin_checks = [north, east, south, west]

t_spin_bonus = [400, 800, 1200, 1600]
t_spin_mini_bonus = [100, 200, 1200]

I_matrix = [
    [False, False, False, False],
    [ True,  True,  True,  True],
    [False, False, False, False],
    [False, False, False, False]
]

O_matrix = [
    [ True,  True, False],
    [ True,  True, False],
    [False, False, False],
]

J_matrix = [
    [ True, False, False],
    [ True,  True,  True],
    [False, False, False]
]

L_matrix = [
    [False, False,  True],
    [ True,  True,  True],
    [False, False, False]
]

S_matrix = [
    [False,  True,  True],
    [ True,  True, False],
    [False, False, False]
]

Z_matrix = [
    [True,   True, False],
    [False,  True,  True],
    [False, False, False]
]

T_matrix = [
    [False,  True, False],
    [True,   True,  True],
    [False, False, False]
]

piece_matrix_list = [I_matrix, J_matrix, L_matrix, O_matrix, S_matrix, T_matrix, Z_matrix]

class I():
    def __init__(self):
        self.x = spawn_x_4w
        self.y = spawn_y
        self.shape = I_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'I: ({}, {})'.format(self.x, self.y)
        return 'I'

class O():
    def __init__(self):
        self.x = spawn_x_4w + 1
        self.y = spawn_y
        self.shape = O_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'O: ({}, {})'.format(self.x, self.y)
        return 'O'

class J():
    def __init__(self):
        self.x = spawn_x_3w
        self.y = spawn_y
        self.shape = J_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'J: ({}, {})'.format(self.x, self.y)
        return 'J'

class L():
    def __init__(self):
        self.x = spawn_x_3w
        self.y = spawn_y
        self.shape = L_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'L: ({}, {})'.format(self.x, self.y)
        return 'L'

class S():
    def __init__(self):
        self.x = spawn_x_3w
        self.y = spawn_y
        self.shape = S_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'S: ({}, {})'.format(self.x, self.y)
        return 'S'

class Z():
    def __init__(self):
        self.x = spawn_x_3w
        self.y = spawn_y
        self.shape = Z_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'Z: ({}, {})'.format(self.x, self.y)
        return 'Z'

class T():
    def __init__(self):
        self.x = spawn_x_3w
        self.y = spawn_y
        self.shape = T_matrix
        self.rot = '0'
        self.rot_index = 0

    def to_string(self, show_pos = False):
        if show_pos:
            return 'T: ({}, {})'.format(self.x, self.y)
        return 'T'
