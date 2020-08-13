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

Which would give you a markdown such as:

```md
## Release Notes: from v1.7.0 to v1.7.2

### devops

* alpha package release
* fix netlify ignore script to account for multi-line commit msg

### table

* update when sort changes dynamically [build]
```

You can learn more about the CLI by typing `release` or `release [COMMAND] --help`.

### Important Note

Currently, this only works if commit messages are formatted like so:

`category - message`
