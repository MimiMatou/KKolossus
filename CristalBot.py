# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import random
import pandas
import os
from dotenv import load_dotenv

"""DISCORD PARAMETERS"""
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)
load_dotenv(dotenv_path="config")

"""DATA PARAMETERS"""
DATA_FOLDER="DATA"



"""FUNCTIONS"""
def getCard(df,file):
    if file.startswith("WORSHIPPERS"):
        #return getValue(df,"FACTION")

        embed=discord.Embed(
        title=getValue(df,"NOM")+" (UNIQUE)" if getValue(df,"UNICITE")=="U" else getValue(df,"NOM"),
            description="",
            color=discord.Color.blue())
        #embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
        embed.add_field(name="***"+getValue(df,"TYPES")+"***", value="Cost: "+getValue(df,"COUT")+". Adoration: "+getValue(df,"ADORATION")+". Attack Power: "+getValue(df,"ATTAQUE")+". Endurance: "+getValue(df,"DEFENSE"), inline=False)
        #embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name="**"+getValue(df,"WSH-TRAITS")+"**", value=getValue(df,"TEXTE"), inline=False)
        #embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        #embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        #embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        #embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        #embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        #'\u200b'
        embed.set_footer(text="**flavor text**")
        return embed

def getValue(df,type):
    if type=="FACTION":
        list_factions=["NEUTRE","GAALDEN","MELI-AKUMI","AÏMA","DJAÏN"]
        return list_factions[int(df[type].values[0])-1]
    elif type=="WSH-TRAITS":
        texte = str(df["TEXTE"].values[0]).split("\\13\\ \\13\\")[0].replace("-","•")
        return texte
    elif type=="TEXTE":
        texte = str(df[type].values[0])
        print(texte)
        texte = texte.split("\\13\\ \\13\\")
        print(texte)
        texte = texte[1]
        texte = texte.replace("\\13\\\\13\\","\n")
        print(texte)
        texte = texte.replace("{","**{").replace("}","}**")
        print(texte)
        return texte
    else:
        return str(df[type].values[0])


"""BOT COMMANDS"""
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.content.find("[[")>0 and message.content.find("]]")>0:
        #print(message.content.index("[["))
        name = message.content[int(message.content.index("[["))+2:int(message.content.index("]]"))]
        ctx = await bot.get_context(message)
        data_path = os.path.join(os.path.abspath(os.path.dirname( __file__)),DATA_FOLDER)
        for path, subdirs, files in os.walk(data_path):
            for f in files:
                result = pandas.read_csv(os.path.join(path,f), sep=';')
                df = result[result.NOM==name]
                if not df.empty:
                    await ctx.send(embed=getCard(df,f))
    await bot.process_commands(message)

@bot.command()
async def carte(ctx, *, name: str):
    data_path = os.path.join(os.path.abspath(os.path.dirname( __file__)),DATA_FOLDER)
    for path, subdirs, files in os.walk(data_path):
        for f in files:
            result = pandas.read_csv(os.path.join(path,f), sep=';')
            df = result[result.NOM==name]
            if not df.empty:
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

bot.run(os.getenv("TOKEN"))
