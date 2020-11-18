#!/usr/bin/env node
const { notes, changelog, tag } = require('./lib')

if (require.main === module) {
  require('yargs')
    .usage('Usage: $0 <command> [options]')
    .command(
      notes.command,
      notes.description,
      notes.options,
      notes.handler,
    )
    .command(
      changelog.command,
      changelog.description,
      changelog.options,
      changelog.handler,
    )
    .command(
      tag.command,
      tag.description,
      tag.options,
      tag.handler,
    )
    .demandCommand()
    .help()
    .argv
} else {
  module.exports = require('./lib/utils')
}
