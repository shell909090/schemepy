#!/usr/bin/make -f
CC=gcc
CFLAGS=$(shell python-config --includes) $(shell python-config --libs)

all: build

clean:
	rm -f *.o *.so *.pyc

build: objects.so

%.so: %.c
	$(CC) $(CFLAGS) -shared -o $@ $^

%.c: %.py
	cython -o $@ $^