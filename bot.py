#!/usr/bin/env python
import discord
from discord.ext import commands
# import pycrest
import requests
import json
from datetime import datetime
from random import randint


with open('config.json') as f:
    config = json.load(f)
print('Creating bot object ...')
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])
# print('Connecting to CREST ...')
# crest = pycrest.EVE()
# print('Getting item data ...')
# item_data = crest().marketTypes()
print('Setup complete')


def log(message):
    message = '[{}] {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)
    print(message)
    with open(config['LOG_FILENAME'], 'a') as f:
        f.write(message + '\n')


@bot.event
async def on_ready():
    log('Running ...')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith(config['COMMAND_PREFIX']):
        log('Command "{}"'.format(message.content))
    if 'bot' in message.content.lower():
        log('Bot in message: "{}"'.format(message.content))


@bot.command(name='slap', no_pm=True, description='slap a user', help='slap a user')
async def command_slap(user):
    await bot.say('* slaps {} around a bit with a large trout*'.format(user))


@bot.command(name='lastkill', no_pm=True, description='show the last Wormbro kill', help='show the last Wormbro kill')
async def command_lastkill():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/kills/limit/1/'.format(config['CORP']['ID'])).json()[0]
    await bot.say('Latest {} kill: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='lastdeath', no_pm=True, description='show the last Wormbro kill', help='show the last Wormbro kill')
async def command_lastdeath():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/losses/limit/1/'.format(config['CORP']['ID'])).json()[0]
    await bot.say('Latest {} death: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='hs', no_pm=True, pass_context=True, description='check if there\'s a highsec system in the chain',
    help='check if there\'s a highsec system in the chain')
async def command_hs(context):
    if not context.message.channel.name == 'opsec':
        await bot.say('This isn\'t the opsec channel, you spy!')
        return
    # TODO
    await bot.say('I don\'t know if there\'s a highsec system in the chain because I don\'t have eyes.')


@bot.command(name='spais', no_pm=True, pass_context=True, description='Find the spies', aliases=['spai', 'spies', 'spy'],
    help='Find the spies')
async def command_spais(context):
    online_members = list(context.message.channel.server.members)
    spy = online_members[randint(0, len(online_members) - 1)]
    if spy.name == context.message.server.me.name:
        await bot.say('I am a spy!')
    else:
        await bot.say('{0.name} is a spy!'.format(spy))


@bot.command(name='price', no_pm=True, description='price-check an item name in Jita', help='Price-check an item name in Jita')
async def command_price(item):
    # TODO
    log('"price" command not implemented')
    await bot.say('*shrugs*')


@bot.command(name='joined', no_pm=True, pass_context=True, description='print the target\'s join date', help='Print the target\'s join date')
async def command_joined(context, member: discord.Member=None):
    if not member:
        member = context.message.author
        await bot.say('You joined on {0.joined_at}'.format(member))
    elif member.name == context.message.server.me.name:
        await bot.say('I joined on {0.joined_at}'.format(member))
    else:
        await bot.say('{0.name} joined on {0.joined_at}'.format(member))


if __name__ == '__main__':
    try:
        log('Starting run loop ...')
        bot.loop.run_until_complete(bot.start(config['BOT_TOKEN']))
    except KeyboardInterrupt:
        log('Logging out ...')
        bot.loop.run_until_complete(bot.logout())
        log('Logged out')
    finally:
        log('Closing ...')
        bot.loop.close()
        log('Done')
