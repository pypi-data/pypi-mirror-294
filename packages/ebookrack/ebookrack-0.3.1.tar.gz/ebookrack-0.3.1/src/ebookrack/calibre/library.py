# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2
"""
list the books in an e-book library
"""

from pathlib import Path

from .metadata import parse_opf


class Library:
    def __init__(self, root_dir):
        self.books = [Book(d) for d in root_dir.glob("*/*")]


class Book:
    def __init__(self, book_dir):
        self.metadata = parse_opf(book_dir / "metadata.opf")

        dir_depth = 2  # how many path segments to get to library root
        self.path = "/".join(book_dir.parts[-dir_depth:])

        self.files = find_ebooks(book_dir)
        self.cover = book_dir / "cover.jpg"

    def __getattr__(self, name):
        if hasattr(self.metadata, name):
            return getattr(self.metadata, name)

        return super().__getattr__(self, name)


class BookFile(Path):
    @property
    def format(self):
        return self.suffix.lstrip(".").upper()


def find_ebooks(book_dir):
    return [BookFile(p) for p in book_dir.glob("*.*") if is_ebook(p)]


def is_ebook(p):
    return p.is_file() and p.name not in {"metadata.opf", "cover.jpg"}
