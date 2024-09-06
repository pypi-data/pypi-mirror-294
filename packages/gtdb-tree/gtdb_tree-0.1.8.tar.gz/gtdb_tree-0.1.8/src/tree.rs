use crate::node::{Node, ParseError};
use memchr::memchr2;

fn parse_label(label: &str) -> Result<(String, f64), ParseError> {
    let label = label.trim_end_matches(";").trim_matches('\'').to_string();

    let parts: Vec<&str> = label.splitn(2, ':').collect();
    if parts.len() == 1 {
        let label_f64 = label.parse::<f64>();
        if let Ok(bootstrap) = label_f64 {
            if bootstrap <= 100.1 {
                return Ok(("".into(), bootstrap));
            }
        }
        return Ok((label, 0.0));
    }
    let parts_0_f64 = parts.get(0).unwrap_or(&"0").parse::<f64>();
    let name = parts.get(1).unwrap_or(&"").to_string();
    if let Ok(bootstrap) = parts_0_f64 {
        if bootstrap <= 100.1 {
            return Ok((name, bootstrap));
        }
    }
    Ok((label, 0.0))
}

/// Parse the name and length of a node from a Newick tree string.
///
/// This function takes a byte slice representing a node in a Newick tree string,
/// and returns the name and length of the node as a tuple.
///
/// # Arguments
///
/// * `node_bytes` - A byte slice representing the node in a Newick tree string.
///
/// # Returns
///
/// Returns a `Result` containing a tuple of the name and length on success,
/// or an `Err(ParseError)` on failure.
///
/// # Example
///
/// ```
/// use gtdb_tree::tree::parse_node;
///
/// let node_bytes = b"A:0.1";
/// let (name, bootstrap, length) = parse_node(node_bytes).unwrap();
/// assert_eq!(name, "A");
/// assert_eq!(bootstrap, 0.0);
/// assert_eq!(length, 0.1);
/// ```
pub fn parse_node(node_bytes: &[u8]) -> Result<(String, f64, f64), ParseError> {
    let node_str = std::str::from_utf8(node_bytes).expect("UTF-8 sequence");
    // gtdb
    // Check if node_str contains single quotes and ensure they are together
    if node_str.matches('\'').count() % 2 != 0 {
        return Err(ParseError::InvalidFormat(format!(
            "Invalid format: single quotes must be paired and not consecutive in '{}'",
            node_str
        )));
    }

    let parts: Vec<&str> = node_str.rsplitn(2, ':').collect();
    if parts.len() == 1 {
        let label = node_str.trim_end_matches(";").to_string();

        return Ok((label, 0.0, 0.0));
    }

    let label = parts.get(1).unwrap_or(&"");

    let (name, bootstrap) = parse_label(label)?;
    let length_str = parts.get(0).unwrap_or(&"").trim();

    // Parse the length
    let length = if length_str.is_empty() {
        0.0
    } else {
        length_str.parse::<f64>().map_err(|_| {
            ParseError::InvalidFormat(format!("Invalid branch length: {}", length_str))
        })?
    };

    Ok((name, bootstrap, length)) // Return the name and length
}

/// Parse a Newick tree string into a vector of nodes.
///
/// This function takes a Newick tree string, trims any trailing whitespace and
/// ensures the string ends with a semicolon. It then parses the string into nodes
/// by iterating through the characters and using a stack to manage the hierarchy.
///
/// # Arguments
///
/// * `newick_str` - A string slice that implements the `AsRef<str>` trait.
///
/// # Returns
///
/// Returns a `Result` containing a `Vec<Node>` on success, or an `Err(ParseError)` on failure.
///
/// # Example
///
/// ```
/// use gtdb_tree::tree::parse_tree;
///
/// let newick_str = "((A:0.1,B:0.2):0.3,C:0.4);";
/// let nodes = parse_tree(newick_str).unwrap();
/// assert_eq!(nodes.len(), 5);
/// ```
pub fn parse_tree(newick_str: &str) -> Result<Vec<Node>, ParseError> {
    let mut nodes: Vec<Node> = Vec::new();
    let mut pos = 0;

    let cleaned_str = newick_str.trim_ascii_end();
    if !cleaned_str.ends_with(';') {
        return Err(ParseError::UnexpectedEndOfInput);
    }
    let bytes = cleaned_str.as_bytes();

    let bytes_len = bytes.len();
    let mut stack: Vec<usize> = Vec::new();
    let mut node_id_counter: usize = 1;

    while pos < bytes_len {
        let token = bytes[pos];
        match token {
            b'(' => {
                stack.push(node_id_counter);
                node_id_counter += 1;
            }
            _ => {
                let end_pos = memchr2(b',', b')', &bytes[pos..]).unwrap_or(bytes_len - pos);
                let node_end_pos = pos + end_pos;
                let node_bytes = &bytes[pos..node_end_pos];
                let (name, bootstrap, length) = parse_node(node_bytes)?;
                let node_id = if &bytes[pos - 1] == &b')' {
                    stack.pop().unwrap_or(0)
                } else {
                    node_id_counter
                };
                let parent = *stack.last().unwrap_or(&0);
                let node = Node {
                    id: node_id,
                    name,
                    bootstrap,
                    length,
                    parent,
                };
                nodes.push(node);
                node_id_counter += 1;
                pos = node_end_pos;
            }
        }
        pos += 1; // Move to the next character
    }
    Ok(nodes)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_tree() {
        let test_cases = vec![
            "((A:0.1,B:0.2)'56:F;H;':0.3,C:0.4);",
            "(,,(,));",                            // no nodes are named
            "(A,B,(C,D));",                        // leaf nodes are named
            "(A,B,(C,D)E)F;",                      // all nodes are named
            "(:0.1,:0.2,(:0.3,:0.4):0.5);",        // all but root node have a distance to parent
            "(:0.1,:0.2,(:0.3,:0.4):0.5):0.0;",    // all have a distance to parent
            "(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);",    // distances and leaf names (popular)
            "(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;",  // distances and all names
            "((B:0.2,(C:0.3,D:0.4)E:0.5)F:0.1)A;", // a tree rooted on a leaf node (rare)
        ];

        for newick_str in test_cases {
            match parse_tree(newick_str) {
                Ok(nodes) => println!(
                    "Parsed nodes for '{}': {:?}, len: {}",
                    newick_str,
                    nodes,
                    nodes.len()
                ),
                Err(e) => println!("Error parsing '{}': {:?}", newick_str, e),
            }
        }
    }
}
