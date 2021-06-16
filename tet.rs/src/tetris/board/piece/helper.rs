use crate::tetris::board::piece::piece_position::{PiecePosition, PositionT};
use crate::tetris::board::piece::{piece_rotation::PieceRotation, piece_type::PieceType};

const SPAWN_X: PositionT = 3;
const SPAWN_Y: PositionT = 19;

pub struct Helper {}

impl Helper {
    fn get_piece_spawn_x(piece_type: PieceType) -> PositionT {
        match piece_type {
            PieceType::TO => SPAWN_X + 1,
            _ => SPAWN_X,
        }
    }

    fn get_piece_spawn_y() -> PositionT {
        SPAWN_Y
    }

    fn get_piece_spawn_r() -> PieceRotation {
        PieceRotation::RN
    }

    pub fn get_piece_spawn_position(piece_type: PieceType) -> PiecePosition {
        PiecePosition::new(
            Helper::get_piece_spawn_x(piece_type),
            Helper::get_piece_spawn_y(),
            Helper::get_piece_spawn_r(),
        )
    }
}
