#pragma once

#include <string>

namespace tetris::board::piece
{
    class PieceRepresentation
    {
    public:
        static const std::string get_taken()
        {
            return "XX";
        }

        static const std::string get_empty()
        {
            return "  ";
        }

        static const std::string get_border()
        {
            return "OO";
        }
    };
}
