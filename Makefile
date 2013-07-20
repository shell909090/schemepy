#!/usr/bin/make -f

## Author: xuzx@shterm.com
## Version: $Id: Makefile,v 0.0 2011/05/18 06:19:52 shell Exp $
## Keywords: 
## X-URL: 

all: build-rpm build-deb

clean:
	rm -rf build dist MANIFEST covhtml .coverage report.txt

test:
	python test_scheme.py

check:
	pymetrics -SC schemepy/*.py > report.txt
	pychecker --no-shadowbuiltin -qtv6r -# 100 schemepy >> report.txt

covhtml:
	python-coverage run test_scheme.py
	python-coverage html -d $@

clean-deb:
	fakeroot debian/rules clean

build-deb:
	dpkg-buildpackage -rfakeroot

build-rpm:
	python setup.py bdist_rpm
