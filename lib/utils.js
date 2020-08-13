const fs = require('fs')


module.exports.processLog = (logs) => {
  const parsed = {}
  try {
    for (let line in logs) {
      const lineSplit = logs[line].split(' - ')
      const feature = lineSplit[0].split(' ')[1]
      const message = lineSplit[1]

      if (!parsed[feature]) {
        parsed[feature] = []
      }
      parsed[feature].push(message)
    }
  } catch (e) {
    console.error(e)
  }
  return parsed
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
