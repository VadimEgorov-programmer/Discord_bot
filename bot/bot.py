import sqlite3
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


@bot.command()
async def test(ctx):
    await ctx.send('Тест')


@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author
    arg = arg.lower()

    if arg == None:
        await ctx.send(
            f'{author.mention}, Введите:\n&инфо общее\n&инфо команды')
    elif arg == 'общее':
        await ctx.send(
            f'{author.mention}, Я бот, слежу за сообщениями в чате.'
            f' \n2 мата - бан')
    elif arg == 'команды':
        await ctx.send(
            f'{author.mention}, &test - Статус работы бота'
            f'\n&предупреждения - предупреждения')
    else:
        await ctx.send(f'{author.mention} Введённая вами команда отсутствует')


bot.run(config('TOKEN'))
