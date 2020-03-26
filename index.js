const fs = require('fs');
const { exec } = require('child_process')

require('dotenv').config()

const projectPath = process.env.PROJECT_PATH
const gitTarget = `git --git-dir=${projectPath}/.git`
const latestTag = process.env.LATEST
const previousTag = process.env.PREVIOUS

function execCommand(cmd, callback) {
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.log(`error ${error}`)
      callback({
        error
      })
    }
    if (stderr) {
      console.log(`stderr ${stderr}`)
      callback({
        error: stderr
      })
    }
    callback({
      output: stdout
    })
  })
}

function processLog(log) {
  try {
    const logList = log.split('\n')
    logList.pop()
    const parsedLog = { success: true, items: {} }
    for (let line in logList) {
      const lineSplit = logList[line].split(' - ')
      const feature = lineSplit[0].split(' ')[1].replace(/[^a-zA-Z ]/g, "")
      const message = lineSplit[1]
  
      if (!parsedLog.items[feature]) {
        parsedLog.items[feature] = []
      } 
      parsedLog.items[feature].push(message)
    }
    return parsedLog
  } catch (e) {
    return e
  }
}

function formatReleaseNotes(parsedLog) {
  let outputString = `## Release Notes: ${latestTag}`

  Object.keys(parsedLog).forEach(key => {
    outputString += `\n\n ### ${key}\n`
    const items = parsedLog[key]
    for (let item in items) {
      outputString += `\n * ${items[item]}`
    }
  })

  return outputString
}

function outputLog(parsedLog) {
  fs.writeFile(`release-notes-${latestTag}.md`,
  formatReleaseNotes(parsedLog),
  function (err) {
    if (err) {
      console.log('Error outputting release notes:');
      console.log(err);
    } else {
      console.log('Release notes saved!');
    }
  });
}

execCommand(`${gitTarget} fetch --prune`, tagResp => {
  try {
    console.log('Fetching tags...')
    if (!tagResp.error) {
      console.log('Tags fetched!')
      console.log('Retrieving log...')
      execCommand(`${gitTarget} log --no-merges --pretty=oneline ${latestTag}...${previousTag}`, logResp => {
        if (!logResp.error) {
          console.log('Log Retrieved!')
          console.log('Parsing log...')
          const parseResp = processLog(logResp.output)
          if (parseResp.success) {
            console.log('Log Parsed!')
            console.log('Outputting log to file...')
            outputLog(parseResp.items)
          } else {
            console.log('Error parsing log:')
            console.log(parseResp)
          }
        } else {
          console.log('Error retrieving log:')
          console.log(logResp.error.toString())
        }
      })
    } else {
      console.log('Error fetching tags:')
      console.log(tagResp.error.toString())
    }
  } catch (e) {
    console.log ('Something went horribly wrong')
    console.log(e)
  }
})
