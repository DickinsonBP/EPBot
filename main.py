import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import requests

import json
from datetime import date, datetime, timedelta
import random

load_dotenv()
TOKEN = os.environ['TOKEN']
UNSPLASH = os.environ['UNSPLASH']
MOVIES_TOKEN = os.environ['MOVIES_TOKEN']
#GPT = os.environ['GPT']

birthday_photos = [
    "media/piolin_cumple.jpeg", "media/piolin_cumple2.jpeg",
    "media/piolin_cumple3.jpeg", "media/piolin_cumple4.jpeg",
    "media/piolin_cumple5.jpeg"
]

#channels id
welcome = 1019315282138894416
chateo = 779103315933528075
valo_gaming = 1018984617451212850

intents = discord.Intents.all()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  print("Bot acitvated!")
  meme_day.start()
  check_birthdays.start()
  weekly_movies.start()
  #check_premier.start()

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
      description=f"{author} aqui puedes ver los comandos que puedes usar!",color=discord.Color.gold())

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
  mbed.add_field(
      name="**!movies**",
      value=
      "Muestra las peliculas de estreno de la semana actual. Ej: !movies",
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
                 value='Genera una encuesta. Ej: !poll "Encuesta" si no. Tener en cuenta que hay que poner doble comillas ""!',
                 inline=False)
  mbed.add_field(
      name="**!add_birthday**",
      value=
      "Añade el cumpleaños de un miembro. Ej: !add_birthday @user fecha_nacimiento (dd/mm/YYYY)",
      inline=False)
  mbed.add_field(
      name="**!delete_birthday**",
      value=
      "Añade el cumpleaños de un miembro. Ej: !delete_birthday @user",
      inline=False)
  mbed.add_field(name="**!next_birthdays**",
                 value="Muestra los cumpleaños que vienen",
                 inline=False)
  mbed.add_field(
      name="**!get_premier_data**",
      value=
      "Muestra toda la información hasta ahora de nuestra clasificación en premier",
      inline=False)
  mbed.add_field(
      name="**!update_premier**",
      value=
      "Actualiza el estado de nuestro equipo en premier. Ej: !update_premier win (añade un win)",
      inline=False)
  mbed.add_field(
      name="**!restart_premier**",
      value=
      "Actualiza el estado de los puntos en premier",
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
      - Julio: https://www.twitch.tv/jeidad_
    """)


@bot.command()
async def image(ctx, *, search):
  # search_formtted = search.replace(' ', '_')
  search_formtted = requests.utils.quote(search)
  url = f'https://api.unsplash.com/photos/random/?query={search_formtted}&orientation=squarish&content_filter=high&client_id={UNSPLASH}'
  try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if 'urls' in data:
                mbed = discord.Embed(title=f'Aquí está tu imagen de **{search}**!',color=discord.Color.gold())
                mbed.set_image(url=data['urls']['regular'])
                await ctx.send(embed=mbed)
            else:
                await ctx.send("No se ha encontrado ninguna imagen que coincida con tu búsqueda.")
        else:
            await ctx.send("🔥 No se ha podido encontrar la imagen.")
  except Exception as e:
    await ctx.send("Error! No se ha podido encontrar la imagen **%s**" % search)


def calculate_next_birthday(birthday_str):
    today = datetime.today()
    birthday_date = datetime.strptime(birthday_str, "%d/%m/%Y")
    birthday_this_year = birthday_date.replace(year=today.year)

    # Si el cumpleaños ya pasó este año, calcular para el próximo año
    if today > birthday_this_year:
        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

    return birthday_this_year

def sort_birthdays(data):

    for user in data:
        user['next_birthday'] = calculate_next_birthday(user['birthday'])
        
     # Ordenar por el campo 'next_birthday'
    sorted_data = sorted(data, key=lambda x: x['next_birthday'])

    # Eliminar el campo 'next_birthday' después de ordenar
    for user in sorted_data:
        del user['next_birthday']

    return sorted_data

@bot.command()
async def add_birthday(ctx, member, birthday):
  try:
    f = open("json/birthdays.json")
    data = json.load(f)
    f.close()

    member = member.replace('<', '')
    member = member.replace('>', '')
    member = member.replace('@', '')

    data.append({"userID": member, "birthday": birthday})

    with open("json/birthdays.json", "w") as json_file:
      json.dump(data, json_file)

    await ctx.send("Se ha guardado el cumpleaños correctamente!")
  except Exception as e:
    await ctx.send(f"🔥Error al ejecutar comando !add_birthdays: {e}")

@bot.command()
async def delete_birthday(ctx, member):
  try:
      # Leer los datos existentes desde el archivo JSON
      with open("json/birthdays.json") as f:
          data = json.load(f)

      # Limpiar el formato del miembro
      member_id = member.replace('<', '').replace('>', '').replace('@', '')

      # Filtrar los datos para eliminar el cumpleaños del miembro especificado
      new_data = [user for user in data if user['userID'] != member_id]

      # Si no se encontró el usuario, enviar un mensaje de error
      if len(new_data) == len(data):
          await ctx.send("No se encontró el cumpleaños del usuario.")
          return

      # Guardar los datos actualizados en el archivo JSON
      with open("json/birthdays.json", "w") as json_file:
          json.dump(new_data, json_file)

      await ctx.send("Se ha eliminado el cumpleaños correctamente!")

  except Exception as e:
      await ctx.send(f"🔥Error al ejecutar comando !delete_birthday: {e}")

@bot.command()
async def next_birthdays(ctx):
  f = open("json/birthdays.json")
  data = json.load(f)
  # print(data)
  data = sort_birthdays(data)
  mbed = discord.Embed(title='Los siguientes cumpleaños son:',
                       color=discord.Color.gold())
  today = datetime.today()
  try:
    for user in data:
      year = 0
      username = bot.get_user(int(user["userID"]))
      if username:
        username = username.mention

        birthday1 = datetime.strptime(user["birthday"], "%d/%m/%Y")
        # birthday1 = datetime(today.year, birthday1.month, birthday1.day)
        if (birthday1.month > today.month) and (birthday1.day > today.day):
        # if (birthday1 > today):
          year = today.year
          birthday = "%s/%s/%s" % (birthday1.day, birthday1.month, year)
        else:
          year = today.year + 1
          birthday = "%s/%s/%s" % (birthday1.day, birthday1.month, year)

        birthday = datetime.strptime(birthday, "%d/%m/%Y")

        mbed.add_field(name="",
                      value="%s Cumple el %s/%s/%s, quedan %s días y **cumple %s añacos**" %
                      (username, birthday.day, birthday.month, birthday.year, (birthday - today).days, year - birthday1.year),
                      inline=False)

    await ctx.send(embed=mbed)
  except Exception as e:
    await ctx.send(f"🔥Error al ejecutar comando !next_birthdays: {e}")

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

  mbed = discord.Embed(title=question, color=discord.Color.gold())
  for i in range(len(options)):
    mbed.add_field(name=options[i], value=reactions[i], inline=True)
  message = await ctx.send(embed=mbed)
  for i in range(len(options)):
    await message.add_reaction(reactions[i])


def check_today_file(day, file):
  with open(file, "r") as f:
    lines = f.readlines()
    #get last line
    last_line = lines[-1].strip()
  last_line = last_line.split()[0]
  return day.strftime("%d/%m/%Y") == last_line


def save_today_file(day, file):
  with open(file, 'a') as file:
    file.write(day.strftime("%d/%m/%Y") + '\n')


@tasks.loop(hours=24)
async def meme_day():
  channel = bot.get_channel(chateo)
  try:
    print("Checking meme of the day")
    today = date.today()
    if (not check_today_file(today, "extra_files/meme_day.txt")):
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
      if (today.strftime("%a") == "Wed"):
        file = discord.File('media/mdm.jpg', filename='mdm.jpg')
        mbed = discord.Embed(title='Miercoles de takos!',
                            color=discord.Color.gold())
        mbed.set_thumbnail(url="attachment://mdm.jpg")
        mbed.add_field(name="Hoy es miercoles de takos!",
                      value="El maldito miercoles de takos!")
        mbed.set_image(url="attachment://mdm.jpg")
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
      if (today.strftime("%a") == "Sun"):
        file = discord.File('media/dds.jpg', filename='dds.jpg')
        mbed = discord.Embed(title='Domingo del señor!',
                            color=discord.Color.gold())
        mbed.set_thumbnail(url="attachment://dds.jpg")
        mbed.add_field(name="Hoy es domingo del señor!",
                      value="El maldito domingo del señor!")
        mbed.set_image(url="attachment://dds.jpg")
        await channel.send(file=file, embed=mbed)
      else:
        pass

      save_today_file(today, "extra_files/meme_day.txt")
  except Exception as e:
    await channel.send(f"🔥Error al ejecutar comando !check_meme_day: {e}")


@tasks.loop(hours=24)
async def check_birthdays():
  channel = bot.get_channel(chateo)
  try:
    print("Checking birthday")
    today = date.today()
    f = open("json/birthdays.json")
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
  except Exception as e:
    await channel.send(f"🔥Error al ejecutar comando !check_birthdays: {e}")

@bot.command()
async def valorant(ctx):
  ids = [
      621672016445046784, 630745427842433044, 490287529833005075,
      348391595613224962, 287305573572018186, 362634148629970944,
      773121539117678622, 621647138539175936,551191398229999629, 
      589915710583472157, 289526674436128768, 407088836666064896
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
        773121539117678622, 621647138539175936, 551191398229999629, 
        589915710583472157, 289526674436128768, 407088836666064896
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
async def update_premier(ctx, status):
  with open("json/premier_data.json", "r") as jsonFile:
    data = json.load(jsonFile)

  if (status == "win"):
    data["premier"][0]["wins"] = data["premier"][0]["wins"] + 1
    data["premier"][0][
        "total_points"] = data["premier"][0]["total_points"] + 100
    await ctx.send("Epaaa menudo win xavaleee")
  if (status == "lose"):
    data["premier"][0]["loses"] = data["premier"][0]["loses"] + 1
    data["premier"][0][
        "total_points"] = data["premier"][0]["total_points"] + 25
    await ctx.send("Mas malos y no naceis")

  data["premier"][0][
      "total_matches_played"] = data["premier"][0]["total_matches_played"] + 1
  data["premier"][0]["matches_left"] = data["premier"][0]["matches_left"] - 1

  with open("json/premier_data.json", "w") as jsonFile:
    json.dump(data, jsonFile)

@bot.command()
async def get_premier_data(ctx):
  file = discord.File('media/Premier.png', filename='Premier.png')
  mbed = discord.Embed(title='PREMIER!',
                       description="Estos son los resultados hasta ahora",
                       color=discord.Color.gold())
  mbed.set_thumbnail(url="attachment://Premier.png")
  f = open("json/premier_data.json")
  data = json.load(f)["premier"][0]
  mbed.add_field(name="Partidos jugados hasta ahora",
                 value="%s" % (data["total_matches_played"]),
                 inline=False)
  mbed.add_field(name="Partidos que quedan por jugar",
                 value="%s" % (data["matches_left"]),
                 inline=False)
  mbed.add_field(name="Total de puntos conseguidos (600 para clasificar)",
                 value="%s" % (data["total_points"]),
                 inline=False)
  mbed.add_field(name="Partidos ganados hasta ahora",
                 value="%s" % (data["wins"]),
                 inline=False)
  mbed.add_field(name="Partidos perdidos hasta ahora",
                 value="%s" % (data["loses"]),
                 inline=False)
  wins = (600 - int(data["total_points"])) // 100
  loses = ((600 - int(data["total_points"])) % 100) // 25

  if (wins + loses > int(data["matches_left"])):
    wins = int(data["matches_left"])
    loses = 0
  mbed.add_field(name="Partidos para clasificar",
                 value="%s wins y %s loses" % (wins, loses),
                 inline=False)

  await ctx.send(file=file, embed=mbed)


@tasks.loop(hours=24)
async def check_premier():
  print("Checking premier day")
  channel = bot.get_channel(chateo)
  today = date.today()
  if (not check_today_file(today, "extra_files/premier_day.txt")):
    file = discord.File('media/Premier.png', filename='Premier.png')
    mbed = discord.Embed(title='Hoy toca premier!',
                         description="Estos son los resultados hasta ahora",
                         color=discord.Color.gold())
    mbed.set_thumbnail(url="attachment://Premier.png")
    f = open("json/premier_data.json")
    data = json.load(f)["premier"][0]
    mbed.add_field(name="Partidos jugados hasta ahora",
                   value="%s" % (data["total_matches_played"]),
                   inline=False)
    mbed.add_field(name="Partidos que quedan por jugar",
                   value="%s" % (data["matches_left"]),
                   inline=False)
    mbed.add_field(name="Total de puntos conseguidos (600 para clasificar)",
                   value="%s" % (data["total_points"]),
                   inline=False)
    mbed.add_field(name="Partidos ganados hasta ahora",
                   value="%s" % (data["wins"]),
                   inline=False)
    mbed.add_field(name="Partidos perdidos hasta ahora",
                   value="%s" % (data["loses"]),
                   inline=False)
    wins = (600 - int(data["total_points"])) // 100
    loses = ((600 - int(data["total_points"])) % 100) // 25
    if (wins + loses > int(data["matches_left"])):
      wins = int(data["matches_left"])
      loses = 0
    mbed.add_field(name="Partidos para clasificar",
                   value="%s wins y %s loses" % (wins, loses),
                   inline=False)
    if (today.strftime("%a") == "Sat"):
      await channel.send(file=file, embed=mbed)
    if (today.strftime("%a") == "Thu"):
      await channel.send(file=file, embed=mbed)

    save_today_file(today, "extra_files/premier_day.txt")

@bot.command()
async def restart_premier(ctx):
  with open("json/premier_data.json", "r") as jsonFile:
    data = json.load(jsonFile)

  data["premier"][0]["wins"] = 0
  data["premier"][0]["total_points"] = 0
  data["premier"][0]["loses"] = 0

  data["premier"][0]["total_matches_played"] = 0
  data["premier"][0]["matches_left"] = 14

  with open("json/premier_data.json", "w") as jsonFile:
    json.dump(data, jsonFile)
  
  await ctx.send("Archivo actualizado!")

@bot.command()
async def test(ctx):
  pass


def get_weekly_movies():
    """
    Función para obtener las películas estrenadas en la última semana.
    """
    url = "https://api.themoviedb.org/3/movie/now_playing?language=es-SP&page=1&region=ES"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {MOVIES_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data["results"]

        # Filtrar películas estrenadas en la última semana
        weekly_movies = []
        today = datetime.now()
        one_week_ago = today - timedelta(days=7)

        for movie in results:
            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
            if release_date >= one_week_ago and release_date <= today:
                weekly_movies.append(movie)

        return weekly_movies
    else:
        print(f"Error fetching data from TMDb: {response.status_code}")
        return []

def generate_movies_embeded():
  movies = get_weekly_movies()
  embeds = []  # Lista para almacenar múltiples embeds si es necesario
  embed = discord.Embed(
      title="Estrenos de Películas de la Semana",
      description="Aquí están los estrenos de películas de la semana en los cines.",
      color=discord.Color.gold()
  )

  for movie in movies:
      title = movie["title"]
      original_title = movie["original_title"]
      release_date = movie["release_date"]
      overview = movie["overview"]
      rating = movie["vote_average"]
      poster_path = movie["poster_path"]
      poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

      # Truncar el resumen si es demasiado largo
      if len(overview) > 100:
          overview = overview[:97] + "..."

      # Verificar si agregar esta película excedería el límite de caracteres del embed
      if len(embed) + len(f"{title} (Rating: {rating})") + len(f"Fecha de estreno: {release_date}\n{overview[:100]}...") > 6000:
          embeds.append(embed)  # Agregar el embed actual a la lista
          embed = discord.Embed(  # Crear un nuevo embed
              title="Estrenos de Películas de la Semana (continuación)",
              description="Continúa la lista de estrenos de la semana.",
              color=discord.Color.blue()
          )
      if original_title == title:
        embed.add_field(
            name=f"{title} (Puntuación: {rating})",
            value=f"Fecha de estreno: {release_date}\n{overview}",
            inline=False
        )
      else:
        embed.add_field(
            name=f"{title} (Titulo original: {original_title}) (Puntuación: {rating})",
            value=f"Fecha de estreno: {release_date}\n{overview}",
            inline=False
        )

      if poster_url:
          embed.set_thumbnail(url=poster_url)

  embeds.append(embed)
  return embeds

@tasks.loop(hours=24)
async def weekly_movies():
  today = date.today()  
  if (today.strftime("%a") == "Mon"):
    channel = bot.get_channel(chateo)
    try:
      print("Cheking weekly movies")
      movies = generate_movies_embeded()

      if not movies:
          await channel.send("No se encontraron estrenos de películas para esta semana.")
          return

      # Enviar todos los embeds
      for embed in movies:
          await channel.send(embed=embed)
    except Exception as e:
      await channel.send(f"🔥Error al ejecutar comando !weekly_movies: {e}")
      
@bot.command()
async def movies(ctx):
  try:
    movies = generate_movies_embeded()

    if not movies:
        await ctx.send("No se encontraron estrenos de películas para esta semana.")
        return

    # Enviar todos los embeds
    for embed in movies:
        await ctx.send(embed=embed)
  except Exception as e:
    await ctx.send(f"🔥Error al ejecutar comando !movies: {e}")


@bot.command()
async def ask_bot(ctx, *, user_message: str):
  bot = commands.Bot(command_prefix="!")

  url = "http://localhost:8080/v1/chat/completions"
  headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer no-key"
  }
  
  data = {
        "model": "LLaMA_CPP",
        "messages": [
            {
                "role": "system",
                "content": "You are LLAMAfile, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
  
  try:
    ctx.send("Por favor dame tiempo toy xikito 👉👈")
    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear la respuesta JSON y formatearla con indentación
        formatted_response = json.dumps(response.json(), indent=2)
        # Enviar la respuesta formateada al canal
        await ctx.send(f"Respuesta de LLaMA:\n```json\n{formatted_response}\n```")
    else:
        await ctx.send(f"Error: {response.status_code} - {response.text}")

  except Exception as e:
    # Manejo de excepciones generales
    await ctx.send(f"Error al conectarse al servidor LLaMA: {str(e)}")


bot.run(TOKEN)
