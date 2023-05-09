# gdrive-cms

## Status: Very early work in Progress

This is yet another google drive backed CMS. The idea is:

- Author docs in google drive
- This tool downloads the docs into local files (maybe HTML / markdown / whatever)
- Use a static site builder to incorporate the content from google drive into a website

We're planning on using google spreadsheets to provide metadata for directories,
and maybe some table-based frontmatter in the google docs for document-specific
metadata.

## Architecture

As a first path, this is a bunch of python scripts orchestrated by `make`.

First we download just the versions of the files in drive, to allow make to keep
track of which files we've already processed and which are new.

Next we download the file contents (where the file version is newer than our
current download).

Then we do some transformations on the contents to make it easier to work with
(e.g. stripping cruft from HTML).

Finally, we tie everything up in a format which should make it easy to work with
in most static site generators. This may include outputting types (e.g.
TypeScript) for each of the documents.
