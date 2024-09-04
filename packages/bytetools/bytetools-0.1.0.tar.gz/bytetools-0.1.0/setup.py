# setup.py
from setuptools import setup, Extension

# Define the C extension module
operation_extensions = Extension(
    "bytetools.operations",  # Module name
    sources=["src/bytetools/operations.c"],  # C source file
)

# Call the setup function to build the module
setup(
    ext_modules=[operation_extensions],
)
