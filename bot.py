#!/usr/bin/env python
from discord.ext import commands
import pycrest
import json


with open('config.json') as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])

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
async def on_error(event, *args, **kwargs):
    print('Error: ' + str(event))


@bot.event
async def on_message(message):
    # print('Messge from "{0.author.name}" of "{0.content}"'.format(message))
    await bot.process_commands(message)


@bot.event
async def on_member_update(before, after):
    # print('{0.name} changed their profile'.format(after))
    pass


@bot.event
async def on_typing(channel, user, when):
    # print('{1.name} is typing in channel {0.name}'.format(channel, user))
    pass


@bot.command(name='slap', description='slap a user')
async def command_slap(user):
    await bot.say('* slaps {} around a bit with a large trout*'.format(user))


@bot.command(name='lastkill')
async def command_lastkill():
    print('"lastkill" command not implemented')


@bot.command(name='lastdeath')
async def command_lastdeath():
    print('"lastdeath" command not implemented')


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
