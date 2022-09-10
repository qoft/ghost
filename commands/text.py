import discord
import requests
import asyncio
import random
import art as asciiart

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import fonts

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="text", description="Text commands.", usage="")
    async def text(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Text")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} text commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="shrug", description="Shrug your arms.", usage="")
    async def shrug(self, ctx):
        await ctx.send("¯\_(ツ)_/¯")

    @commands.command(name="tableflip", description="Flip the table.", usage="")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command(name="unflip", description="Put the table back.", usage="")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.command(name="lmgtfy", description="Let me Google that for you.", usage="[search]", aliases=["letmegooglethatforyou"])
    async def lmgtfy(self, ctx, *, search):
        await ctx.send(f"https://lmgtfy.app/?q={search.replace(' ', '+')}")

    @commands.command(name="blank", description="Send a blank message", usage="", aliases=["empty"])
    async def blank(self, ctx):
        await ctx.send("** **")

    @commands.command(name="ascii", description="Create ascii text art from text.", usage="[text]")
    async def ascii_(self, ctx, *, text: str):
        await ctx.send(f"```\n{asciiart.text2art(text)}\n```")

    @commands.command(name="aesthetic", description="Make your text aesthetic.", usage="[text]")
    async def aesthetic(self, ctx, *, text: str):
        result = " ".join(list(fonts.bypass(text)))
        await ctx.send(result)

    @commands.command(name="chatbypass", description="Bypass chat filters.", aliases=["bypass"], usage="[text]")
    async def chatbypass(self, ctx, *, text: str):
        await ctx.send(fonts.bypass(text))

def setup(bot):
    bot.add_cog(Text(bot))