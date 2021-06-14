#include "tetris/board/board.hh"

#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <iostream>
#include <random>

#include "utype.hh"

namespace tetris::board
{
    Board::Board()
        : active_piece_position_(0, 0) /* FIXME: this is ugly */
    {
        ensure_complete_queue(true);
        spawn_next_piece();
    }

    void Board::ensure_complete_queue(bool init)
    {
        static std::random_device rd;
        static std::mt19937 g(rd());

        if (init)
        {
            for (size_t i = 0; i < PIECE_QUEUE_BAG_SIZE; i++)
                second_bag_.push_back(static_cast<piece::PieceType>(i));

            std::shuffle(second_bag_.begin(), second_bag_.end(), g);
        }

        if (queue_.size() == 0)
        {
            // Swap empty current queue with full secondary bag
            std::swap(queue_, second_bag_);

            // fill secondary bag
            for (size_t i = 0; i < PIECE_QUEUE_BAG_SIZE; i++)
                second_bag_.push_back(static_cast<piece::PieceType>(i));

            // shuffle second bag
            std::shuffle(second_bag_.begin(), second_bag_.end(), g);
        }

        /*
        std::cout << "Queue after ensure_complete_queue:" << std::endl;
        for (auto const& p : queue_)
            std::cout << utils::utype(p) << " ";

        std::cout << std::endl << "Secondary queue:" << std::endl;
        for (auto const& p : second_bag_)
            std::cout << utils::utype(p) << " ";

        std::cout << std::endl;
        */
    }

    bool Board::get_cell(size_t x, size_t y) const
    {
        assert(x < BOARD_WIDTH);
        assert(y < BOARD_HEIGHT * 2);
        return board_.test(xy_to_i(x, y));
    }

    void Board::set_cell(size_t x, size_t y, bool val)
    {
        assert(x < BOARD_WIDTH);
        assert(y < BOARD_HEIGHT * 2);
        board_.set(xy_to_i(x, y), val);
    }

    piece::PieceType Board::get_queue_at(size_t i) const
    {
        size_t size = queue_.size();
        return i < size ? queue_.at(i) : second_bag_.at(i - size);
    }

    bool Board::spawn_next_piece()
    {
        ensure_complete_queue();

        piece::PieceType piece_type = queue_.front();
        queue_.pop_front();

        /*
        std::cout << utils::utype(piece_type) << std::endl
            << "This piece will spawn at "
            << piece::PieceHelper::get_piece_spawn_position(piece_type)
            << std::endl;
        */

        piece::PiecePosition spawn_position =
            piece::PieceHelper::get_piece_spawn_position(piece_type);

        // spawn_position = piece::PiecePosition(-1, 20, piece::PieceRotation::R_N);

        if (!put_piece_at(piece_type, spawn_position))
            return false;

        active_piece_type_ = piece_type;
        active_piece_position_ = spawn_position;

        return true;
    }

    // TODO: optimize this shit, like... it sooooo bad
    size_t Board::clear_completed_lines()
    {
        board_t mask{"1111111111"}; // 10 '1's for a complete line mask

        std::array<bool, BOARD_HEIGHT * 2> completed_lines;
        for (size_t i = 0; i < completed_lines.size(); i++)
            completed_lines.at(i) = false;

        for (size_t y = 0; y < BOARD_HEIGHT * 2; y++) // FIXME: x2 for hidden lines ?
        {
            board_t cp = mask;

            if ((cp & board_).count() == 10)
                completed_lines.at(y) = true;

            mask <<= 10;
        }

        size_t yw = 0;
        size_t yr = 0;

        for (size_t y = 0; y < BOARD_HEIGHT * 2; y++)
        {
            while (completed_lines.at(y))
            {
                y++;
                yr++;
            }

            if (yr >= BOARD_HEIGHT * 2)
            {
                for (; yw < BOARD_HEIGHT * 2; yw++)
                    for (size_t x = 0; x < BOARD_WIDTH; x++)
                        set_cell(x, yw, 0);

                break;
            }

            for (size_t x = 0; x < BOARD_WIDTH; x++)
                set_cell(x, yw, get_cell(x, yr));

            yw++;
            yr++;
        }

        return completed_lines.size();
    }

    bool Board::lock_active_piece()
    {
        clear_completed_lines();

        return true;
    }

    void Board::disable_current_piece()
    {
        piece::piece_matrix_t piece_matrix = piece::PieceMatrix::get_piece_matrix(
                active_piece_type_, active_piece_position_.get_rotation());

        size_t piece_size = piece::PieceMatrix::get_piece_size(active_piece_type_);

        for (size_t y = 0; y < piece_size; y++)
        {
            for (size_t x = 0; x < piece_size; x++)
            {
                size_t inpiece_index = piece::PieceMatrix::
                    get_inpiece_index(x, y, active_piece_type_);

                if (!piece_matrix.test(inpiece_index))
                    continue;

                size_t index = xy_to_i(x + active_piece_position_.get_x(),
                        y + active_piece_position_.get_y());

                board_.set(index, false);
            }
        }
    }

    bool Board::is_valid_move(char dx, char dy, char dr) const
    {
        // Check only one of dx, dy, or dr is set. Also,
        // check dx, dy is one of [-1, 1], dr in [-2, -1, 1, 2] as well

        if ((dx && (dy || dr))
                || (dy && (dx || dr))
                || (dr && (dx || dy)))
        {
            std::cerr << "The fuck are you doing ?" << std::endl;
            return false;
        }

        if (dr)
            return std::abs(dr) <= 2;

        return std::abs(dx ? dx : dy) == 1;
    }

    bool Board::rotate_piece(char dr)
    {
        piece::PieceRotation new_rotation = active_piece_position_.get_rotation() + dr;
        /*
        std::cout << "rotation is now: " << new_rotation << std::endl;
        std::cout << "matrix is: "
            << piece::PieceMatrix::get_piece_matrix(active_piece_type_, new_rotation)
            << std::endl
            << piece::PieceHelper::piece_to_string(active_piece_type_, new_rotation)
            << std::endl;
        */

        disable_current_piece();

        // - Get kick table corresponding to the active piece
        piece::kick_table_t kick_table = piece::get_kick_table(
                active_piece_type_, active_piece_position_.get_rotation(), new_rotation);

        // - Test each kick offset
        for (auto const& kick : kick_table)
        {
            /*
            std::cout << "trying kick: "
                    << kick.first << ", " << kick.second
                    << std::endl;
            */

            piece::PiecePosition new_position{
                active_piece_position_.get_x() + kick.first,
                active_piece_position_.get_y() + kick.second,
                new_rotation
            };

            if (put_piece_at(active_piece_type_, new_position))
            {
                /*
                std::cout << "rotation succeeded for kick: "
                    << kick.first << ", " << kick.second
                    << std::endl;
                */

                active_piece_position_ = new_position;
                return true;
            }

            /*
            std::cout << "rotation failed for kick: "
                    << kick.first << ", " << kick.second
                    << std::endl;
            */
        }

        // Restore active piece
        put_piece_at(active_piece_type_, active_piece_position_);
        return false;
    }

    bool Board::move_piece(char dx, char dy, char dr)
    {
        if (!is_valid_move(dx, dy, dr))
            return false;

        if (dr)
            return rotate_piece(dr);

        disable_current_piece();

        piece::PiecePosition new_position = piece::PiecePosition(
            active_piece_position_.get_x() + dx,
            active_piece_position_.get_y() + dy,
            active_piece_position_.get_rotation()
        );

        if (!put_piece_at(active_piece_type_, new_position))
        {
            put_piece_at(active_piece_type_, active_piece_position_);
            return false;
        }

        active_piece_position_ = new_position;

        return true;
    }

    bool Board::put_piece_at(piece::PieceType type, piece::PiecePosition position)
    {
        piece::piece_matrix_t piece_matrix =
            piece::PieceMatrix::get_piece_matrix(type, position.get_rotation());

        // std::cout << piece::PieceHelper::piece_to_string(type, position.get_rotation()) << std::endl;

        size_t piece_size = piece::PieceMatrix::get_piece_size(type);

        board_t save = board_;

        for (size_t y = 0; y < piece_size; y++)
        {
            for (size_t x = 0; x < piece_size; x++)
            {
                size_t inpiece_index = piece::PieceMatrix::get_inpiece_index(x, y, type);

                bool cell_state = piece_matrix.test(inpiece_index);

                if (!cell_state)
                    continue;

                if (x + position.get_x() >= BOARD_WIDTH
                        || y + position.get_y() >= BOARD_HEIGHT * 2)
                {
                    board_ = save;
                    return false;
                }

                size_t index = xy_to_i(x + position.get_x(), y + position.get_y());

                // TODO: Check we're not out of bounds
                if (board_.test(index) && cell_state)
                {
                    board_ = save;
                    return false;
                }

                board_.set(index, cell_state);
            }
        }

        return true;
    }

    size_t Board::xy_to_i(size_t x, size_t y) const
    {
        return y * BOARD_WIDTH + x;
    }

    std::ostream& operator<<(std::ostream& o, const Board& b)
    {
        // TODO: Draw margin ?
        for (size_t i = 0; i < PIECE_QUEUE_DISPLAY_LENGTH; i++)
        {
            o << b.get_queue_at(i);

            if (i + 1 < PIECE_QUEUE_DISPLAY_LENGTH)
                o << piece::PieceRepresentation::get_empty();
            else
                o << std::endl;
        }

        for (ssize_t y = BOARD_HEIGHT + 2; y >= 0; y--)
        {
            o << piece::PieceRepresentation::get_border();

            for (size_t x = 0; x < BOARD_WIDTH; x++)
            {
                o << (b.get_cell(x, y)
                    ? piece::PieceRepresentation::get_taken()
                    : piece::PieceRepresentation::get_empty());
            }

            o << piece::PieceRepresentation::get_border()
                << std::endl;
        }

        for (ssize_t x = -1; x <= BOARD_WIDTH; x++)
            o << piece::PieceRepresentation::get_border();

        return o;
    }
}
