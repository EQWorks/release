const { tagOptions: options, tagHandler } = require('./tag-handler')


const command = 'tag'
const description = `Generate ${command} based on last commit message`
const handler = tagHandler(command)

module.exports = { command, description, options, handler }

