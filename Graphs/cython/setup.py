from distutils.core import setup
from Cython.Build import cythonize

# Compile with: python setup.py build_ext --inplace

setup(name="homogeneous", ext_modules=cythonize('homogeneous.pyx'),)
