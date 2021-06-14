#pragma once

#include <ostream>

#include "tetris/board/piece/piece_rotation.hh"

namespace tetris::board::piece
{
    class PiecePosition
    {
    public:
        PiecePosition(size_t x, size_t y, PieceRotation rotation = PieceRotation::R_N)
            : x_(x)
            , y_(y)
            , rotation_(rotation)
        {}

        size_t get_x() const
        {
            return x_;
        }

        size_t get_y() const
        {
            return y_;
        }

        PieceRotation get_rotation() const
        {
            return rotation_;
        }

        PiecePosition operator+(const PiecePosition& rhs) const
        {
            return {
                x_ + rhs.x_,
                y_ + rhs.y_,
                rotation_, /* + rhs.rotation_ // don't rotate the piece */
            };
        }

    private:
        size_t x_;
        size_t y_;
        PieceRotation rotation_;
    };

    inline std::ostream& operator<<(std::ostream& o, const PiecePosition& p)
    {
        return (o << "(" << p.get_x() << ", " << p.get_y() << ", " << p.get_rotation() << ")");
    }
}
