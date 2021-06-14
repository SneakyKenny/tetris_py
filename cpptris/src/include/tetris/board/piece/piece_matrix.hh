#pragma once

#include <bitset>

#include "tetris/board/piece/piece_type.hh"
#include "tetris/board/piece/piece_rotation.hh"

#define PIECE_WIDTH 4 // TODO: Get rid of this

namespace tetris::board::piece
{
    using piece_matrix_t = std::bitset<PIECE_WIDTH * PIECE_WIDTH>; // 4x4 by default (for Is), for others, treat this as a 3x3, setting other bits to 0

    class PieceMatrix
    {
    public:
        static piece_matrix_t get_I_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"0000111100000000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"0010001000100010"};
            case PieceRotation::R_S:
                return piece_matrix_t{"0000000011110000"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"0100010001000100"};
            }
        }

        static piece_matrix_t get_O_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"110110000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"011011000"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000011011"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"000110110"};
            }
        }

        static piece_matrix_t get_J_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"100111000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"011010010"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000111001"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"010010110"};
            }
        }

        static piece_matrix_t get_L_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"001111000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"010010011"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000111100"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"110010010"};
            }
        }

        static piece_matrix_t get_S_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"011110000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"010011001"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000011110"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"100110010"};
            }
        }

        static piece_matrix_t get_Z_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"110011000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"001011010"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000110011"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"010110100"};
            }
        }

        static piece_matrix_t get_T_matrix(PieceRotation rotation)
        {
            switch (rotation)
            {
            case PieceRotation::R_N:
                return piece_matrix_t{"010111000"};
            case PieceRotation::R_E:
                return piece_matrix_t{"010011010"};
            case PieceRotation::R_S:
                return piece_matrix_t{"000111010"};
            // case PieceRotation::R_W:
            default:
                return piece_matrix_t{"010110010"};
            }
        }

        static piece_matrix_t get_piece_matrix(PieceType type, PieceRotation rotation)
        {
            switch (type)
            {
                case PieceType::T_I:
                    return get_I_matrix(rotation);
                case PieceType::T_O:
                    return get_O_matrix(rotation);
                case PieceType::T_S:
                    return get_S_matrix(rotation);
                case PieceType::T_Z:
                    return get_Z_matrix(rotation);
                case PieceType::T_L:
                    return get_L_matrix(rotation);
                case PieceType::T_J:
                    return get_J_matrix(rotation);
                case PieceType::T_T:
                    return get_T_matrix(rotation);
            }

            throw; // FIXME: this is not explicit enough
        }

        static size_t get_piece_size(PieceType type)
        {
            switch (type)
            {
                case PieceType::T_I:
                    return 4;
                default:
                    return 3;
            }
        }

        static size_t get_inpiece_index(size_t x, size_t y, PieceType type)
        {
            size_t piece_size = get_piece_size(type);
            return y * piece_size + (piece_size - x - 1);
        }
    };
}
