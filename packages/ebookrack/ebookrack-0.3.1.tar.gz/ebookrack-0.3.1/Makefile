# SPDX-FileCopyrightText: 2024 JA Viljoen <ebookrack@javiljoen.net>
# SPDX-License-Identifier: EUPL-1.2

check: test lint

lint:
	black --check -q src tests
	isort --check -q src tests
	flake8 src tests
	reuse lint --lines

test:
	pytest -qq

fmt:
	black src tests
	isort src tests

build:
	flit build --format wheel

publish:
	flit publish --use-vcs

upload: clean build
	hut git artifact upload dist/*-$(version)-*.whl --rev $(version)
upload: version != python -c 'import ebookrack; print(ebookrack.__version__)'

clean:
	find src/ tests/ -type d -name __pycache__ -exec rm -r '{}' +
	rm -rf .pytest_cache/
	rm -rf dist/

.PHONY: build check clean fmt lint publish test upload
