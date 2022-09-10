import discord

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import shortener

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="info", description="Information commands.", aliases=["information"], usage="")
    async def info(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Info")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} info commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="userinfo", description="Get information about a user.", aliases=["ui"], usage="[user]")
    async def userinfo(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        created_at = user.created_at.strftime("%d %B, %Y")
        msg = codeblock.Codeblock(title=f"user info", extra_title=f"{user.name}#{user.discriminator}", description=f"""Username   :: {user.name}
ID         :: {user.id}
Created at :: {created_at}""")

        await ctx.send(str(msg) + shortener.shorten(f"{user.avatar_url}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="serverinfo", description="Get information about the server.", aliases=["si"], usage="")
    async def serverinfo(self, ctx):
        cfg = config.Config()
        msg = codeblock.Codeblock(title=f"server info", extra_title=f"{ctx.guild.name}", description=f"""Name    :: {ctx.guild.name}
ID      :: {ctx.guild.id}
Owner   :: {ctx.guild.owner}
Members :: {ctx.guild.member_count}""")

        await ctx.send(str(msg) + shortener.shorten(str(ctx.guild.icon_url)), delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="avatar", description="Get the avatar of a user.", aliases=["av"], usage="[user]")
    async def avatar(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        await ctx.send(str(codeblock.Codeblock(title="avatar", extra_title=str(user))) + shortener.shorten(f"{user.avatar_url}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(Info(bot))