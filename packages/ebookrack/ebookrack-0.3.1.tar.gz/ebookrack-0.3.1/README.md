# EBookRack

Python library for managing a personal e-book library

The `ebookrack.calibre` subpackage allows querying an e-book library managed by Calibre.


## Installation

The package is available on PyPI and can be installed with `pip`:

    pip install ebookrack


## Usage

The `Library` class in `ebookrack.calibre` provides a high-level entry point
for querying the contents of a Calibre library.

```python
from pathlib import Path
from ebookrack.calibre.library import Library

lib_path = Path("~/Books").expanduser()
library = Library(lib_path)

for book in library.books:
    print(book.title)
    print(" & ".join(book.authors))

    for file in book.files:
        print(f"{file.format:6s}: {file}")

    print("---")
```

The modules in the `ebookrack` core package are not yet ready for use.
