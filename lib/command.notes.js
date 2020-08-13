const { execSync } = require('child_process')

const { processLog, formatNotes, writeNotes } = require('./utils')


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
    if (verbose) {
      console.log(cmd)
    }
    execSync(cmd)

    cmd = `git tag -il '${pattern}' --cleanup=srip --sort version:refname | tail -2`
    if (verbose){
      console.log(cmd)
    }
    const [_base, _head] = execSync(cmd).toString().trim().split('\n')

    const version = head || _head
    const previous = base || _base
    cmd = `git log --no-merges --format='%h::%s' ${version}...${previous}`
    if (verbose){
      console.log(cmd)
    }
    const logs = execSync(cmd).toString().trim().split('\n')
    const parsed = processLog(logs)

    const notes = formatNotes({ parsed, version, previous })
    writeNotes({ notes, version, previous, file })
  } catch(err) {
    console.error(err)
  }
}

module.exports = {
  command: 'notes',
  description: 'Generate notes based on git refs',
  options,
  handler,
}
