# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from ebookrack.calibre.metadata import (
    Metadata,
    parse_date,
    parse_ids,
    parse_opf,
    parse_year,
)

DATA_DIR = Path("tests", "library")
ELVES_OPF = DATA_DIR.joinpath(
    "Andrzej Sapkowski",
    "Blood of Elves (219)",
    "metadata.opf",
)
ORIGIN_OPF = DATA_DIR.joinpath(
    "Charles Darwin",
    "On the Origin of Species By Means of Natural Selection, or, the Preservation of Favoured Races (195)",
    "metadata.opf",
)
ALICE_OPF = DATA_DIR.joinpath(
    "Lewis Carroll",
    "Alice's Adventures in Wonderland (1)",
    "metadata.opf",
)
PLANTS_OPF = DATA_DIR.joinpath(
    "Charles Darwin",
    "Insectivorous Plants (2)",
    "metadata.opf",
)
HOMER_OPF = DATA_DIR.joinpath(
    "Homer",
    "The Odyssey (3)",
    "metadata.opf",
)
opf_files = [ELVES_OPF, ORIGIN_OPF, ALICE_OPF, PLANTS_OPF, HOMER_OPF]

elves_data = Metadata(
    title="Blood of Elves",
    authors=["Andrzej Sapkowski"],
    pubdate="2010",
    publisher="Orion",
    language="eng",
    tags={"Fiction"},
    ids={"MOBI-ASIN": "B0043M66Z4"},
    series="The Witcher",
    series_index="3",
    importdate="2020-11-12",
)
origin_data = Metadata(
    title=(
        "On the Origin of Species By Means of Natural Selection, or, "
        "the Preservation of Favoured Races in the Struggle for Life"
    ),
    authors=["Charles Darwin"],
    pubdate="2009",
    publisher="Project Gutenberg",
    language="eng",
    tags={"Non-fiction", "Biology"},
    ids={"URI": "http://www.gutenberg.org/ebooks/1228"},
    series="",
    series_index="",
    importdate="2019-12-09",
)
alice_data = Metadata(
    title="Alice's Adventures in Wonderland",
    authors=["Lewis Carroll"],
    pubdate="2008",
    publisher="",
    language="eng",
    tags={"Children's stories", "Fantasy fiction"},
    ids={},
    series="",
    series_index="",
    importdate="2023-06-22",
)
plants_data = Metadata(
    title="Insectivorous Plants",
    authors=["Charles Darwin"],
    pubdate="2004",
    publisher="",
    language="eng",
    tags={"Carnivorous plants"},
    ids={},
    series="",
    series_index="",
    importdate="2023-06-22",
)
homer_data = Metadata(
    title="The Odyssey",
    authors=["Homer", "Samuel Butler"],
    pubdate="1999",
    publisher="",
    language="eng",
    tags={"Epic poetry"},
    ids={},
    series="",
    series_index="",
    importdate="2023-06-22",
)
data_sets = [elves_data, origin_data, alice_data, plants_data, homer_data]


@pytest.mark.parametrize("opf_file,data", zip(opf_files, data_sets))
def test_parse_opf(opf_file, data):
    assert parse_opf(opf_file) == data


@pytest.mark.parametrize(
    "timestamp,date",
    [
        ("2020-11-12T11:00:58+00:00", "2020-11-12"),
        ("", ""),
    ],
)
def test_parse_date(timestamp, date):
    assert parse_date(timestamp) == date


@pytest.mark.parametrize(
    "timestamp,year",
    [
        ("2020-11-12T11:00:58+00:00", "2020"),
        ("", ""),
    ],
)
def test_parse_year(timestamp, year):
    assert parse_year(timestamp) == year


ids_xml = """\
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
  <dc:identifier opf:scheme="calibre" id="calibre_id">219</dc:identifier>
  <dc:identifier opf:scheme="uuid" id="uuid_id">29a8f81c-ca4f-43d5-9638-535936ed62d5</dc:identifier>
  <dc:identifier opf:scheme="MOBI-ASIN">B0043M66Z4</dc:identifier>
  <dc:identifier opf:scheme="URI">http://www.gutenberg.org/ebooks/1228</dc:identifier>
  <dc:identifier opf:scheme="ISBN">9781680508451</dc:identifier>
</metadata>
"""


def test_parse_ids():
    meta = ET.fromstring(ids_xml)
    ids = meta.findall("{http://purl.org/dc/elements/1.1/}identifier")
    assert parse_ids(ids) == {
        "MOBI-ASIN": "B0043M66Z4",
        "ISBN": "9781680508451",
        "URI": "http://www.gutenberg.org/ebooks/1228",
    }
