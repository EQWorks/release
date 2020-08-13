const fs = require('fs')


module.exports.processLog = (logs) => {
  try {
    return logs.reduce((acc, line) => {
      const [hash, subject] = line.split('::')
      const [cat, title] = subject.split('-').map(v => v.trim())
      const key = cat.toLowerCase()
      acc[key] = [...(acc[key] || []), `${title} (${hash})`]
      return acc
    }, {})
  } catch(e) {
    console.error(e)
    return {}
  }
}

module.exports.formatNotes = ({ parsed, version, previous }) => {
  let notes = `## Release Notes: from ${previous} to ${version}`

  Object.keys(parsed).forEach(key => {
    notes += `\n\n### ${key}\n`
    const items = parsed[key]
    for (let item in items) {
      notes += `\n* ${items[item]}`
    }
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
