# release

A CLI for release notes generation based on tags and commit history.

## Installation

```shell
yarn global add @eqworks/release
# or
npm i -g @eqworks/release
```

## Usage

In any git repo (suppose the tagging pattern is `v*`, you can use `--pattern` option to fit yours), run:

```shell
release notes --print --skip alpha
```

Which would give you a markdown such as:

```md
## Release Notes: from v1.4.0 to v1.5.0

### devops

* [CORRECTIVE, FEATURES] dogfood github release notes after npm publish (f5718f8 by Runzhou Li (woozyking))

### notes

* [FEATURES, PERFECTIVE] `--fetch` flag to control whether to run git fetch (28550c9 by Runzhou Li (woozyking))
* [FEATURES, CORRECTIVE] `--github` flag to update the head ref associated GitHub release (21d6278 by Runzhou Li (woozyking))
	* omit local file output
	* factor out `utils.exec` to perform `execSync` and `log`
	* requires `$GITHUB_TOKEN`, `$GITHUB_OWNER`, and `$GITHUB_REPO` env vars
	* `$GITHUB_REPO` falls back to local repo toplevel name
```

Since v2.0.0, a new command `changelog` with NLP based auto labelling intended for changelog-like formatting is added:

```shell
release changelog --print --skip alpha
```

Which gives:

```md
## Changelog: from v1.4.0 to v1.5.0

### CORRECTIVE

* devops - dogfood github release notes after npm publish (f5718f8 by Runzhou Li (woozyking))

### FEATURES

* notes - `--fetch` flag to control whether to run git fetch (28550c9 by Runzhou Li (woozyking))
* notes - `--github` flag to update the head ref associated GitHub release (21d6278 by Runzhou Li (woozyking))
	* omit local file output
	* factor out `utils.exec` to perform `execSync` and `log`
	* requires `$GITHUB_TOKEN`, `$GITHUB_OWNER`, and `$GITHUB_REPO` env vars
	* `$GITHUB_REPO` falls back to local repo toplevel name
```

You can learn more about the CLI by typing `release` or `release <command> --help`.

### Tips

The following convention should be applied on your commit messages for ideal parsing:

> category - message

where `category` can contain a secondary portion such as

> category/sub category.

For example:

> builder/details - show job viz for newly created, unprocessed jobs

Since v1.3.0, a generic `others` category is added to capture all unparsed commit messages.
