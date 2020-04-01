const fs = require('fs')


module.exports.processLog = (logs) => {
  const parsed = {}
  try {
    for (let line in logs) {
      const lineSplit = logs[line].split(' - ')
      const feature = lineSplit[0].split(' ')[1].replace(/[^a-zA-Z ]/g, "")
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

const formatNotes = ({ parsed, version }) => {
  let notes = `## Release Notes: ${version}`

  Object.keys(parsed).forEach(key => {
    notes += `\n\n### ${key}\n`
    const items = parsed[key]
    for (let item in items) {
      notes += `\n* ${items[item]}`
    }
  })

  return `${notes}\n`
}
module.exports.formatNotes = formatNotes

module.exports.writeNotes = ({ notes, version, file }) => {
  fs.writeFile(
    file || `release-notes-${version}.md`,
    notes,
    function (err) {
      if (err) {
        console.log('Error outputting release notes:')
        console.log(err)
      } else {
        console.log('Release notes saved!')
      }
    },
  )
}
