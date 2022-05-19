#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from os import stat, utime
from sys import platform


is_win = platform.startswith('win')


def copy_timestamp(source, target, follow_symlinks=True, ):
	if is_win:
		follow_symlinks = True
	src_stat = stat(source, follow_symlinks=follow_symlinks)
	return utime(target, ns=(src_stat.st_atime_ns, src_stat.st_mtime_ns), follow_symlinks=follow_symlinks)


def main(*args):
	parser = ArgumentParser(description='Copy access/modification time from one file to another.')
	parser.add_argument("source_file", help="file to copy timestamp from")
	parser.add_argument("target_file", help="file to copy timestamp to")
	parser.add_argument(
		"-n", "--nofollow", help="don't follow symlinks (followed by default; unix-only)",
		action='store_false', dest='follow',
	)
	parser.add_argument(
		"-v", "--verbose", help="print what's being done",
		action='store_true',
	)

	out_args = parser.parse_args(args)
	source = out_args.source_file
	target = out_args.target_file
	follow = out_args.follow
	win_nofollow_msg = ''
	if is_win and not follow:
		win_nofollow_msg = "[no --nofollow on Windows] "
		follow = True
	
	res = copy_timestamp(source, target, follow_symlinks=follow)
	
	if out_args.verbose:
		symlinks = '' if follow else ' [nofollow]'
		print(f"{win_nofollow_msg}Timestamps copied{symlinks}: {source} -> {target}")
	return res


if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])
