import discord
from discord.ext import commands
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="tarkovbot"
)

cursor = db.cursor()

client = commands.Bot(command_prefix = '>>')

calibres = [".366","4.6x30","5.7x28","5.45x39","5.56x45","7.62x25","7.62x39","7.62x51","7.62x54R","9x18","9x19","9x21","9x39","12.7x55","12x70","12/70","20x70","20/70"]
mapas = ["FACTORY","CUSTOMS","WOODS","SHORELINE","INTERCHANGE","LABS","RESERVE"]
traders = ["PRAPOR","THERAPIST","FENCE","SKIER","PEACEKEEPER","MECHANIC","RAGMAN","JAEGER"]
comandos = ["map","item","quests","ammo","ajuda"]

@client.event
async def on_ready ():
    print('Estou pronto!')
    servers = client.guilds
    for x in servers:
        print(x)
    print (servers)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"```diff\n-Este comando não existe\n+Nossos comandos são: {comandos}```")
    else:
        raise error

@client.event
async def on_command(ctx):
    print(ctx.command)
    print(ctx.author)
    print(ctx.guild)

@client.command()
async def map (ctx, *, mapa = ""):
    if mapa == "":
        await ctx.send("```py\nPara obter um mapa da raid desejada, digite:\n'>>map nome da raid'\n```")
    else:
        mapa = mapa.upper()
        if str(mapa) != None and str(mapa) in mapas:
            await ctx.send(file=discord.File(f'Maps/{mapa}.jpg'))
        else:
            await ctx.send(f"```diff\n-Este mapa não existe.\n+Nossos mapas são: {mapas} ```")

@client.command()
async def ajuda (ctx):
    await ctx.send("Nossos comandos são: \n>>map 'nome da raid' (Comando para receber o mapa de uma raid)\n>>ammo 'calibre' (Comando que disponibiliza uma tabela com os detalhes da munição de acordo com o calibre requisitado)\n>>item 'nome do item' (Comando que mostra se o item pesquisado esta presente em alguma quest do jogo e quantos serão necessários.)\n>>quests (Link da wiki que possui todas as quests do tarkov)\n")

@client.command()
async def ammo (ctx, *, ammo = ""):
    if ammo == "":
        await ctx.send(f"```py\nPara obter a tabela de balas do calibre desejado, digite:\n'>>ammo (calibre)'\nCalibres: {calibres}```")
    else:
        if ammo in calibres:
            if ammo == "12x70" or ammo == "12/70":
                ammo = "12GAUGE"
            elif ammo =="20x70" or ammo =="20/70":
                ammo = "20GAUGE"
            await ctx.send(file=discord.File(f'Ammo/{ammo}.jpg'))
        else:
            await ctx.send(f"```diff\n-Este calibre não existe.\n+Nossos calibres são: {calibres} ```")

@client.command()
async def item (ctx, *,item = ""):
    if item == "":
        await ctx.send("```py\nPara saber se um item é requisitado em alguma quest, digite:\n'>>item nome do item'\n```")
    else:
        item = str(item)
        cursor.execute(f"SELECT * FROM missao where item LIKE '%{item}%'")
        resultado = cursor.fetchall()
        if not resultado:
            await ctx.send("```diff\n-Este item não está presente em nenhuma quest.\n```")
        else:
            await ctx.send(f"Os resultados encontrados para o item : {item}")
            for row in resultado:
                await ctx.send(f"```fix\nO item está presente em uma quest = \nNome do item: {row[0]} \nTrader: {row[1]} \nQuantidade necessária: {row[2]} \n```")

@client.command()
async def quests(ctx):
    await ctx.send("\nO link para a wiki com todas as quests detalhadas:\nhttps://escapefromtarkov.gamepedia.com/Quests")

client.run('')
