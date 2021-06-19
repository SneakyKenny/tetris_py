use termion::*;

#[derive(Copy, Clone)]
pub enum PieceType {
    TI,
    TO,
    TJ,
    TL,
    TS,
    TZ,
    TT,
}

impl std::fmt::Display for PieceType {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match *self {
                PieceType::TI => "I",
                PieceType::TO => "O",
                PieceType::TJ => "J",
                PieceType::TL => "L",
                PieceType::TS => "S",
                PieceType::TZ => "Z",
                PieceType::TT => "T",
            }
        )
    }
}
