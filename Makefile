.PHONY: all clean local release

# PLEASE CHANGE THE FOLLOWING
COMPONENT="digital-paper-edit"

all: local


prepare: 
	# Bundle the source code into a single .tar.gz file, used in
	# combination with the .spec file to create the RPM(s)
	mkdir -p RPMS SRPMS SOURCES
	#tar --exclude=".svn" --exclude="*.sw?" --exclude="*.pyc" -czf SOURCES/src.tar.gz src/


clean:
	rm -rf RPMS SRPMS SOURCES

clean-deps:
	cd dpe-client && make clean
	cd dpe-api && make clean

local: clean prepare
	# Build an RPM locally without any cosmos interactions
	mock-build --os 7

local-deps:
	cd dpe-client && make local
	cd dpe-api && make local

release: clean prepare
	# Build the package in an fresh CentOS 7 build environment, containing
	# just the RPMs listed as build dependencies in the .spec file.  See
	# https://github.com/bbc/bbc-mock-tools for more information.  Also
	# adds an extra part to the version string containing an
	# auto-incrementing build number.
	mock-build --os 7 --define "buildnum $(shell cosmos-release generate-version $(COMPONENT))"

	# Send the RPM and other release metadata to Cosmos.  See
	# https://github.com/bbc/cosmos-release/ for more information
	cosmos-release service $(COMPONENT) RPMS/*.rpm

release-deps: 
	cd dpe-client && make release
	cd dpe-api && make release
