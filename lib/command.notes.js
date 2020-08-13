const { execSync } = require('child_process')

const { parseCommits, formatNotes, writeNotes, log } = require('./utils')


const options = (yargs) => {
  yargs.option('base', {
    type: 'string',
    default: null,
    description: 'base ref, default second latest tag',
  }).option('head', {
    type: 'string',
    default: null,
    description: 'head ref, default latest tag',
  }).option('pattern', {
    type: 'string',
    default: 'v*',
    description: 'tag matching pattern. Ignored when both head and base refs are specified',
  }).option('file', {
    type: 'string',
    alias: 'f',
    describe: 'Output file path, default "./release-notes-{version}.md"',
    default: null,
  })
}

const handler = ({ base, head, pattern, file, verbose }) => {
  try {
    let cmd = 'git fetch --prune'
    log(cmd, { verbose })
    execSync(cmd)

    cmd = `git tag -il '${pattern}' --cleanup=strip --sort version:refname | tail -2`
    log(cmd, { verbose })
    const [_base, _head] = execSync(cmd).toString().trim().split('\n')

    const version = head || _head
    const previous = base || _base
    cmd = `git log --no-merges --format='%h::%s' ${version}...${previous}`
    log(cmd, { verbose })
    const logs = execSync(cmd).toString().trim().split('\n')
    const parsed = parseCommits(logs)

    const notes = formatNotes({ parsed, version, previous })
    writeNotes({ notes, version, previous, file })
  } catch(err) {
    log(err, { severity: 'error' })
  }
}

module.exports = {
  command: 'notes',
  description: 'Generate notes based on git refs',
  options,
  handler,
}
