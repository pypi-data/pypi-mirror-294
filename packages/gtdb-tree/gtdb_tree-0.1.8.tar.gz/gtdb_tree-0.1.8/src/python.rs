use crate::node::Node as RustNode;
use crate::tree;

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

#[cfg(feature = "python")]
#[pyfunction]
pub fn parse_tree(newick_str: &str) -> PyResult<Vec<Node>> {
    tree::parse_tree(newick_str)
        .map(|rust_nodes| rust_nodes.into_iter().map(|rn| Node { node: rn }).collect())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))
}
