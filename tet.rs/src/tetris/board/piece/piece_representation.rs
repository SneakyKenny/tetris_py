pub fn get_border() -> String {
    String::from("o")
}

pub fn get_empty() -> String {
    String::from(" ")
}

pub fn get_taken() -> String {
    String::from("x")
}

pub fn get_ghost() -> String {
    String::from("~")
}

pub fn get_garbage() -> String {
    get_taken()
}
