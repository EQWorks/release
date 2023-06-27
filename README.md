# release

A CLI for changelog and release notes generation based on tags and commit history.

## Installation

If you have `npx` available, you can directly use it without explicit installation:

```shell
% npx @eqworks/release --help
```

Otherwise, or when explicitly local installation is needed:

```shell
% yarn global add @eqworks/release
% # or
% npm i -g @eqworks/release
```

Then:

```shell
% release --help
```

## Usage

For best formatting result, follow the conventions below:

> category - message

Where `category` can have a `sub-category` following a forward slash `/`.

> main-category/sub-category - message

For example:

> builder/details - show job viz for newly created, unprocessed jobs

Since v1.3.0, a generic `others` category is added to capture all unparsed commit messages.

Check the detailed [git conventions](https://github.com/EQWorks/common/blob/main/git.md) for more details.

### Changelog (by label)

In any git repo (suppose the tagging pattern is `v*`, you can use `--pattern` option to fit yours), run:

```shell
% npx @eqworks/release changelog --print --skip alpha
```

The result is in markdown formatted changelog.

Since v2.0.0, an NLP-based auto labelling mechanism has been added, along with the sub-command `changelog` intended for changelog-like formatting (as shown above).

Since v3.0.0, the NLP model has been [retrained](https://github.com/EQWorks/release/pull/20) to adhere to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

### Notes (by category)

The sub-command `notes` can be used for more category-oriented formatting:

```shell
% npx @eqworks/release notes --print --skip alpha
```

The result is in markdown formatted release notes.

### Tag

Since v3.1.0, the sub-command `tag` identifies the version inside the commit messages and can either create a local tag with the commit version as its name or make a GitHub release using the `--github` flag:

```shell
% npx @eqworks/release tag --github
```

The above command reads from the latest three commits (by default, change with the `-n` flag.)

## Important note for Node.js 18

When running the CLI commands on Node.js 18, you may need to add the `--no-experimental-fetch` flag to the `NODE_OPTIONS` environment variable. This flag is required to disable the experimental fetch feature introduced in Node.js 18.

To execute the CLI commands with the `--no-experimental-fetch` flag, use the following syntax:

```shell
% NODE_OPTIONS=--no-experimental-fetch npx @eqworks/release <command>