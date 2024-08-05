import discord
from discord.ext import commands
from config import *
import re

bot = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")

@bot.event
async def on_message(message : discord.Message):
    if not message.author.bot:
        for word in message.content.split():
            link = None
            
            if match := ebay(word):
                match = get_link(match)
                link = f"{match}{EBAY}"
                name = 'an Ebay Link'
            elif match := amazon(word):
                match = get_link(match)
                link = f"{match+AMAZON_CA if 'amazon.ca' in match else match+AMAZON}"
                name = 'an Amazon Link'
            elif match:= tcgplayer(word):
                match = get_link(match)
                link = message.content.replace(word, f'{TCGPLAYER}{match}')
                name = 'a TCGPlayer Link'
            elif match:= fantastic_collect(word):
                match = get_link(match)
                link = message.content.replace(word, f'{FANTASTIC_COLLECT}{match}')
                name = 'a Fanatics Collect Link'
            elif match:= bestbuy(word):
                match = get_link(match)
                link = message.content.replace(word, f'{BESTBUY}{match}')
                name = 'a Best Buy Link'
            else:
                pass
        
            if link:
                await message.delete()
                await message.channel.send(f"**{message.author.mention} has posted {name}:**\n{link}")

def get_link(match: list):
    link = match[0] if (match[0].startswith('https://') or match[0].startswith('http://')) else f'https://{match[0]}'
    return link

def ebay(input_text):
    pattern = re.compile(r"www\.ebay\.[a-z]+/(itm|usr|str)/([a-zA-Z0-9]+)")
    return pattern.search(input_text)

def amazon(input_text):
    pattern = re.compile(r"www.amazon.+([a-z]+)+/+([a-zA-Z0-9_-]+)/dp/+([a-zA-Z0-9]+)")
    return pattern.search(input_text)

def tcgplayer(input_text):
    pattern = re.compile(r"tcgplayer\.com/[^\s]+")
    return pattern.search(input_text)

def fantastic_collect(input_text):
    pattern = re.compile(r"www\.fanaticscollect\.com/[^\s]+")
    return pattern.search(input_text)

def bestbuy(input_text):
    pattern = re.compile(r"www\.bestbuy\.com/[^\s]+")
    return pattern.search(input_text)


bot.run(TOKEN)