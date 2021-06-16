use nanorand::{RNG, WyRand};
use bit_vec::BitVec;

use crate::tetris::board::piece::{piece_type::PieceType, piece_position::PiecePosition, piece_rotation::PieceRotation, helper::Helper};
use crate::tetris::board::piece::piece_matrix::{PieceMatrix, MatrixT};

type BoardT = BitVec;
type QueueT = std::collections::VecDeque<PieceType>;
type HeldPieceT = Option<self::PieceType>;

const BOARD_WIDTH: usize = 10;
const BOARD_HEIGHT: usize = 20;

pub struct Board
{
    board: BoardT,
    active_piece_type: PieceType,
    active_piece_position: PiecePosition,
    queue: QueueT,
    second_bag: QueueT,
    held_piece: HeldPieceT,
    has_held: bool,
    rng: WyRand,
}

impl std::fmt::Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        Ok(()) // TODO
    }
}

impl Board {
    pub fn new() -> Self {
        let mut board: Self = Self {
            board: BoardT::with_capacity(BOARD_WIDTH * BOARD_HEIGHT * 2),
            active_piece_type: PieceType::TI, // We'll set a new one right after
            active_piece_position: PiecePosition::new(0, 0, PieceRotation::RN), // Same, this will get a new value
            queue: QueueT::new(),
            second_bag: QueueT::new(),
            held_piece: None,
            has_held: false,
            rng: WyRand::new(),
        };

        board.ensure_complete_queue(true);
        board.spawn_next_piece();

        board
    }

    fn get_random_bag(&mut self) -> QueueT {
        let mut bag = [PieceType::TI, PieceType::TO, PieceType::TJ,
                       PieceType::TL, PieceType::TS, PieceType::TZ,
                       PieceType::TT];
        self.rng.shuffle(&mut bag);

        let mut resulting_bag = QueueT::with_capacity(bag.len());
        for piece in bag.iter() {
            resulting_bag.push_back(*piece);
        }

        resulting_bag
    }

    fn ensure_complete_queue(&mut self, is_init: bool) {

        if is_init {
            self.second_bag = self.get_random_bag();
        }

        if self.queue.len() == 0 {
            for _ in 0..self.second_bag.len() {
                self.queue.push_back(self.second_bag.pop_front().unwrap());
            }

            self.second_bag = self.get_random_bag();
        }
    }

    fn pop_piece_from_queue(&mut self) -> PieceType {
        self.ensure_complete_queue(false);

        self.queue.pop_front().unwrap()
    }

    pub fn spawn_next_piece(&mut self) -> bool {
        let piece_type: PieceType = self.pop_piece_from_queue();

        self.has_held = false;

        self.spawn_piece(piece_type)
    }

    fn spawn_piece(&mut self, piece_type: PieceType) -> bool {
        let spawn_position: PiecePosition =
            Helper::get_piece_spawn_position(piece_type);

        match self.put_piece_at(piece_type, spawn_position) {
            true => {
                self.active_piece_type = piece_type;
                self.active_piece_position = spawn_position;
                true
            },
            false => false,
        }
    }

    fn put_piece_at(&mut self, piece_type: PieceType, piece_position: PiecePosition) -> bool {
        let px: usize = piece_position.get_x();
        let py: usize = piece_position.get_y();

        let piece_matrix: MatrixT = PieceMatrix::get_matrix_for(piece_type, piece_position.get_rotation());

        let piece_size: usize = PieceMatrix::get_piece_size(piece_type);

        let save: BoardT = self.board.clone();

        for y in 0..piece_size {
            for x in 0..piece_size {
                let inpiece_index = PieceMatrix::get_inpiece_index(x, y, piece_type);

                let cell_state: bool = piece_matrix[inpiece_index];

                if !cell_state {
                    continue;
                }

                // TODO: make rust understand overflowing is ok
                let index: usize = Board::xy_to_index(x + px, y + py);

                if x + px >= BOARD_WIDTH || y + py >= BOARD_HEIGHT * 2
                    || self.board[index] {
                    self.board = save;
                    return false;
                }

                self.board.set(index, true);
            }
        }

        true
    }

    fn xy_to_index(x: usize, y: usize) -> usize {
        y * BOARD_WIDTH + x
    }
}
