use pyo3_build_config;

fn main() {
    pyo3_build_config::add_extension_module_link_args();
    // println!("cargo:rustc-link-search=-lintl -ldl -L/opt/homebrew/lib -Wl,-rpath,/opt/homebrew/lib -framework CoreFoundation");
}
