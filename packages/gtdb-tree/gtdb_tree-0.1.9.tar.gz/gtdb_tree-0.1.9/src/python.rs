use crate::node::Node as RustNode;
use crate::node::ParseError;
use crate::tree::{self, NodeParser};
use std::convert::From;
use std::sync::Arc;

// 添加一个从 PyErr 到 ParseError 的转换实现
impl From<PyErr> for ParseError {
    fn from(err: PyErr) -> Self {
        ParseError::PythonError(err.to_string())
    }
}

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pyclass]
pub struct Node {
    node: RustNode,
}

#[cfg(feature = "python")]
#[pymethods]
impl Node {
    #[getter]
    fn id(&self) -> PyResult<usize> {
        Ok(self.node.id)
    }

    #[getter]
    fn name(&self) -> PyResult<String> {
        Ok(self.node.name.clone())
    }

    #[getter]
    fn bootstrap(&self) -> PyResult<f64> {
        Ok(self.node.bootstrap)
    }

    #[getter]
    fn length(&self) -> PyResult<f64> {
        Ok(self.node.length)
    }

    #[getter]
    fn parent(&self) -> PyResult<usize> {
        Ok(self.node.parent)
    }
}

// #[cfg(feature = "python")]
// #[pyfunction]
// pub fn parse_tree(newick_str: &str) -> PyResult<Vec<Node>> {
//     tree::parse_tree(newick_str)
//         .map(|rust_nodes| rust_nodes.into_iter().map(|rn| Node { node: rn }).collect())
//         .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))
// }

#[cfg(feature = "python")]
#[pyfunction]
#[pyo3(signature = (newick_str, custom_parser = None))]
#[pyo3(text_signature = "(newick_str, custom_parser=None)")]
/// Parse a Newick format string into a list of Node objects.
///
/// This function takes a Newick format string and optionally a custom parser function,
/// and returns a list of Node objects representing the phylogenetic tree.
///
/// Parameters:
/// -----------
/// newick_str : str
///     The Newick format string representing the phylogenetic tree.
/// custom_parser : callable, optional
///     A custom parsing function for node information. If not provided, the default parser will be used.
///     The custom parser should have the following signature:
///
///     def custom_parser(node_str: str) -> Tuple[str, float, float]:
///         '''
///         Parse a node string and return name, bootstrap, and length.
///
///         Parameters:
///         -----------
///         node_str : str
///             The node string to parse.
///
///         Returns:
///         --------
///         Tuple[str, float, float]
///             A tuple containing (name, bootstrap, length) for the node.
///         '''
///         # Your custom parsing logic here
///         return name, bootstrap, length
///
/// Returns:
/// --------
/// List[Node]
///     A list of Node objects representing the parsed phylogenetic tree.
///
/// Raises:
/// -------
/// ValueError
///     If the Newick string is invalid or parsing fails.
///
/// Example:
/// --------
/// >>> newick_str = "(A:0.1,B:0.2,(C:0.3,D:0.4)70:0.5);"
/// >>> nodes = parse_tree(newick_str)
/// >>>
/// >>> # Using a custom parser
/// >>> def my_parser(node_str):
/// ...     parts = node_str.split(':')
/// ...     name = parts[0]
/// ...     length = float(parts[1]) if len(parts) > 1 else 0.0
/// ...     return name, 100.0, length  # Always set bootstrap to 100.0
/// >>>
/// >>> nodes_custom = parse_tree(newick_str, custom_parser=my_parser)
pub fn parse_tree(
    _py: Python,
    newick_str: &str,
    custom_parser: Option<PyObject>,
) -> PyResult<Vec<Node>> {
    let parser = match custom_parser {
        Some(py_func) => {
            let py_func = Arc::new(py_func);
            NodeParser::Custom(Box::new(
                move |node_str: &str| -> Result<(String, f64, f64), ParseError> {
                    Python::with_gil(|py| {
                        let result = py_func.call1(py, (node_str,))?;
                        let (name, bootstrap, length): (String, f64, f64) = result.extract(py)?;
                        Ok((name, bootstrap, length))
                    })
                    .map_err(|e: PyErr| ParseError::PythonError(e.to_string()))
                },
            ))
        }
        None => NodeParser::Default,
    };

    tree::parse_tree(newick_str, parser)
        .map(|rust_nodes| rust_nodes.into_iter().map(|rn| Node { node: rn }).collect())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))
}
