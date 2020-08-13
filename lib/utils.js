const fs = require('fs')


module.exports.processLog = (logs) => {
  try {
    return logs.reduce((acc, line) => {
      const [hash, subject] = line.split('::')
      const [cat, title] = subject.split('-').map(v => v.trim())
      const [t1, t2] = cat.toLowerCase().split('/')
      acc[t1] = [...(acc[t1] || []), `${t2 ? `${t2} - ` : ''}${title} (${hash})`]
      return acc
    }, {})
  } catch(e) {
    console.error(e)
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
        console.error(`Unable to save release notes to ${f}:`)
        console.error(err)
      } else {
        console.log(`Release notes saved to ${f}`)
      }
    },
  )
}
