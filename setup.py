from setuptools import setup, Extension
import sys
import platform

# Set compiler flags based on the platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = ['/openmp']
elif platform.system() == "Linux" or platform.system() == "Darwin":
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']

setup(
    name="yggdrasil",
    version="0.1",
    py_modules=['yggdrasil'],
    ext_modules=[
        Extension(
            'yggdrasil_c',
            sources=['yggdrasil_c.c'],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
    ],
    install_requires=[],
)
