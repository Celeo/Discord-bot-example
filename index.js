const Discord = require('discord.js')
const config = require('./config.json')


const bot = new Discord.Client()

bot.on('ready', () => {
  console.log('Ready!')
})

bot.on('message', (message) => {
  if (message.author.id !== bot.user.id) {
    if (message.content.startsWith('!')) {
      // TODO
    }
  }
})

bot.login(config.TOKEN)
