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
  channel = bot.get_channel(1152589104140259448)
  role = discord.utils.get(member.guild.roles, name="ExampleRol")
  await member.add_roles(role)
  await channel.send(
      "Un aplauso, ha entrado otro retrasad@ a **%s** y se llama....: **%s**" %
      (member.guild.name, member.name))


@bot.command()
async def hola(ctx):
  await ctx.send("Holaaa!!! Soy el fokin EPBot")


@bot.command()
async def twitch(ctx):
  await ctx.send("""Estos son los canales de twitch de mis amigos!
      - Alis: https://www.twitch.tv/alis_trh
    """)


@bot.command()
async def gpt(ctx, content='hola'):
  await ctx.send("Has enviado el siguiente mensaje: " + str(content))


bot.run(TOKEN)
