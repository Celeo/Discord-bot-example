#!/usr/bin/env python
import discord
from discord.ext import commands
import json


with open('config.json') as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])


@bot.event
async def on_ready():
    print('Running ...')


@bot.event
async def on_error(event, *args, **kwargs):
    print('Error: ' + str(event))


@bot.event
async def on_message(message):
    print('Messge from "{0.author.name}" of "{0.content}"'.format(message))
    await bot.process_commands(message)


@bot.event
async def on_member_update(before, after):
    print('{0.name} changed their profile'.format(after))


@bot.event
async def on_typing(channel, user, when):
    print('{1.name} is typing in channel {0.name}'.format(channel, user))


@bot.command(name='slap', description='slap a user')
async def slap(user):
    print('slap command')
    await bot.say('* slaps {} *'.format(user))


if __name__ == '__main__':
    bot.run(config['BOT_TOKEN'])
