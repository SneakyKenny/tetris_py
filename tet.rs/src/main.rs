use std::io::{stdin, stdout, Write};
use termion::{input::TermRead, raw::IntoRawMode};

mod tetris;

use crate::tetris::my_tetris::Tetris;

fn main() {
    let mut tetris: Tetris = Tetris::new();
    let mut stdout = stdout().into_raw_mode().unwrap();

    write!(
        stdout,
        "{}{}{}",
        termion::clear::All,
        termion::cursor::Goto(1, 1),
        tetris
    )
    .unwrap();

    for input in stdin().keys() {
        if !tetris.process_input(input.unwrap()) {
            break;
        }

        write!(
            stdout,
            "{}{}{}",
            termion::clear::All,
            termion::cursor::Goto(1, 1),
            tetris
        )
        .unwrap();
    }

    /*
    // input experiment
    match input.unwrap() {
        Key::Char('q') | Key::Esc => std::process::exit(0),
        Key::Char(c) => format!("{}", c),
        Key::Alt(c) => format!("^[{}", c.to_lowercase()),
        Key::Ctrl(c) => format!("^{}", c.to_uppercase()),
        Key::Left => String::from("←"),
        Key::Right => String::from("→"),
        Key::Up => String::from("↑"),
        Key::Down => String::from("↓"),
        Key::Backspace => String::from("×"),
        _ => String::from("wtf"),
    }
    */
}
