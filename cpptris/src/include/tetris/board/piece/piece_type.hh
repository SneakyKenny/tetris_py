#pragma once

#include <iostream>

namespace tetris::board::piece
{
    enum PieceType
    {
        T_I,
        T_O,
        T_J,
        T_L,
        T_S,
        T_Z,
        T_T,
    };

    inline std::ostream& operator<<(std::ostream& o, PieceType type)
    {
        switch (type)
        {
            case PieceType::T_I:
                o << "I";
                break;
            case PieceType::T_O:
                o << "O";
                break;
            case PieceType::T_J:
                o << "J";
                break;
            case PieceType::T_L:
                o << "L";
                break;
            case PieceType::T_S:
                o << "S";
                break;
            case PieceType::T_Z:
                o << "Z";
                break;
            case PieceType::T_T:
                o << "T";
                break;
        }

        return o;
    }
}
