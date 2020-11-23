# release

A CLI for changelog and release notes generation based on tags and commit history.

## Installation

```shell
yarn global add @eqworks/release
# or
npm i -g @eqworks/release
```

## Usage

### Changelog
In any git repo (suppose the tagging pattern is `v*`, you can use `--pattern` option to fit yours), run:

```shell
release changelog --print --skip alpha
```

Which would give you a markdown such as:

```md
## Changelog: from v2.1.1 to v3.0.0

### CHANGED

* version - v3.0.0 (b2156bd by Tamires)

### FIXED

* lib/parse-subject - fix t2 when no match by default it to 'others' (3593397 by Tamires Lowande)
* lib/baseHandler - cover single tag and no tag cases (281c4c0 by Runzhou Li (woozyking))

### ADDED

* nlp - add model training process as a jupyter notebook (1c57956 by Runzhou Li (woozyking))
* lib/parseCommits - update to the newly trained sub-1MB NLP model (d7c4a1e by Runzhou Li (woozyking))
```

Since v2.0.0, an NLP based auto labelling mechanism has been added, along with the sub-command `changelog` intended for changelog-like formatting (as shown above).

Since v3.0.0, the NLP model has been [retrained](https://github.com/EQWorks/release/pull/20) to adhere to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

### Notes

The original sub-command `notes` can be used for a more "feature" oriented formatting:

```shell
% release notes --print --skip alpha
```

Which gives:

```md
## Release Notes: from v2.1.1 to v3.0.0

### version

  * [CHANGED, ADDED] v3.0.0 (b2156bd by Tamires)

### lib

* #### parse-subject

  * [FIXED, CHANGED] fix t2 when no match by default it to 'others' (3593397 by Tamires Lowande)

* #### parseCommits

  * [ADDED, CHANGED] update to the newly trained sub-1MB NLP model (d7c4a1e by Runzhou Li (woozyking))

* #### baseHandler

  * [FIXED, CHANGED] cover single tag and no tag cases (281c4c0 by Runzhou Li (woozyking))

### nlp

  * [ADDED, CHANGED] add model training process as a jupyter notebook (1c57956 by Runzhou Li (woozyking))
```


### Tag

Since v3.1.0, the sub-command `tag` identifies the version inside the commit messages and can either create a local tag with the commit version as its name or make a github release using the `--github` flag
```shell
% release tag --github
```
Reads from the latest 3 commits (default) and can be changed with the `-n` flag


You can learn more about the CLI by typing `release` or `release <command> --help`.

### Tips

The following convention should be applied on your commit message's subject for ideal parsing:

> category - message

where `category` can have a `sub-category` following a forward slash `/`

> main-category/sub-category - message

For example:

> builder/details - show job viz for newly created, unprocessed jobs

Since v1.3.0, a generic `others` category is added to capture all unparsed commit messages.
