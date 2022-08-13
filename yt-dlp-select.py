#!/usr/bin/env python
# encoding: utf-8
"""
Wrapper for ``yt-dlp`` utility, letting to choose it's arguments easier.

It requires the main executable to be in `PATH`

The main program:
https://github.com/yt-dlp/yt-dlp
"""

__version__ = '1.0.0'
__author__ = 'Lex Darlog (DRL)'

import shutil
import subprocess


PROGRAM = 'yt-dlp'
PROGRAM_PATH = shutil.which(PROGRAM)
OUT_DIR = "E:/0-Downloads/0-YouTube"
NAME_FORMAT = "%(title)s - %(id)s.%(ext)s"
RES_LIMIT = {
	"1080": "[height<=?1080]",
	"720": "[height<=?720]",
	"480": "[height<=?480]",
}
FORMAT_SELECTOR = "bestvideo{res_limit}[ext=mp4]+bestaudio[ext=m4a]"
EXTRA_ARGS = [
	"--merge-output-format", "mp4",
]


def main(*args):
	video_url = input(f"Video link:")

	all_res = '/'.join(RES_LIMIT.keys())
	res_arg = input(f"Max resolution ([empty=best]/{all_res}):")

	format_selector = FORMAT_SELECTOR.format(res_limit=RES_LIMIT.get(res_arg, ''))

	cmd = [
		PROGRAM_PATH,
		'-P', OUT_DIR,
		'-P', "temp:",
		'-o', NAME_FORMAT,
		'-f', format_selector,
	]
	cmd.extend(EXTRA_ARGS)
	cmd.append(video_url)

	print('')
	print(' '.join(repr(x) for x in cmd))
	print('')
	res = subprocess.call(cmd)

	input("Done!")

	exit(res)


if __name__ == '__main__':
	from sys import argv

	main(*argv[1:])
