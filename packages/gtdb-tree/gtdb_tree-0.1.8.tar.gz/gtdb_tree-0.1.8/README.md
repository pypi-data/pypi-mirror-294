# gtdb_tree

A library for parsing Newick format files, especially GTDB tree files.

## Features

- Parse Newick formatted strings into a structured representation of trees.
- Handle various formats of Newick strings, including those with bootstrap values and distances.

## Installation

Add this crate to your `Cargo.toml`:

```toml
[dependencies]
gtdb_tree = "0.1.0"
```

## Usage

Here's a simple example of how to use the library:

```rust
use gtdb_tree::tree::parse_tree;

fn main() {
    let newick_str = "((A:0.1,B:0.2):0.3,C:0.4);";
    match parse_tree(newick_str) {
        Ok(nodes) => println!("Parsed nodes: {:?}", nodes),
        Err(e) => println!("Error parsing: {:?}", e),
    }
}
```

## Python Usage
A Python package for parsing GTDB trees using Rust.

## Installation

```
pip install gtdb_tree
```

```python
import gtdb_tree

result = gtdb_tree.parse_tree("((A:0.1,B:0.2):0.3,C:0.4);")
print(result)
```

