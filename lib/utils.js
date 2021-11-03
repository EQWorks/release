const fs = require('fs')
const { execSync } = require('child_process')

const chalk = require('chalk')
const FastText = require('fasttext.js')


// model/training data from https://github.com/gesteves91/fasttext-commit-classification
// training/prediction through https://github.com/loretoparisi/fasttext.js
const model = new FastText({ loadModel: `${__dirname}/../bin/commits.bin` })
const R = /(?<cat>\S+?)(\/(?<t2>\S+))? - (?<title>.*)/

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
  const matches = s.match(R)
  // unmatched to generic "others" category
  if (!matches) {
    return ['others', 'others', s]
  }
  // with T2
  const { groups: { cat, t2, title } } = matches
  return [cat.toLowerCase(), t2, title]
}

const parseBody = (b) => b.trim().split('\n').map(v => v.replace(/^(-|\*)\s/, '').trim()).filter(v => v)

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

module.exports.parseCommits = async ({ logs, verbose = false }) => {
  try {
    await model.load()
    return await Promise.all(logs.map(async (line) => {
      const [h, s, b, an] = line.split('::')
      const labels = (await model.predict(s.toLowerCase()) || []).map(({ label }) => label)
      const [t1, t2, message] = parseSubject(s)
      const msg = { s: `${message} (${h} by ${an})`, t2 }
      if (b) {
        msg.b = parseBody(b)
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
