#pragma once

#include <iostream>

#include "utype.hh"

namespace tetris::board::piece
{
    enum PieceRotation
    {
        R_N,
        R_E,
        R_S,
        R_W,
    };

    inline PieceRotation operator+(const PieceRotation& lhs, const PieceRotation& rhs)
    {
        return lhs + utils::utype(rhs);
    }

    inline PieceRotation operator+(const PieceRotation& lhs, const int rhs)
    {
        int ulhs = utils::utype(lhs);

        int new_rotation = (ulhs + rhs) % 4; // FIXME: I don't like that this is hardcoded
        while (new_rotation < 0)
            new_rotation += 4;

        return static_cast<PieceRotation>(new_rotation);
    }

    inline std::ostream& operator<<(std::ostream& o, const PieceRotation& r)
    {
        switch (r)
        {
        case R_N:
            return o << "N";
        case R_E:
            return o << "E";
        case R_S:
            return o << "S";
        // case R_W:
        default:
            return o << "W";
        }
    }
}
