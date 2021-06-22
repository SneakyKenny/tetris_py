use bit_vec::BitVec;
use nanorand::{WyRand, RNG};

use super::piece::*;

const QUEUE_DISPLAY_SIZE: usize = 5;

const BOARD_WIDTH: piece_position::PositionT = 10;
const BOARD_HEIGHT: piece_position::PositionT = 20;
const BOARD_SIZE: usize = BOARD_WIDTH as usize * BOARD_HEIGHT as usize * 2;

type BoardT = BitVec;
type OptionalTypeT = Option<piece_type::PieceType>;
type TypedBoardT = [OptionalTypeT; BOARD_SIZE];
type QueueT = std::collections::VecDeque<piece_type::PieceType>;
type HeldPieceT = OptionalTypeT;

pub struct Board {
    board: BoardT,
    piece_types: TypedBoardT,
    active_piece_type: piece_type::PieceType,
    active_piece_position: piece_position::PiecePosition,
    queue: QueueT,
    second_bag: QueueT,
    held_piece: HeldPieceT,
    has_held: bool,
    rng: WyRand,
}

// TODO: Store dropped pieces types so we can display their color

impl std::fmt::Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        piece_color::reset_color(f)?;

        write!(
            f,
            "[ {}{}{} ]",
            piece_color::get_piece_color(self.held_piece, false, false),
            if self.held_piece.is_none() {
                " ".to_string()
            } else {
                format!("{}", self.held_piece.unwrap())
            },
            piece_color::get_piece_color(None, false, false)
        )?;

        write!(f, " ")?;

        let max_len: usize = self.queue.len() + self.second_bag.len();
        for i in 0..QUEUE_DISPLAY_SIZE {
            if i >= max_len {
                break;
            }

            let queue_at_index: OptionalTypeT = self.get_queue_at(i);

            write!(
                f,
                "{}{}{}",
                piece_color::get_piece_color(queue_at_index, false, false),
                format!("{}", queue_at_index.unwrap()),
                if i + 1 < QUEUE_DISPLAY_SIZE && i + 1 < max_len {
                    " "
                } else {
                    "\r\n"
                }
            )?;
        }

        piece_color::reset_color(f)?;

        for y in (0..(BOARD_HEIGHT + 4)).rev() {
            write!(f, "{}", piece_representation::get_border())?;

            for x in 0..BOARD_WIDTH {
                let cell_state: bool = self.get_cell(x, y).unwrap();
                if cell_state {
                    write!(
                        f,
                        "{}{}",
                        piece_color::get_piece_color(self.get_cell_type(x, y), false, false), // FIXME: color is hardcoded
                        piece_representation::get_taken()
                    )?;
                } else {
                    write!(f, "{}", piece_representation::get_empty())?;
                }
            }

            piece_color::reset_color(f)?;
            write!(f, "{}\r\n", piece_representation::get_border())?;
        }

        for _ in 0..BOARD_WIDTH + 2 {
            write!(f, "{}", piece_representation::get_border())?;
        }

        write!(f, "\r\n")
    }
}

impl Board {
    pub fn new() -> Self {
        let mut board: Self = Self {
            board: BoardT::from_elem(BOARD_SIZE, false),
            piece_types: [None; BOARD_SIZE],
            active_piece_type: piece_type::PieceType::TI, // We'll set a new one right after
            active_piece_position: piece_position::PiecePosition::new(
                0,
                0,
                piece_rotation::PieceRotation::RN,
            ), // Same, this will get a new value
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

    pub fn get_cell(
        &self,
        x: piece_position::PositionT,
        y: piece_position::PositionT,
    ) -> Option<bool> {
        match Board::xy_to_index(x, y) {
            Ok(index) => Some(self.board[index]),
            Err(_) => None,
        }
    }

    pub fn set_cell(
        &mut self,
        x: piece_position::PositionT,
        y: piece_position::PositionT,
        val: bool,
    ) {
        match Board::xy_to_index(x, y) {
            Ok(index) => self.board.set(index, val),
            Err(_) => {}
        }
    }

    pub fn get_cell_type(
        &self,
        x: piece_position::PositionT,
        y: piece_position::PositionT,
    ) -> OptionalTypeT {
        match Board::xy_to_index(x, y) {
            Ok(index) => self.piece_types[index],
            Err(_) => None,
        }
    }

    pub fn set_cell_type(
        &mut self,
        x: piece_position::PositionT,
        y: piece_position::PositionT,
        val: OptionalTypeT,
    ) {
        match Board::xy_to_index(x, y) {
            Ok(index) => self.piece_types[index] = val,
            Err(_) => {}
        }
    }

    fn get_random_bag(&mut self) -> QueueT {
        let mut bag = [
            piece_type::PieceType::TI,
            piece_type::PieceType::TO,
            piece_type::PieceType::TJ,
            piece_type::PieceType::TL,
            piece_type::PieceType::TS,
            piece_type::PieceType::TZ,
            piece_type::PieceType::TT,
        ];
        self.rng.shuffle(&mut bag);

        bag.iter().copied().collect()
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

    pub fn get_queue_at(&self, index: usize) -> OptionalTypeT {
        let max_len: usize = self.queue.len() + self.second_bag.len();

        if index >= max_len {
            return None;
        }

        let size: usize = self.queue.len();
        if index < size {
            Some(self.queue[index])
        } else {
            Some(self.second_bag[index - size])
        }
    }

    fn pop_piece_from_queue(&mut self) -> piece_type::PieceType {
        self.ensure_complete_queue(false);

        self.queue.pop_front().unwrap()
    }

    pub fn spawn_next_piece(&mut self) -> bool {
        let piece_type: piece_type::PieceType = self.pop_piece_from_queue();

        self.has_held = false;

        self.spawn_piece(piece_type)
    }

    fn spawn_piece(&mut self, piece_type: piece_type::PieceType) -> bool {
        let spawn_position: piece_position::PiecePosition =
            helper::get_piece_spawn_position(piece_type);

        match self.put_piece_at(piece_type, spawn_position) {
            true => {
                self.active_piece_type = piece_type;
                self.active_piece_position = spawn_position;
                true
            }
            false => false,
        }
    }

    fn put_piece_at(
        &mut self,
        piece_type: piece_type::PieceType,
        piece_position: piece_position::PiecePosition,
    ) -> bool {
        let px: piece_position::PositionT = piece_position.get_x();
        let py: piece_position::PositionT = piece_position.get_y();

        let piece_matrix: piece_matrix::MatrixT =
            piece_matrix::get_matrix_for(piece_type, piece_position.get_rotation());

        let piece_size: usize = piece_matrix::get_piece_size(piece_type);

        let save: BoardT = self.board.clone();

        for y in 0..piece_size {
            for x in 0..piece_size {
                if !piece_matrix::test_bit(
                    piece_matrix,
                    piece_type,
                    x as piece_position::PositionT,
                    y as piece_position::PositionT,
                ) {
                    continue;
                }

                let x: piece_position::PositionT = x as piece_position::PositionT;
                let y: piece_position::PositionT = y as piece_position::PositionT;

                // FIXME: properly check both validity of position and
                // board state at this position
                if x + px >= BOARD_WIDTH
                    || y + py >= BOARD_HEIGHT * 2
                    || self.get_cell(x + px, y + py).is_none()
                    || self.get_cell(x + px, y + py).unwrap()
                {
                    self.board = save;
                    return false;
                }

                self.set_cell(x + px, y + py, true);
            }
        }

        // Set piece type
        for y in 0..piece_size as piece_position::PositionT {
            for x in 0..piece_size as piece_position::PositionT {
                if !piece_matrix::test_bit(piece_matrix, piece_type, x, y) {
                    continue;
                }

                let index: usize = Board::xy_to_index(x + px, y + py).unwrap();
                self.piece_types[index] = Some(piece_type);
            }
        }

        true
    }

    fn xy_to_index(
        x: piece_position::PositionT,
        y: piece_position::PositionT,
    ) -> Result<usize, &'static str> {
        if x < 0 || y < 0 || x >= BOARD_WIDTH || y >= BOARD_HEIGHT * 2 {
            Err("Coordinate is outside the board.")
        } else {
            Ok((y * BOARD_WIDTH + x) as usize)
        }
    }

    pub fn is_valid_move(
        &self,
        dx: piece_position::PositionT,
        dy: piece_position::PositionT,
        dr: piece_position::PositionT,
    ) -> bool {
        match (dx, dy, dr) {
            (dx, 0, 0) if dx != 0 => dx.abs() == 1,
            (0, dy, 0) if dy != 0 => dy.abs() == 1,
            (0, 0, dr) if dr != 0 => dr.abs() <= 2,
            _ => false,
        }
    }

    fn disable_current_piece(&mut self) {
        let piece_matrix: piece_matrix::MatrixT = piece_matrix::get_matrix_for(
            self.active_piece_type,
            self.active_piece_position.get_rotation(),
        );

        let piece_size: usize = piece_matrix::get_piece_size(self.active_piece_type);

        for y in 0..piece_size as piece_position::PositionT {
            for x in 0..piece_size as piece_position::PositionT {
                if !piece_matrix::test_bit(piece_matrix, self.active_piece_type, x, y) {
                    continue;
                }

                // We assume the current piece is in the board
                self.set_cell(
                    x + self.active_piece_position.get_x(),
                    y + self.active_piece_position.get_y(),
                    false,
                );
            }
        }
    }

    fn enable_current_piece(&mut self) {
        self.put_piece_at(self.active_piece_type, self.active_piece_position);
    }

    fn rotate_piece(&mut self, dr: piece_position::PositionT) -> bool {
        let new_rotation: piece_rotation::PieceRotation =
            self.active_piece_position.get_rotation().compute_add(dr);

        self.disable_current_piece();

        for kick in kick_tables::get_kick_table(
            self.active_piece_type,
            self.active_piece_position.get_rotation(),
            new_rotation,
        )
        .iter()
        {
            let new_position: piece_position::PiecePosition = piece_position::PiecePosition::new(
                kick.0 + self.active_piece_position.get_x(),
                kick.1 + self.active_piece_position.get_y(),
                new_rotation,
            );

            if self.put_piece_at(self.active_piece_type, new_position) {
                self.active_piece_position = new_position;
                return true;
            }
        }

        self.enable_current_piece();
        false
    }

    pub fn move_piece(
        &mut self,
        dx: piece_position::PositionT,
        dy: piece_position::PositionT,
        dr: piece_position::PositionT,
    ) -> bool {
        if !self.is_valid_move(dx, dy, dr) {
            return false;
        }

        if dr != 0 {
            return self.rotate_piece(dr);
        }

        self.disable_current_piece();

        let new_position: piece_position::PiecePosition = piece_position::PiecePosition::new(
            dx + self.active_piece_position.get_x(),
            dy + self.active_piece_position.get_y(),
            self.active_piece_position.get_rotation(),
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

        let piece_type: piece_type::PieceType = match self.held_piece {
            Some(piece) => piece,
            None => self.pop_piece_from_queue(),
        };

        self.held_piece = Some(self.active_piece_type);
        self.active_piece_type = piece_type;
        self.has_held = true;

        self.spawn_piece(piece_type)
    }

    fn is_line_completed(&self, y: piece_position::PositionT) -> bool {
        // TODO: optimize ffs

        for x in 0..BOARD_WIDTH {
            if !self.get_cell(x, y).unwrap() {
                return false;
            }
        }

        true
    }

    fn clear_completed_lines(&mut self) {
        let mut completed_lines: [bool; BOARD_HEIGHT as usize * 2] =
            [false; BOARD_HEIGHT as usize * 2];

        for y in 0..(BOARD_HEIGHT * 2) {
            if self.is_line_completed(y) {
                completed_lines[y as usize] = true;
            }
        }

        let mut y: piece_position::PositionT = 0;
        let mut yread: piece_position::PositionT = 0;
        let mut ywrite: piece_position::PositionT = 0;

        while y < BOARD_HEIGHT * 2 {
            while completed_lines[y as usize] {
                y += 1;
                yread += 1;
            }

            if yread >= BOARD_HEIGHT * 2 {
                while ywrite <= BOARD_HEIGHT * 2 {
                    for x in 0..BOARD_WIDTH {
                        self.set_cell(x, ywrite, false);
                        self.set_cell_type(x, ywrite, None);
                    }

                    ywrite += 1;
                }
            }

            for x in 0..BOARD_WIDTH {
                self.set_cell(x, ywrite, self.get_cell(x, yread).unwrap());
                self.set_cell_type(x, ywrite, self.get_cell_type(x, yread));
            }

            yread += 1;
            ywrite += 1;

            y += 1;
        }
    }

    pub fn lock_active_piece(&mut self) -> bool {
        self.clear_completed_lines();

        self.spawn_next_piece()
    }
}

// Ah :oe: les tests
