/// A node in a Newick tree.
///
/// # Fields
///
/// * `id` - The unique identifier of the node.
/// * `name` - The name of the node.
/// * `length` - The length of the branch leading to this node.
/// * `parent` - The identifier of the parent node.
/// * `bootstrap` - The bootstrap value of the node. 0.0-100.0
#[derive(Debug, PartialEq, Clone)]
pub struct Node {
    pub id: usize,
    pub name: String,
    pub bootstrap: f64,
    pub length: f64,
    pub parent: usize,
}

/// An error that occurs during parsing.
#[derive(Debug)]
pub enum ParseError {
    UnexpectedEndOfInput,
    #[allow(dead_code)]
    InvalidFormat(String),
}

impl std::fmt::Display for ParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ParseError::UnexpectedEndOfInput => write!(f, "Unexpected end of input"),
            ParseError::InvalidFormat(msg) => write!(f, "Invalid format: {}", msg),
        }
    }
}

impl std::error::Error for ParseError {}
