import os, sqlite3
import discord
from discord.ext import commands
from decouple import config

# Бот реагирует на &. К примеру &time
bot = commands.Bot(command_prefix='&', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Бот запустился')

    global base, cur
    base = sqlite3.connect('Bot.db')
    cur = base.cursor()
    if base:
        print('База данных заработала')


bot.run(config('TOKEN'))
