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
        embed=discord.Embed(title="__"+getValue(df,"NOM")+" (UNIQUE)__" if getValue(df,"UNICITE")=="U" else "__"+getValue(df,"NOM")+"__", description = "", color = 0x1abc9c)
        embed.add_field(name="***"+getValue(df,"FACTION")+" Worshipper • "+getValue(df,"TYPES")+"***", value="Cost: "+getValue(df,"COUT")+". Adoration: "+getValue(df,"ADORATION")+". Attack Power: "+getValue(df,"ATTAQUE")+". Endurance: "+getValue(df,"DEFENSE"), inline=False)
        embed.add_field(name="**"+getValue(df,"WSH-TRAITS")+"**", value=getValue(df,"WSH-TEXTE"), inline=False)
        embed.set_footer(text="**flavor text**")
        return embed
    if file.startswith("CRUSADES"):
        embed=discord.Embed(title="__"+getValue(df,"NOM")+"__",description="",color=discord.Color.blue())
        embed.add_field(name="***"+getValue(df,"FACTION")+" Event • "+getValue(df,"TYPES")+"***", value="Cost: "+getValue(df,"COUT")+". Elemental Value: "+getValue(df,"RAPIDITE"), inline=False)
        embed.add_field(name="**"+getValue(df,"CRU-ICONES")+"**", value=getValue(df,"TEXTE"), inline=False)
        embed.set_footer(text="**flavor text**")
        #'\u200'
        return embed
    if file.startswith("MUTATIONS"):
        embed=discord.Embed(title="__"+getValue(df,"NOM")+" (UNIQUE)__" if getValue(df,"UNICITE")=="U" else "__"+getValue(df,"NOM")+"__",description="",color=discord.Color.blue())
        embed.add_field(name="***"+getValue(df,"FACTION")+" Mutation • "+getValue(df,"TYPES")+"***", value="Cost: "+getValue(df,"COUT")+". Elemental Value: "+getValue(df,"RAPIDITE"), inline=False)
        embed.add_field(name="**"+getValue(df,"CRU-ICONES")+"**", value=getValue(df,"TEXTE"), inline=False)
        embed.set_footer(text="**flavor text**")
        #'\u200'
        return embed
    if file.startswith("KKOLOSSAL"):
        embed=discord.Embed(title="__"+getValue(df,"NOM")+"__",description="",color=discord.Color.blue())
        embed.add_field(name="***KKolossal Action***", value="Adoration required: "+getValue(df,"COUT")+". Swiftness: "+getValue(df,"RAPIDITE"), inline=False)
        embed.add_field(name="**"+getValue(df,"KK-ICONES")+"**", value=getValue(df,"TEXTE"), inline=False)
        embed.set_footer(text="**flavor text**")
        #'\u200b'
        return embed
    if file.startswith("TRIBES"):
        embed=discord.Embed(title="__"+getValue(df,"NOM")+"__",description="",color=discord.Color.blue())
        embed.add_field(name="***"+getValue(df,"FACTION")+" Tribe***", value='\u200b', inline=False)
        embed.add_field(name="**"+getValue(df,"CRU-ICONES")+"**", value=getValue(df,"TEXTE"), inline=False)
        embed.set_footer(text="**flavor text**")
        #'\u200b'
        return embed

def getValue(df,type):
    if type=="FACTION":
        list_factions=["Neutral","Gaalden","Meli-Akumi","Aïma","Djaïn"]
        return list_factions[int(df[type].values[0])-1]
    elif type=="WSH-TRAITS":
        texte = str(df["TEXTE"].values[0]).split("\\13\\ \\13\\")[0].replace("-","•")
        return texte
    elif type=="WSH-TEXTE":
        texte = str(df["TEXTE"].values[0])
        texte = texte.split("\\13\\ \\13\\")
        texte = texte[1]
        texte = texte.replace("\\13\\","\n> ")
        texte = texte.replace("{","**{").replace("}","}**")
        texte = "> "+texte
        if texte[-1]==">":
            texte=texte[:-1]
        if texte[-2]==">":
            texte=texte[:-2]
        return texte
    elif type=="TEXTE":
        texte = str(df["TEXTE"].values[0])
        texte = texte.replace("\\13\\","\n> ")
        texte = texte.replace("{","**{").replace("}","}**")
        if texte.startswith("> "):
            texte=texte[2:]
        return texte
    elif type=="CRU-ICONES":
        dict_icones={'A':'Ethereal','S':'Corrupted','F':'Incandescent','T':'Telluric','E':'Aqueous'}
        icones = df["ICONES"].values[0]
        elements = ""
        for l in icones:
            elements = dict_icones[l] if elements=="" else elements + " • " + dict_icones[l]
        return elements
    elif type=="KK-ICONES":
        dict_icones={'K':'Kham','D':'Diil','I':'Inks','M':'Maka','Z':'Zhunnu','R':'Rogvok','H':'Gomm'}
        icones = df["ICONES"].values[0]
        runes = ""
        for l in icones:
            runes = dict_icones[l] if runes=="" else runes + " • " + dict_icones[l]
        return runes
    else:
        return str(df[type].values[0]).replace(".0","")

"""BOT COMMANDS"""
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    index=0
    while message.content.find("[[",index)>-1 and message.content.find("]]",index)>-1:
        name = message.content[int(message.content.index("[[",index))+2:int(message.content.index("]]",index))]
        index = int(message.content.index("]]",index))+2
        ctx = await bot.get_context(message)
        data_path = os.path.join(os.path.abspath(os.path.dirname( __file__)),DATA_FOLDER)
        for path, subdirs, files in os.walk(data_path):
            for f in files:
                result = pandas.read_csv(os.path.join(path,f), sep=';')
                #df = result.loc[:,result.NOM.dropna().str.contains(name, case=False)]
                df = result[result.NOM.str.contains(name, case=False, na=False)]
                #df = result[result.NOM==name]
                if not df.empty:
                    #print(df)
                    await ctx.send(embed=getCard(df,f))
    await bot.process_commands(message)

@bot.command()
async def carte(ctx, *, name: str):
    data_path = os.path.join(os.path.abspath(os.path.dirname( __file__)),DATA_FOLDER)
    for path, subdirs, files in os.walk(data_path):
        for f in files:
            result = pandas.read_csv(os.path.join(path,f), sep=';')
            #df = result.loc[:,result.NOM.dropna().str.contains(name, case=False)]
            df = result[result.NOM.str.contains(name, case=False, na=False)]
            #df = result[result.NOM==name]
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