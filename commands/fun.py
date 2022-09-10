import discord
import requests
import asyncio
import random
import faker
import datetime

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()
        self.fake = faker.Faker()

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

    @commands.command(name="kanye", description="Random kanye quote.", usage="")
    async def kanye(self, ctx):
        resp = requests.get("https://api.kanye.rest/")
        if resp.status_code == 200:
            data = resp.json()
            await ctx.send(str(codeblock.Codeblock("kanye", extra_title=data["quote"])))
        else:
            await ctx.send(str(codeblock.Codeblock("error", extra_title="Failed to get data.")))

    @commands.command(name="socialcredit", description="Get a user's social credit score.", usage="[user]", aliases=["socialcreditscore", "socialcreditrating", "socialcredits", "socialrating", "socialscore"])
    async def socialcredit(self, ctx, *, user: discord.User):
        score = random.randint(-5000000, 10000000)
        await ctx.send(codeblock.Codeblock("social credit", extra_title=f"{user.name}'s social credit score is {score}."))

    @commands.command(name="dice", description="Roll a dice with a specific side count.", usage="[sides]", aliases=["roll"])
    async def dice(self, ctx, sides: int = 6):
        number = random.randint(1, sides)
        await ctx.send(codeblock.Codeblock(f"{sides} side dice", extra_title=f"You rolled a {number}."))

    @commands.command(name="rainbow", description="Create rainbow text.", usage="[text]", aliases=["rainbowtext"])
    async def rainbow(self, ctx, *, text: str):
        colours = {
            "red": {
                "codeblock": "diff",
                "prefix": "-",
                "suffix": ""
            },
            "orange": {
                "codeblock": "cs",
                "prefix": "#",
                "suffix": ""
            },
            "yellow": {
                "codeblock": "fix",
                "prefix": "",
                "suffix": ""
            },
            "green": {
                "codeblock": "cs",
                "prefix": "'",
                "suffix": "'",
            },
            "blue": {
                "codeblock": "md",
                "prefix": "#",
                "suffix": ""
            }
        }
        
        message = await ctx.send(text)

        for _ in range(3):
            for colour in colours:
                colour = colours[colour]
                await message.edit(content=f"""> ```{colour['codeblock']}\n> {colour['prefix']}{text}{colour['suffix']}```""")
                await asyncio.sleep(1)

    def calculate_age(self, born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @commands.command(name="dox", description="Dox a user.", usage=["[user]"])
    async def dox(self, ctx, *, user: discord.User):
        name = self.fake.name()
        email = name.lower().split(" ")[0][:random.randint(3, 5)] + "." + name.lower().split(" ")[1] + str(random.randint(10, 99)) + random.choice(["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"])
        dob = datetime.date(random.randint(1982, 2010), random.randint(1, 12), random.randint(1, 28))
        age = self.calculate_age(dob)
        phone = f"+1 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

        address_resp = requests.post("https://randommer.io/random-address", data={"number": "1", "culture": "en_US"}, headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"})
        address = address_resp.json()[0]

        await ctx.send(codeblock.Codeblock("dox", extra_title=f"{user.name}'s dox", description=f"""
Name          :: {name}
Email         :: {email}
Date of birth :: {dob.strftime("%d/%m/%Y")}
Age           :: {age}
Phone number  :: {phone}
Address       :: {address}
"""))

def setup(bot):
    bot.add_cog(Fun(bot))