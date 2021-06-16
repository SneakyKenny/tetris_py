pub struct PieceRepresentation {
}

impl PieceRepresentation {
    pub fn get_border() -> String {
        String::from("o")
    }

    pub fn get_empty() -> String {
        String::from(" ")
    }

    pub fn get_taken() -> String {
        String::from("x")
    }
}
