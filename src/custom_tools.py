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

def O_180_spin(rot):
    if rot == '0':
        return  [
            [False, False, False, False],
            [False,  True,  True, False],
            [False,  True,  True, False],
        ]
    return [
        [False,  True,  True, False],
        [False,  True,  True, False],
        [False, False, False, False],
    ]

def matrix_180_rot(shape):
    for _ in range(2):
        shape = matrix_left_rot(shape)

    return shape

def copy_matrix(m):
    ret = []
    for i in range(len(m)):
        line = []
        for j in range(len(m[i])):
            line.append(m[i][j])
        ret.append(line)
    return ret

def copy(piece):
    s = piece.to_string()

    new_piece = None

    if s == 'I':
        new_piece = pieces.I()
    elif s == 'J':
        new_piece = pieces.J()
    elif s == 'L':
        new_piece = pieces.L()
    elif s == 'O':
        new_piece = pieces.O()
    elif s == 'S':
        new_piece = pieces.S()
    elif s == 'T':
        new_piece = pieces.S()
    elif s == 'Z':
        new_piece = pieces.Z()
    else:
        print(f'unknown piece type: {s}')
        return None

    new_piece.x = piece.x
    new_piece.y = piece.y
    new_piece.rot = piece.rot
    new_piece.rot_index = piece.rot_index

    new_piece.shape = copy_matrix(piece.shape)
    return new_piece
