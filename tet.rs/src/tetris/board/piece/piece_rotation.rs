use super::piece_position::PositionT;

#[derive(Copy, Clone)]
pub enum PieceRotation {
    RN,
    RE,
    RS,
    RW,
}

impl std::fmt::Display for PieceRotation {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match *self {
                PieceRotation::RN => "N",
                PieceRotation::RE => "E",
                PieceRotation::RS => "S",
                PieceRotation::RW => "W",
            }
        )
    }
}

impl PieceRotation {
    pub fn compute_add(&self, dr: PositionT) -> Self {
        let ulhs: PositionT = *self as PositionT;

        let mut new_rotation_num: PositionT = (ulhs + dr) % 4;
        while new_rotation_num < 0 {
            new_rotation_num += 4;
        }

        match new_rotation_num {
            0 => PieceRotation::RN,
            1 => PieceRotation::RE,
            2 => PieceRotation::RS,
            // 3
            _ => PieceRotation::RW,
        }
    }
}
