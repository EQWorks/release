const { log, exec } = require('./utils')
const { githubHandler } = require('./github')
const fs = require('fs')


module.exports.tagOptions = (yargs) => yargs
  .option('github', {
    type: 'boolean',
    alias: 'gh',
    description: 'Flag to create a tag from commit version and execute a GitHub release',
    default: false,
  }).option('number', {
    type: 'number',
    alias: 'n',
    description: 'Limit the number of commits to read tag from',
    default: 3,
  }).option('verbose', {
    type: 'boolean',
    alias: 'v',
    describe: 'Show verbose output',
    default: false,
  })

const versionPattern = /([0-9]\d*\.[0-9]\d*\.[0-9]\d*)([-]\w+)?([.]\d+)?/

module.exports.tagHandler = (command) => async ({ github, verbose, number }) => {
  const _exec = exec({ verbose })
  try {
    const { version } = JSON.parse(fs.readFileSync('package.json', 'utf8'))
    // default to the top 3 commits in master
    const commits = _exec(`git log --no-merges --format='%s' -n ${number}`).toString().trim().split('\n')
    const [versionBump] = commits.map((commit) => commit.match(versionPattern)).filter((c) => c)

    if (!versionBump) {
      console.error('No version bump commit available')
      process.exit(0)
    }

    const [tagVersion, , preRelease] = versionBump

    if (tagVersion !== version) {
      console.error('Intended version bump does not match package.json version field')
      process.exit(1)
    }
    if (github) {
      await githubHandler({ tag: `v${tagVersion}`, action: command, isPre: Boolean(preRelease) })
    } else {
      _exec('git fetch --prune')
      _exec(`git tag v${tagVersion} -a -m "v${tagVersion}"`)
    }
  } catch (err) {
    if (verbose) {
      console.error(err)
    }
    log(err, { severity: 'error' })
  }
}
