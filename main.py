import os
import discord
from discord.ext import commands, tasks
from _bot import keep_alive
import aiohttp
#import openai
import json
from datetime import date

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
  my_loop.start()


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


def birthday_key(user):
  today = date.today()
  current_day = int(today.strftime("%d"))
  current_month = int(today.strftime("%m"))
  day = int(user["birthday"].split("/")[0])
  month = int(user["birthday"].split("/")[1])

  if current_month <= month:
    month = month - current_month
  else:
    month = 12 - (current_month - month)

  if current_day <= day:
    day = day - current_day
  else:
    day = 31 - (current_day - day)

  return month, day


@bot.command()
async def add_birthday(ctx, member, birthday):
  f = open("birthdays.json")
  data = json.load(f)
  f.close()

  member = member.replace('<', '')
  member = member.replace('>', '')
  member = member.replace('@', '')

  data.append({"userID": member, "birthday": birthday})

  with open("birthdays.json", "w") as json_file:
    json.dump(data, json_file)

  await ctx.send("Se ha guardado el cumpleaños correctamente!")


@bot.command()
async def next_birthdays(ctx):
  f = open("birthdays.json")
  data = json.load(f)
  data = sorted(data, key=birthday_key)
  mbed = discord.Embed(title='Los siguientes cumpleaños son:')

  for user in data:
    username = bot.get_user(int(user["userID"])).mention
    mbed.add_field(name="",
                   value="%s %s" % (username, user["birthday"]),
                   inline=False)

  await ctx.send(embed=mbed)


@bot.command()
async def poll(ctx, question, *options: str):
  reactions = [
      '🅰', '🅱', '©', '🍀', '🎲', '🎉', '🎊', '🔥', '💡', '💥', '🚀', '🚁', '🚂', '🚕',
      '🛸', '🛰️', '🚤', '🛳️'
  ]

  if len(options) <= 1:
    await ctx.send("```Error! A poll must have more than one option.```")
    return

  if len(options) == 2 and options[0] == "si" and options[1] == "no":
    reactions = ['👍', '👎']

  mbed = discord.Embed(title=question, color=discord.Color.red())
  for i in range(len(options)):
    mbed.add_field(name=options[i], value=reactions[i], inline=True)
  message = await ctx.send(embed=mbed)
  for i in range(len(options)):
    await message.add_reaction(reactions[i])


@tasks.loop(hours=24)
async def my_loop():
  mbed = None
  file = None
  today = date.today()
  if (today.strftime("%a") == "Thu"):
    file = discord.File('media/jdr.png', filename='jdr.png')
    mbed = discord.Embed(title='Jueves de racismo!',
                         color=discord.Color.gold())
    mbed.set_thumbnail(url="attachment://jdr.png")
    mbed.add_field(name="Hoy es jueves de racismo!",
                   value="El maldito jueves de racismo!")
    mbed.set_image(url="attachment://jdr.png")
  elif (today.strftime("%a") == "Fri"):
    file = discord.File('media/vhn.png', filename='vhn.png')
    mbed = discord.Embed(title='Viernes de humor negro!',
                         color=discord.Color.gold())
    mbed.set_thumbnail(url="attachment://vhn.png")
    mbed.add_field(name="Hoy es viernes de humor negro!",
                   value="El maldito viernes de humor negro!")
    mbed.set_image(url="attachment://vhn.png")

  channel = bot.get_channel(1152589104140259448)
  await channel.send(file=file, embed=mbed)


#TODO: look for other library. OpenAI has a free trial but then we have to pay for the API
#@bot.command()
#async def gpt(ctx, content='hola'):
#  openai.api_key = GPT
#  response = openai.Completion.create(engine="davinci-002",
#                                      prompt=content,
#                                      max_tokens=2048)
#  await ctx.send(response.choices[0].text)

bot.run(TOKEN)
