.PHONY: all

all: out/versions/%.version

out/versions/%.version:
	python3 scripts/get-versions.py $(FOLDER_ID)
