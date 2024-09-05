from setuptools import setup

name = "types-xdgenvpy"
description = "Typing stubs for xdgenvpy"
long_description = '''
## Typing stubs for xdgenvpy

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`xdgenvpy`](https://gitlab.com/deliberist-group/xdgenvpy) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`xdgenvpy`.

This version of `types-xdgenvpy` aims to provide accurate annotations
for `xdgenvpy==2.4.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/xdgenvpy. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`236ec8e9cf1abcf7ca418445a6424f05ee07919f`](https://github.com/python/typeshed/commit/236ec8e9cf1abcf7ca418445a6424f05ee07919f) and was tested
with mypy 1.11.1, pyright 1.1.379, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.4.0.20240905",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/xdgenvpy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['xdgenvpy-stubs'],
      package_data={'xdgenvpy-stubs': ['__init__.pyi', '_defaults.pyi', 'xdgenv.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
