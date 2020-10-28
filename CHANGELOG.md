# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.1] - 2020-10-28

### CORRECTIVE

* common/github - order tags by committerdate instead of version name (8aa4d22 by Tamires Lowande)

## [2.1.0] - 2020-10-15

### FEATURES

* lib/formatNotes - group by T2 (242ebea by Tamires Lowande)
* lib/parseCommits - T1-categories to be normalized (9b27f1c by Tamires Lowande)

## [2.0.1] - 2020-10-06

### CORRECTIVE

* github - fix incorrect reference to the formatted notes (f70cf62 by Runzhou Li (woozyking))

## [2.0.0] - 2020-10-06 (NLP enchanted)

### CORRECTIVE

* lib - fix NLP model loading to be portable (58ef627 by Runzhou Li (woozyking))
* lib/parseCommits - fix error case return, print full error log on `-v` (c83c3b3 by Runzhou Li (woozyking))

### FEATURES

* notes - utilize NLP labels into the format (1ac3818 by Runzhou Li (woozyking))
	* README - update with latest big changes
* misc - update CHANGELOG.md by dogfooding the changelog cmd (ea4be5b by Runzhou Li (woozyking))
* common - --print flag to redirect file output to stdout (print) (558da11 by Runzhou Li (woozyking))
* changelog - command to generate changelog with NLP predicted labels (ddf4799 by Runzhou Li (woozyking))
* lib/parseCommits - enrich with NLP model predicted label (27ecd40 by Runzhou Li (woozyking))
	* [BREAKING] `parseCommits` now returns a Promise (async function)
	* NLP model trained and applied through fastText (by facebook)

### PERFECTIVE

* lib - factor out lib/common and refactor command to be like plugins (ce658b4 by Runzhou Li (woozyking))

## [1.5.0] - 2020-09-22

### CORRECTIVE

* devops - dogfood github release notes after npm publish (f5718f8 by Runzhou Li (woozyking))

### FEATURES

* notes - `--fetch` flag to control whether to run git fetch (28550c9 by Runzhou Li (woozyking))
* notes - `--github` flag to update the head ref associated GitHub release (21d6278 by Runzhou Li (woozyking))
	* omit local file output
	* factor out `utils.exec` to perform `execSync` and `log`
	* requires `$GITHUB_TOKEN`, `$GITHUB_OWNER`, and `$GITHUB_REPO` env vars
	* `$GITHUB_REPO` falls back to local repo toplevel name

## [1.4.0] - 2020-09-14

### Changed
- `notes` - parse with named capture groups (beb99f6 by hyx131)
- `notes` - match invalid filename chars and replace with dash (ea2862b by hyx131)

### Added
- `notes` - `--skip, -s` multi-options to skip tags based on keywords (eg `-s alpha -s beta`) (19f65d9 by Runzhou Li (woozyking))
- `notes` - (actually officialize) `--verbose, -v` option (19f65d9 by Runzhou Li (woozyking))

## [1.3.0] - 2020-09-11

### Added
- `notes` - support commit message body (b386123 by Runzhou Li (woozyking))
	* body is persed per line as list item and indented under its subject
	* body lines that start with `- ` and `* ` are standardized as `- `
- `notes` - A generic "others" category to capture all parser-unmatched (fe5bfb1 by Runzhou Li (woozyking))

### Changed
- `notes` - regex based parser (0488a32 by Runzhou Li (woozyking))

### Fixed
- `notes` - dash `-` parsing error for category (b57aedb by hyx131)

## [1.2.0] - 2020-08-21
### Added
- `notes` - author name per commit

### Fixed
- `notes` - unexpected cutoff at extra "-" and "/" characters

## [1.1.0] - 2020-08-14
### Added
- `notes` - support tier 2 category, when commit message subject is in the form of `tier1/tier2 - title`
- `notes` - CLI `--verbose` option controlled non-error and non-eventual output messages
- `notes` - colorful output messages

### Changed
- `notes` - improve tag sorting to support semver (where `v0.10.0` would be properly considered as newer than `v0.3.4`)

## [1.0.1] - 2020-04-02
### Added
- `notes` - portable CLI
- `notes` - include previous and current versions in output header and default file name

## [0.1.0] - 2020-03-26
### Added
- `notes` - initial release
