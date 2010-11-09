#!/usr/bin/make -f
CC=gcc

all: build

clean:
	rm -f *.o

build: parser

parser: parser.o