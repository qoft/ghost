import discord
import requests
import asyncio
import random

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="fun", description="Fun commands.", usage="")
    async def fun(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Fun")

        msg = codeblock.Codeblock(
            f"{cfg.get('theme')['emoji']} fun commands",
            description=pages[selected_page - 1],
            extra_title=f"Page {selected_page}/{len(pages)}"
        )

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="rickroll", description="Never gonna give you up.", usage="")
    async def rickroll(self, ctx):
        lyrics = requests.get("https://gist.githubusercontent.com/bentettmar/c8f9a62542174cdfb45499fdf8719723/raw/2f6a8245c64c0ea3249814ad8e016ceac45473e0/rickroll.txt").text    
        for line in lyrics.splitlines():
            await ctx.send(line)
            await asyncio.sleep(1)

    @commands.command(name="iq", description="Get the IQ of a user.", usage="[user]", aliases=["howsmart", "iqrating"])
    async def iq(self, ctx, *, user: discord.User):
        cfg = config.Config()
        iq = random.randint(45, 135)
        smart_text = ""

        if iq > 90 and iq < 135:
            smart_text = "They're very smart!"
        if iq > 70 and iq < 90:
            smart_text = "They're just below average."
        if iq > 50 and iq < 70:
            smart_text = "They might have some issues."
        elif iq < 50:
            smart_text = "They're severely retarded."

        msg = codeblock.Codeblock("iq", extra_title=f"{user.name}'s IQ is {iq}. {smart_text}")
        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="howgay", description="Get the gayness of a user.", usage="[user]", aliases=["gay", "gayrating"])
    async def howgay(self, ctx, *, user: discord.User):
        cfg = config.Config()
        gay_percentage = random.randint(0, 100)
        msg = codeblock.Codeblock("how gay", extra_title=f"{user.name} is {gay_percentage}% gay.")

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="howblack", description="Get the blackness of a user.", usage="[user]", aliases=["black", "blackrating"])
    async def howblack(self, ctx, *, user: discord.User):
        cfg = config.Config()
        black_percentage = random.randint(0, 100)
        msg = codeblock.Codeblock("how black", extra_title=f"{user.name} is {black_percentage}% black.")

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="pp", description="Get the size of a user's dick.", usage="[user]", aliases=["dick", "dicksize", "penis"])
    async def pp(self, ctx, *, user: discord.User):
        cfg = config.Config()
        penis = "8" + ("=" * random.randint(0, 12)) + "D"
        inches = str(len(penis)) + "\""
        msg = codeblock.Codeblock("pp", extra_title=f"{user.name} has a {inches} dick.", description=penis)

        await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

    @commands.command(name="blocksend", description="Send a message to a blocked user.", usage="[user] [message]")
    async def blocksend(self, ctx, user: discord.User, *, message: str):
        cfg = config.Config()
        
        await user.unblock()
        await user.send(message)
        await user.block()

        msg = codeblock.Codeblock("block send", extra_title=f"Sent a message to {user.name} ({user.id})", description=f"Message :: {message}")

        await ctx.send(msg, delete_after=self.cfg.get("message_settings")["auto_delete_delay"])

    def get_formatted_items(self, json_obj, tabs=0):
        formatted = ""
        sub_items_count = 0

        for item in json_obj:
            if isinstance(json_obj[item], dict):
                sub_items_count += 1 + tabs
                formatted += ("\t" * tabs) + f"{item}:\n"
                formatted += self.get_formatted_items(json_obj[item], sub_items_count)
                sub_items_count = 0
            else:
                formatted += ("\t" * tabs) + f"{item}: {json_obj[item]}\n"

        return formatted

    @commands.command(name="randomdata", description="Generate random data.", usage="[type]")
    async def randomdata(self, ctx, type_name: str = "unknown"):
        url = ""
        types = [{"name": "businesscreditcard", "url": "https://random-data-api.com/api/business_credit_card/random_card"},
            {"name": "cryptocoin", "url": "https://random-data-api.com/api/crypto_coin/random_crypto_coin"},
            {"name": "hipster", "url": "https://random-data-api.com/api/hipster/random_hipster_stuff"},
            {"name": "google", "url": "https://random-data-api.com/api/omniauth/google_get"},
            {"name": "facebook", "url": "https://random-data-api.com/api/omniauth/facebook_get"},
            {"name": "twitter", "url": "https://random-data-api.com/api/omniauth/twitter_get"},
            {"name": "linkedin", "url": "https://random-data-api.com/api/omniauth/linkedin_get"},
            {"name": "github", "url": "https://random-data-api.com/api/omniauth/github_get"},
            {"name": "apple", "url": "https://random-data-api.com/api/omniauth/apple_get"}]

        for _type in types:
            if type_name == _type["name"]:
                url = _type["url"]
                break
            else:
                url = "unknown"

        if url == "unknown":
            await ctx.send(str(codeblock.Codeblock("error", extra_title="Unkown data type.", description="The current types are: " + ", ".join([_type["name"] for _type in types]))))
            return

        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            formatted = self.get_formatted_items(data)

            msg = codeblock.Codeblock("random data", extra_title=f"Random {type_name}", description=formatted, style="yaml")
            await ctx.send(str(msg))
        else:
            await ctx.send(str(codeblock.Codeblock("error", extra_title="Failed to get data.")))

def setup(bot):
    bot.add_cog(Fun(bot))