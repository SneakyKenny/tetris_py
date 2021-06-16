use crate::tetris::board::piece::piece_rotation::PieceRotation;

pub type PositionT = i16;

#[derive(Copy, Clone)]
pub struct PiecePosition {
    x: PositionT,
    y: PositionT,
    r: PieceRotation,
}

impl std::fmt::Display for PiecePosition {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.r)
    }
}

impl std::ops::Add for PiecePosition {
    type Output = Self;

    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            r: self.r, // since we'll use this with kick tables, don't rotate, only move
        }
    }
}

impl PiecePosition {
    pub fn new(x: PositionT, y: PositionT, r: PieceRotation) -> Self {
        Self { x, y, r }
    }

    pub fn get_x(self) -> PositionT {
        self.x
    }

    pub fn get_y(self) -> PositionT {
        self.y
    }

    pub fn get_rotation(self) -> PieceRotation {
        self.r
    }
}
