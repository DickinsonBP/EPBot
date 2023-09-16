import os
import discord
from discord.ext import commands
from _bot import keep_alive
import aiohttp
import openai

TOKEN = os.environ['TOKEN']
UNSPLASH = os.environ['UNSPLASH']
GPT = os.environ['GPT']

intents = discord.Intents.all()
intents.message_content = True

keep_alive()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  print("Bot acitvated!")


@bot.event
async def on_member_join(member):
  channel = bot.get_channel(1152589104140259448)  #get the cannel id
  role = discord.utils.get(member.guild.roles, name="ExampleRol")
  await member.add_roles(role)
  await channel.send(
      "Un aplauso, ha entrado otro retrasad@ a **%s** y se llama....: **%s**" %
      (member.guild.name, member.name))


@bot.command()
async def members_channel(ctx):
  guild = ctx.guild
  total_members = len(guild.members) - 1
  overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      guild.me: discord.PermissionOverwrite(read_messages=True)
  }
  await guild.create_voice_channel('Total miembros %s' % total_members,
                                   overwrites=overwrites)


@bot.command()
async def hola(ctx):
  await ctx.send("""
  Holaaa!!! Soy el fokin EPBot
  Puedes usar los siguientes comandos:
    **!hola**: sirve para mostrar este mismo comando :P
    **!twitch**: muestra los canales de twitch de nuestros streamers :P
    **!gpt**: sirve para preguntarle cositas a chatgpt :P (desarrollo)
    """)


@bot.command()
async def ayuda(ctx):
  await ctx.send("""
    Puedes usar los siguientes comandos:
    **!hola**: sirve para mostrar este mismo comando :P
    **!twitch**: muestra los canales de twitch de nuestros streamers :P
    **!gpt**: sirve para preguntarle cositas a chatgpt :P (desarrollo)
    """)


@bot.command()
async def twitch(ctx):
  await ctx.send("""Estos son los canales de twitch de mis amigos!
      - Alis: https://www.twitch.tv/alis_trh
    """)


@bot.command()
async def image(ctx, *, search):
  search = search.replace(' ', '')
  url = f'https://api.unsplash.com/photos/random/?query={search}&orientation=squarish&content_filter=high&client_id={UNSPLASH}'
  async with aiohttp.ClientSession() as session:
    request = await session.get(url)
    json_data = await request.json()
  mbed = discord.Embed(title='Aqui esta tu imágen de **%s**!' % search)
  mbed.set_image(url=json_data['urls']['regular'])
  await ctx.send(embed=mbed)

#TODO: look for other library. OpenAI has a free trial but then we have to pay for the API
#@bot.command()
#async def gpt(ctx, content='hola'):
#  openai.api_key = GPT
#  response = openai.Completion.create(engine="davinci-002",
#                                      prompt=content,
#                                      max_tokens=2048)
#  await ctx.send(response.choices[0].text)


bot.run(TOKEN)
