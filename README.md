# release

A CLI for release notes generation based on tags and commit history.

## Installation

```shell
yarn global add @eqworks/release
# or
npm i -g @eqworks/release
```

## Usage

In any git repo, run:

```shell
release notes
```

You can learn more about the CLI by typing `release` or `release [COMMAND] --help`.

### Important Note

Currently, this only works if commit messages are formatted like so:

`[feature name] - message`
