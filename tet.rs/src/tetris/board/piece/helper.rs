const SPAWN_X: usize = 3;
const SPAWN_Y: usize = 19;

use crate::tetris::board::piece::{piece_type::PieceType, piece_position::PiecePosition, piece_rotation::PieceRotation};

pub struct Helper {

}

impl Helper {
    fn get_piece_spawn_x(piece_type: PieceType) -> usize {
        match piece_type {
            _ => SPAWN_X,
        }
    }

    fn get_piece_spawn_y(piece_type: PieceType) -> usize {
        match piece_type {
            _ => SPAWN_Y,
        }
    }

    fn get_piece_spawn_r(piece_type: PieceType) -> PieceRotation {
        match piece_type {
            _ => PieceRotation::RN,
        }
    }

    pub fn get_piece_spawn_position(piece_type: PieceType) -> PiecePosition {
        PiecePosition::new(Helper::get_piece_spawn_x(piece_type),
                           Helper::get_piece_spawn_y(piece_type),
                           Helper::get_piece_spawn_r(piece_type))
    }
}
