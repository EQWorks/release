const { parseCommits, write, log, exec } = require('./utils')
const { githubHandler } = require('./github')


const INCEPTION = 'INCEPTION'
const { GITHUB_TOKEN } = process.env

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
  }).option('remove-revert', {
    type: 'boolean',
    alias: 'rr',
    describe: 'Remove revert commits',
    default: false,
  }).option('include-contributors', {
    type: 'boolean',
    describe: 'Include contributors stats and their GitHub profile links. Default true if $GITHUB_TOKEN is present, ignored otherwise.',
    default: Boolean(GITHUB_TOKEN),
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
  'remove-revert': revert,
  'include-contributors': contrib,
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
    const [_head, _base] = _exec(cmd).toString().trim().split('\n').filter(t => t)

    const isRevert = /(revert)/gi
    let _revertCommits = []
    const version = (head || _head || 'HEAD').trim()
    const previous = (base || _base || INCEPTION).trim()
    const diff = `${version}${previous !== INCEPTION ? `...${previous}` : ''}`
    cmd = `git log --no-merges --format='%h::%s::%b::%an||' ${diff}`

    const _logs = _exec(cmd).toString().trim().split('||').map((log) => {
      if (revert) {
        log.match(isRevert) && _revertCommits.push(log.split('::')[0].replace(/^(\n)/, ''))
      }
      return log.trim()
    })

    /** since we're filtering out merge commits from this flow initially, parents will always have one direct commit */
    const getParentCmd = (commit) => `git show -s --pretty=%p ${commit}`
    const parentCommit = (commit) => _exec(getParentCmd(commit)).toString().trim()
    let revertCommits = [..._revertCommits]
    if (_revertCommits.length) {
      _revertCommits.forEach((c) => {
        const parent = parentCommit(c)
        /** check if parent is a merge commit */
        const grandParent = parentCommit(parent).split(' ')
        const isMergeCommit = grandParent.length > 1
        if (isMergeCommit) {
          const commitList = _exec(`git log --format='%h' ${parent}^..${parent}`).toString().trim().split('\n')
          revertCommits = revertCommits.concat(commitList)
        } else {
          revertCommits.push(parent)
        }
      })
    }

    const logs = _logs.filter((log) => {
      if (revert && log) {
        const isRevert = revertCommits.some((commit) => {
          const regex = new RegExp(commit)
          return log.match(regex)
        })
        return !isRevert
      }
      return log
    })

    const payload = { version, previous }
    let ghContributions = []
    if (Boolean(GITHUB_TOKEN) && contrib) { // TODO: the look up can be time-consuming, seek ways to optimize
      const shas = logs.map(l => l.split('::')[0]) // commit filter-set
      ghContributions = await githubHandler({ tag: shas[0], action: 'contributions' }) // TODO: local commits would result in empty contributions for now
        .then(r => r.filter(({ sha }) => shas.includes(sha))) // all shas shorthanded through git rev-parse --short
      const pastContributors = new Set()
      let since = new Date().toISOString()
      for (let page = 1; page <= 5; page++) { // max 500 commits
        const nextPage = await githubHandler({ tag: previous, action: 'contributions', page })
        if (!nextPage.length) {
          break
        }
        nextPage.forEach(({ login, date }) => {
          pastContributors.add(login)
          if (date < since) {
            since = date // update furthest "at least since" datetime based on the lookback pages
          }
        })
      }
      payload.since = since // would be used to claim "fresh contributor since at least YYYY-MM-DD...""
      payload.contributors = ghContributions.reduce((acc, { login, date }) => {
        if (!acc[login]) {
          acc[login] = {
            commits: 0,
            fresh: !pastContributors.has(login),
            days: new Set(),
          }
        }
        acc[login].days.add(date.split('T')[0]) // only care about days
        acc[login].commits++
        return acc
      }, {})
    }
    payload.parsed = await parseCommits({ logs, verbose, ghContributions })

    const formatted = formatter(payload)

    if (print) {
      console.log(formatted)
    } else if (github) {
      await githubHandler({ formatted, tag: version, verbose })
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
