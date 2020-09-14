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
    describe: 'Output file path, default "./release-notes-{base}-{head}.md"',
    default: null,
  }).option('skip', {
    type: 'array',
    alias: 's',
    describe: 'One or more keywords to skip from the given pattern match',
    default: [],
  }).option('verbose', {
    type: 'boolean',
    alias: 'v',
    describe: 'Show verbose output',
    default: false,
  })
}

const handler = ({ base, head, pattern, file, skip, verbose }) => {
  try {
    let cmd = 'git fetch --prune'
    log(cmd, { verbose })
    execSync(cmd)

    cmd = `git tag -il '${pattern}' --cleanup=strip --sort version:refname`
    if (skip.length) {
      cmd += ` | grep -v '${skip.join('\\|')}'`
    }
    cmd += ' | tail -2'
    log(cmd, { verbose })
    const [_base, _head] = execSync(cmd).toString().trim().split('\n')

    const version = (head || _head).trim()
    const previous = (base || _base).trim()
    cmd = `git log --no-merges --format='%h::%s::%b::%an||' ${version}...${previous}`
    log(cmd, { verbose })
    const logs = execSync(cmd).toString().trim().split('||').map(log => log.trim()).filter(log => log)
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
