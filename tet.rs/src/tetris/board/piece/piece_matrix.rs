use bit_vec::BitVec;

pub type MatrixT = BitVec;

use crate::tetris::board::piece::{piece_type::PieceType, piece_rotation::PieceRotation};

// TODO/FIXME: OH MY F*CKING G*D THIS COMPLEXITY IS HORRIBLE HOW DO I MAKE THIS STATIC ????

pub struct PieceMatrix {
}

impl PieceMatrix {
    fn get_matrix_i(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b00001111, 0b00000000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b00100010, 0b00100010]),
            PieceRotation::RS => BitVec::from_bytes(&[0b00000000, 0b11110000]),
            PieceRotation::RW => BitVec::from_bytes(&[0b01000100, 0b01000100]),
        }
    }

    fn get_matrix_o(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b1, 0b10110000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b11011000]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00011011]),
            PieceRotation::RW => BitVec::from_bytes(&[0b0, 0b00110110]),
        }
    }

    fn get_matrix_j(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b1, 0b00111000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b11010010]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00111001]),
            PieceRotation::RW => BitVec::from_bytes(&[0b0, 0b10010110]),
        }
    }

    fn get_matrix_l(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b0, 0b01111000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b10010011]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00111100]),
            PieceRotation::RW => BitVec::from_bytes(&[0b1, 0b10010010]),
        }
    }

    fn get_matrix_s(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b0, 0b11110000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b10011001]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00011110]),
            PieceRotation::RW => BitVec::from_bytes(&[0b1, 0b00110010]),
        }
    }

    fn get_matrix_z(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b1, 0b10011000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b01011010]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00110011]),
            PieceRotation::RW => BitVec::from_bytes(&[0b0, 0b10110100]),
        }
    }

    fn get_matrix_t(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => BitVec::from_bytes(&[0b0, 0b10111000]),
            PieceRotation::RE => BitVec::from_bytes(&[0b0, 0b10011010]),
            PieceRotation::RS => BitVec::from_bytes(&[0b0, 0b00111010]),
            PieceRotation::RW => BitVec::from_bytes(&[0b0, 0b10110010]),
        }
    }

    pub fn get_matrix_for(piece_type: PieceType, piece_rotation: PieceRotation) -> MatrixT {
        match piece_type {
            PieceType::TI => PieceMatrix::get_matrix_i(piece_rotation),
            PieceType::TO => PieceMatrix::get_matrix_o(piece_rotation),
            PieceType::TJ => PieceMatrix::get_matrix_j(piece_rotation),
            PieceType::TL => PieceMatrix::get_matrix_l(piece_rotation),
            PieceType::TS => PieceMatrix::get_matrix_s(piece_rotation),
            PieceType::TZ => PieceMatrix::get_matrix_z(piece_rotation),
            PieceType::TT => PieceMatrix::get_matrix_t(piece_rotation),
        }
    }

    pub fn get_piece_size(piece_type: PieceType) -> usize {
        match piece_type {
            PieceType::TI => 4,
            _ => 3,
        }
    }

    pub fn get_inpiece_index(x: usize, y: usize, piece_type: PieceType) -> usize {
        let piece_size: usize = PieceMatrix::get_piece_size(piece_type);
        y * piece_size + (piece_size - x - 1)
    }
}
