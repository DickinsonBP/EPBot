import os
import discord
from _bot import EPBot

intents = discord.Intents.default()
intents.message_content = True

bot = EPBot(intents=intents)
bot.setCommand("!hello", "Hello!")

bot.run(os.environ['TOKEN'])