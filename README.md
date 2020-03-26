# release-notes-util

A tool for compiling release notes

## Usage

Install necessary packages:
`yarn`

Create a `.env` file, formatted like so:

```bash
PROJECT_PATH=[path to root project folder]
LATEST=[most recent git tag]
PREVIOUS=[previous git tag]

# Example

PROJECT_PATH=[homepath]/EQWorks/Projects/snoke
LATEST=v1.4.4
PREVIOUS=v1.4.3
```

Run with `yarn start`

A file will be created called `release-notes-[the value of LATEST]`.

### Important Note

Currently, this only works if commit messages are formatted like so:

`[feature name] - message`
