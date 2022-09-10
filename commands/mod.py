import discord

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="mod", description="Moderation commands.", aliases=["moderation"], usage="")
    async def mod(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Mod")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} mod commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="clear", description="Clear a number of messages.", aliases=["purge"], usage="[number]")
    async def clear(self, ctx, number: int):
        cfg = config.Config()
        deleted = await ctx.channel.purge(limit=number + 1)
        await ctx.send(codeblock.Codeblock(f"clear", extra_title=f"Purged {len(deleted) - 1} messages."), delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="ban", description="Ban a member from the command server.", usage="[member]")
    async def ban(self, ctx, member: discord.Member):
        try:
            await member.ban()
            await ctx.send(codeblock.Codeblock(f"ban", extra_title=f"Banned {member.name}#{member.discriminator}"))
        except Exception as e:
            await ctx.send(codeblock.Codeblock(f"error", extra_title=str(e)))

    @commands.command(name="kick", description="Kick a member from the command server.", usage="[member]")
    async def kick(self, ctx, member: discord.Member):
        try:
            await member.kick()
            await ctx.send(codeblock.Codeblock(f"kick", extra_title=f"Kicked {member.name}#{member.discriminator}"))
        except Exception as e:
            await ctx.send(codeblock.Codeblock(f"error", extra_title=str(e)))

def setup(bot):
    bot.add_cog(Mod(bot))