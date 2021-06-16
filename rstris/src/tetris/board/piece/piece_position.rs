use crate::tetris::board::piece::piece_rotation::PieceRotation;

#[derive(Copy, Clone)]
pub struct PiecePosition {
    x: usize,
    y: usize,
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
    pub fn new(x: usize, y: usize, r: PieceRotation) -> Self {
        Self {
            x: x,
            y: y,
            r: r,
        }
    }

    pub fn get_x(self) -> usize {
        self.x
    }

    pub fn get_y(self) -> usize {
        self.y
    }

    pub fn get_rotation(self) -> PieceRotation {
        self.r
    }
}
