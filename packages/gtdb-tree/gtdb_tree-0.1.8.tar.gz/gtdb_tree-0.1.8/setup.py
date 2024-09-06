from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="gtdb_tree",
    version="0.1.8",
    rust_extensions=[RustExtension("gtdb_tree.gtdb_tree", binding=Binding.PyO3)],
    packages=["gtdb_tree"],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,
)
