const { options, baseHandler } = require('./common')
const { formatChangelog: formatter } = require('./utils')


const command = 'changelog'
const description = `Generate ${command} based on git refs`
const handler = baseHandler({ command, formatter })

module.exports = { command, description, options, handler }
