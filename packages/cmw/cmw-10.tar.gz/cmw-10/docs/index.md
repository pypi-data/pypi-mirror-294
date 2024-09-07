## Introduction

CommonMark Website (cmw) is a command-line utility designed to simplify the
creation and management of websites using markdown files. It eliminates the
repetitive task of updating raw HTML pages by allowing you to configure your
site through a YAML file and generate HTML automatically.

## Getting started

Run the following command to install cmw:

    pip install cmw

Then run the following commands to make a new directory, and initialize a new
project:

    mkdir project
    cd project
    cmw init

Then cmw initializes your site by creating three essential files: config.yaml,
template.html, and index.md. You can then customize the config.yaml for
configuration, and add your content to index.md. You can preview the site by
running:

    cmw server

Doing this will convert the markdown files into HTML and launch a development
server for live viewing in your browser. If you just want to generate HTML
files without a server, simply run cmw without any arguments.

## Rationale / Purpose

The CommonMark Website (cmw) utility was born out of frustration with the
repetitive and tedious work required to maintain websites built using raw HTML.
For websites with multiple pages—such as portfolios with dozens of
projects—updating shared elements like headers, navigation bars, and footers
across all pages becomes a time-consuming task. This is especially true for
websites that are actively being developed or updated over time.

The purpose of cmw is to simplify this process by allowing users to write their
website content in markdown files and then automatically generate the HTML for
the entire site, complete with shared elements. By abstracting away the
repetitive manual updates, cmw not only streamlines the workflow but also
empowers users to focus on content creation rather than code maintenance. It’s
an efficient, lightweight solution for developers who want the flexibility of a
professional-looking website without the complexity of manually managing each
individual page in HTML.

We chose YAML for its simplicity and ease of use, making configuration
straightforward. CommonMark allows for flexibility with raw HTML when needed,
while also simplifying common formatting tasks like text, lists, and links.
It’s a great fit for text-heavy websites.
