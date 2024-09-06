# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

import shutil
from pathlib import Path

import pytest

from ebookrack.shelf import Book, Shelf, slugify


def test_slugify():
    assert slugify("Hello, World…/ ") == "hello-world"


@pytest.fixture
def input_file(tmpdir):
    upload_dir = Path(tmpdir) / "uploads"
    upload_dir.mkdir()
    book_path = upload_dir / "TheInferno.epub"
    book_path.write_text("# The Inferno\n")
    return book_path


@pytest.fixture
def shelf(tmpdir):
    return Shelf(Path(tmpdir))


def test_shelve_renames_file_and_retains_original(shelf, input_file):
    shelf.shelve(1, dict(title="The Inferno"), input_file)
    assert shelf.locate(1) == [Book(shelf._root_dir / "1" / "the-inferno.epub")]
    assert (shelf._root_dir / "1" / "the-inferno.epub").is_file()
    assert input_file.is_file()


def test_reshelve_moves_file_and_updates_location_table(shelf, input_file):
    shelf.shelve(1, dict(title="The Inferno"), input_file)
    shelf.reshelve(1, dict(title="Inferno"))

    assert shelf.locate(1) == [Book(shelf._root_dir / "1" / "inferno.epub")]
    assert (shelf._root_dir / "1" / "inferno.epub").is_file()
    assert (shelf._root_dir / "1" / "the-inferno.epub").is_file() is False


def test_discarding_book_deletes_files_and_record(shelf, input_file):
    input_file2 = shutil.copy2(input_file, input_file.with_suffix(".pdf"))
    shelf.shelve(1, dict(title="The Inferno"), input_file)
    shelf.shelve(1, dict(title="The Inferno"), input_file2)
    stored_books = shelf.locate(1)
    assert len(stored_books) == 2
    assert all(book.path.is_file() for book in stored_books)

    shelf.discard(1)

    assert not any(book.path.is_file() for book in stored_books)
    assert shelf.locate(1) == []
