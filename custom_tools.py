import board
import pieces

def matrix_left_rot(shape):
    res = []
    for i in range(len(shape)):
        res_line = []
        for j in range(len(shape[i])):
            new_i = j
            new_j = len(shape[i]) - i - 1
            res_line.append(shape[new_i][new_j])
        res.append(res_line)
    return res

def matrix_right_rot(shape):
    for _ in range(3):
        shape = matrix_left_rot(shape)

    return shape

def matrix_180_rot(shape):
    for _ in range(2):
        shape = matrix_left_rot(shape)

    return shape
