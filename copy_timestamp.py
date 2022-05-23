#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from os import stat, utime
from sys import platform


is_win = platform.startswith('win')


def __copy_timestamp_platform_decorator(f):
	"""Makes function conditionless and yet platform-specific. To avoid recursion, it's actually easier with decorator."""
	if not is_win:
		# for unix - use the function as is
		return f
	
	# for windows - completely ignore 'follow_symlinks' argument
	def _wrapper(source, target, follow_symlinks=True, ):
		return f(source, target, follow_symlinks=True, )
	return _wrapper


@__copy_timestamp_platform_decorator
def copy_timestamp(source, target, follow_symlinks=True, ):
	"""
	Copy timestamps from one file to another. follow_symlinks arg is ignored on Windows.
	
	Return the applied timestamp (nanoseconds precision, as returned by os.stat).
	"""
	src_stat = stat(source, follow_symlinks=follow_symlinks)
	timestamp_ns = (src_stat.st_atime_ns, src_stat.st_mtime_ns)
	utime(target, ns=timestamp_ns, follow_symlinks=follow_symlinks, )
	return timestamp_ns


def main(*args):
	parser = ArgumentParser(description='Copy access/modification time from one file to another.')
	parser.add_argument("source_file", help="file to copy timestamp from")
	parser.add_argument("target_file", help="file to copy timestamp to")
	parser.add_argument(
		"-n", "--nofollow", help="[unix-only] don't follow symlinks (followed by default)",
		dest='follow', action='store_false',
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
	# with open(r"P:\1-Scripts\_Python\Py-CMD\qqq.log", 'wt', newline='\n') as f:
	# 	f.writelines(f"{x}\n" for x in argv)
	main(*argv[1:])
