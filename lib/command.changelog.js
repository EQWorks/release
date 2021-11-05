const { options, baseHandler } = require('./common')
const { changelog: formatter } = require('./formatter')


const command = 'changelog'
const description = `Generate ${command} based on git refs`
const handler = baseHandler({ command, formatter })

module.exports = { command, description, options, handler }
