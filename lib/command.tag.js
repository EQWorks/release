const { execSync } = require('child_process')
const packageJson = require('./package.json')


const versionPattern = /([0-9]\d*\.[0-9]\d*\.[0-9]\d*)(-alpha||-beta)?(-[0-9]\d*)?/

const command = 'tag'
const description = `Generate ${command} based on last commit message`
const handler = async () => {
  // array of the top 3 commits in master
  const commits = execSync("git log --no-merges --format='%s' -n 3").toString().trim().split('\n')
  const versionBump = commits.find((commit) => commit.startsWith('version'))

  if (!versionBump) {
    console.error('No version bump commit available')
    process.exit(1)
  }

  const [semver] = versionBump.match(versionPattern) || []

  if (semver !== packageJson.version) {
    console.error('Intended version bump does not match package.json version field')
    process.exit(1)
  }

}

module.exports = { command, description, handler }

