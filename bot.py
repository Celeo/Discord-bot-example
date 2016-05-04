#!/usr/bin/env python
from discord.ext import commands
import pycrest
import requests
import json
from datetime import datetime


with open('config.json') as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])
crest = pycrest.EVE()
item_data = crest().marketTypes()
command_names = ('slap', 'lastkill', 'lastdeath', 'hs', 'spais', 'price')

# Commands:
#   - slap [user] - slap a user
#   - lastkill - links to the most recent corp kill
#   - lastdeath - links to the most recent corp dath
#   - hs - prints if there's a HS in the chain
#   - spais - prints the names of the people in chat who aren't in the corp
#   - price [name] - prints the Jita price for the item by name


def log(message):
    with open(config['LOG_FILENAME'], 'a') as f:
        f.write('[{}] {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))


@bot.event
async def on_ready():
    log('Running ...')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith(config['COMMAND_PREFIX']) and not message.content.lower() in command_names:
        await bot.send_message(message.channel, 'If you were talking to me, I didn\'t catch that')
        log('Unknown command "{}"'.format(message.content))
    if 'bot' in message.content.lower():
        log('Bot in message: "{}"'.format(message.content))


@bot.command(name='slap', description='slap a user')
async def command_slap(user):
    await bot.say('* slaps {} around a bit with a large trout*'.format(user))


@bot.command(name='lastkill')
async def command_lastkill():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/kills/limit/1/'.format(config['CORP']['ID'])).json()
    await bot.say('Latest {} kill: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='lastdeath')
async def command_lastdeath():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/losses/limit/1/'.format(config['CORP']['ID'])).json()
    await bot.say('Latest {} death: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='hs')
async def command_hs():
    log('"hs" command not implemented')


@bot.command(name='spais')
async def command_spais():
    log('"spais" command not implemented')


@bot.command(name='price')
async def command_price(item):
    log('"price" command not implemented')


if __name__ == '__main__':
    bot.run(config['BOT_TOKEN'])
