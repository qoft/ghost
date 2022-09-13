import os
import discord

from . import codeblock
from . import config
from . import embed

def cog_desc(cmd, desc):
    return f"{desc}\n{cmd}"

def get_command_help(cmd):
    prefix = ""

    if cmd.parent is not None:
        prefix = f"{cmd.parent.name} {cmd.name}"
    else:
        prefix = f"{cmd.name}"

    return prefix

def generate_help_pages(bot, cog):
    pages = []
    pages_2 = []
    commands = bot.get_cog(cog).walk_commands()
    commands_formatted = []
    commands_formatted_2 = []
    commands_2 = []
    spacing = 0

    for cmd in commands:
        if cmd.name.lower() != cog.lower():
            prefix = get_command_help(cmd)

            if len(prefix) > spacing:
                spacing = len(prefix)

            commands_2.append([prefix, cmd.description])

    for cmd in commands_2:
        commands_formatted_2.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")
        commands_formatted.append(f"**{bot.command_prefix}{cmd[0]}** {cmd[1]}")

    commands_str = ""
    for cmd in commands_formatted:
        if len(commands_str) + len(cmd) > 300:
            pages.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages.append(commands_str)

    commands_str = ""
    for cmd in commands_formatted_2:
        if len(commands_str) + len(cmd) > 500:
            pages_2.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages_2.append(commands_str)

    return {"codeblock": pages_2, "image": pages}

async def send_message(ctx, discord_embed: discord.Embed, extra_title=""):
    cfg = config.Config()
    description = discord_embed.description
    title = discord_embed.title
    footer = discord_embed.footer.text

    if cfg.get("theme")["style"] == "codeblock":
        description = description.replace("*", "")
        description = description.replace("`", "")

        await ctx.send(str(codeblock.Codeblock(title=title, description=description, extra_title=extra_title)))
    elif cfg.get("theme")["style"] == "image":
        embed2 = embed.Embed(title=title, description=description)
        embed2.set_footer(text=footer)
        embed2.set_thumbnail(url=discord_embed.thumbnail.url)
        embed_file = embed2.save()
        await ctx.send(file=discord.File(embed_file, filename="embed.png"))
        os.remove(embed_file)
