# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

"""Shelf for storing and retrieving books

The Shelf is used to place books in the storage system
and maintains an index of the storage locations.

Books can be shelved, in multiple formats;
moved to a new location on the shelf by providing updated metadata;
moved to a different shelf;
or discarded.

shelf
    index and interface to the storage system
book_id
    the identifier for a book, used throughout the library system
book_data
    the book metadata retrieved from the library catalogue
book
    the e-book itself, in a given format, e.g. epub
"""

import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Shelf"]


@dataclass(frozen=True)
class Shelf:
    _root_dir: Path
    _books: dict[str, list[Path]] = field(default_factory=lambda: defaultdict(list))

    def shelve(self, book_id, book_data, book_file):
        book = Book(book_file)
        location = self.prepare_location(book_id, book_data, book)
        shelved_book = book.copy_to(location)
        self._books[book_id].append(shelved_book)

    def reshelve(self, book_id, book_data):
        books = self._books.pop(book_id)

        for book in books:
            location = self.prepare_location(book_id, book_data, book)
            shelved_book = book.move_to(location)
            self._books[book_id].append(shelved_book)

    def prepare_location(self, book_id, book_data, book):
        basename = slugify(book_data["title"]) + book.format
        return self._root_dir / str(book_id) / basename

    def transfer_all(self, card_index, new_shelf):
        for book_id in list(self._books):
            book_data = card_index[book_id]
            books = self._books.pop(book_id)

            for book in books:
                new_shelf.shelve(book_id, book_data, book.path)
                book.delete()

    def locate(self, book_id):
        return self._books[book_id]

    def discard(self, book_id):
        for book in self._books.pop(book_id):
            book.delete()


@dataclass(frozen=True)
class Book:
    _path: Path

    @property
    def path(self):
        return self._path

    @property
    def format(self):
        return self._path.suffix

    def copy_to(self, dest):
        dest.parent.mkdir(exist_ok=True)
        shutil.copy2(self._path, dest)
        return Book(dest)

    def move_to(self, dest):
        self._path.rename(dest)
        return Book(dest)

    def delete(self):
        self._path.unlink()


def slugify(string):
    """Convert the string to lowercase and dash-separated.

    Loosely based on: https://github.com/zacharyvoase/slugify
    """
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", string).strip().lower())
