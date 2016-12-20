Neko
====

Neko is a Discord bot for OpenArena server. Currently it only displays
OpenArena server list and players, and performs some usual functions found in
other Discord bots.

You can find info about the OpenArena game at http://www.openarena.ws. To join
the Discord server you can use this invite link: https://discord.me/openarena.

Bot Commands
------------

Neko accepts the following commands in private chat:
- .when &lt;text&gt; -- shows last time players have appeared containing &lt;text&gt; in their name
- .last &lt;numhours&gt; -- shows the total number of players that have appeared in the last &lt;numhours&gt; hours
- .sv &lt;text&gt; -- shows online servers containing &lt;text&gt; in their name

Running
-------

Use the `run.sh` script.

Requirements
------------

- python 3.5
- discord.py -- https://github.com/Rapptz/discord.py
- lxml -- http://lxml.de

Testing
-------

To test this bot on your own Discord server:

- go to https://discordapp.com/developers/applications/me and
  choose `New Applicatons`
- name the bot, choose `Create Application`
- choose `Create a Bot User`
- uncheck the `Public Bot` (recommended)
- under `APP BOT USER` click on the reveal token. Use this token with neko.ini
  file.
- Create a discord server and invite the bot with this link (replace
  Client_ID with your bot Client ID):
  https://discordapp.com/oauth2/authorize?client_id=Client_ID&scope=bot&permissions=0
- copy channel ID's to neko.ini (they can be found on web app by choosing
  a channel on your Discord server and looking at the link
  https://discordapp.com/channels/<server_id>/<channel_id>)
- run the app
