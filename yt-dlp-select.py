#!/usr/bin/env python
# encoding: utf-8
"""
Wrapper for ``yt-dlp`` utility, letting to choose it's arguments easier.

It requires the main executable to be in `PATH`

The main program:
https://github.com/yt-dlp/yt-dlp
"""

__version__ = '1.0.3'
__author__ = 'Lex Darlog (DRL)'

from itertools import chain
import os
from pathlib import Path
from shlex import quote
import shutil
import subprocess
import sys

from typing import *


# Put your system-specific config here:

OUT_DIR = "E:/0-Downloads/0-YouTube"
COOKIES_FILE = '_cookies.txt'  # empty = don't use / absolute path / path relative to `OUT_DIR`
FORMAT_SELECTOR = "bestvideo{res_limit}[ext=mp4]+bestaudio[ext=m4a]"
EXTRA_ARGS_PRE = [
	"-U",
]
EXTRA_ARGS_POST = [
	"--merge-output-format", "mp4",
	# "--cookies-from-browser", "firefox:DRL"  # DRL: doesn't work, throws error # format: "BROWSER[+KEYRING][:PROFILE]"
	"--sponsorblock-mark", "all",
	"--sponsorblock-remove", "sponsor,interaction",
]
PATH_EXTEND = [
	# if you don't want to put `ffmpeg` and `yt-dlp` directories to system `PATH` variable, you can set them here.
	# You need to put DIRECTORIES of these programs, not full paths to them.
	# Each path as a separate string (dont forget comma at the end). Example:
	# 'C:/Users/MyUserName/Documents',

	'',
]


# -----------------------------------------------------------------------------


PROGRAM = 'yt-dlp'
PROGRAM_URL = 'https://github.com/yt-dlp/yt-dlp/releases'
PROGRAM_DEPENDENCIES = [
	('https://www.ffmpeg.org/download.html\n\n(for Windows - recommended: full-GPL-static-shared)', ['ffmpeg', 'ffprobe'])
]
COOKIES_HELP_URL = 'https://github.com/ytdl-org/youtube-dl/blob/master/README.md#how-do-i-pass-cookies-to-youtube-dl'
NAME_FORMAT = "%(title)s - %(id)s.%(ext)s"
RES_LIMIT = {
	"1080":	"[height<=?1080]",
	"720":	"[height<=?720]",
	"480":	"[height<=?480]",
}
RES_BEST = ''


def is_ok_str(val):
	return isinstance(val, str) and val


def exit_error(msg: str):
	input(msg)
	exit(msg)


def exit_binary_missing(nice_name: str, binary: str, url: str = None):
	url_postfix = f"\n\nIf the binary is missing, you can download it here:\n{url}\n" if url else ''
	return exit_error(
		f"{nice_name} not found: {binary}\n"
		f"You might need to add it's directory to system `PATH` environment variable "
		f"or to `PATH_EXTEND` variable in the script.{url_postfix}"
	)


def check_module_config():
	for val, var_name, nice_name in [
		(PROGRAM, 'PROGRAM', 'Main program'),
		(OUT_DIR, 'OUT_DIR', 'Output directory'),
		(NAME_FORMAT, 'NAME_FORMAT', 'Output filename format'),
		(FORMAT_SELECTOR, 'FORMAT_SELECTOR', 'Video-format selector'),
	]:
		if not is_ok_str(val):
			exit_error(f"{nice_name} is not specified. Define the proper value for `{var_name}`")

	for extra_arg in EXTRA_ARGS_PRE:
		if extra_arg is None or (isinstance(extra_arg, str) and not extra_arg):
			exit_error(f"Incorrect prefix extra arg: `{extra_arg}`")
	for extra_arg in EXTRA_ARGS_POST:
		if extra_arg is None or (isinstance(extra_arg, str) and not extra_arg):
			exit_error(f"Incorrect suffix extra arg: `{extra_arg}`")


def cookies_warning(msg: str):
	print(
		f"\n\t▼ WARNING ▼\n{msg}\n"
		f"Some videos might fail downloading. Instructions on how to configure cookies:\n{COOKIES_HELP_URL}"
	)


def append_cookies_arg(cmd: List[str]):
	file_subpath = COOKIES_FILE if COOKIES_FILE is None or isinstance(COOKIES_FILE, str) else str(COOKIES_FILE)
	if not file_subpath:
		return cookies_warning("Cookies file is not configured.")

	file_path = Path(OUT_DIR) / COOKIES_FILE
	file_path_str = str(file_path.absolute())
	if not file_path.is_file():
		return cookies_warning(f"Cookies file is missing: {file_path_str}")

	cmd.extend([
		'--cookies', file_path_str
	])


def update_sys_path(*paths: str):
	"""Sync `os.environ['PATH']` and `sys.path` + append given paths to both"""

	new_paths = list(sys.path)
	sys_paths_set = set(new_paths)
	# also add those which are somehow defined in `os.environ['PATH']` but not in `sys.path`
	new_paths.extend(x for x in os.environ['PATH'].split(os.pathsep) if x not in sys_paths_set)
	new_paths.extend(paths)

	new_paths = [x for x in new_paths if x and isinstance(x, str)]

	sys.path[:] = new_paths
	os.environ['PATH'] = os.pathsep.join(new_paths)


def main(*args):
	check_module_config()

	update_sys_path(*PATH_EXTEND)

	program_path = shutil.which(PROGRAM)
	if not is_ok_str(program_path):
		exit_binary_missing('Main program', PROGRAM, PROGRAM_URL)
	for bin_url, bin_names in PROGRAM_DEPENDENCIES:
		for bin_nm in bin_names:
			bin_path = shutil.which(bin_nm)
			if not is_ok_str(bin_path):
				exit_binary_missing('Dependency', bin_nm, bin_url)

	video_url = input(f"Video link >")
	if not is_ok_str(video_url):
		exit_error(f"No video link given")

	all_res_options = '/'.join(chain(
		['[empty=best]', ],
		RES_LIMIT.keys()
	))
	res_arg = input(f"Max resolution ({all_res_options}) >")

	format_selector = FORMAT_SELECTOR.format(res_limit=RES_LIMIT.get(res_arg, RES_BEST))

	cmd = [program_path, ]
	cmd.extend(EXTRA_ARGS_PRE)
	cmd.extend([
		'-P', OUT_DIR,
		'-P', "temp:",
		'-o', NAME_FORMAT,
		'-f', format_selector,
	])
	append_cookies_arg(cmd)
	cmd.extend(EXTRA_ARGS_POST)
	cmd.append(video_url)

	cmd_str = ' '.join(quote(x) for x in cmd)
	print(f"\nStarting:\n{cmd_str}\n")
	return subprocess.call(cmd)


if __name__ == '__main__':
	from sys import argv

	res = main(*argv[1:])
	input("Done!")

	exit(res)
