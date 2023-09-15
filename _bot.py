import discord
from discord.ext import commands

from flask import Flask
from threading import Thread

from _support_functions import *


class EPBot(discord.Client):
  __commands = []
  app = Flask('')

  @app.route('/')
  def home():
    return "Hello, The bot is running!"

  def runServer(self):
    self.app.run(host='0.0.0.0', port=8181)

  def keep_alive(self):
    t = Thread(target=self.runServer)
    t.start()

  async def on_ready(self):
    print("Bot acitvated! {0}".format(self.user))

  async def on_message(self, message):
    # we do not want the bot to reply to itself
    if (message.author.id == self.user.id):
      return

    for command in self.__commands:
      if (message.content == command[0]):
        print("Channel: {0.channel} | User {0.author} : {0.content}".format(
            message))
        await message.channel.send(command[1])

  async def on_member_join(self, member):
    await member.send("Hola!!")

  #basic !command
  def setCommand(self, command, text):
    new_command = (command, text)
    self.__commands.append(new_command)

  def run(self, token):
    self.keep_alive()
    return super().run(token)
