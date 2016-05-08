#!/usr/bin/env python
import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# import pycrest


with open('config.json') as f:
    config = json.load(f)
print('Creating bot object ...')
bot = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])
# print('Connecting to CREST ...')
# crest = pycrest.EVE()
# print('Getting item data ...')
# item_data = crest().marketTypes()
# TODO: convert all keys to lowercase
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
        log('Command "{}" from "{}"'.format(message.content, message.author.name))
        if message.content[1:].lower() in config['DISMISS_TRIGGERS']:
            if message.author.name in config['ADMINS']:
                await bot.say('*waves*')
                # TODO: leave the server or channel
                return
    if 'bot' in message.content.lower():
        log('Bot in message: "{}" by "{}"'.format(message.content, message.author.name))


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
    await bot.send_typing(context.message.channel)
    try:
        driver = webdriver.PhantomJS()
        driver.get('https://tripwire.eve-apps.com/?system=J214811')
        driver.find_element_by_xpath('//*[@id="app_info"]/h1[2]/a').click()
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(config['TRIPWIRE']['LOGIN']['USERNAME'])
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(config['TRIPWIRE']['LOGIN']['PASSWORD'])
        driver.find_element_by_xpath('//*[@id="reg"]/form/div[3]/button').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chainMap"]/table/tbody/tr[2]')))
        soup = BeautifulSoup(driver.find_element_by_xpath('//*[@id="chainMap"]/table/tbody').get_attribute('innerHTML'), 'html.parser')
        driver.quit()
        tags = soup.find_all('td', {'class': 'node'})
        highsecs = []
        for tag in tags:
            for child in tag.findChildren('span'):
                if 'hisec' in child['class']:
                    highsecs.append(tag.findChildren('a')[0].text)
        await bot.say('Yes, the following systems are in the chain: ' + ', '.join(highsecs))
    except Exception as e:
        log('Exception occured when getting highsec systems: ' + str(e))
        await bot.say('Well, something broke, so I don\'t know.')


@bot.command(name='spais', no_pm=True, pass_context=True, aliases=['spai', 'spies', 'spy'], help='Find the spies')
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


@bot.command(name='register', no_pm=True, pass_context=True, help='link your Discord account with auth')
async def command_register(context, key: str=None):
    if not key:
        await bot.say('It\'s !register [key]')
        return
    r = requests.post(config['AUTH']['LINK_URL'].format(context.message.author.name, key),
        headers={'bot-secret': config['AUTH']['SECRET']})
    log('Registration POST returned status code {}'.format(r.status_code))
    if r.status_code == 200:
        await bot.say('Linking successful!')
    elif r.status_code == 204:
        await bot.say('You\'ve already linked your account - no need to do it again.')
    else:
        await bot.say('Didn\'t work. Are you sure you have the key correct?')


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
