# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import random
import pandas
import os

"""DISCORD PARAMETERS"""
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)

"""DATA PARAMETERS"""
DATA_FOLDER="DATA"



"""FUNCTIONS"""
def getCard(df,file):
    if f.startswith("WORSHIPPERS"):
        #return getValue(df,"FACTION")
        embed=discord.Embed(
        title="Text Formatting",
            url="https://realdrewdata.medium.com/",
            description="Here are some ways to format text",
            color=discord.Color.blue())
        embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
        embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
        embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        embed.set_footer(text="Learn more here: realdrewdata.medium.com")
        return embed

def getValue(df,type):
    if type=="FACTION":
        list_factions=["NEUTRE","GAALDEN","MELI-AKUMI","AÏMA","DJAÏN"]
        return list_factions[int(df[type].values[0])-1]
    else:
        return df[type].values[0]


"""BOT COMMANDS"""
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def carte(ctx, name: str):
    data_path = os.path.join(os.path.abspath(os.path.dirname( __file__)),DATA_FOLDER)
    print("OK")
    for path, subdirs, files in os.walk(data_path):
        for f in files:
            result = pandas.read_csv(os.path.join(path,f), sep=';')
            if not result[result.NOM==searched_value].empty:
                df = result[result.NOM==searched_value]
                await ctx.send(embed=getCard(df,f))

@bot.command()
async def embed(ctx):
    embed=discord.Embed(
    title="Text Formatting",
        url="https://realdrewdata.medium.com/",
        description="Here are some ways to format text",
        color=discord.Color.blue())
    embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Learn more here: realdrewdata.medium.com")
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()
    for each_message in messages:
        await each_message.delete()

bot.run("ODg3ODI0NDY3NDI0ODQ5OTYw.YUJw-A.VtgyFXNwlJkHBVISsgD7kFDWH34")
