pub type MatrixT = u16;

use super::{
    piece_position::PositionT,
    piece_rotation::PieceRotation,
    piece_type::PieceType,
};

const IN: u16 = 0b0000_1111_0000_0000;
const IE: u16 = 0b0010_0010_0010_0010;
const IS: u16 = 0b0000_0000_1111_0000;
const IW: u16 = 0b0100_0100_0100_0100;

const ON: u16 = 0b1_1011_0000;
const OE: u16 = 0b0_1101_1000;
const OS: u16 = 0b0_0001_1011;
const OW: u16 = 0b0_0011_0110;

const JN: u16 = 0b1_0011_1000;
const JE: u16 = 0b0_1101_0010;
const JS: u16 = 0b0_0011_1001;
const JW: u16 = 0b0_1001_0110;

const LN: u16 = 0b0_0111_1000;
const LE: u16 = 0b0_1001_0011;
const LS: u16 = 0b0_0011_1100;
const LW: u16 = 0b1_1001_0010;

const SN: u16 = 0b0_1111_0000;
const SE: u16 = 0b0_1001_1001;
const SS: u16 = 0b0_0001_1110;
const SW: u16 = 0b1_0011_0010;

const ZN: u16 = 0b1_1001_1000;
const ZE: u16 = 0b0_0101_1010;
const ZS: u16 = 0b0_0011_0011;
const ZW: u16 = 0b0_1011_0100;

const TN: u16 = 0b0_1011_1000;
const TE: u16 = 0b0_1001_1010;
const TS: u16 = 0b0_0011_1010;
const TW: u16 = 0b0_1011_0010;

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
        PieceType::TI => get_matrix_i(piece_rotation),
        PieceType::TO => get_matrix_o(piece_rotation),
        PieceType::TJ => get_matrix_j(piece_rotation),
        PieceType::TL => get_matrix_l(piece_rotation),
        PieceType::TS => get_matrix_s(piece_rotation),
        PieceType::TZ => get_matrix_z(piece_rotation),
        PieceType::TT => get_matrix_t(piece_rotation),
    }
}

pub fn get_piece_size(piece_type: PieceType) -> usize {
    match piece_type {
        PieceType::TI => 4,
        _ => 3,
    }
}

pub fn get_inpiece_index(x: PositionT, y: PositionT, piece_type: PieceType) -> usize {
    let piece_size: usize = get_piece_size(piece_type);
    y as usize * piece_size + (piece_size - x as usize - 1)
}

pub fn test_bit(matrix: MatrixT, piece_type: PieceType, x: PositionT, y: PositionT) -> bool {
    let inpiece_index: usize = get_inpiece_index(x, y, piece_type);
    matrix & (1 << inpiece_index) != 0
}
