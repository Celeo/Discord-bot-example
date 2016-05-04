#!/usr/bin/env python
from discord.ext import commands
# import pycrest
import requests
import json
from datetime import datetime


with open('config.json') as f:
    config = json.load(f)
print('Creating bot object ...')
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])
# print('Connecting to CREST ...')
# crest = pycrest.EVE()
# print('Getting item data ...')
# item_data = crest().marketTypes()
command_names = ('slap', 'lastkill', 'lastdeath', 'hs', 'spais', 'spies', 'spy', 'price', 'joined')
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
    if message.content.startswith(config['COMMAND_PREFIX']) and not message.content.lower()[1:].split(' ')[0] in command_names:
        await bot.send_message(message.channel, 'If you were talking to me, I didn\'t catch that')
        log('Unknown command "{}"'.format(message.content))
    if 'bot' in message.content.lower():
        log('Bot in message: "{}"'.format(message.content))


@bot.command(name='slap', description='slap a user')
async def command_slap(user):
    await bot.say('* slaps {} around a bit with a large trout*'.format(user))


@bot.command(name='lastkill')
async def command_lastkill():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/kills/limit/1/'.format(config['CORP']['ID'])).json()[0]
    await bot.say('Latest {} kill: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='lastdeath')
async def command_lastdeath():
    js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/losses/limit/1/'.format(config['CORP']['ID'])).json()[0]
    await bot.say('Latest {} death: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))


@bot.command(name='hs')
async def command_hs():
    # TODO
    log('"hs" command not implemented')
    await bot.say('I don\'t know if there\'s a highsec system in the chain yet.')


@bot.command(name='spais', aliases=['spies', 'spy'], pass_context=True)
async def command_spais():
    await bot.say('You\'re a spy, {0.author.name}!'.format(member))


@bot.command(name='price')
async def command_price(item):
    # TODO
    log('"price" command not implemented')
    await bot.say('*shrugs*')


@bot.command(name='joined')
async def command_joined(member):
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


if __name__ == '__main__':
    try:
        log('Running ...')
        bot.loop.run_until_complete(bot.start(config['BOT_TOKEN']))
    except KeyboardInterrupt:
        log('Logging out ...')
        bot.loop.run_until_complete(bot.logout())
        log('Logged out')
    finally:
        log('Closing ...')
        bot.loop.close()
        log('Done')
