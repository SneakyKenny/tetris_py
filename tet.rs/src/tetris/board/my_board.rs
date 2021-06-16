use nanorand::{RNG, WyRand};
use bit_vec::BitVec;

use crate::tetris::board::piece::{piece_type::PieceType, piece_representation::PieceRepresentation, piece_rotation::PieceRotation, helper::Helper};
use crate::tetris::board::piece::piece_matrix::{PieceMatrix, MatrixT};
use crate::tetris::board::piece::piece_position::{PiecePosition, PositionT};

type BoardT = BitVec;
type QueueT = std::collections::VecDeque<PieceType>;
type HeldPieceT = Option<self::PieceType>;

const BOARD_WIDTH: PositionT = 10;
const BOARD_HEIGHT: PositionT = 20;
const QUEUE_DISPLAY_SIZE: usize = 5;

pub struct Board {
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
        match self.held_piece {
            Some(piece) => write!(f, "[ {} ]", piece),
            None => write!(f, "[   ]"),
        }?;

        write!(f, " ")?;

        for i in 0..QUEUE_DISPLAY_SIZE {
            write!(f, "{}{}",
                self.get_queue_at(i),
                if i + 1 < QUEUE_DISPLAY_SIZE { " " } else { "\n" }
            )?;
        }

        for y in (0..(BOARD_HEIGHT + 4)).rev() {
            write!(f, "{}", PieceRepresentation::get_border())?;

            for x in 0..BOARD_WIDTH {
                write!(f, "{}", if self.get_cell(x, y) {
                    PieceRepresentation::get_taken()
                } else {
                    PieceRepresentation::get_empty()
                })?;
            }

            writeln!(f, "{}", PieceRepresentation::get_border())?;
        }

        for _ in 0..BOARD_WIDTH + 2 {
            write!(f, "{}", PieceRepresentation::get_border())?;
        }

        writeln!(f)?;

        Ok(())
    }
}

impl Board {
    pub fn new() -> Self {
        let mut board: Self = Self {
            board: BoardT::from_elem((BOARD_WIDTH * BOARD_HEIGHT * 2) as usize, false),
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

    pub fn get_cell(&self, x: PositionT, y: PositionT) -> bool {
        let index: usize = Board::xy_to_index(x, y);
        self.board[index]
    }

    pub fn set_cell(&mut self, x: PositionT, y: PositionT, val: bool) {
        let index: usize = Board::xy_to_index(x, y);
        self.board.set(index, val);
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

        if self.queue.is_empty() {
            for _ in 0..self.second_bag.len() {
                self.queue.push_back(self.second_bag.pop_front().unwrap());
            }

            self.second_bag = self.get_random_bag();
        }
    }

    pub fn get_queue_at(&self, index: usize) -> PieceType {
        let size: usize = self.queue.len();
        if index < size {
            self.queue[index]
        } else {
            self.second_bag[index - size]
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
        let px: PositionT = piece_position.get_x();
        let py: PositionT = piece_position.get_y();

        let piece_matrix: MatrixT = PieceMatrix::get_matrix_for(piece_type, piece_position.get_rotation());

        let piece_size: usize = PieceMatrix::get_piece_size(piece_type);

        let save: BoardT = self.board.clone();

        for y in 0..piece_size {
            for x in 0..piece_size {
                if !PieceMatrix::test_bit(piece_matrix, piece_type, x as PositionT, y as PositionT) {
                    continue;
                }

                let x: PositionT = x as PositionT;
                let y: PositionT = y as PositionT;

                if x + px >= BOARD_WIDTH || y + py >= BOARD_HEIGHT * 2
                    || self.get_cell(x, y) {
                    self.board = save;
                    return false;
                }

                self.set_cell(x + px, y + py, true);
            }
        }

        true
    }

    fn xy_to_index(x: PositionT, y: PositionT) -> usize {
        // TODO: assert coordinates are valid
        (y * BOARD_WIDTH + x) as usize
    }

    pub fn is_valid_move(&self, dx: PositionT, dy: PositionT, dr: PositionT) -> bool {
        if dx != 0 && dy != 0 || dx != 0 && dr != 0 || dy != 0 && dr != 0 {
            return false;
        }

        if dr != 0 {
            dr.abs() <= 2
        } else if dx != 0 {
            dx.abs() == 1
        } else {
            dy.abs() == 1
        }
    }

    pub fn disable_current_piece(&mut self) {
        let piece_matrix: MatrixT = PieceMatrix::get_matrix_for(self.active_piece_type, self.active_piece_position.get_rotation());

        let piece_size: usize = PieceMatrix::get_piece_size(self.active_piece_type);

        for y in 0..piece_size as PositionT {
            for x in 0..piece_size as PositionT {
                if !PieceMatrix::test_bit(piece_matrix, self.active_piece_type, x, y) {
                    continue;
                }

                // We assume the current piece is in the board
                self.set_cell(
                    x + self.active_piece_position.get_x(),
                    y + self.active_piece_position.get_y(),
                    false
                );
            }
        }
    }

    pub fn move_piece(&mut self, dx: PositionT, dy: PositionT, dr: PositionT) -> bool {
        if !self.is_valid_move(dx, dy, dr) {
            return false;
        }

        if dr != 0 {
            // return self.rotate_piece(dr); // TODO
            return true;
        }

        self.disable_current_piece();

        let new_position: PiecePosition = PiecePosition::new(
            dx + self.active_piece_position.get_x(),
            dy + self.active_piece_position.get_y(),
            self.active_piece_position.get_rotation()
        );

        if self.put_piece_at(self.active_piece_type, new_position) {
            self.active_piece_position = new_position;
            true
        } else {
            self.put_piece_at(self.active_piece_type, self.active_piece_position);
            false
        }
    }

    pub fn hold_active_piece(&mut self) -> bool {
        if self.has_held {
            return false;
        }

        self.disable_current_piece();

        let piece_type: PieceType = match self.held_piece {
            Some(piece) => piece,
            None => self.pop_piece_from_queue(),
        };

        self.held_piece = Some(self.active_piece_type);
        self.active_piece_type = piece_type;
        self.has_held = true;

        self.spawn_piece(piece_type)
    }
}

// Ah :oe: les tests
