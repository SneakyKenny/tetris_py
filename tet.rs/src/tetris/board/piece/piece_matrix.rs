pub type MatrixT = u16;

use crate::tetris::board::piece::{
    piece_position::PositionT, piece_rotation::PieceRotation, piece_type::PieceType,
};

const IN: u16 = 0b0000111100000000;
const IE: u16 = 0b0010001000100010;
const IS: u16 = 0b0000000011110000;
const IW: u16 = 0b0100010001000100;

const ON: u16 = 0b110110000;
const OE: u16 = 0b011011000;
const OS: u16 = 0b000011011;
const OW: u16 = 0b000110110;

const JN: u16 = 0b100111000;
const JE: u16 = 0b011010010;
const JS: u16 = 0b000111001;
const JW: u16 = 0b010010110;

const LN: u16 = 0b001111000;
const LE: u16 = 0b010010011;
const LS: u16 = 0b000111100;
const LW: u16 = 0b110010010;

const SN: u16 = 0b011110000;
const SE: u16 = 0b010011001;
const SS: u16 = 0b000011110;
const SW: u16 = 0b100110010;

const ZN: u16 = 0b110011000;
const ZE: u16 = 0b001011010;
const ZS: u16 = 0b000110011;
const ZW: u16 = 0b010110100;

const TN: u16 = 0b010111000;
const TE: u16 = 0b010011010;
const TS: u16 = 0b000111010;
const TW: u16 = 0b010110010;

pub struct PieceMatrix {}

impl PieceMatrix {
    fn get_matrix_i(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => IN,
            PieceRotation::RE => IE,
            PieceRotation::RS => IS,
            PieceRotation::RW => IW,
        }
    }

    fn get_matrix_o(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => ON,
            PieceRotation::RE => OE,
            PieceRotation::RS => OS,
            PieceRotation::RW => OW,
        }
    }

    fn get_matrix_j(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => JN,
            PieceRotation::RE => JE,
            PieceRotation::RS => JS,
            PieceRotation::RW => JW,
        }
    }

    fn get_matrix_l(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => LN,
            PieceRotation::RE => LE,
            PieceRotation::RS => LS,
            PieceRotation::RW => LW,
        }
    }

    fn get_matrix_s(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => SN,
            PieceRotation::RE => SE,
            PieceRotation::RS => SS,
            PieceRotation::RW => SW,
        }
    }

    fn get_matrix_z(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => ZN,
            PieceRotation::RE => ZE,
            PieceRotation::RS => ZS,
            PieceRotation::RW => ZW,
        }
    }

    fn get_matrix_t(piece_rotation: PieceRotation) -> MatrixT {
        match piece_rotation {
            PieceRotation::RN => TN,
            PieceRotation::RE => TE,
            PieceRotation::RS => TS,
            PieceRotation::RW => TW,
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

    pub fn get_inpiece_index(x: PositionT, y: PositionT, piece_type: PieceType) -> usize {
        let piece_size: usize = PieceMatrix::get_piece_size(piece_type);
        y as usize * piece_size + (piece_size - x as usize - 1)
    }

    pub fn test_bit(matrix: MatrixT, piece_type: PieceType, x: PositionT, y: PositionT) -> bool {
        let inpiece_index: usize = PieceMatrix::get_inpiece_index(x, y, piece_type);
        matrix & (1 << inpiece_index) != 0
    }
}
