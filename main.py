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

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

bot.run(TOKEN)