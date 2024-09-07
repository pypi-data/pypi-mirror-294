# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

from pathlib import Path

root_path = Path(__file__).parent
version_file = root_path / "tycki" / "VERSION"

__version__=version_file.read_text()

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

# g++ -Wall -std=c++17 -O3 -shared -fPIC -march=native -ffp-contract=fast -I./../../eigen/ -I./../header_only_version/ $(python3-config --includes) -I./../extern/pybind11/include tycki.cpp -o tycki$(python3-config --extension-suffix)
ext_modules = [
    Pybind11Extension(
        "tycki",
        ["tycki/tycki.cpp"],
        extra_compile_args=["-O3", "-fPIC", "-march=native", "-ffp-contract=fast", "-funroll-loops"],
        #extra_compile_args=["-O0", "-fPIC", "-g"],
        include_dirs=['./extern/eigen/', './extern/mcmc/header_only_version/'],
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tycki",
    version=__version__,
    author="Richard D. Paul",
    author_email="richard@los-paul.eu",
    url="https://github.com/ripaul/tycki",
    description="Fast MCMC in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
