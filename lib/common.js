const { parseCommits, write, log, exec } = require('./utils')
const { updateRelease } = require('./github')

module.exports.options = (yargs) => yargs
  .option('base', {
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
    describe: 'Output file path, default "./release-{command}-{base}-{head}.md"',
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
  }).option('print', {
    type: 'boolean',
    alias: 'p',
    description: 'Flag to redirect file output to stdout (print)',
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

module.exports.baseHandler = ({ command, formatter }) => async ({
  base,
  head,
  pattern,
  file,
  skip,
  github,
  print,
  fetch,
  verbose,
}) => {
  const _exec = exec({ verbose })
  try {
    if (fetch) {
      _exec('git fetch --prune')
    }

    let cmd = `git tag -il '${pattern}' --cleanup=strip --sort=-committerdate`
    if (skip.length) {
      cmd += ` | grep -v '${skip.join('\\|')}'`
    }
    cmd += ' | head -2'
    const [_head, _base] = _exec(cmd).toString().trim().split('\n')

    const version = (head || _head || '').trim()
    const previous = (base || _base || '').trim()
    cmd = `git log --no-merges --format='%h::%s::%b::%an||' ${version}...${previous}`
    const logs = _exec(cmd).toString().trim().split('||').map(log => log.trim()).filter(log => log)
    const parsed = await parseCommits({ logs, verbose })

    const formatted = formatter({ parsed, version, previous })

    if (print) {
      console.log(formatted)
    } else if (github) {
      await updateRelease({ formatted, tag: version, verbose })
    } else {
      write(command)({ formatted, version, previous, file })
    }
  } catch(err) {
    if (verbose) {
      console.error(err)
    }
    log(err, { severity: 'error' })
  }
}
