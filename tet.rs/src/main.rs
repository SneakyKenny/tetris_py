mod tetris;

use tetris::board::my_board::Board;

fn main() {
    println!("Hello, world!");

    let mut board: Board = Board::new();

    board.hold_active_piece();

    board.move_piece(0, 0, -1);
    while board.move_piece(1, 0, 0) {}
    board.move_piece(0, -1, 0);
    board.move_piece(0, -1, 0);
    board.move_piece(0, -1, 0);

    board.lock_active_piece();

    print!("{}", board);
}
