# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

from pathlib import Path

import pytest

from ebookrack.calibre.library import Book, Library

DATA_DIR = Path("tests", "library")
BOOK_DIR = DATA_DIR / "Charles Darwin" / "Insectivorous Plants (2)"


def test_library_has_list_of_books():
    library = Library(DATA_DIR)
    assert len(library.books) == 5


@pytest.mark.parametrize("field", ["title", "authors", "path", "files", "cover"])
def test_book_has_field(field):
    book = Book(BOOK_DIR)
    assert hasattr(book, field)


def test_book_path_is_relative_to_library_root():
    book = Book(BOOK_DIR)
    assert DATA_DIR / book.path == BOOK_DIR


def test_book_files_have_format():
    book = Book(BOOK_DIR)
    assert {f.format for f in book.files} == {"EPUB", "PDF"}
