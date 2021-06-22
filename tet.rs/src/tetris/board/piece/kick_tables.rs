use std::ops::Shl;

use super::*;

pub type KickTableEntryT = (piece_position::PositionT, piece_position::PositionT);
pub type KickTableT = &'static [KickTableEntryT];
type KickTableArrT = &'static [&'static [KickTableEntryT]];

/*
 * Ok so this is going to be weird...
 * Fuck using tuple as key for a map !
 * So instead I'll make an array that indexes using the pair of rotation
 * Since a rotation has 4 possibilities, it takes 2 bits to store its info
 * Therefore, for 2 rotations, there are 16 possibilites, that fits on 4 bits,
 * so a char can be used.
 * Since some rotations are impossible, let's make an empty vec for it.
 * The MSB will be used to store the source, LSB will store the destination.
*/

/* NORMAL KICK TABLES */
static KICK_TABLES_NORMAL: KickTableArrT = &[
    /* NORTH KICK TABLES */
    &[],
    &[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    &[
        (0, 0),
        (1, 0),
        (2, 0),
        (1, 1),
        (2, 1),
        (-1, 0),
        (-2, 0),
        (-1, 1),
        (-2, 1),
        (0, -1),
        (3, 0),
        (-3, 0),
    ],
    &[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    /* EAST KICK TABLSE */
    &[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    &[],
    &[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    &[
        (0, 0),
        (0, 1),
        (0, 2),
        (-1, 1),
        (-1, 2),
        (0, -1),
        (0, -2),
        (-1, -1),
        (-1, -2),
        (1, 0),
        (0, 3),
        (0, -3),
    ],
    /* SOUTH KICK TABLES */
    &[
        (0, 0),
        (-1, 0),
        (-2, 0),
        (-1, -1),
        (-2, -1),
        (1, 0),
        (2, 0),
        (1, -1),
        (2, -1),
        (0, 1),
        (-3, 0),
        (3, 0),
    ],
    &[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    &[],
    &[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    /* WEST KICK TABLES */
    &[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    &[
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (0, -1),
        (0, -2),
        (1, -1),
        (1, -2),
        (-1, 0),
        (0, 3),
        (0, -3),
    ],
    &[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    &[],
];

/* I KICK TABLES*/
static KICK_TABLES_I: KickTableArrT = &[
    /* NORTH KICK TABLES */
    &[],
    &[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    &[(0, 0), (-1, 0), (-2, 0), (1, 0), (2, 0), (0, 1)],
    &[(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    /* EAST KICK TABLSE */
    &[(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    &[],
    &[(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    &[(0, 0), (0, 1), (0, 2), (0, -1), (0, -2), (-1, 0)],
    /* SOUTH KICK TABLES */
    &[(0, 0), (1, 0), (2, 0), (-1, 0), (-2, 0), (0, -1)],
    &[(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    &[],
    &[(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    /* WEST KICK TABLES */
    &[(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    &[(0, 0), (0, 1), (0, 2), (0, -1), (0, -2), (1, 0)],
    &[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    &[],
];

fn get_table_index(
    src: piece_rotation::PieceRotation,
    dst: piece_rotation::PieceRotation,
) -> usize {
    (src as usize).shl(2) | dst as usize
}

pub fn get_kick_table(
    piece_type: piece_type::PieceType,
    src: piece_rotation::PieceRotation,
    dst: piece_rotation::PieceRotation,
) -> KickTableT {
    let index: usize = get_table_index(src, dst);
    match piece_type {
        piece_type::PieceType::TI => KICK_TABLES_I[index],
        _ => KICK_TABLES_NORMAL[index],
    }
}
