#!/usr/bin/python

import discord
import asyncio
import configparser
import dpmaster
import oaforum
import stats
import datetime
import argparse

SLEEP_TIME = 60

# initialization
try:
    neko = discord.Client()

    config = configparser.ConfigParser()
    config.read('neko.ini')
    #  config.read('neko_test.ini')
    token = config['Credentials']['token']
    ch_svlist = config['Channels']['servers']
    ch_general = config['Channels']['general']
    ch_notifications = config['Channels']['notifications']
except Exception as ex:
    print(ex)

stats.Load()

async def sv_update():
    try:
        await neko.wait_until_ready()
        channel = neko.get_channel(ch_svlist)

        # clear previous neko messages on the servers channel
        try:
            await neko.purge_from(channel, limit=100, check=lambda m: m.author == neko.user)
        except Exception as exm:
            print(exm)

        message = None
        s_message = None
        while not neko.is_closed:
            try:
                # neko is typing :)
                neko.send_typing(channel)
                text = dpmaster.sv_list(track_players=True)
                stats.Save()
                if not text: text = '-'
                if not message:
                    message = await neko.send_message(channel, text)
                else:
                    await neko.edit_message(message, text)
                await asyncio.sleep(SLEEP_TIME)
            except discord.errors.NotFound:
                print('Servers message deleted. Creating new one.')
                message = None
            try:
                text = stats.QueryTimerange(datetime.timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
                if not text or len(text) <= 0: text = '-'
                else: text = '\n\n' + text
                if not s_message:
                    s_message = await neko.send_message(channel, text)
                else:
                    await neko.edit_message(s_message, text)
            except discord.errors.NotFound:
                print('Stats message deleted. Creating new one.')
                s_message = None
            except Exception as e:
                print(e)
    except Exception as ex:
        print(ex)

async def forum_feed():
    try:
        await neko.wait_until_ready()
        channel = neko.get_channel(ch_notifications)
        while not neko.is_closed:
            try:
                for text in oaforum.feed():
                    await neko.send_message(channel, text)
                await asyncio.sleep(300)
            except Exception as e:
                print(e)
                print('Exception while getting forum feed')
    except Exception as ex:
        print(ex)

@neko.event
async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    channel = neko.get_channel(ch_general)
    text = 'Welcome to the ' + channel.server.name + ' server, ' \
           + member.mention + '!'
    try:
        await neko.send_message(channel, text)
    except:
        print('Error while sending welcome message.')

@neko.event
async def on_message(message):
    try:
        # proceed only if the message was received on a private channel
        if message.channel.is_private:
            # ask players timestamps
            if message.content.startswith('.when '):
                #TODO: discord user timezone issue, timestamps for now are stored as UTC datetimes
                answer = stats.QueryTimestamps(message.content[6:])
                if len(answer) <= 0:
                    answer = 'No matches found for *{}*\n'.format(message.content[6:])
            # ask number of players in timerange
            elif message.content.startswith('.last '):
                m = 0
                h = 0
                if len(message.content[6:]) > 0:
                    h = int(message.content[6:])
                else:
                    m = 1
                answer = stats.QueryTimerange(datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=m, hours=h, weeks=0))
                if len(answer) <= 0:
                    return
            # ask server name
            elif message.content.startswith('.sv '):
                answer = stats.QueryServers(message.content[4:])
                if len(answer) <= 0:
                    answer = 'No matches found for *{}*\n'.format(message.content[4:])
            #unsupported command
            else:
                return
            await neko.send_message(message.channel, answer)
    except Exception as ex:
        print(ex)

@neko.event
async def on_resume():
    print('Resuming...')

@neko.event
async def on_error():
    print('Error occured.')

# create tasks and run main loop
try:
    neko.loop.create_task(sv_update())
    #neko.loop.create_task(forum_feed())
    neko.run(token)
except Exception as ex:
    print(ex)
