const Discord = require('discord.js')
const config = require('./config.json')


const bot = new Discord.Client()

bot.on('ready', () => {
  console.log('Ready')
  bot.user.setGame('Auth')
})

const commands = {
  help(message) {
    message.channel.sendMessage(
      '**GETIN-Auth Discord bot**\n\n' +
      '**Available commands**:\n' +
      '- slap (`!slap [target]`) - slaps someone\n' +
      '- apps (`!apps`) - Check applications\n' +
      '- source (`!source`) - Link the bot\'s source\n' +
      '- schedule (`!schedule`) - Show the synchronization schedule\n' +
      '- sync (`!sync`) - Sync the applications now\n'
    )
  },
  slap(message, args) {
    if (args.length === 1) {
      message.channel.sendMessage(`* slaps ${args[0]} around a bit with a large trout*`)
    } else {
      message.channel.sendMessage('Command usage: `!slap [target]`')
    }
  },
  apps(message) {
    // TODO
  },
  source(message) {
    // TODO
  },
  schedule(message) {
    // TODO
  },
  sync(message) {
    // TODO
  }
}

bot.on('message', (message) => {
  try {
    if (message.author.id !== bot.user.id) {
      if (message.content.startsWith('!')) {
        let [command, ...args] = message.content.split(' ')
        command = command.substring(1)
        try {
          commands[command](message, args)
        } catch (err) {
          console.error(`Error in running command ${command} with args: ${JSON.stringify(args)}`)
        }
      }
    }
  } catch (err) {
    console.error(`Error happened in on::message: ${err}`)
  }
})

bot.login(config.TOKEN)
