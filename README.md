# release

A CLI for release notes generation based on tags and commit history.

## Installation

```shell
yarn global add @eqworks/release
# or
npm i -g @eqworks/release
```

## Usage

In any git repo (suppose the tagging pattern is `v*`), run:

```shell
release notes
```

Which would give you a markdown such as:

```md
## Release Notes: from v1.1.0-alpha to v1.2.0-alpha

### notes

* add - author name per commit (ee73c70 by Runzhou Li (woozyking))
* fix - unxpected cutoff on extra "-", "/" (e8454fc by Runzhou Li (woozyking))
* fix - tag cleanup mode :typo: on 'strip' (97e0763 by Runzhou Li (woozyking))

### version

* 1.1.0 (af3bb6d by Runzhou Li (woozyking))
```

You can learn more about the CLI by typing `release` or `release [COMMAND] --help`.

```shell
% release notes --help
release notes

Generate notes based on git refs

Options:
  --version   Show version number                                      [boolean]
  --help      Show help                                                [boolean]
  --base      base ref, default second latest tag       [string] [default: null]
  --head      head ref, default latest tag              [string] [default: null]
  --pattern   tag matching pattern. Ignored when both head and base refs are
              specified                                 [string] [default: "v*"]
  --file, -f  Output file path, default "./release-notes-{version}.md"
                                                        [string] [default: null]
```

### Important Note

Currently, this only works if commit messages are formatted like so:

`category - message`, where `category` can contain a secondary portion such as `category/sub category`.
