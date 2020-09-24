const { options, baseHandler } = require('./common')
const { formatNotes: formatter } = require('./utils')


const command = 'notes'
const description = `Generate ${command} based on git refs`
const handler = baseHandler({ command, formatter })

module.exports = { command, description, options, handler }
