# gtdb_tree

A library for parsing Newick format files, especially GTDB tree files.

## Features

- Parse Newick formatted strings into a structured representation of trees.
- Handle various formats of Newick strings, including those with bootstrap values and distances.

## Installation

Add this crate to your `Cargo.toml`:

```toml
[dependencies]
gtdb_tree = "0.1.9"
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

## Advanced Usage
### Custom Node Parser
You can provide a custom parser function to handle special node formats:

```python
import gtdb_tree

def custom_parser(node_str):
    # Custom parsing logic
    name, length = node_str.split(':')
    return name, 100.0, float(length)  # name, bootstrap, length

result = gtdb_tree.parse_tree("((A:0.1,B:0.2):0.3,C:0.4);", custom_parser=custom_parser)
print(result)
```

## Working with Node Objects
## Each Node object in the result has the following attributes:

* id: Unique identifier for the node
* name: Name of the node
* bootstrap: Bootstrap value (if available)
* length: Branch length
* parent: ID of the parent node
