.PHONY: clean all versions

DOCS_VERSIONS = $(wildcard out/versions/*.google-docs-version)
DOCS_CONTENTS = $(DOCS_VERSIONS:out/versions/%.google-docs-version=out/contents/%.html)
SHEETS_VERSIONS = $(wildcard out/versions/*.google-sheets-version)
SHEETS_CONTENTS = $(SHEETS_VERSIONS:out/versions/%.google-sheets-version=out/contents/%.csv)

all: versions $(DOCS_CONTENTS) $(SHEETS_CONTENTS)

clean:
	rm -f out/versions/*version out/contents/*.html out/contents/*.csv

versions: scripts/get-versions.py
	python3 scripts/get-versions.py $(FOLDER_ID)

out/contents/%.html: out/versions/%.google-docs-version
	python3 scripts/get-contents.py $^ > $@

out/contents/%.csv: out/versions/%.google-sheets-version
	python3 scripts/get-contents.py $^ > $@