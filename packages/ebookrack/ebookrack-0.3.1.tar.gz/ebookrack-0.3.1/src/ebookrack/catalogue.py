# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

import dataclasses
import enum
from dataclasses import dataclass

__all__ = ["Catalogue"]


Status = enum.Enum("Status", "ACTIVE DELETED")


@dataclass
class Card:
    _book_id: int
    _data: dict
    _status: Status = Status.ACTIVE

    @property
    def book_data(self):
        return {"id": self._book_id, "status": str(self._status.name), **self._data}

    @property
    def is_deleted(self):
        return self._status is Status.DELETED

    def matches(self, params):
        for field, search_term in params.items():
            if field not in self._data:
                return False

            if isinstance(search_term, set):
                if not search_term.issubset(self._data[field]):
                    return False
            else:
                if self._data[field] != search_term:
                    return False

        return True

    def edit(self, new_data):
        self._data.update(new_data)

    def erase(self):
        self._data = {}
        self._status = Status.DELETED


@dataclass(frozen=True)
class Catalogue:
    _cards: list[Card] = dataclasses.field(default_factory=list)

    @property
    def card_index(self):
        return {
            card.book_data["id"]: card._data
            for card in self._cards
            if not card.is_deleted
        }

    def new_card(self, book_data):
        card = Card(len(self._cards), book_data)
        self._cards.append(card)
        return card.book_data["id"]

    def search(self, **query):
        return [card._data for card in self._cards if card.matches(query)]

    def retrieve_card(self, book_id):
        return self._cards[book_id].book_data

    def edit_card(self, book_id, **new_data):
        card = self._cards[book_id]
        card.edit(new_data)

    def destroy_card(self, book_id):
        card = self._cards[book_id]
        card.erase()
