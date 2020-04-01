#!/usr/bin/env node
const { execSync } = require('child_process')

const lib = require('./lib')

if (require.main === module) {
  require('yargs')
  .usage('Usage: $0 <command> [options]')
  .command(
    'notes',
    'Generate notes based on git refs',
    yargs => yargs
      .option('base', {
        type: 'string',
        default: null,
        description: 'base ref, default second latest tag',
      })
      .option('head', {
        type: 'string',
        default: null,
        description: 'head ref, default latest tag',
      })
      .option('pattern', {
        type: 'string',
        default: 'v*',
        description: 'tag matching pattern. Ignored when both head and base refs are specified',
      })
      .option('file', {
        type: 'string',
        alias: 'f',
        describe: 'Output file path, default "./release-notes-{version}.md"',
        default: null,
      })
    ,
    ({ base, head, pattern, file }) => {
      try {
        let cmd = 'git fetch --prune'
        console.log(cmd)
        execSync(cmd)

        cmd = `git tag -il '${pattern}' --cleanup=srip | tail -2`
        console.log(cmd)
        const [_base, _head] = execSync(cmd).toString().trim().split('\n')

        const version = head || _head
        const previous = base || _base
        cmd = `git log --no-merges --abbrev-commit --pretty=oneline ${version}...${previous}`
        console.log(cmd)
        const logs = execSync(cmd).toString().trim().split('\n')
        const parsed = lib.processLog(logs)

        const notes = lib.formatNotes({ parsed, version, previous })
        lib.writeNotes({ notes, version, previous, file })
      } catch(err) {
        // console.log(err)
      }
    },
  )
  .demandCommand()
  .help()
  .argv
} else {
  module.exports = lib
}
