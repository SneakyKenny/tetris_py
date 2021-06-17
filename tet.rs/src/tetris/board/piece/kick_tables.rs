use std::ops::Shl;

use crate::tetris::board::piece::{
    piece_type::PieceType,
    piece_rotation::PieceRotation,
    piece_position::PositionT
};

pub type KickTableT = std::vec::Vec<(PositionT, PositionT)>;

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

pub struct KickTables {
}

impl KickTables {
    fn get_table_index(src: PieceRotation, dst: PieceRotation) -> usize {
        (src as usize).shl(2) | dst as usize
    }

    pub fn get_kick_table(piece_type: PieceType, src: PieceRotation, dst: PieceRotation) -> KickTableT {
        let index: usize = KickTables::get_table_index(src, dst);
        match piece_type {
            PieceType::TI => KickTables::get_kick_table_i(index),
            _ => KickTables::get_kick_table_normal(index),
        }
    }

    fn get_kick_table_normal(index: usize) -> KickTableT {
        /* NORMAL KICK TABLES */
            /* NORTH KICK TABLES */
        static NN: KickTableT = [].to_vec();
        static NE: KickTableT = [( 0,  0), (-1,  0), (-1,  1), ( 0, -2), (-1, -2)].to_vec();
        static NS: KickTableT = [( 0,  0), ( 1,  0), ( 2,  0), ( 1,  1), ( 2,  1),
                        (-1,  0), (-2,  0), (-1,  1), (-2,  1), ( 0, -1),
                        ( 3,  0), (-3,  0)].to_vec();
        static NW: KickTableT = [( 0,  0), ( 1,  0), ( 1,  1), ( 0, -2), ( 1, -2)].to_vec();

            /* EAST KICK TABLSE */
        static EN: KickTableT = [( 0,  0), ( 1,  0), ( 1, -1), ( 0,  2), ( 1,  2)].to_vec();
        static EE: KickTableT = [].to_vec();
        static ES: KickTableT = [( 0,  0), ( 1,  0), ( 1, -1), ( 0,  2), ( 1,  2)].to_vec();
        static EW: KickTableT = [( 0,  0), ( 0,  1), ( 0,  2), (-1,  1), (-1,  2),
                        ( 0, -1), ( 0, -2), (-1, -1), (-1, -2), ( 1,  0),
                        ( 0,  3), ( 0, -3)].to_vec();

            /* SOUTH KICK TABLES */
        static SN: KickTableT = [( 0,  0), (-1,  0), (-2,  0), (-1, -1), (-2, -1),
                        ( 1,  0), ( 2,  0), ( 1, -1), ( 2, -1), ( 0,  1),
                        (-3,  0), ( 3,  0)].to_vec();
        static SE: KickTableT = [( 0,  0), (-1,  0), (-1,  1), ( 0, -2), (-1, -2)].to_vec();
        static SS: KickTableT = [].to_vec();
        static SW: KickTableT = [( 0,  0), ( 1,  0), ( 1,  1), ( 0, -2), ( 1, -2)].to_vec();

            /* WEST KICK TABLES */
        static WN: KickTableT = [( 0,  0), (-1,  0), (-1, -1), ( 0,  2), (-1,  2)].to_vec();
        static WE: KickTableT = [( 0,  0), ( 0,  1), ( 0,  2), ( 1,  1), ( 1,  2),
                        ( 0, -1), ( 0, -2), ( 1, -1), ( 1, -2), (-1,  0),
                        ( 0,  3), ( 0, -3)].to_vec();
        static WS: KickTableT = [( 0,  0), (-1,  0), (-1, -1), ( 0,  2), (-1,  2)].to_vec();
        static WW: KickTableT = [].to_vec();
        static KICK_TABLES_NORMAL: [KickTableT; 16] = [
            NN, NE, NS, NW,     EN, EE, ES, EW,
            SN, SE, SS, SW,     WN, WE, WS, WW
        ];

        KICK_TABLES_NORMAL[index].clone()
    }

    fn get_kick_table_i(index: usize) -> KickTableT {
        /* I KICK TABLES*/
            /* NORTH KICK TABLES */
        static INN: KickTableT = [].to_vec();
        static INE: KickTableT = [( 0,  0), (-2,  0), ( 1,  0), (-2, -1), ( 1,  2)].to_vec();
        static INS: KickTableT = [( 0,  0), (-1,  0), (-2,  0), ( 1,  0), ( 2,  0), ( 0,  1)].to_vec();
        static INW: KickTableT = [( 0,  0), (-1,  0), ( 2,  0), (-1,  2), ( 2, -1)].to_vec();

            /* EAST KICK TABLSE */
        static IEN: KickTableT = [( 0,  0), ( 2,  0), (-1,  0), ( 2,  1), (-1, -2)].to_vec();
        static IEE: KickTableT = [].to_vec();
        static IES: KickTableT = [( 0,  0), (-1,  0), ( 2,  0), (-1,  2), ( 2, -1)].to_vec();
        static IEW: KickTableT = [( 0,  0), ( 0,  1), ( 0,  2), ( 0, -1), ( 0, -2), (-1,  0)].to_vec();

            /* SOUTH KICK TABLES */
        static ISN: KickTableT = [( 0,  0), ( 1,  0), ( 2,  0), (-1,  0), (-2,  0), ( 0, -1)].to_vec();
        static ISE: KickTableT = [( 0,  0), ( 1,  0), (-2,  0), ( 1, -2), (-2,  1)].to_vec();
        static ISS: KickTableT = [].to_vec();
        static ISW: KickTableT = [( 0,  0), ( 2,  0), (-1,  0), ( 2,  1), (-1, -2)].to_vec();

            /* WEST KICK TABLES */
        static IWN: KickTableT = [( 0,  0), ( 1,  0), (-2,  0), ( 1, -2), (-2,  1)].to_vec();
        static IWE: KickTableT = [( 0,  0), ( 0,  1), ( 0,  2), ( 0, -1), ( 0, -2), ( 1,  0)].to_vec();
        static IWS: KickTableT = [( 0,  0), (-2,  0), ( 1,  0), (-2, -1), ( 1,  2)].to_vec();
        static IWW: KickTableT = [].to_vec();

        static KICK_TABLES_I: [KickTableT; 16] = [
            INN, INE, INS, INW,     IEN, IEE, IES, IEW,
            ISN, ISE, ISS, ISW,     IWN, IWE, IWS, IWW
        ];

        KICK_TABLES_I[index]
    }
}
