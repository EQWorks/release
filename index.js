#!/usr/bin/env node
const { notes, changelog } = require('./lib')

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
    .demandCommand()
    .help()
    .argv
} else {
  module.exports = require('./lib/utils')
}
