.PHONY: all clean npm-install prepare local release

# PLEASE CHANGE THE FOLLOWING
COMPONENT="dpe-api"

all: local

test:
	# Install all dependencies for test, including devDependencies
	npm install --prefix src --no-bin-links
	# Run the tests in a centos7 mock environment for access to a newer version of node
	# and to more closely mimic the target environment
	mock-run --os 7 --install "npm" --copyin src src --shell "npm test --prefix src"

.PHONY: npm-test
npm-test:
	npm install --prefix src
	npm test --prefix src

.PHONY: test-docker
test-docker:
	docker run --rm -v `pwd`:/workspace -w /workspace node:10 make npm-test

clean:
	rm -rf src/node_modules RPMS SRPMS SOURCES

npm-install:
	# Avoid installing the devDependencies with --production
	npm --production --prefix src install --no-bin-links

prepare: npm-install
	# Bundle the source code into a single .tar.gz file, used in
	# combination with the .spec file to create the RPM(s)
	mkdir -p RPMS SRPMS SOURCES
	tar --exclude=".svn" --exclude="*.sw?" --exclude="*.pyc" -czf SOURCES/src.tar.gz src/

local: clean prepare
	# Build an RPM locally without any cosmos interactions
	mock-build --os 7

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

deploy_int:
	cosmos deploy $(COMPONENT) int -f
	cosmos deploy-progress $(COMPONENT) int
