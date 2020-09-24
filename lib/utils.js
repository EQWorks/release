const fs = require('fs')
const { execSync } = require('child_process')

const chalk = require('chalk')
const FastText = require('fasttext.js')


// model/training data from https://github.com/gesteves91/fasttext-commit-classification
// training/prediction through https://github.com/loretoparisi/fasttext.js
const model = new FastText({ loadModel: './bin/commits.bin' })
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
    return ['others', s]
  }
  // with T2
  const { groups: { cat, t2, title } } = matches
  return [cat, t2, title]
}

const parseBody = (b) => b.trim().split('\n').map(v => v.replace(/^(-|\*)\s/, '').trim()).filter(v => v)

module.exports.parseCommits = async (logs) => {
  try {
    await model.load()
    return await Promise.all(logs.map(async (line) => {
      const [h, s, b, an] = line.split('::')
      const [{ label = 'CHANGED' } = {}] = await model.predict(s)
      const [t1, t2, message] = parseSubject(s)
      const msg = { s: `${message} (${h} by ${an})`, t2 }
      if (b) {
        msg.b = parseBody(b)
      }
      return { t1, label, msg }
    }))
  } catch(e) {
    log(e, { severity: 'error' })
    return {}
  } finally {
    try {
      await model.unload()
    } catch(_) {
      //
    }
  }
}

module.exports.formatNotes = ({ parsed, version, previous }) => {
  // group by T1
  const byT1 = parsed.reduce((acc, { t1, msg }) => {
    acc[t1] = [...(acc[t1] || []), msg]
    return acc
  }, {})
  // construct notes
  let notes = `## Release Notes: from ${previous} to ${version}`
  Object.entries(byT1).forEach(([cat, item]) => {
    const [t1] = cat.split('::')
    notes += `\n\n### ${t1}\n`
    item.forEach(({ t2, s, b = [] }) => {
      notes += `\n* ${t2 ? `${t2} - ` : ''}${s}`
      b.forEach((v) => {
        notes += `\n\t* ${v}`
      })
    })
  })
  return `${notes}\n`
}

module.exports.formatChangelog = ({ parsed, version, previous }) => {
  // group by label
  const byLabel = parsed.reduce((acc, { t1, label, msg }) => {
    acc[label] = [...(acc[label] || []), { ...msg, t1 }]
    return acc
  }, {})
  // construct changelog
  let changelog = `## Changelog: from ${previous} to ${version}`
  Object.entries(byLabel).forEach(([label, item]) => {
    changelog += `\n\n### ${label}\n`
    item.forEach(({ t1, t2, s, b = [] }) => {
      changelog += `\n* ${t1}${t2 ? `/${t2}` : ''} - ${s}`
      b.forEach((v) => {
        changelog += `\n\t* ${v}`
      })
    })
  })
  return `${changelog}\n`
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
