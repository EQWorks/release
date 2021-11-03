const { options, baseHandler } = require('./common')
const { notes: formatter } = require('./formatter')


const command = 'notes'
const description = `Generate ${command} based on git refs`
const handler = baseHandler({ command, formatter })

module.exports = { command, description, options, handler }
