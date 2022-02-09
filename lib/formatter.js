const { groupParsed } = require('./utils')

const contributorsReport = ({ contributors, since }) => {
  if (!Object.keys(contributors || {}).length) {
    return ''
  }
  let r = '\n\n# Contributors:\n'
  Object.entries(contributors || {}).forEach(([login, { commits, fresh, days } ]) => {
    r += `\n- [@${login}](https://github.com/${login})`
    // commit stats (count and days)
    const cs = `${commits} commit${commits > 1 ? 's' : ''} across ${days.size} day${days.size > 1 ? 's' : ''}`
    if (fresh) {
      r += ` (🎉 fresh contributor since at least ${since.split('T')[0]} - ${cs})`
    } else {
      r += ` (returning contributor - ${cs})`
    }
  })
  return r
}

module.exports.notes = (payload) => {
  const { parsed, version, previous } = payload
  const grouped = groupParsed(parsed, { by: 'notes' })
  // construct notes
  let notes = `# Release Notes (by category): from ${previous} to ${version}`
  Object.entries(grouped).forEach(([t1, t2s]) => {
    notes += `\n\n## ${t1}\n`

    Object.entries(t2s).forEach(([t2, item]) => {
      // commits without T2 skip the title
      notes += t2 === 'others' ? '\n' : `\n### ${t2}\n`

      item.forEach(({ labels, s, b }) => {
        notes += `${(labels || []).length ? `[${labels[0]}] ` : ''}`
        notes += `${s}\n`
        if (b) {
          notes += `${t2 === 'others' ? '' : '\t'}\n${b}\n` // include body
        }
      })
    })
  })
  notes += contributorsReport(payload)
  return `${notes}\n`
}

module.exports.changelog = (payload) => {
  const { parsed, version, previous } = payload
  const grouped = groupParsed(parsed, { by: 'labels' })
  // construct changelog
  let changelog = `# Changelog (by label): from ${previous} to ${version}`
  Object.entries(grouped).forEach(([label, item]) => {
    changelog += `\n\n## ${label}\n`
    item.forEach(({ t1, t2, s, b }) => {
      changelog += `\n### ${t1}${t2 ? `/${t2}` : ''} - ${s}`
      if (b) {
        changelog += `\n${b}` // include body
      }
    })
  })
  changelog += contributorsReport(payload)
  return `${changelog}\n`
}
