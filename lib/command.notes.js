const { parseCommits, formatNotes, writeNotes, log, exec } = require('./utils')
const { updateRelease } = require('./github')


const options = (yargs) => {
  yargs.option('base', {
    type: 'string',
    default: null,
    description: 'base ref, default second latest tag of the given --pattern',
  }).option('head', {
    type: 'string',
    default: null,
    description: 'head ref, default latest tag of the given --pattern',
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
  }).option('github', {
    type: 'boolean',
    alias: 'gh',
    description: 'Flag to redirect file output to updating the head ref (tag) associated GitHub release',
    default: false,
  }).option('fetch', {
    type: 'boolean',
    description: 'Perform a `git fetch --prune` before carrying out the rest of the command',
    default: true,
  }).option('verbose', {
    type: 'boolean',
    alias: 'v',
    describe: 'Show verbose output',
    default: false,
  })
}

const handler = async ({ base, head, pattern, file, skip, github, fetch, verbose }) => {
  const _exec = exec({ verbose })
  try {
    if (fetch) {
      _exec('git fetch --prune')
    }

    let cmd = `git tag -il '${pattern}' --cleanup=strip --sort version:refname`
    if (skip.length) {
      cmd += ` | grep -v '${skip.join('\\|')}'`
    }
    cmd += ' | tail -2'
    const [_base, _head] = _exec(cmd).toString().trim().split('\n')

    const version = (head || _head || '').trim()
    const previous = (base || _base || '').trim()
    cmd = `git log --no-merges --format='%h::%s::%b::%an||' ${version}...${previous}`
    const logs = _exec(cmd).toString().trim().split('||').map(log => log.trim()).filter(log => log)
    const parsed = parseCommits(logs)

    const notes = formatNotes({ parsed, version, previous })

    if (!github) {
      writeNotes({ notes, version, previous, file })
    } else {
      await updateRelease({ notes, tag: version, verbose })
    }
  } catch(err) {
    if (verbose) {
      console.error(err)
    }
    log(err, { severity: 'error' })
  }
}

module.exports = {
  command: 'notes',
  description: 'Generate notes based on git refs',
  options,
  handler,
}
