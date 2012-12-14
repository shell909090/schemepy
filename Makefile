#!/usr/bin/make -f
CC=gcc
CFLAGS=$(shell python-config --includes) $(shell python-config --libs)

all: build

clean:
	rm -f *.o *.so *.pyc

build: parser.so

%.so: %.c
	$(CC) $(CFLAGS) -shared -o $@ $^

%.c: %.pyx
	cython -o $@ $^