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


@bot.command(name='slap', help='slap a user')
async def command_slap(user: str):
    await bot.say('* slaps {} around a bit with a large trout*'.format(user))


@bot.command(name='lastkill', pass_context=True, help='show the last Wormbro kill')
async def command_lastkill(context):
    await bot.send_typing(context.message.channel)
    try:
        js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/kills/limit/1/'.format(config['CORP']['ID']), timeout=10).json()[0]
        await bot.say('Latest {} kill: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))
    except Exception as e:
        log('Excepton with command_lastkill: ' + str(e))
        await bot.say('Something went wrong and I couldn\'t get the zkb data.')


@bot.command(name='lastdeath', pass_context=True, help='show the last Wormbro kill')
async def command_lastdeath(context):
    await bot.send_typing(context.message.channel)
    try:
        js = requests.get('https://zkillboard.com/api/kills/corporationID/{}/losses/limit/1/'.format(config['CORP']['ID']), timeout=10).json()[0]
        await bot.say('Latest {} death: https://zkillboard.com/kill/{}/'.format(config['CORP']['NAME'], js['killID']))
    except Exception as e:
        log('Excepton with command_lastdeath: ' + str(e))
        await bot.say('Something went wrong and I couldn\'t get the zkb data.')


@bot.command(name='hs', no_pm=True, pass_context=True, help='check if there\'s a highsec system in the chain')
async def command_hs(context):
    if not context.message.channel.name == 'opsec':
        await bot.say('This isn\'t the opsec channel, you spy!')
        return
    # TODO
    await bot.say('I don\'t know if there\'s a highsec system in the chain because I don\'t have eyes.')


@bot.command(name='spais', no_pm=True, pass_context=True, aliases=['spai', 'spies', 'spy'],
    help='Find the spies')
async def command_spais(context):
    online_members = list(context.message.channel.server.members)
    spy = online_members[randint(0, len(online_members) - 1)]
    if spy.name == context.message.server.me.name:
        await bot.say('I am a spy!')
    else:
        await bot.say('{0.name} is a spy!'.format(spy))


@bot.command(name='price', help='Price-check an item name in Jita')
async def command_price(item: str):
    # TODO
    log('"price" command not implemented')
    await bot.say('*shrugs*')


@bot.command(name='joined', pass_context=True, help='Print the target\'s join date')
async def command_joined(context, member: discord.Member=None):
    if not member:
        member = context.message.author
        await bot.say('You joined on {0.joined_at}'.format(member))
    elif member.name == context.message.server.me.name:
        await bot.say('I joined on {0.joined_at}'.format(member))
    else:
        await bot.say('{0.name} joined on {0.joined_at}'.format(member))


@bot.command(name='link', aliases=['links'], help='shows a link')
async def command_link(target: str=None):
    if not target:
        if config['LINKS']:
            await bot.say('Configured links: ' + ', '.join(config['LINKS'].keys()))
        else:
            await bot.say('No links configured - add links with !addlink [name] [url]')
        return
    target = target.lower()
    if target in config['LINKS']:
        await bot.say(config['LINKS'][target])
    else:
        await bot.say('I don\'t know what that is. Have you tried Google?')


@bot.command(name='addlink', aliases=['setlink'], help='add or set a link')
async def command_addlink(target: str=None, url: str=None):
    if not target or not url:
        await bot.say('It\'s !addlink [name] [url]')
        return
    url = ('http://' + url) if not url.lower().startswith('http://') and not url.lower().startswith('https://') else url
    config["LINKS"][target.lower()] = url
    log('Writing new configuration ...')
    with open('config.json', 'w') as f:
        f.write(json.dumps(config, indent=4, sort_keys=True))
    log('Done writing configuration')
    await bot.say('Link added')


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
