module.exports.formatNotes = ({ parsed, version, previous }) => {
  // group by T1 & T2, enrich msg with label
  const byT1 = parsed.reduce((acc, { t1, labels, msg }) => {
    // to organize commits without T2
    const t2 = msg['t2'] ? msg.t2 : 'others'
    delete msg.t2
    acc[t1] = {
      ...acc[t1],
      [t2]: [...(acc[t1] ? acc[t1][t2] || [] : []), { ...msg, labels }],
    }
    return acc
  }, {})

  // construct notes
  let notes = `## Release Notes: from ${previous} to ${version}`

  Object.entries(byT1).forEach(([t1, grouped]) => {
    notes += `\n\n### ${t1}\n`

    Object.entries(grouped).forEach(([t2, item]) => {
      // commits without T2 skip the title
      notes += t2 === 'others' ? '\n' : `\n* #### ${t2}\n\t`

      item.forEach(({ labels, s, b = [] }) => {
        notes += `* ${(labels || []).length ? `[${labels[0]}] ` : ''}`
        notes += `${s}\n`
        b.forEach((v) => {
          notes += `${t2 === 'others' ? '' : '\t'}\t* ${v}\n`
        })
      })
    })
  })
  return `${notes}\n`
}

module.exports.formatChangelog = ({ parsed, version, previous }) => {
  // group by first label (most scored)
  const byLabel = parsed.reduce((acc, { t1, labels, msg }) => {
    const label = labels[0] || 'CHANGED'
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
