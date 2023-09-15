import os
import discord
from discord.ext import commands
from _bot import keep_alive

TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
intents.message_content = True

keep_alive()
#bot.setCommand("!hello", "Hello!")
#bot.setCommand("!penis", "Esto es un penis jeje :P")
#bot.setCommand("!malo", "no seas malo :P")

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  print("Bot acitvated!")


@bot.event
async def on_member_join(member):
  role = discord.utils.get(member.guild.roles, name="ExampleRol")
  await member.add_roles(role)


bot.run(TOKEN)
