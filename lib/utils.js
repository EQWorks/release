const fs = require('fs')

const chalk = require('chalk')


const T2R = /(\S+)\/{1}(\S+) - (.*)/
const T1R = /(\S+) - (.*)/

const getColors = (severity) => ({
  info: { bgColor: 'bgCyanBright', color: 'black' },
  warning: { bgColor: 'bgYellowBright', color: 'black' },
  error: { bgColor: 'bgRedBright', color: 'white' },
}[severity] || { bgColor: 'bgWhite', color: 'black' })

const log  = (msg, { verbose, severity = 'info' }) => {
  if (verbose || severity === 'error') {
    const { bgColor, color } = getColors(severity)
    console[severity === 'error' ? severity : 'log'](chalk[bgColor][color](msg))
  }
}
module.exports = { log }

const parseSubject = (s) => {
  // TODO: find a more elegant way to capture both cases in one regex
  let matches = s.match(T2R)
  if (!matches || matches.some((v) => !v)) {
    matches = s.match(T1R)
  }
  // unmatched to generic "others" category
  if (!matches) {
    return ['others', s]
  }
  // with T2
  if (matches.length === 4) {
    const [, cat, t2, title] = matches
    return [cat, [t2, title].join(' - ')]
  }
  return matches.slice(1)
}

const parseBody = (b) => b.trim().split('\n').map(v => v.replace(/^(-|\*)\s/, '').trim()).filter(v => v)

module.exports.parseCommits = (logs) => {
  try {
    return logs.reduce((acc, line) => {
      const [h, s, b, an] = line.split('::')
      const [t1, message] = parseSubject(s)
      const msg = { s: `${message} (${h} by ${an})` }
      if (b) {
        msg.b = parseBody(b)
      }
      acc[t1] = [...(acc[t1] || []), msg]
      return acc
    }, {})
  } catch(e) {
    log(e, { severity: 'error' })
    return {}
  }
}

module.exports.formatNotes = ({ parsed, version, previous }) => {
  let notes = `## Release Notes: from ${previous} to ${version}`

  Object.entries(parsed).forEach(([t1, item]) => {
    notes += `\n\n### ${t1}\n`
    item.forEach(({ s, b = [] }) => {
      notes += `\n* ${s}`
      b.forEach((v) => {
        notes += `\n\t* ${v}`
      })
    })
  })

  return `${notes}\n`
}

module.exports.writeNotes = ({ notes, version, previous, file }) => {
  const f = file || `release-notes-${previous}-${version}.md`
  fs.writeFile(
    f,
    notes,
    (err) => {
      if (err) {
        log(`${f} ✖️:`, { severity: 'error' })
        log(err, { severity: 'error' })
      } else {
        log(`${f} ✔️`, { verbose: true })
      }
    },
  )
}
