# Digital Paper Edit - Infrastructure

This is purely the infrastructural part to tie together with
[firebase](https://github.com/bbc/digital-paper-edit-firebase/) of Digital Paper
Edit.

| Environment | URL                                               |
| :---------- | :------------------------------------------------ |
| Test        | <https://digital-paper-edit.test.tools.bbc.co.uk> |
| Live        | <https://digital-paper-edit.live.tools.bbc.co.uk> |

For historical undestanding of this repo, read
[ADR 2019-04-23-transcript-architecture.md](https://github.com/bbc/digital-paper-edit-client/blob/master/docs/ADR/2019-04-23-transcript-architecture.md)
for more information.

## System Architecture

## Usage

- `infrastructure` contains deployment configurations.
- `SPEC` contains instructions to build an RPM. specific code. (WIP)

The `Makefile` has instructions that will allow you to build your RPMS and
release them. `Makefile`, you can build the RPM that pulls in the NPM modules,
that contain the logic.

These `Makefile` instructions will only work on BBC CentOS based machines, as it
requires certain BBC specific dependencies.

## Development

Development for components should be done in the
[Client](https://github.com/bbc/digital-paper-edit-firebase/).

### Dependencies

See [Client](https://github.com/bbc/digital-paper-edit-firebase/).

### Build

The RPM build is specific per environment. What this means is that environment
specific configuration is pulled in at build-time. It's retrieved via the SSM
(AWS's System Service Manager) and bundled in with `npm run build`. See
[Configuration section](#configuration-files) for more details.

#### Cloudformation

You can build the AWS Stacks in `infrastructure` by running `make all`. This
will install Python dependencies in your `virtualenv` folder and generate the
templates.

If you only want to build the stacks, run `make stacks`. If you want to create
the Cloudformation, you will need to do it manually
[here](https://cosmos.tools.bbc.co.uk/services/digital-paper-edit-infrastructure).

### Deployment

For BBC deployment we use
[Jenkins job](https://jenkins.newslabs.tools.bbc.co.uk/job/digital-paper-edit-infrastructure/).
This will use the [Jenkins Deploy script](./jenkins-deploy) to update CFNs,
build and release the RPM to the corresponding environment.

### Configuration files

The [Client](https://github.com/bbc/digital-paper-edit-firebase/) needs a
working `.env` to be able to run.

The `.env` file is pulled in during the `make dpe-prep` step. This step will
work on EC2 instances with attached instance profiles, that have permissions to
access the specified parameters and keys. With working instances, it's able to
pull in environment specific file and corresponding decrypt keys.

The parameters in SSM should be named:

- test-digital-paper-edit-env
- live-digital-paper-edit-env

The keys in KMS should have aliases:

- alias/test-digital-paper-edit
- alias/live-digital-paper-edit

Jenkin's IAM Policy has been updated as part of
[issue 15](https://github.com/bbc/newslabs-jenkins/pull/15) and
[issue 16](https://github.com/bbc/newslabs-jenkins/pull/16) in Jenkins.

## Licence

<!-- mention MIT Licence -->

See [LICENCE](./LICENCE.md)

## Legal Disclaimer

_Despite using React and DraftJs, the BBC is not promoting any Facebook products
or other commercial interest._
