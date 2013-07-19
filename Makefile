#!/usr/bin/make -f

## Author: xuzx@shterm.com
## Version: $Id: Makefile,v 0.0 2011/05/18 06:19:52 shell Exp $
## Keywords: 
## X-URL: 

PYTHON=python2.6
CC=gcc
CFLAGS=$(shell python-config --includes) $(shell python-config --libs)

all: build-rpm build-deb

clean:
	rm -rf build dist MANIFEST covhtml

test:
	python test_scheme.py

check:
	pychecker --no-shadowbuiltin -qtv6r -# 100 schemepy

covhtml:
	python-coverage run test_scheme.py
	python-coverage html -d $@

clean-deb:
	fakeroot debian/rules clean

build-deb:
	dpkg-buildpackage -rfakeroot

build-rpm:
	$(PYTHON) setup.py bdist_rpm --python=$(PYTHON)
