NAME:=digital-paper-edit-client

all: RPMS

SOURCES/$(NAME).tar.gz: dpe
	@ # Create a tarball to be used as a source in the RPM spec.
	mkdir -p SOURCES
	tar --exclude ".svn" --exclude ".*.sw?" --exclude "*.py[co]" -czf SOURCES/$(NAME).tar.gz src/

SOURCES: SOURCES/$(NAME).tar.gz

dpe-prep: 
	@ mkdir -p src/usr/lib/$(NAME)
	git clone git@github.com:bbc/digital-paper-edit-firebase.git src/usr/lib/$(NAME)
	cd src/usr/lib/$(NAME) && npm install 

dpe-build:
	aws --region eu-west-1 ssm get-parameters --name test-digital-paper-edit-env --with-decryption | jq '.Parameters[0].Value' > .env
	npm run build

dpe: dpe-prep dpe-build

RPMS: SOURCES SPECS/$(NAME).spec
	@ rm -rf RPMS && mkdir RPMS
	mock-build --os 7 -r repos.d

clean:
	rm -rf SOURCES RPMS SRPMS src/usr/lib/$(NAME)

release: clean dpe SOURCES SPECS/$(NAME).spec
	@ mkdir RPMS
	# Build the package in an fresh CentOS 7 build environment, containing\
	# just the RPMs listed as build dependencies in the .spec file.  See
	# https://github.com/bbc/bbc-mock-tools for more information.  Also
	# adds an extra part to the version string containing an
	# auto-incrementing build number.
	mock-build --os 7 --define "buildnum $(shell cosmos-release generate-version $(NAME))"
	# Send the RPM and other release metadata to Cosmos.  See
	# https://github.com/bbc/cosmos-release/ for more information
	cosmos-release service $(NAME) RPMS/*.rpm

deploy_test:
	cosmos deploy $(NAME) test -f
	cosmos deploy-progress $(NAME) test

.PHONY: test deploy_test release clean all dpe
