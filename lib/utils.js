const fs = require('fs')

const chalk = require('chalk')


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

module.exports.parseCommits = (logs) => {
  try {
    return logs.reduce((acc, line) => {
      const [hash, subject] = line.split('::')
      const [cat, title] = subject.split('-').map(v => v.trim())
      const [t1, t2] = cat.toLowerCase().split('/')
      acc[t1] = [...(acc[t1] || []), `${t2 ? `${t2} - ` : ''}${title} (${hash})`]
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
    item.forEach((msg) => {
      notes += `\n* ${msg}`
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
