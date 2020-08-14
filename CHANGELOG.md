# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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
