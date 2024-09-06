# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

import pytest

from ebookrack.catalogue import Catalogue

inferno = dict(
    ISBN="1234",
    author="Dante",
    title="The Inferno",
    tags={"fiction", "renaissance"},
    language="Italian",
)
life_story = dict(
    ISBN="1235",
    author="Dante",
    translator="Chaucer",
    title="My life story",
    tags={"non-fiction"},
    language="English",
)
canterbury = dict(
    ISBN="1236",
    author="Chaucer",
    title="The Canterbury tales",
    tags={"fiction", "renaissance"},
    language="English",
)


@pytest.fixture
def catalogue():
    catalogue = Catalogue()
    catalogue.new_card(inferno)
    catalogue.new_card(life_story)
    catalogue.new_card(canterbury)
    return catalogue


def test_search_by_author(catalogue):
    assert catalogue.search(author="Dante") == [inferno, life_story]


def test_search_by_single_tag(catalogue):
    assert catalogue.search(tags={"renaissance"}) == [inferno, canterbury]


def test_search_by_multiple_tags(catalogue):
    assert catalogue.search(tags={"fiction", "renaissance"}) == [inferno, canterbury]


def test_search_by_author_and_tag(catalogue):
    assert catalogue.search(author="Dante", tags={"fiction"}) == [inferno]


def test_search_empty_query(catalogue):
    assert catalogue.search() == [inferno, life_story, canterbury]


def test_search_by_unknown_params(catalogue):
    assert catalogue.search(translator="Chaucer") == [life_story]
    assert catalogue.search(reviewer="booksRsux69") == []


def test_search_by_known_and_unknown_param(catalogue):
    assert catalogue.search(author="Dante", translator="Chaucer") == [life_story]
    assert catalogue.search(author="Dante", banned=False) == []
    assert catalogue.search(author="Dante", banned=True) == []


def test_edit_card_updates_card_data():
    catalogue = Catalogue()
    book_id = catalogue.new_card(inferno)

    catalogue.edit_card(book_id, author="Dante Alighieri")

    assert catalogue.retrieve_card(book_id) == {
        **inferno,
        "id": book_id,
        "status": "ACTIVE",
        "author": "Dante Alighieri",
    }


def test_destroy_card_replaces_with_placeholder(catalogue):
    book_id = list(catalogue.card_index).pop()
    catalogue.destroy_card(book_id)

    assert catalogue.retrieve_card(book_id) == {"id": book_id, "status": "DELETED"}


def test_destroyed_cards_are_excluded_from_card_index(catalogue):
    initial_index = catalogue.card_index
    assert list(initial_index) == [0, 1, 2]
    catalogue.destroy_card(1)

    assert catalogue.card_index == {0: initial_index[0], 2: initial_index[2]}
