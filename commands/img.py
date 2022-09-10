import requests

from discord.ext import commands

from utils import config
from utils import codeblock
from utils import cmdhelper

class Img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="img", description="Image commands.", aliases=["image"], usage="")
    async def img(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Img")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} image commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="gato", description="Get a random cat picture.", aliases=["cat", "catpic"], usage="")
    async def gato(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/cats")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="doggo", description="Get a random cat picture.", aliases=["dog", "dogpic"], usage="")
    async def doggo(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/dogs")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="bird", description="Get a random cat picture.", aliases=["birb", "birdpic"], usage="")
    async def birb(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://api.alexflipnote.dev/birb")
        image = resp.json()["file"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="fox", description="Get a random fox picture.", aliases=["foxpic"], usage="")
    async def fox(self, ctx):
        cfg = config.Config()
        resp = requests.get("https://randomfox.ca/floof/")
        image = resp.json()["image"]

        await ctx.send(image, delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Img(bot))