# Digital Paper Edit - Infrastructure

This is purely the infrastructural part to tie together the (API)[https://github.com/bbc/digital-paper-edit-api/] and the [client](https://github.com/bbc/digital-paper-edit-client/) of Digital Paper Edit.

[See here for overall project architecture info](https://github.com/bbc/digital-paper-edit-client#project-architecture)

[Link to API]()

[Confluence Page](<link to confluence page>)
![](<Screenshot of UI>)

## System Architecture

## Usage

* `infrastructure` contains AWS specific configurations.
* `SPEC` contains instructions to build an RPM.
* `dpe-api` contains [API](https://github.com/bbc/digital-paper-edit-api/) specific code.
* `dpe-client` contains [Client](https://github.com/bbc/digital-paper-edit-client/) specific code.

The `Makefile` has instructions that will allow you to build your RPMS and release them.
There are 3 `Makefile`s in this repository:

1. Root level
2. `dpe-api`
3. `dpe-client`

The root level `Makefile` will allow you to package an RPM that will pull in `dpe-client` and `dpe-api` that is released into a `yum` repository in Cosmos. There is nothing else in there. This will be deployed to Cosmos via Jenkins to install and automatically start the services. It is still a WIP, and will not work as is - there still needs to be work done for accessing the `Cosmos yum` repo.

At the `dpe-api` and `dpe-client` `Makefile`, you can build the RPM that pulls in the NPM modules, that contain the logic.

These `Makefile` instructions will only work on BBC CentOS based machines, as it requires certain BBC specific dependencies.

## Development

### Dependencies

Both `dpe-api` and `dpe-client` services pull in a dependency from the BBC NPM.

#### dpe-api

* [API](https://github.com/bbc/digital-paper-edit-api/)

The API Express is directly used without assignment.

#### dpe-client

* [Client](https://github.com/bbc/digital-paper-edit-client/)

### Running

#### Locally

In both `dpe-api` and `dpe-client` run:
```
npm start
```

This will start client and api at [http://localhost:8080](http://localhost:8080) and [http://localhost:5000](http://localhost:5000).

### Build

#### Cloudformation

You can build the AWS Stacks in `infrastructure` by running `make all`. This will install Python dependencies in your `virtualenv` folder and generate the templates.

### Style guide
<airbnb style, Typescript>

### Deployment

The [Jenkins job](https://jenkins.newslabs.tools.bbc.co.uk/job/digital-paper-edit/) is still WIP, and will not work as is. If you want to update Cloudformation, you will need to do it manually [here](https://cosmos.tools.bbc.co.uk/services/digital-paper-edit-infrastructure).

## Contact
Please contact [BBC News Labs Team](BBCNewsLabsTeam@bbc.co.uk) if you want to get in touch.

<!-- 

## Brief of the project

_One liner + link to confluence page_

_Screenshot of UI - optional_

 

## Setup

_stack - optional_

_How to build and run the code/app_

 

## Usage

 

## System Architecture

_High level overview of system architecture_

 

## Development env

 _How to run the development environment_

_Coding style convention ref optional, eg which linter to use_

_Linting, github pre-push hook - optional_

 

## Build

_How to run build_

 

## Tests

_How to carry out tests_

 

## Deployment

_How to deploy the code/app into test/staging/production_

 -->

 <!-- ## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) guidelines and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) guidelines. -->

## Licence
<!-- mention MIT Licence -->
See [LICENCE](./LICENCE.md)

## Legal Disclaimer

_Despite using React and DraftJs, the BBC is not promoting any Facebook products or other commercial interest._