const { Octokit } = require('@octokit/core')

const { exec, log } = require('./utils')


const { GITHUB_TOKEN, GITHUB_OWNER: owner = 'eqworks', GITHUB_REPO } = process.env


module.exports.githubHandler = async ({
  formatted,
  tag,
  verbose = false,
  action = 'update',
  isPre = false,
  ...rest
}) => {
  if (!GITHUB_TOKEN) {
    throw new Error('$GITHUB_TOKEN not set')
  }

  const _exec = exec({ verbose })
  const octokit = new Octokit({ auth: GITHUB_TOKEN })

  const repo = GITHUB_REPO || _exec('basename `git rev-parse --show-toplevel`').toString().trim()

  if (action === 'update') {
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

  if (action === 'tag') {
    const { data: { tag_name } } = await octokit.request('POST /repos/:owner/:repo/releases', {
      owner,
      repo,
      tag_name: tag,
      name: tag,
      prerelease: isPre,
    })
    log(`Release ${tag_name} created based on commit message`, { verbose })
  }

  if (action === 'contributions') {
    const { data } = await octokit.request('GET /repos/:owner/:repo/commits', {
      owner,
      repo,
      sha: tag,
      per_page: 100,
      ...rest,
    })
    return data
      .filter(({ author }) => author)
      .map(({ sha, author: { login } }) => ({
        sha: _exec(`git rev-parse --short ${sha}`).toString().trim(),
        login,
      }))
  }
}
