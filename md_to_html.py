import os
import re
import sys
import argparse
from subprocess import check_output

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def parse_arguments():
	"""Parses the input arguments and returns a tuple of the requisite variables."""

	parser = argparse.ArgumentParser(description="Markdown to HTML Converter")
	parser.add_argument('md_file', action='store', help='Relative path to the markdown file to convert.')
	parser.add_argument('-o', '--output_file', action='store', default=None,
	                    help='Specifies output filename, otherwise uses the original filename with a .html extension')
	parser.add_argument('-c', '--contents', action='store_true', default=False,
	                    help='Creates a dynamic contents menu based on the headings in the document.')
	parser.add_argument('-n', '--numbered', action='store_true', default=False,
	                    help='Numbers headings and sub headings according to their level.')
	args = parser.parse_args()

	md_file = os.path.abspath(args.md_file)
	if not os.path.exists(md_file):
		raise FileNotFoundError('Markdown file %s does not exist.' % md_file)

	if args.output_file is None:
		output_file = md_file[:-2] + 'html'
	else:
		output_file = os.path.abspath(args.output_file)

	return md_file, output_file, not args.contents, args.numbered


def convert_md(md_file, output_file, contents, numbered):
	"""Converts the markdown file to HTML using Pandoc."""

	script = ['pandoc', '-s', md_file, '-o', output_file]
	script += ['-c', os.path.join(SCRIPT_DIR, 'themes', 'base.css')]
	script += ['-B', os.path.join(SCRIPT_DIR, 'themes', 'header.html')]

	# Check the markdown to see if we need to include MathJax
	maths = False if re.search('\\n\\$\\$(.*?)\\$\\$\\n', read_file(md_file),
	                           flags=re.MULTILINE | re.DOTALL) is None else True

	if numbered:
		script.append('--number-sections')

	if contents:
		script.append('--toc')

	if maths:
		script.append('--mathjax')

	script += ['--self-contained', '--highlight-style=haddock']

	with cd(os.path.dirname(md_file)):
		print('Converting %s to %s using Pandoc...' % (os.path.basename(md_file), os.path.basename(output_file)))
		check_output(script)  # Runs the script on the OS and raises an exception on failure

	include_fonts(output_file)  # Include Google fonts
	if contents or maths:
		include_js(output_file, maths)
		add_contents(output_file)


def add_contents(html_file):
	"""Adds content navigation pane."""
	html = read_file(html_file)
	contents_js = read_file(os.path.join(SCRIPT_DIR, 'themes', 'contents.js'))
	html = html.replace('function loadFunc() {', contents_js)

	place_holder = '<div class="header_banner">'
	tags = '<div class="navbar_container">\n<div class="navbar"/>\n</div>'
	tags += '<div class="content_button">\n<div class="chevron">></div>\n</div>'
	tags += '\n' + place_holder

	html = html.replace(place_holder, tags)
	html = html.replace('<div id="TOC">', '<div class="canvas">\n<div id="TOC">')
	html = html.replace('</body>', '</div>\n</body>')
	write_file(html_file, html)


class cd:
	"""Context manager for changing the current working directory."""

	def __init__(self, new_path):
		self.new_path = new_path

	def __enter__(self):
		self.saved_path = os.getcwd()
		os.chdir(self.new_path)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.saved_path)


def read_file(file_path):
	with open(file_path, 'r') as f:
		content = f.read()
	return content


def write_file(file_path, content):
	with open(file_path, 'w') as f:
		f.write(content)


def replace_in_file(file_path, find, replace):
	"""Update HTML by replacing a known tag"""
	content = read_file(file_path)
	content = content.replace(find, replace)
	write_file(file_path, content)


def include_js(html_file, maths=False):
	"""Includes JS files in the file"""
	meta = '<meta name="generator" content="pandoc" />'
	html = read_file(html_file)

	js_html = meta
	js_html += '\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>'  # jQuery

	if maths:  # MathJax
		# Find the injected JS from Pandoc for MathJax and remove it. Using this flag keeps the correct syntax in the HTML
		# The Pandoc MathJax inject doesn't apply the right option flags
		injected_js = re.findall('<script src="data:application/javascript;.*?type="text/javascript"></script>', html)
		html = html.replace(injected_js[0], '')
		js_html += '\n<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>'

	html = html.replace(meta, js_html)
	write_file(html_file, html)

	replace_in_file(html_file, meta, js_html)


def include_fonts(html_file):
	meta = '<meta name="generator" content="pandoc" />'
	html = meta
	for f in ['Open Sans', 'Source Sans Pro']:
		ref = f.replace(' ', '+')
		ref = ref + ':300,400,400italic,700italic,700'
		html += '\n<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=%s">' % ref

	replace_in_file(html_file, meta, html)


def main():
	md_file, output_file, contents, numbered = parse_arguments()
	convert_md(md_file, output_file, contents, numbered)


if __name__ == '__main__':
	main()
