# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

import sys
from pathlib import Path

from ebookrack.calibre.library import Library


def print_library(lib_path):
    library = Library(lib_path)

    for b in library.books:
        print_book(b)


def print_book(book):
    print(book.title)
    print(" & ".join(book.authors))

    for file in book.files:
        print(f"{file.format:6s}: {file}")

    print()


if __name__ == "__main__":
    try:
        lib_path = Path(sys.argv[1])
    except IndexError:
        print("missing argument: path to library", file=sys.stderr)
        sys.exit(1)

    print_library(lib_path)
