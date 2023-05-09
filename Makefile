.PHONY: clean all versions

DOCS_VERSIONS = $(wildcard out/versions/*.google-docs-version)
DOCS_CONTENTS = $(DOCS_VERSIONS:out/versions/%.google-docs-version=out/contents/%.html)
DOCS_TRANSFORMED = $(DOCS_CONTENTS:out/contents/%.html=out/transformed-contents/%.html)
SHEETS_VERSIONS = $(wildcard out/versions/*.google-sheets-version)
SHEETS_CONTENTS = $(SHEETS_VERSIONS:out/versions/%.google-sheets-version=out/contents/%.csv)
SHEETS_TRANSFORMED = $(SHEETS_CONTENTS:out/contents/%.csv=out/transformed-contents/%.csv)

all: versions $(DOCS_TRANSFORMED) $(SHEETS_TRANSFORMED)

clean:
	rm -f out/versions/*version out/contents/*.html out/contents/*.csv out/transformed-contents/*.csv out/transformed-contents/*.html

versions: scripts/get-versions.py
	python3 scripts/get-versions.py $(FOLDER_ID)

out/transformed-contents/%.html: out/contents/%.html
	python3 scripts/transform-html.py < $^ > $@

out/transformed-contents/%.csv: out/contents/%.csv
	cp $^ $@

out/contents/%.html: out/versions/%.google-docs-version
	python3 scripts/get-contents.py $^ > $@

out/contents/%.csv: out/versions/%.google-sheets-version
	python3 scripts/get-contents.py $^ > $@