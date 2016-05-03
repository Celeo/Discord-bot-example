#!/usr/bin/env python
from discord.ext import commands
import pycrest
import requests
import json


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


@bot.event
async def on_ready():
    print('Running ...')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith(config['COMMAND_PREFIX']) and not message.content.lower() in command_names:
        await bot.send_message(message.channel, 'If you were talking to me, I didn\'t catch that')
        print('Unknown command "{}"'.format(message.content))


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
    print('"hs" command not implemented')


@bot.command(name='spais')
async def command_spais():
    print('"spais" command not implemented')


@bot.command(name='price')
async def command_price(item):
    print('"price" command not implemented')


if __name__ == '__main__':
    bot.run(config['BOT_TOKEN'])
