import discord
import os
import time

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import embed as embedmaker

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="A list of all categories.", usage="")
    async def help(self, ctx, command: str = None):
        cfg = config.Config()
        if command is None:
            if cfg.get("theme")["style"] == "codeblock":
                msg = codeblock.Codeblock(f"{cfg.get('theme')['emoji']} {cfg.get('theme')['title']}", f"""fun  :: Fun commands
img  :: Image commands
info :: Information commands
mod  :: Moderation commands
util :: Utility commands
text :: Text commands""")

                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = embedmaker.Embed(title=cfg.get('theme')['title'], description=f"""**{self.bot.command_prefix}fun** Fun commands
**{self.bot.command_prefix}img** Image commands
**{self.bot.command_prefix}info** Information commands
**{self.bot.command_prefix}mod** Moderation commands
**{self.bot.command_prefix}util** Utility commands
**{self.bot.command_prefix}text** Text commands

There are **{len(self.bot.commands)}** commands!""", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed.set_thumbnail(url=cfg.get("theme")["image"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)
        else:
            cmd_obj = self.bot.get_command(command)
            if cmd_obj is None:
                if cfg.get("theme")["style"] == "codeblock":
                    await ctx.send(codeblock.Codeblock(title=f"help", description=f"Command not found.", extra_title=command), delete_after=cfg.get("message_settings")["auto_delete_delay"])

                else:
                    embed = embedmaker.Embed(title=f"Help", description=f"That command wasn't found.", colour=cfg.get("theme")["colour"])
                    embed.set_footer(text=cfg.get("theme")["footer"])
                    embed_file = embed.save()

                    await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                    os.remove(embed_file)

            else:

                if cfg.get("theme")["style"] == "codeblock":
                    msg = codeblock.Codeblock(f"help", f"""Name        :: {cmd_obj.name}
Description :: {cmd_obj.description}
Usage       :: {cmd_obj.usage}""")

                    await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

                else:
                    embed = embedmaker.Embed(title="Help", description=f"""**Name:** {cmd_obj.name}
**Description:** {cmd_obj.description}
**Usage:** {cmd_obj.usage}""", colour=cfg.get("theme")["colour"])
                    embed.set_footer(text=cfg.get("theme")["footer"])
                    embed_file = embed.save()

                    await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                    os.remove(embed_file)

    @commands.command()
    async def ping(self, ctx):
        cfg = config.Config()
        msg = codeblock.Codeblock(f"ping", extra_title=f"Your latency is {round(self.bot.latency * 1000)}ms")

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
            if cfg.get("theme")["style"] == "codeblock":
                commands_formatted.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")
            else:
                commands_formatted.append(f"**{cmd[0]}** {cmd[1]}")

        commands_str = ""
        for cmd in commands_formatted:
            if len(commands_str) + len(cmd) > 1000:
                pages.append(commands_str)
                commands_str = ""

            commands_str += f"{cmd}\n"

        if len(commands_str) > 0:
            pages.append(commands_str)
        
        if len(pages) == 0:
            if cfg.get("theme")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"search", description=f"No results found.", extra_title=query)
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = embedmaker.Embed(title="Search", description=f"No results found for **{query}**.", colour=cfg.get("theme")["colour"])
                embed.set_footer(text=cfg.get("theme")["footer"])
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        else:
            if cfg.get("theme")["style"] == "codeblock":
                msg = codeblock.Codeblock(title=f"search", description=pages[selected_page - 1], extra_title=f"Page {selected_page}/{len(pages)}")
                await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

            else:
                embed = embedmaker.Embed(title="Search", description=pages[selected_page - 1], colour=cfg.get("theme")["colour"])
                embed.set_footer(text=f"Page {selected_page}/{len(pages)}")
                embed_file = embed.save()

                await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
                os.remove(embed_file)

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

def setup(bot):
    bot.add_cog(General(bot))