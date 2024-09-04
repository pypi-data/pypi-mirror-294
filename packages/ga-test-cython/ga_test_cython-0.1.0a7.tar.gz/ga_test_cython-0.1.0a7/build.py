import os
import numpy
import shutil
from setuptools import Distribution, Extension

from Cython.Build import build_ext, cythonize


output_dir = "cython_build"
modules_dir = "ga_test_cython"

# Manage extensions
dot_products = Extension(
	f"{modules_dir}.operations_utils.dot_product_utils",
	sources=[os.path.join(modules_dir, "operations_utils", "dot_product_utils.pyx")],
	include_dirs=[numpy.get_include()],
	extra_compile_args=["-O3"],
)

cython_modules = [
	dot_products,
]

external_modules = cythonize(
	cython_modules,
	compiler_directives={"language_level": 3},  # Specify Cython we are using Python 3.
	include_path=[modules_dir],
	build_dir=output_dir,  # Do not build auxiliary files in the source tree, leavind C/C++ files behind.
	annotate=False,  # Do no generate an .html output file. It could contain useless references to our code.
	force=True,  # Always rebuild, even without changes in our project. This step is optional.
)

dist = Distribution({ "ext_modules": external_modules, })
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
	relative_extension = os.path.relpath(output, cmd.build_lib)
	shutil.copyfile(output, relative_extension)
