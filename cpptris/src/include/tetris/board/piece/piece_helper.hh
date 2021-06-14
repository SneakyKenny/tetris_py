#pragma once

#include "tetris/board/piece/piece_matrix.hh"
#include "tetris/board/piece/piece_position.hh"
#include "tetris/board/piece/piece_type.hh"
#include "tetris/board/piece/piece_rotation.hh"

#ifdef BIGMODE // FIXME: this literaly doesn't work kekw
# define SPAWN_X_2W 1
# define SPAWN_X_3W 1
# define SPAWN_X_4W 1
#else
# define SPAWN_X_2W 3
# define SPAWN_X_3W 3
# define SPAWN_X_4W 3
#endif /* !BIGMODE */

#define SPAWN_Y 19

namespace tetris::board::piece
{
    class PieceHelper
    {
    public:
        static size_t get_piece_spawn_x(PieceType type)
        {
            switch (type)
            {
                case PieceType::T_I:
                    return SPAWN_X_4W;
                case PieceType::T_O:
                    return SPAWN_X_2W;
                default:
                    return SPAWN_X_3W;
            }
        }

        static PiecePosition get_piece_spawn_position(PieceType type)
        {
            return PiecePosition{get_piece_spawn_x(type), SPAWN_Y};
        }
    };
}
