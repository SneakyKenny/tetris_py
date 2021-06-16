#[derive(Copy, Clone)]
pub enum PieceRotation {
    RN,
    RE,
    RS,
    RW,
}

impl std::fmt::Display for PieceRotation {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", match *self {
            PieceRotation::RN => "N",
            PieceRotation::RE => "E",
            PieceRotation::RS => "S",
            PieceRotation::RW => "W",
        })
    }
}

impl PieceRotation {
    // TODO: add a PieceRotation and an int
}
