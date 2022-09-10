import os
import sys
import requests
import time
import discord
import faker
import random
import asyncio
import colorama
import base64
import threading
import json
import string

from discord.errors import LoginFailure
from discord.ext import commands

from pypresence import Presence

from utils import console
from utils import config
from utils import Notifier
from utils import scripts
from utils import files

cfg = config.Config()
cfg.check()
files.create_defaults()

status_resp = requests.get("https://discord.com/api/users/@me/settings", headers={"Authorization": cfg.get("token")})
if status_resp.status_code == 200:
    status = status_resp.json()["status"]
else:
    status = "online"

ghost = commands.Bot(command_prefix=cfg.get("prefix"), self_bot=True, help_command=None, status=discord.Status.try_value(status))
user = requests.get("https://discord.com/api/users/@me", headers={"Authorization": cfg.get("token")}).json()

try:
    rich_presence = Presence("1018195507560063039")
    rich_presence.connect()
    rich_presence.update(details=f"Logged in as {user['username']}#{user['discriminator']}", large_image="icon", start=time.time())
except:
    console.print_error("Failed to connect to Discord RPC")

for command_file in os.listdir("commands"):
    if command_file.endswith(".py"):
        ghost.load_extension(f"commands.{command_file[:-3]}")

for script_file in os.listdir("scripts"):
    if script_file.endswith(".py"):
        scripts.add_script("scripts/" + script_file, globals(), locals())

@ghost.event
async def on_connect():
    console.clear()
    console.resize(columns=90, rows=25)
    console.print_banner()
    console.print_info(f"Logged in as {ghost.user.name}#{ghost.user.discriminator}")
    console.print_info(f"You can now use commands with {cfg.get('prefix')}")
    print()

    Notifier.send("Ghost", f"Logged in as {ghost.user.name}#{ghost.user.discriminator}")

@ghost.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except Exception as e:
        console.print_error(str(e))

    command = ctx.message.content[len(ghost.command_prefix):]
    console.print_cmd(command)

# @ghost.event
# async def on_command_error(ctx, error):
#     cfg = config.Config()

#     try:
#         await ctx.message.delete()
#     except Exception as e:
#         console.print_error(str(e))

#     try:
#         await ctx.send(f"```ini\n[ error ] {str(error).lower()}\n```", delete_after=cfg.get("message_settings")["auto_delete_delay"])
#     except Exception as e:
#         console.print_error(f"{e}")

#     console.print_error(str(error))

try:
    ghost.run(cfg.get("token"))
except LoginFailure:
    console.print_error("Invalid token, please set a new one below.")
    new_token = input("> ")
    cfg.set("token", new_token)
    cfg.save()

    os.execl(sys.executable, sys.executable, *sys.argv)