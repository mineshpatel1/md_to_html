# md_to_html

Markdown to HTML converter using [Pandoc](https://pandoc.org/) and a customised HTML template. This is a wrapper for Pandoc which is already highly feature rich, just allowing some customisations and syntax changes for personal use. Documents created with this are standalone HTML files with images embedded, but are required to be online for the following:

* Fonts (default to Helvetica/Arial)
* JQuery, for content navigation and animation
* MathJax, for rendering equations

## Requirements

* [Pandoc](https://pandoc.org/installing.html)
* [Python 3](https://www.python.org/downloads/)

## Usage

```bash
md_to_html sample/sample.md
```

Will create an output file `sample.html` in the same directory as sample.md. Please see:

* `sample/sample.md` for help with markdown syntax and examples
* `sample/sample.html` for an example of output

### Optional Arguments

* `-o`, `--output`: Specify an output filename, must have a `.html` extension.
* `-c`, `--contents`: Dynamically creates a content navigation pane based on the headers.
* `-n`, `numbered`: Numbers all of the headings based on their hierarchy.
* `-h`, `--help`: Brings up the help text