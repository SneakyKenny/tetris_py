use termion::event::Key;

use super::board::my_board::Board;

pub struct Tetris {
    board: Board,
}

impl std::fmt::Display for Tetris {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        writeln!(f, "{}", self.board)
    }
}

fn key_to_string(key: Key) -> String {
    match key {
        Key::Char(c) => format!("{}", c),
        Key::Alt(c) => format!("^[{}", c.to_lowercase()),
        Key::Ctrl(c) => format!("^{}", c.to_uppercase()),
        Key::Esc => String::from("ESC"),
        Key::Left => String::from("←"),
        Key::Right => String::from("→"),
        Key::Up => String::from("↑"),
        Key::Down => String::from("↓"),
        Key::Backspace => String::from("×"),
        _ => String::from("other"),
    }
}

impl Tetris {
    pub fn new() -> Self {
        Tetris {
            board: Board::new(),
        }
    }

    pub fn process_input(&mut self, input: Key) -> bool {
        // Returns whether the game shall continue
        match input {

            Key::Char('q')  => false,

            // Hard-drop
            Key::Char(' ')  => {
                while self.board.move_piece(0, -1, 0) {}
                self.board.lock_active_piece()
            }

            // Hold
            Key::Char('c')  => { self.board.hold_active_piece();    true },

            // Rotation
            Key::Char('z')  => { self.board.move_piece( 0,  0, -1); true },
            Key::Char('x')  => { self.board.move_piece( 0,  0,  2); true },
            Key::Up         => { self.board.move_piece( 0,  0,  1); true },

            // Movement
            Key::Left       => { self.board.move_piece(-1,  0,  0); true },
            Key::Right      => { self.board.move_piece( 1,  0,  0); true },

            // Move piece down. Special behavior in case the piece locks.
            // XXX: Change this later, we don't always want to lock it.
            Key::Down       =>   self.board.move_piece( 0, -1,  0)
                            || self.board.lock_active_piece(),

            // Unrecognized
            _ => { print!("unknown key: {}\r\n", key_to_string(input)); false },
        }
    }
}
