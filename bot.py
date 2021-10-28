import os

import discord
from discord.ext import commands
import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# client = discord.Client()
client = commands.Bot(command_prefix='!')

voice_channel_notif_enabled = False

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # return

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)
    
    # if message.content == '$toggle_vc_notif':
    #     global Toggle
    #     Toggle = not Toggle
    #     response = 'Voice chat ' + 'enabled' if Toggle else 'disabled'
    #     await message.channel.send(response)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and after.channel is not None and len(after.channel.members) == 1:
        # print(f'{member.display_name} has started a voice chat in {after.channel.name}')

        embedMessage = discord.Embed(description=f'{member.mention} `started` voice channel **{after.channel.name}**', color=0xF1C40F)
        embedMessage.set_author(name="Voice Channel Started", icon_url="https://cdn.discordapp.com/emojis/644579102472273959.png?v=1")
        embedMessage.set_footer(icon_url=member.avatar_url, text="\u200b")
        embedMessage.timestamp = datetime.datetime.utcnow()

        c: discord.TextChannel = client.get_channel(903075051761459222)
        await c.send(embed=embedMessage)

@client.command(name="toggle_vc_notif")
async def toggle_vc_notif(ctx):
    global voice_channel_notif_enabled
    voice_channel_notif_enabled = not voice_channel_notif_enabled
    response = 'Voice chat notifications are ' + 'enabled' if voice_channel_notif_enabled else 'disabled'
    await ctx.send(response)

    
client.run(TOKEN)