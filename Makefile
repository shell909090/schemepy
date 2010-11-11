#!/usr/bin/make -f
CC=gcc

all: build

clean:
	rm -f *.o *.pyc

build: parser

parser: parser.o