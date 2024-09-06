pub mod node;
pub mod tree;

#[cfg(feature = "python")]
mod python;

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
// #[pyo3(name = "gtdb_tree")]
fn gtdb_tree(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(python::parse_tree, m)?)?;
    m.add_class::<python::Node>()?;
    Ok(())
}
