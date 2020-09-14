const fs = require('fs')

const chalk = require('chalk')


const R = /(?<cat>\S+?)(\/(?<t2>\S+))? - (?<title>.*)/

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
  const matches = s.match(R)
  // unmatched to generic "others" category
  if (!matches) {
    return ['others', s]
  }
  // with T2
  const { groups: { cat, t2, title } } = matches
  if (t2) {
    return [cat, [t2, title].join(' - ')]
  }
  return [cat, title]
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
  const invalidFNChars = /[\\/:"*?<>|#%$&{}!+`='" ]+/g
  const f = file || `release-notes-${previous}-${version}.md`.toLowerCase().replace(invalidFNChars, '-')
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
