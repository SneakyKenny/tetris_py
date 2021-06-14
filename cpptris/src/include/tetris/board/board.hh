#pragma once

#include <bitset>
#include <deque>

#include "tetris/board/piece/kick_tables.hh"
#include "tetris/board/piece/piece_helper.hh"
#include "tetris/board/piece/piece_matrix.hh"
#include "tetris/board/piece/piece_position.hh"
#include "tetris/board/piece/piece_representation.hh"
#include "tetris/board/piece/piece_rotation.hh"
#include "tetris/board/piece/piece_type.hh"

#ifdef BIGMODE
# define BOARD_WIDTH 5
# define BOARD_HEIGHT 10
#else
# define BOARD_WIDTH 10
# define BOARD_HEIGHT 20
#endif /* !BIGMODE */

#define PIECE_QUEUE_DISPLAY_LENGTH 5
#define PIECE_QUEUE_BAG_SIZE 7

namespace tetris::board
{
    using board_t = std::bitset<BOARD_WIDTH * BOARD_HEIGHT * 2>;
    using piece_queue_t = std::deque<piece::PieceType>;

    class Board
    {
    public:
        Board();

        bool get_cell(size_t x, size_t y) const;
        void set_cell(size_t x, size_t y, bool val);

        piece::PieceType get_queue_at(size_t i) const;
        size_t get_queue_size() const;

        bool is_valid_move(char dx, char dy, char dr) const;
        bool move_piece(char dx, char dy, char dr);

        bool spawn_next_piece();
        bool lock_active_piece();

    private:
        board_t board_;
        piece::PieceType active_piece_type_;
        piece::PiecePosition active_piece_position_;
        piece_queue_t queue_;
        piece_queue_t second_bag_;

        void ensure_complete_queue(bool init = false);
        size_t xy_to_i(size_t x, size_t y) const;
        void disable_current_piece();
        bool put_piece_at(piece::PieceType type, piece::PiecePosition position);
        bool rotate_piece(char dr);
        size_t clear_completed_lines();
    };

    std::ostream& operator<<(std::ostream& o, const Board& b);
}
