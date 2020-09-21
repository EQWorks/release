# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `notes` - `--github, --gh` flag to redirect file output to updating the head ref (tag) associated GitHub release
	* Requires valid `$GITHUB_TOKEN` and `$GITHUB_OWNER` environment variables
	* Support `$GITHUB_REPO` environment variable, but default to git local toplevel name
- `notes` - `--fetch` flag to control whether to run git fetch before the rest fo the command

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
