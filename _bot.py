import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from flask import Flask
from threading import Thread

from _support_functions import *

load_dotenv()
token = os.environ['TOKEN']

app = Flask('')


@app.route('/')
def home():
  return "Hello, The bot is running!"


def runServer():
  app.run(host='0.0.0.0', port=8181)


def keep_alive():
  t = Thread(target=runServer)
  t.start()
