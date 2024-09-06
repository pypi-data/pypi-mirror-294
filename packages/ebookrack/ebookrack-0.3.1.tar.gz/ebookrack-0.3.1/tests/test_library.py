# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

from pathlib import Path
from zlib import adler32

import pytest

from ebookrack.catalogue import Catalogue
from ebookrack.library import Library
from ebookrack.shelf import Shelf


def checksum(path):
    return adler32(path.read_bytes())


@pytest.fixture()
def book_data():
    data_inferno = dict(author="Dante", title="The Inferno")
    data_canterb = dict(author="Chaucer", title="The Canterbury tales")
    return [data_inferno, data_canterb]


@pytest.fixture()
def book_files(tmpdir):
    upload_dir = Path(tmpdir) / "uploads"
    upload_dir.mkdir()

    file_inferno = upload_dir / "TheInferno.epub"
    file_inferno.write_text("# The Inferno\n")

    file_canterb = upload_dir / "canterbury+tales.pdf"
    file_canterb.write_text("= Chaucer's Canterbury Tales\n")

    return [file_inferno, file_canterb]


@pytest.fixture()
def library(tmpdir):
    return Library(Catalogue(), Shelf(Path(tmpdir)))
    # TODO: Change initialisation of Library


def test_acquired_books_are_listed_in_inventory(library, book_data, book_files):
    for data, file_ in zip(book_data, book_files):
        library.acquire(data, file_)

    assert library.inventory() == book_data


def test_acquired_books_can_be_located_on_shelf(library, book_data, book_files):
    book_ids = []

    for data, file_ in zip(book_data, book_files):
        book_id = library.acquire(data, file_)
        book_ids.append(book_id)

    for book_id, uploaded_book in zip(book_ids, book_files):
        stored_book = library.locate(book_id)[0]
        assert stored_book.is_file()
        assert checksum(stored_book) == checksum(uploaded_book)


def test_storing_book_in_multiple_formats(library, book_data, book_files):
    inferno_data = book_data[0]
    inferno_epub, tmp_pdf = book_files
    inferno_pdf = inferno_epub.with_suffix(".pdf")
    tmp_pdf.rename(inferno_pdf)

    book_id = library.acquire(inferno_data, inferno_epub)
    library.acquire_additional_format(book_id, inferno_pdf)

    stored_books = library.locate(book_id)
    assert stored_books[1].suffix == ".pdf"
    assert stored_books[1].is_file()
    assert checksum(stored_books[1]) == checksum(inferno_pdf)


def test_transferring_books_to_new_shelf(tmpdir, book_data, book_files):
    root0 = Path(tmpdir) / "initial"
    root1 = Path(tmpdir) / "updated"
    root0.mkdir()
    library = Library(Catalogue(), Shelf(root0))
    book_ids = []

    for data, file_ in zip(book_data, book_files):
        book_id = library.acquire(data, file_)
        book_ids.append(book_id)

    for book_id in book_ids:
        for book_file in library.locate(book_id):
            assert book_file.relative_to(root0)

    root1.mkdir()
    library.replace_shelf(Shelf(root1))

    for book_id in book_ids:
        for book_file in library.locate(book_id):
            assert book_file.relative_to(root1)

    initial_files = [fp for fp in root0.glob("**") if fp.is_file()]
    assert not initial_files


def test_modifying_author_updates_catalogue_card(library, book_data, book_files):
    inferno_data, uploaded_book = book_data[0], book_files[0]
    book_id = library.acquire(inferno_data, uploaded_book)
    initial_path = library.locate(book_id)[0]

    library.edit_metadata(book_id, author="Dante Alighieri", publication_date=1320)

    data = library.search(title="The Inferno")[0]
    assert data["author"] == "Dante Alighieri"
    assert data["publication_date"] == 1320
    assert library.locate(book_id)[0] == initial_path


def test_modifying_title_triggers_reshelving(library, book_data, book_files):
    inferno_data, uploaded_book = book_data[0], book_files[0]
    book_id = library.acquire(inferno_data, uploaded_book)
    initial_path = library.locate(book_id)[0]

    library.edit_metadata(book_id, title="Inferno")

    data = library.search(author="Dante")[0]
    assert data["title"] == "Inferno"

    new_path = library.locate(book_id)[0]
    assert new_path != initial_path
    assert checksum(new_path) == checksum(uploaded_book)


def test_discard_book_destroys_record_and_files(library, book_data, book_files):
    for data, file_ in zip(book_data, book_files):
        book_id = library.acquire(data, file_)

    stored_book = library.locate(book_id)[0]
    assert stored_book.is_file()
    assert len(library.search(title=data["title"])) == 1

    library.discard(book_id)

    assert library.locate(book_id) == []
    assert not stored_book.is_file()
    assert len(library.inventory()) == 1
    assert library.search(title=data["title"]) == []
