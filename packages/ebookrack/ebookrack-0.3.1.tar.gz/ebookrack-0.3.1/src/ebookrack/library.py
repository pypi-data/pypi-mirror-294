# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

"""Library component

The Library is the interface by which users (librarians and borrowers)
interact with the contents of the library (books and their metadata).

The following use cases can be performed by a web app, API, CLI, etc.
through this interface:

   #. Acquire new book (add metadata & upload file/s)
   #. Add / update book metadata
   #. Move book to different storage location
   #. Add (upload) multiple formats to a book
   #. Discard a book (metadata & file/s)
   #. Search for a book / certain books
   #. List all books in the library
   #. Download / locate a book
"""

import logging
from dataclasses import dataclass

from .catalogue import Catalogue
from .shelf import Shelf

__all__ = ["Library"]


@dataclass
class Library:
    _catalogue: Catalogue
    _shelf: Shelf

    def acquire(self, book_data, book_file):
        book_id = self._catalogue.new_card(book_data)
        book_data = self._catalogue.retrieve_card(book_id)
        self._shelf.shelve(book_id, book_data, book_file)
        return book_id

    def edit_metadata(self, book_id, **new_data):
        self._catalogue.edit_card(book_id, **new_data)

        if "title" in new_data:
            self.reshelve(book_id)

    def reshelve(self, book_id):
        book_data = self._catalogue.retrieve_card(book_id)
        self._shelf.reshelve(book_id, book_data)

    def acquire_additional_format(self, book_id, book_file):
        book_data = self._catalogue.retrieve_card(book_id)
        self._shelf.shelve(book_id, book_data, book_file)

    def replace_shelf(self, new_shelf):
        self._shelf.transfer_all(self._catalogue.card_index, new_shelf)
        self._shelf = new_shelf

    def discard(self, book_id):
        self._shelf.discard(book_id)
        self._catalogue.destroy_card(book_id)

    def search(self, **query):
        matches = self._catalogue.search(**query)
        logging.info(f"Found {format_count(len(matches), 'book')} matching {query}")
        return matches

    def inventory(self):
        return list(self._catalogue.card_index.values())

    def locate(self, book_id):
        books = self._shelf.locate(book_id)
        return [book.path for book in books]


def format_count(number, noun):
    suffix = "s" if number != 1 else ""
    return f"{number} {noun}{suffix}"
