.PHONY: all build test check clean build-deb
all: build

build:
	uv build

test:
	uv run python -m unittest discover -v

check:
	ruff check --select E9,F63,F7,F82 schemepy test_scheme.py

clean:
	rm -rf build dist MANIFEST covhtml .coverage report.txt

build-deb:
	dpkg-buildpackage -rfakeroot
