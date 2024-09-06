# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2
"""
parse book metadata from an OPF file
"""

import functools
import xml.etree.ElementTree as ET
from dataclasses import dataclass

nss = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "opf": "http://www.idpf.org/2007/opf",
}


@dataclass(frozen=True)
class Metadata:
    title: str
    authors: list[str]
    pubdate: str
    publisher: str
    language: str
    tags: set[str]
    ids: dict[str, str]
    series: str
    series_index: str
    importdate: str


def parse_date(timestamp):
    return timestamp.split("T")[0]


def parse_year(timestamp):
    return parse_date(timestamp)[:4]


def parse_ids(identifiers):
    """Extract relevant IDs as a scheme:ID mapping.

    Expected input: list of <dc:identifiers> elements
    """
    return {
        scheme: el.text
        for el in identifiers
        if (scheme := el.get("{http://www.idpf.org/2007/opf}scheme"))
        not in {"uuid", "calibre"}
    }


def parse_metadata(metadata):
    find_all = functools.partial(metadata.findall, namespaces=nss)
    find_text = functools.partial(metadata.findtext, namespaces=nss)

    title = find_text("dc:title")
    authors = [x.text for x in find_all("dc:creator")]
    pubdate = parse_year(find_text("dc:date"))
    publisher = find_text("dc:publisher")
    language = find_text("dc:language")
    tags = {x.text for x in find_all("dc:subject")}
    ids = parse_ids(find_all("dc:identifier"))

    extra = {x.get("name"): x.get("content") for x in find_all("opf:meta")}
    series = extra.get("calibre:series", "")
    series_index = extra.get("calibre:series_index", "")
    importdate = parse_date(extra.get("calibre:timestamp", ""))

    return Metadata(
        title or "",
        authors,
        pubdate or "",
        publisher or "",
        language or "",
        tags,
        ids,
        series,
        series_index,
        importdate,
    )


def parse_opf(opf_file):
    tree = ET.parse(opf_file)
    root = tree.getroot()
    meta_elem = root.find("opf:metadata", namespaces=nss)
    return parse_metadata(meta_elem)
