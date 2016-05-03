from discord.ext import commands
import json


with open('config.json') as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])


@bot.event
async def on_ready():
    print('Running ...')


if __name__ == '__main__':
    bot.run(config['BOT_TOKEN'])
