#!/usr/bin/env node
const { notes } = require('./lib')

if (require.main === module) {
  require('yargs')
    .usage('Usage: $0 <command> [options]')
    .command(
      notes.command,
      notes.description,
      notes.options,
      notes.handler,
    )
    .demandCommand()
    .help()
    .argv
} else {
  module.exports = require('./lib/utils')
}
