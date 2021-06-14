#include <iostream>
#include <sstream>

#include <ncurses.h>

#include <cstdio>
#include <unistd.h>

#include "tetris/board/board.hh"

void make_tst(tetris::board::Board& board)
{
    for (size_t i = 0; i < 13; i++)
        for (size_t j = 0; j < 10; j++)
            board.set_cell(j, i, true);

    for (size_t i = 13; i < 20; i++)
    {
        for (size_t j = 0; j < 10; j++)
        {
            if (j >= 3 && j < 6)
                continue;

            board.set_cell(j, i, true);
        }
    }

    board.set_cell(4, 13, true);
    board.set_cell(4, 15, true);

    board.set_cell(5, 13, true);
    board.set_cell(5, 14, true);
    board.set_cell(5, 15, true);

    board.set_cell(3, 17, true);

    std::cout << board.spawn_next_piece() << std::endl;

    // std::cout << board << std::endl;

    board.move_piece(0, 0, -1);
    board.move_piece(1, 0, 0);

    while (board.move_piece(0, -1, 0));

    board.move_piece(0, 0, 1);

    board.move_piece(0, 0, 1);
}

void init_ncurses()
{
    // Init ncurses
    initscr();

    // Setup random sh*t
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    // Non-blocking I/O
    timeout(0);
}

int main(/* int argc, char **argv */)
{
    init_ncurses();

    // Do the thing
    tetris::board::Board board;
    board.spawn_next_piece();
    std::stringstream ss{};

    // Wait input and bail
    while (true)
    {
        if (!board.move_piece(0, -1, 0))
        {
            board.lock_active_piece();
            if (!board.spawn_next_piece())
                board = tetris::board::Board{};
        }

        int ch = getch();
        switch (ch)
        {
            // Game inputs

                // Rotation
        case 'i':
        case KEY_UP:
            board.move_piece( 0,  0,  1);
            break;
        case 'x':
            board.move_piece( 0,  0,  2);
            break;
        case 'z':
            board.move_piece( 0,  0, -1);
            break;

                // Movements
        case 'j':
        case KEY_LEFT:
            board.move_piece(-1,  0,  0);
            break;
        case 'l':
        case KEY_RIGHT:
            board.move_piece( 1,  0,  0);
            break;

                // Drop
        case 'k':
        case KEY_DOWN:
            board.move_piece( 0, -1,  0);
            break;
        case ' ':
            while (board.move_piece(0, -1, 0));
            break;

                // Hold
        case 'c':
            board.hold_active_piece();
            break;

            // Other inputs

                // Freeze the game
        case 'f':
            while (getch() != 'f');
            break;

                // General inputs
        case 'r':
            board = tetris::board::Board{};
            break;
        case 'q':
            goto end;
        }

        ss.str(std::string());
        ss << board << std::endl;
        move(0, 0);
        printw(ss.str().c_str());

        // Actually print
        refresh();
        // usleep(100000);
        usleep(160000);
    }

end:
    endwin();

    /*
    while (board.move_piece(-1, 0, 0));
    while (board.move_piece(0, -1, 0));

    std::cout << board.spawn_next_piece() << std::endl;
    while (board.move_piece(1, 0, 0));
    while (board.move_piece(0, -1, 0));

    std::cout << board.spawn_next_piece() << std::endl;
    while (board.move_piece(0, -1, 0));

    std::cout << board.spawn_next_piece() << std::endl;
    while (board.move_piece(0, -1, 0));
    */

    /*
    while (true)
        tetris::play_game();
    */
}
