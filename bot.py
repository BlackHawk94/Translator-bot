import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from googletrans import Translator
import os
import requests

bot = commands.Bot(command_prefix=':t')

"""ready message"""
@bot.event
async def on_ready():  
    if(len(bot.servers)==1):
        await bot.change_presence(game=discord.Game(name=':thelp with '+str(len(bot.servers))+" server"))
    else:
        await bot.change_presence(game=discord.Game(name=':thelp with '+str(len(bot.servers))+" servers"))
    print('Translator v1.0 --')
    print('Successfully joined account: ' + bot.user.name)

"""translating"""            
@bot.command(pass_context=True)
async def r(ctx, *arg):
    try:
        await bot.delete_message(ctx.message)
    except:
        a=0
        
    try:
        text = str(' '.join(arg))
    except:
        text = str(' '.join(arg)).encode("utf-8")
        
    translator = Translator()
    src=""
    dest=""
    text+=" "
    if(text.find('s-')!=-1):
        src=text[text.find('s-')+2:text.find(' ', text.find('s-'))]
        text=text.replace("s-"+src, "")
    if(text.find('d-')!=-1):
        dest=text[text.find('d-')+2:text.find(' ', text.find('d-'))]
        text=text.replace("d-"+dest, "")
    
    if dest=="" and src=="":
        startext=str(translator.translate(text))
    elif src=="":
        startext=str(translator.translate(text, dest=dest))
    elif dest=="":
        startext=str(translator.translate(text, src=src))
    else:
        startext=str(translator.translate(text, dest=dest, src=src))
        
    text=startext[startext.find("text=")+5:startext.find(", pronunciation=")]
    
    if(text.find("<@")!=-1 and text.find(">")!=-1):
        text=text.replace("<@ ", "<@!")
        
    embed=discord.Embed(title="", description=text)
    try:
        await bot.send_message(ctx.message.channel, "<@!"+str(ctx.message.author.id)+">: "+text)
    except:
        try:
            await bot.send_message(ctx.message.channel, "invalid name: "+text)
        except:
            await bot.send_message(ctx.message.channel, "sorry, we're under maintanance :c we'll fix this as soon as possible")

"""direct help message"""
@bot.command(pass_context=True)
async def help(ctx):
    await bot.send_message(ctx.message.author, "```[] :tr 'text' s-'source language tag' d-'destination language tag' \n -translates a message \n -if source language tag is not provided it will be assigned automatically \n -if destination language tag is not provided it's automatically set as english(en) \n *do not use the apostrophe(')```")

bot.run(str(os.environ.get('TOKEN')))
