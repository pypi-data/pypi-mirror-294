import py_compile
import os

# List of modules to compile
modules = ['__init__.py', 'explorer.py']

for module in modules:
    py_compile.compile(module, cfile=module + 'c')  # Save as .pyc file
