import io
import os
import re
import sys

try:
    from setuptools import find_packages, setup
except ImportError:
    print(
        "Package setuptools is missing from your Python installation. "
        "Please see the installation section in the esptool documentation"
        " for instructions on how to install it."
    )
    exit(1)


# Example code to pull version from esptool module with regex, taken from
# https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


if os.name != "nt":
    scripts = ["codetemplategen.py"]
    entry_points = {}
else:
    scripts = []
    entry_points = {
        "console_scripts": [
            "codetemplategen.py=pycodetemplategen.__init__:_main"
        ],
    }


long_description = """
==========
codetemplategen.py
==========
A Python-based, open-source, platform-independent utility to generate \
C/C++ code templates

The codetemplategen.py project is `hosted on github <https://github.com/schreinerman/CodeTemplateGen>`_.

Documentation
-------------
Run ``codetemplategen.py -h``.

"""

setup(
    name="codetemplategen",
    version=find_version("pycodetemplategen/__init__.py"),
    description="A utility to generate C/C++ code templates",
    long_description=long_description,
    url="https://github.com/schreinerman/CodeTemplateGen",
    project_urls={
        "Documentation": "https://github.com/schreinerman/CodeTemplateGen",
        "Source": "https://github.com/schreinerman/CodeTemplateGen",
        "Tracker": "https://github.com/schreinerman/CodeTemplateGen/issues/",
    },
    author="Manuel Schreiner",
    author_email="info@io-expert.com",
    license="GPLv2+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    setup_requires=(["wheel"] if "bdist_wheel" in sys.argv else []),
    extras_require={
        "dev": [
            "flake8>=3.2.0",
            "flake8-import-order",
            "pyelftools",
            # the replacement of the old xmlrunner package
            "unittest-xml-reporting",
            "coverage~=6.0",
            "black",
            "pre-commit",
        ],
    },
    install_requires=[
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["templates/*"]},
    entry_points=entry_points,
    scripts=scripts,
)