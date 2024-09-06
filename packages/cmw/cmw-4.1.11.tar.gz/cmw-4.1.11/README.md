# CommonMark Website

This is a Python package that provides the command line utility `cmw`.

It stands for "CommonMark Website".

It converts `.md` CommonMark files into HTML then deploys to GitHub.

## Installation

    pip install cmw

## Usage

Place your `.md` CommonMark files into the `input` directory like this:

    input/index.md
    input/About.md
    input/Contact_Us.md

To compile your code into HTML files:

    cmw

It will place results in the `output` directory.

To override input and output directories, provide them as arguments:

    cmw docs-src docs

To initialize a boilerplate HTML template into the `input` directory, run:

    cmw init

or, to initialize it in a custom directory:

    cmw init docs-src

## Dependencies

- [mistletoe](https://github.com/miyuchina/mistletoe), one of the Python
  CommonMark implementations listed on the CommonMark spec
  [wiki](https://github.com/commonmark/commonmark-spec/wiki/List-of-CommonMark-Implementations)
