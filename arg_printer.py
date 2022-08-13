#!/usr/bin/env python
# encoding: utf-8

def main(*args):
	print(args)


if __name__ == '__main__':
	from sys import argv
	
	main(*argv[1:])
