const { Octokit } = require('@octokit/core')

const { exec, log } = require('./utils')


const { GITHUB_TOKEN, GITHUB_OWNER: owner, GITHUB_REPO } = process.env

module.exports.updateRelease = async ({ formatted, tag, verbose }) => {
  if (!GITHUB_TOKEN) {
    throw new Error('$GITHUB_TOKEN not set')
  }

  if (!owner) {
    throw new Error('$GITHUB_OWNER not set')
  }

  const _exec = exec({ verbose })
  const octokit = new Octokit({ auth: GITHUB_TOKEN })

  const repo = GITHUB_REPO || _exec('basename `git rev-parse --show-toplevel`').toString().trim()

  const { data: { name, id: release_id } } = await octokit.request('GET /repos/:owner/:repo/releases/tags/:tag', {
    owner,
    repo,
    tag,
  })
  log(`Release ${name} (ID: ${release_id}) found based on tag: ${tag}`, { verbose })

  if (release_id) {
    await octokit.request('PATCH /repos/:owner/:repo/releases/:release_id', {
      owner,
      repo,
      release_id,
      body: formatted,
    })
    log(`Release ${name} (ID: ${release_id}) updated with notes: ${formatted}`, { verbose })
  }
}
