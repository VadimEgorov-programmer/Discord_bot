import sqlite3
import discord
from discord.ext import commands
from decouple import config
import string, json

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


@bot.event
async def on_member_join(member):
    await member.send('Привет, я бот. Команды &инфо')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.mame == 'общее':
            await bot.get_channel(ch.id).send(f'{member} приветствую')


@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.mame == 'общее':
            await bot.get_channel(ch.id).send(f'{member} вышел')


@bot.command()
async def test(ctx):
    await ctx.send('Тест')


@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author

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


@bot.command
async def предупреждения(ctx):
    base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(
        ctx.message.guild.name))
    base.commit()
    warning = cur.execute(
        'SELECT = FROM {} WHERE userid == ?'.format(ctx.message.guild.name),
        (ctx.message.author.id,)).fetchone()
    if warning == None:
        await ctx.send(
            f'{ctx.message.author.mention}, у вас нет предупреждений')
    else:
        await ctx.send(
            f'{ctx.message.author.mention}, у'
            f' вас {warning[1]} нет предупреждений')


@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i
        in message.content.split(' ')}.intersection(
        set(json.load(open('mat.json')))) != set():
        await message.channel.send(f'{message.author.mention}, чат без матов')
        await message.delete()

        name = message.guild.name

        base.execute(
            'CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(
                name))
        base.commit()

        warning = cur.execute(
            'SELECT * FROM {} WHERE userid == ?'.format(name),
            (message.author.id,)).fetchone()

        if warning == None:
            cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name),
                        (message.author.id, 1))
            base.commit()
            await message.channel.send(
                f'{message.author.mention}, это первое предупреждение,'
                f' за третье бан')
        elif warning[1] == 1:
            cur.execute(
                'UPDATE {} SET count == ? WHERE userid ==?'.format(name),
                (2, message.author.id))
            base.commit()
            await message.channel.send(
                f'{message.author.mention}, это второе предупреждение,'
                f' за третье бан')
        elif warning[1] == 2:
            cur.execute(
                'UPDATE {} SET count == ? WHERE userid == ?'.format(name),
                (3, message.author.id))
            base.commit()
            await message.channel.send(
                f'{message.author.mention}, забанен за маты')
            await message.author.ban(reason='Нецензурные выражения')

    await bot.process_commands(message)


bot.run(config('TOKEN'))
