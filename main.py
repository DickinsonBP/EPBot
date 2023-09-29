import os
import discord
from discord.ext import commands, tasks
from _bot import keep_alive
import aiohttp
#import openai
import json
from datetime import date, datetime
import random

TOKEN = os.environ['TOKEN']
UNSPLASH = os.environ['UNSPLASH']
GPT = os.environ['GPT']

birthday_photos = [
    "media/piolin_cumple.jpeg", "media/piolin_cumple2.jpeg",
    "media/piolin_cumple3.jpeg", "media/piolin_cumple4.jpeg",
    "media/piolin_cumple5.jpeg"
]

#channels id
welcome = 1019315282138894416
chateo = 779103315933528075
bot_always = 1155897749099786330
valo_gaming = 1018984617451212850

intents = discord.Intents.all()
intents.message_content = True

keep_alive()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  print("Bot acitvated!")
  meme_day.start()
  check_birthdays.start()
  do_something.start()


@bot.event
async def on_member_join(member):
  channel = bot.get_channel(welcome)  #get the cannel id
  role = discord.utils.get(member.guild.roles, name="👽NPC's👽")
  await member.add_roles(role)
  await channel.send(
      "Un aplauso, ha entrado otro retrasad@ a **%s** y se llama....: **%s**" %
      (member.guild.name, member.name))


@bot.event
async def on_member_remove(member):
  channel = bot.get_channel(welcome)  #get the cannel id
  await channel.send("Chao **%s** mariquita" % (member.name))


@bot.command()
async def members_channel(ctx):
  guild = ctx.guild
  total_members = len(guild.members) - 1
  overwrites = {
      guild.default_role:
      discord.PermissionOverwrite(view_channel=True, connect=False),
      guild.me:
      discord.PermissionOverwrite(view_channel=True)
  }
  await guild.create_voice_channel(name=f'Total miembros {total_members}',
                                   overwrites=overwrites)


@bot.command()
async def hola(ctx):
  dbp = bot.get_user(621672016445046784).mention
  amb = bot.get_user(490287529833005075).mention
  mvc = bot.get_user(551191398229999629).mention
  await ctx.send(
      """Holaaa!!! Soy el fokin EPBot y he sido creado para teneros aqui a ralla. Mis creadores han sido nada mas y nada menos que **%s, %s y %s**, así que hay que respetarlos sinó os cae shit. Para saber que comandos se pueden usar ejecuta **!ayuda**"""
      % (dbp, amb, mvc))


@bot.command()
async def ayuda(ctx):
  author = ctx.message.author.mention
  mbed = discord.Embed(
      title='Guia de ayuda!',
      description=f"{author} aqui puedes ver los comandos que puedes usar!")

  mbed.add_field(name="**!ayuda**",
                 value="Sirve para mostrar esta guia de ayuda",
                 inline=False)
  mbed.add_field(
      name="**!valorant**",
      value="Envia un mensaje por DM a EP para jugar al fokin valorant",
      inline=False)
  mbed.add_field(
      name="**!gaming**",
      value=
      "Envia un mensaje por DM a EP para jugar al juego que se diga. Ej: !gaming gta",
      inline=False)
  mbed.add_field(name="**!hola**",
                 value="Sirve para mostrar el saludo del fokin bot",
                 inline=False)
  mbed.add_field(
      name="**!twitch**",
      value="Muestra los canales de twitch de nuestros streamers :P",
      inline=False)
  mbed.add_field(name="**!image**",
                 value="Busca una foto pasada por parámetro. Ej: !image cat",
                 inline=False)
  mbed.add_field(name="**!poll**",
                 value="Genera una encuesta. Ej: !poll 'Encuesta' si no",
                 inline=False)
  mbed.add_field(
      name="**!add_birthday**",
      value=
      "Añade el cumpleaños de un miembro. Ej: !add_birthday @user fecha_nacimiento (mm/dd/YYYY)",
      inline=False)
  mbed.add_field(name="**!next_birthdays**",
                 value="Muestra los cumpleaños que vienen",
                 inline=False)
  mbed.add_field(name="**!talk**",
                 value="(en desarrollo) hablar con un chatbot",
                 inline=False)
  mbed.add_field(name="**!musica**",
                 value="(en desarrollo) buscar y escuchar musica",
                 inline=False)

  await ctx.send(embed=mbed)


@bot.command()
async def twitch(ctx):
  await ctx.send("""Estos son los canales de twitch de mis amigos!
      - Alis: https://www.twitch.tv/alis_trh
      - Julio: https://www.twitch.tv/jeidad_
    """)


@bot.command()
async def image(ctx, *, search):
  search_formtted = search.replace(' ', '_')
  url = f'https://api.unsplash.com/photos/random/?query={search_formtted}&orientation=squarish&content_filter=high&client_id={UNSPLASH}'
  try:
    async with aiohttp.ClientSession() as session:
      request = await session.get(url)
      json_data = await request.json()
    mbed = discord.Embed(title='Aqui esta tu imágen de **%s**!' % search)
    mbed.set_image(url=json_data['urls']['regular'])
    await ctx.send(embed=mbed)
  except Exception as e:
    await ctx.send("Error! No se ha podido encontrar la imagen **%s**" % search
                   )


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
  today = datetime.today()
  for user in data:
    year = 0
    username = bot.get_user(int(user["userID"])).mention

    birthday1 = datetime.strptime(user["birthday"], "%d/%m/%Y")
    if (birthday1.month >= today.month):
      year = today.year
      birthday = "%s/%s/%s" % (birthday1.day, birthday1.month, today.year)
    else:
      year = today.year + 1
      birthday = "%s/%s/%s" % (birthday1.day, birthday1.month, today.year + 1)

    birthday = datetime.strptime(birthday, "%d/%m/%Y")

    mbed.add_field(name="",
                   value="%s Quedan %s días y **cumple %s añacos LOL**" %
                   (username, (birthday - today).days, year - birthday1.year),
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


def check_today_file(day):
  with open("meme_day.txt", "r") as f:
    for line in f:
      pass
    #get last line
    last_line = line

  return day.strftime("%d/%m/%Y") == last_line


def save_today_file(day):
  with open("meme_day.txt", 'a') as file:
    file.write(day.strftime("%d/%m/%Y") + '\n')


@tasks.loop(hours=24)
async def meme_day():
  global jueves
  global viernes
  print("Checking meme of the day")
  channel = bot.get_channel(chateo)
  today = date.today()
  if (not check_today_file(today)):
    if (today.strftime("%a") == "Mon"):
      file = discord.File('media/ldg.jpg', filename='ldg.jpg')
      mbed = discord.Embed(title='Lunes de gatos!', color=discord.Color.gold())
      mbed.set_thumbnail(url="attachment://ldg.jpg")
      mbed.add_field(name="Hoy es lunes de gatos!",
                     value="El maldito lunes de gatos!")
      mbed.set_image(url="attachment://ldg.jpg")
      await channel.send(file=file, embed=mbed)
    if (today.strftime("%a") == "Tue"):
      file = discord.File('media/mdc.jpg', filename='mdc.jpg')
      mbed = discord.Embed(title='Martes de cumbia!',
                           color=discord.Color.gold())
      mbed.set_thumbnail(url="attachment://mdc.jpg")
      mbed.add_field(name="Hoy es martes de cumbia!",
                     value="El maldito martes de cumbia!")
      mbed.set_image(url="attachment://mdc.jpg")
      await channel.send(file=file, embed=mbed)
    if (today.strftime("%a") == "Thu"):
      file = discord.File('media/jdr.png', filename='jdr.png')
      mbed = discord.Embed(title='Jueves de racismo!',
                           color=discord.Color.gold())
      mbed.set_thumbnail(url="attachment://jdr.png")
      mbed.add_field(name="Hoy es jueves de racismo!",
                     value="El maldito jueves de racismo!")
      mbed.set_image(url="attachment://jdr.png")
      await channel.send(file=file, embed=mbed)
    if (today.strftime("%a") == "Fri"):
      file = discord.File('media/vhn.png', filename='vhn.png')
      mbed = discord.Embed(title='Viernes de humor negro!',
                           color=discord.Color.gold())
      mbed.set_thumbnail(url="attachment://vhn.png")
      mbed.add_field(name="Hoy es viernes de humor negro!",
                     value="El maldito viernes de humor negro!")
      mbed.set_image(url="attachment://vhn.png")
      await channel.send(file=file, embed=mbed)
    else:
      pass

    save_today_file(today)


@tasks.loop(hours=24)
async def check_birthdays():
  print("Checking birthday")
  channel = bot.get_channel(chateo)
  today = date.today()
  f = open("birthdays.json")
  data = json.load(f)
  for user in data:
    birthday = datetime.strptime(user["birthday"], "%d/%m/%Y")
    if (birthday.day == today.day and birthday.month == today.month):
      username = bot.get_user(int(user["userID"])).mention
      file = discord.File(random.choice(birthday_photos), filename='image.png')

      mbed = discord.Embed(title='Cumpleaños!', color=discord.Color.gold())
      mbed.add_field(
          name="",
          value="Hoy es el cumpleaños de %s y esta cumpliendo **%s** añoooos!"
          % (username, today.year - birthday.year))
      mbed.set_image(url="attachment://image.png")
      await channel.send(file=file, embed=mbed)


@tasks.loop(minutes=3)
async def do_something():
  channel = bot.get_channel(bot_always)
  await channel.send("Mensaje para no morir")


@bot.command()
async def valorant(ctx):
  ids = [
      621672016445046784, 630745427842433044, 490287529833005075,
      348391595613224962, 287305573572018186, 362634148629970944,
      649732529858805790, 773121539117678622, 621647138539175936,
      551191398229999629, 589915710583472157
  ]
  #ids = [925870780548526132,621672016445046784,551191398229999629]
  ids.remove(ctx.message.author.id)
  author = ctx.message.author.mention
  for id in ids:
    try:
      user = bot.get_user(id)
      print(user.name)
      await user.send(
          f"Hola JEJE 👉👈, dice {author} que si quieres jugar valorant :P. Cualquier cosa está en el servidor 🫡"
      )
    except Exception as e:
      print(f"No he podido enviar el mensaje para el id {id}. {e}")
  await ctx.send("Enviando mensajes!")


@bot.command()
async def gaming(ctx, game):
  if (game):
    ids = [
        621672016445046784, 630745427842433044, 490287529833005075,
        348391595613224962, 287305573572018186, 362634148629970944,
        649732529858805790, 773121539117678622, 621647138539175936,
        551191398229999629, 589915710583472157
    ]
    ids.remove(ctx.message.author.id)
    author = ctx.message.author.mention
    for id in ids:
      try:
        user = bot.get_user(id)
        print(user.name)
        await user.send(
            f"Hola JEJE 👉👈, dice {author} que si quieres jugar {game} :P. Cualquier cosa está en el servidor 🫡"
        )
      except Exception as e:
        print(f"No he podido enviar el mensaje para el id {id}. {e}")
    await ctx.send("Enviando mensajes!")
  else:
    await ctx.send("Tienes que decir un juego bobo")


@bot.command()
async def test(ctx):
  channel = bot.get_channel(valo_gaming)
  await channel.connect()


bot.run(TOKEN)
