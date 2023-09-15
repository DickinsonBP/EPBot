import os
import discord
from discord.ext import commands
from _bot import keep_alive

TOKEN = os.environ['TOKEN']

#command dictionary
__commands = {
    "!hola":
    "Hola!!!",
    "!twitch":
    """Estos son los canales de twitch de mis amigos!
      - Alis: https://www.twitch.tv/alis_trh
    """
}

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


@bot.event
async def on_message(message):
  # we do not want the bot to reply to itself
  if message.author == bot.user:
    return

  for command, text in __commands.items():
    if (message.content == command):
      print("Channel: {0.channel} | User {0.author} : {0.content}".format(
          message))
      await message.channel.send(text)


bot.run(TOKEN)
