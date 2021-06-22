use super::piece_type::PieceType;

type ColorT = termion::color::Rgb;

const D_CYAN: ColorT = ColorT {
    0: 0,
    1: 159,
    2: 218,
};
const D_YELLOW: ColorT = ColorT {
    0: 254,
    1: 203,
    2: 0,
};
const D_BLUE: ColorT = ColorT {
    0: 0,
    1: 101,
    2: 189,
};
const D_ORANGE: ColorT = ColorT {
    0: 255,
    1: 121,
    2: 0,
};
const D_GREEN: ColorT = ColorT {
    0: 105,
    1: 190,
    2: 40,
};
const D_RED: ColorT = ColorT {
    0: 237,
    1: 41,
    2: 57,
};
const D_PURPLE: ColorT = ColorT {
    0: 149,
    1: 45,
    2: 152,
};
const L_CYAN: ColorT = ColorT {
    0: 127,
    1: 255,
    2: 255,
};
const L_YELLOW: ColorT = ColorT {
    0: 255,
    1: 255,
    2: 127,
};
const L_BLUE: ColorT = ColorT {
    0: 100,
    1: 200,
    2: 255,
};
const L_ORANGE: ColorT = ColorT {
    0: 255,
    1: 180,
    2: 142,
};
const L_GREEN: ColorT = ColorT {
    0: 127,
    1: 255,
    2: 127,
};
const L_RED: ColorT = ColorT {
    0: 255,
    1: 145,
    2: 145,
};
const L_PURPLE: ColorT = ColorT {
    0: 215,
    1: 142,
    2: 255,
};
const WHITE: ColorT = ColorT {
    0: 255,
    1: 255,
    2: 255,
};
const DARK_GREY: ColorT = ColorT {
    0: 50,
    1: 50,
    2: 50,
};

// TODO: garbage color
pub fn get_piece_color(
    piece_type: PieceType,
    is_reset: bool,
    is_garbage: bool,
    is_ghost: bool,
) -> String {
    if is_reset {
        return WHITE.fg_string();
    }

    if is_garbage {
        return DARK_GREY.fg_string();
    }

    match piece_type {
        PieceType::TI => if is_ghost { L_CYAN } else { D_CYAN }.fg_string(),
        PieceType::TO => if is_ghost { L_YELLOW } else { D_YELLOW }.fg_string(),
        PieceType::TJ => if is_ghost { L_BLUE } else { D_BLUE }.fg_string(),
        PieceType::TL => if is_ghost { L_ORANGE } else { D_ORANGE }.fg_string(),
        PieceType::TS => if is_ghost { L_GREEN } else { D_GREEN }.fg_string(),
        PieceType::TZ => if is_ghost { L_RED } else { D_RED }.fg_string(),
        PieceType::TT => if is_ghost { L_PURPLE } else { D_PURPLE }.fg_string(),
    }
}

pub fn reset_color(f: &mut std::fmt::Formatter) -> std::fmt::Result {
    write!(f, "{}", termion::color::Fg(termion::color::Reset))
}
