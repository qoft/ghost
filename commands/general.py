from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="A list of all categories.", usage="")
    async def help(self, ctx, command: str = None):
        cfg = config.Config()
        if command is None:
            msg = codeblock.Codeblock(f"{cfg.get('theme')['emoji']} {cfg.get('theme')['title']}", f"""fun  :: Fun commands
img  :: Image commands
info :: Information commands
mod  :: Moderation commands
util :: Utility commands""")
        else:
            cmd_obj = self.bot.get_command(command)
            if cmd_obj is None:
                msg = codeblock.Codeblock(title=f"help", description=f"Command not found.", extra_title=command)
            else:
                msg = codeblock.Codeblock(title=f"help", description=f"""Name        :: {cmd_obj.name}
Description :: {cmd_obj.description}
Usage       :: {cmd_obj.usage}""", extra_title=command)

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command()
    async def ping(self, ctx):
        cfg = config.Config()
        msg = codeblock.Codeblock(f"{cfg.get('theme')['emoji']} {cfg.get('theme')['title']}", extra_title=f"Your latency is {round(self.bot.latency * 1000)}ms")

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])
    
    @commands.command(name="search", description="Search for commands.", usage="[query]")
    async def search(self, ctx, query: str, selected_page: int = 1):
        cfg = config.Config()
        commands = self.bot.walk_commands()
        commands_formatted = []
        commands_2 = []
        spacing = 0
        pages = []

        for cmd in commands:
            if query in cmd.name or query in cmd.description:
                prefix = cmdhelper.get_command_help(cmd)

                if len(prefix) > spacing:
                    spacing = len(prefix)

                commands_2.append([prefix, cmd.description])

        for cmd in commands_2:
            commands_formatted.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")

        commands_str = ""
        for cmd in commands_formatted:
            if len(commands_str) + len(cmd) > 1000:
                pages.append(commands_str)
                commands_str = ""

            commands_str += f"{cmd}\n"

        if len(commands_str) > 0:
            pages.append(commands_str)
        
        if len(pages) == 0:
            msg = codeblock.Codeblock(title=f"search", description=f"No results found.", extra_title=query)
        else:
            msg = codeblock.Codeblock(title=f"search", description=pages[selected_page - 1], extra_title=f"Page {selected_page}/{len(pages)}")

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(General(bot))