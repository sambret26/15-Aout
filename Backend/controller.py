# -*- coding: utf-8 -*-

# Global packages
import sys
sys.path.append("modules")

from discord.ext import commands
import discord
import asyncio

# My packages
from databases.base import Base, engine
import messages
import service
import config

Base.metadata.create_all(engine)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Commandes
@bot.command()
async def mail(ctx):
    await service.mail(ctx)
    
@bot.command()
async def init(ctx):
    await service.init(ctx)
    
@bot.command()
async def test(ctx):
    await service.test(ctx)
    
@bot.command()
async def clear(ctx, nombre: int = 100):
    await service.clear(ctx, nombre)

@bot.event
async def on_message(message):
    if message.attachments:
        await service.importFile(bot, message)
    if message.author == bot.user : return
    await bot.process_commands(message)
        
async def start_bot():
    if config.DEBUG:
        print(messages.DEBUG_START)
    else:
        print(messages.CLASSIC_START) 
    await bot.start(config.DISCORD_TOKEN)

loop = asyncio.get_event_loop()
if loop.is_running():
    task = loop.create_task(start_bot())
else:
    loop.run_until_complete(start_bot())
        
        