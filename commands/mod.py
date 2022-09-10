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

    # @commands.command(name="clear", description="Clear a number of messages.", aliases=["purge"], usage="[number]")

def setup(bot):
    bot.add_cog(Mod(bot))