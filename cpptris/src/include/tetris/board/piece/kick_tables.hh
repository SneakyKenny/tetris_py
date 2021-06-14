#pragma once

#include <map>
#include <vector>

#include "tetris/board/piece/piece_rotation.hh"
#include "tetris/board/piece/piece_type.hh"

namespace tetris::board::piece
{
    using from_to_pair_t = std::pair<PieceRotation, PieceRotation>;
    using kick_table_t = std::vector<std::pair<int, int>>;

    static std::map<from_to_pair_t, kick_table_t> kick_tables_regular {
        { { R_N, R_E }, { { 0,  0}, {-1,  0}, {-1,  1}, { 0, -2}, {-1, -2} } },
        { { R_E, R_S }, { { 0,  0}, { 1,  0}, { 1, -1}, { 0,  2}, { 1,  2} } },
        { { R_E, R_N }, { { 0,  0}, { 1,  0}, { 1, -1}, { 0,  2}, { 1,  2} } },
        { { R_S, R_E }, { { 0,  0}, {-1,  0}, {-1,  1}, { 0, -2}, {-1, -2} } },
        { { R_S, R_W }, { { 0,  0}, { 1,  0}, { 1,  1}, { 0, -2}, { 1, -2} } },
        { { R_W, R_S }, { { 0,  0}, {-1,  0}, {-1, -1}, { 0,  2}, {-1,  2} } },
        { { R_W, R_N }, { { 0,  0}, {-1,  0}, {-1, -1}, { 0,  2}, {-1,  2} } },
        { { R_N, R_W }, { { 0,  0}, { 1,  0}, { 1,  1}, { 0, -2}, { 1, -2} } },

        // 180s
        { { R_N, R_S }, { { 0,  0}, { 1,  0}, { 2,  0}, { 1,  1}, { 2,  1},
                          {-1,  0}, {-2,  0}, {-1,  1}, {-2,  1}, { 0, -1},
                          { 3,  0}, {-3,  0} } },
        { { R_E, R_W }, { { 0,  0}, { 0,  1}, { 0,  2}, {-1,  1}, {-1,  2},
                          { 0, -1}, { 0, -2}, {-1, -1}, {-1, -2}, { 1,  0},
                          { 0,  3}, { 0, -3} } },
        { { R_S, R_N }, { { 0,  0}, {-1,  0}, {-2,  0}, {-1, -1}, {-2, -1},
                          { 1,  0}, { 2,  0}, { 1, -1}, { 2, -1}, { 0,  1},
                          {-3,  0}, { 3,  0} } },
        { { R_W, R_E }, { { 0,  0}, { 0,  1}, { 0,  2}, { 1,  1}, { 1,  2},
                          { 0, -1}, { 0, -2}, { 1, -1}, { 1, -2}, {-1,  0},
                          { 0,  3}, { 0, -3} } },
    };

    static std::map<from_to_pair_t, kick_table_t> kick_tables_I {
        { { R_N, R_E }, { { 0,  0}, {-2,  0}, { 1,  0}, {-2, -1}, { 1,  2} } },
        { { R_E, R_S }, { { 0,  0}, {-1,  0}, { 2,  0}, {-1,  2}, { 2, -1} } },
        { { R_E, R_N }, { { 0,  0}, { 2,  0}, {-1,  0}, { 2,  1}, {-1, -2} } },
        { { R_S, R_E }, { { 0,  0}, { 1,  0}, {-2,  0}, { 1, -2}, {-2,  1} } },
        { { R_S, R_W }, { { 0,  0}, { 2,  0}, {-1,  0}, { 2,  1}, {-1, -2} } },
        { { R_W, R_S }, { { 0,  0}, {-2,  0}, { 1,  0}, {-2, -1}, { 1,  2} } },
        { { R_W, R_N }, { { 0,  0}, { 1,  0}, {-2,  0}, { 1, -2}, {-2,  1} } },
        { { R_N, R_W }, { { 0,  0}, {-1,  0}, { 2,  0}, {-1,  2}, { 2, -1} } },

        // 180s
        { { R_N, R_S }, { { 0,  0}, {-1,  0}, {-2,  0}, { 1,  0}, { 2,  0}, { 0,  1} } },
        { { R_E, R_W }, { { 0,  0}, { 0,  1}, { 0,  2}, { 0, -1}, { 0, -2}, {-1,  0} } },
        { { R_S, R_N }, { { 0,  0}, { 1,  0}, { 2,  0}, {-1,  0}, {-2,  0}, { 0, -1} } },
        { { R_W, R_E }, { { 0,  0}, { 0,  1}, { 0,  2}, { 0, -1}, { 0, -2}, { 1,  0} } },
    };

    inline kick_table_t get_kick_table(PieceType type, PieceRotation from, PieceRotation to)
    {
        from_to_pair_t key{from, to};
        if (type == PieceType::T_I)
            return kick_tables_I.at(key);
        return kick_tables_regular.at(key);
    }
}
