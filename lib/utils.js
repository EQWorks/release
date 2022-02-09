const fs = require('fs')
const { execSync } = require('child_process')

const { Octokit } = require('@octokit/core')
const chalk = require('chalk')
const FastText = require('fasttext.js')

const { GITHUB_TOKEN } = process.env

// TODO: it makes more sense in the ./github.js module, but it'd cause circular dependency with this module
const getGHRelease = ({ owner, repo, tag }) => {
  if (!GITHUB_TOKEN) {
    return {}
  }

  const octokit = new Octokit({ auth: GITHUB_TOKEN })

  return octokit.request('GET /repos/:owner/:repo/releases/tags/:tag', {
    owner,
    repo,
    tag,
  })
}

// model/training data from https://github.com/gesteves91/fasttext-commit-classification
// training/prediction through https://github.com/loretoparisi/fasttext.js
const model = new FastText({ loadModel: `${__dirname}/../bin/commits.bin` })

// Regex patterns
const COMMIT_MSG = /(?<cat>\S+?)(\/(?<t2>\S+))? - (?<title>.*)/
const NPM_DEP = /(@(?<pkg_name>[\w.-]*\/[\w.-]+))\s+((from){0,1}\s*(?<from_ver>v[\w.-]+|\w+-\w+)\s+)*((to){0,1}\s*(?<to_ver>v[\w.-]+|\w+-\w+))/ig

const getColors = (severity) => ({
  info: { bgColor: 'bgCyanBright', color: 'black' },
  warning: { bgColor: 'bgYellowBright', color: 'black' },
  error: { bgColor: 'bgRedBright', color: 'white' },
}[severity] || { bgColor: 'bgWhite', color: 'black' })

const log  = (msg, { verbose = false, severity = 'info' } = {}) => {
  if (verbose || severity === 'error') {
    const { bgColor, color } = getColors(severity)
    console[severity === 'error' ? severity : 'log'](chalk[bgColor][color](msg))
  }
}
module.exports = { log }

module.exports.exec = ({ verbose }) => (cmd) => {
  log(cmd, { verbose })
  return execSync(cmd)
}

const parseSubject = (s) => {
  const matches = s.match(COMMIT_MSG)
  // unmatched to generic "others" category
  if (!matches) {
    return ['others', 'others', s]
  }
  // with T2
  const { groups: { cat, t2, title } } = matches
  return [cat.toLowerCase(), t2, title]
}

module.exports.parseRaw = async (logs = []) => {
  try {
    await model.load()
    return await Promise.all(logs.map(async (s) => {
      const labels = (await model.predict(s.toLowerCase()) || []).map(({ label }) => label)
      const [t1, t2, message] = parseSubject(s)
      return { labels, t1, t2, message }
    }))
  } catch(_) {
    return []
  } finally {
    try {
      await model.unload()
    } catch(_) {
      //
    }
  }
}

module.exports.parseCommits = async ({ logs, verbose = false, ghContributions = [] }) => {
  try {
    await model.load()
    return await Promise.all(logs.map(async (line) => {
      const [h, s, b, an] = line.split('::') // hash, subject, body, author
      const labels = (await model.predict(s.toLowerCase()) || []).map(({ label }) => label)
      const [t1, t2, message] = parseSubject(s)
      // find GitHub author's login handle through ghContributions
      const { login } = ghContributions.find(({ sha }) => sha === h) || {}
      const msg = {
        s: `${message} (${h} by ${login ? `[@${login}](https://github.com/${login})` : an})\n`,
        t2,
      }
      if (b.trim()) {
        msg.b = b.trim()
      }
      // extract npm package names from commit message
      const matches = message.matchAll(NPM_DEP)
      for (const m of matches) {
        const {
          groups: {
            pkg_name,
            to_ver,
            // from_ver, // TODO: from_ver not used yet
          },
        } = m
        // TODO: check against GitHub releases of the mentioned package repo
        const [owner, repo] = pkg_name.split('/')
        try {
          const { data: { html_url, body } = {} } = await getGHRelease({ owner, repo, tag: to_ver })
          if (!html_url) {
            continue
          }
          // attach link to GitHub release
          msg.b = `${msg.b || ''}\n- [${pkg_name}@${to_ver} release](${html_url})`
          // attach to release body as indented quote block
          if ((body || '').length) {
            msg.b += `\n${body.split('\n').map(l => `> ${l}`).join('\n')}\n`
          }
        } catch (e) {
          log(`Unable to trace ${pkg_name} release info (${e.message})`, { verbose, severity: 'warning' })
        }
      }
      return { t1, labels, msg }
    }))
  } catch(e) {
    if (verbose) {
      console.error(e)
    }
    log(e, { severity: 'error' })
    return []
  } finally {
    try {
      await model.unload()
    } catch(_) {
      //
    }
  }
}

module.exports.write = (command = 'notes') => ({ formatted, version, previous, file }) => {
  const invalidFNChars = /[\\/:"*?<>|#%$&{}!+`='" ]+/g
  const f = file || `release-${command}-${previous}-${version}.md`.toLowerCase().replace(invalidFNChars, '-')
  fs.writeFile(f, formatted, (err) => {
    if (err) {
      log(`${f} ✖️:`, { severity: 'error' })
      log(err, { severity: 'error' })
    } else {
      log(`${f} ✔️`, { verbose: true })
    }
  })
}

module.exports.groupParsed = (parsed, { by = 'notes' } = {}) => {
  if (by === 'notes') {
    return parsed.reduce((acc, { t1, labels, msg }) => {
      // to organize commits without T2
      const t2 = msg['t2'] ? msg.t2 : 'others'
      delete msg.t2
      acc[t1] = {
        ...acc[t1],
        [t2]: [...(acc[t1] ? acc[t1][t2] || [] : []), { ...msg, labels }],
      }
      return acc
    }, {})
  }
  return parsed.reduce((acc, { t1, labels, msg }) => {
    const label = labels[0] || 'CHANGED'
    acc[label] = [...(acc[label] || []), { ...msg, t1 }]
    return acc
  }, {})
}
