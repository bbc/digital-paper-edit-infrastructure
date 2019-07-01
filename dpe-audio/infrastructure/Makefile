.PHONY: all clean cleanvenv venv stacks

SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,stacks/templates/%.json,$(SOURCES))

all: clean venv $(TARGETS)

clean:
	rm -rf $(TARGETS)

cleanvenv:
	rm -rf venv

stacks/templates/%.json: src/%.py 
	venv/bin/python3 $< > $@

stacks: $(TARGETS)

venv: cleanvenv requirements.txt
	python3 -m venv $@
	$@/bin/pip install --upgrade pip setuptools wheel
	$@/bin/pip install -r requirements.txt
