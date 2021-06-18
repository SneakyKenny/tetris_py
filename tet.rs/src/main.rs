mod tetris;

use tetris::board::my_board::Board;

fn main() {
    println!("Hello, world!");

    let mut board: Board = Board::new();
    print!("{}", board);

    board.move_piece(0, 0, -1);
    print!("{}", board);

    board.hold_active_piece();
    print!("{}", board);
}
