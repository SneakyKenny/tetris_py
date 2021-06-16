extern crate nanorand;
extern crate bit_vec;

mod tetris;

use tetris::board::my_board::Board;

fn main() {
    println!("Hello, world!");

    let mut board: Board = Board::new();
    print!("{}", board);

    board.move_piece(1, 0, 0);
    print!("{}", board);
}
