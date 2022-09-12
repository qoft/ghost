import random
import requests

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle([(upper_left_point[0], upper_left_point[1] + corner_radius), (bottom_right_point[0], bottom_right_point[1] - corner_radius)], fill=fill, outline=outline)
    self.rectangle([(upper_left_point[0] + corner_radius, upper_left_point[1]), (bottom_right_point[0] - corner_radius, bottom_right_point[1])], fill=fill, outline=outline)
    self.pieslice([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],180, 270, fill=fill, outline=outline)
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],0, 90, fill=fill, outline=outline)
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],90, 180, fill=fill, outline=outline)
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)], 270, 360, fill=fill, outline=outline)

ImageDraw.rounded_rectangle = rounded_rectangle

def generate_gradient(colour1: str, colour2: str, width: int, height: int) -> Image:
    """Generate a vertical gradient."""
    base = Image.new('RGB', (width, height), colour1)
    top = Image.new('RGB', (width, height), colour2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return '\n'.join(lines)

def hex_to_rgb(hex: str) -> tuple:
    """Convert a hex colour to RGB."""
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) 

class Embed:
    def __init__(self, bot, title, description = "", footer = "", colour = "#1E1E1E", color = "", thumbnail = "", image = ""):
        self.bot = bot
        self.title = title
        self.description = description.replace("```", "")
        self.footer = footer
        self.thumbnail = thumbnail
        self.image = image
        self.colour = None

        if colour != "":
            self.colour = colour
        elif color != "":
            self.colour = color
        
        self.title_font = ImageFont.truetype("data/fonts/Roboto-Bold.ttf", 70)
        self.description_font = ImageFont.truetype("data/fonts/Roboto-Regular.ttf", 54)
        self.description_font_bold = ImageFont.truetype("data/fonts/Roboto-Bold.ttf", 54)
        self.footer_font = ImageFont.truetype("data/fonts/Roboto-LightItalic.ttf", 54)

        self.height = 200 + 50
        self.width = 1500

        if self.height < 400:
            self.height = 380

        if self.footer != "":
            self.height += 100

        # if self.image != "":
        #     image = Image.open(BytesIO(requests.get(self.image).content)).convert("RGBA")
        #     image.thumbnail((self.width, image.height), Image.ANTIALIAS)
        #     self.height += image.height + 50
        #     self.width = image.width + 120

        if self.description != "":
            for line in self.description.splitlines():
                wrap = get_wrapped_text(line, self.description_font, self.width - 450).split("\n")
                self.height += len(wrap) * 60
            
            self.height -= 100

    def draw(self):
        template = Image.new("RGBA", (self.width, self.height), (30, 30, 30, 0))
        draw = ImageDraw.Draw(template)

        # draw background
        draw.rounded_rectangle([(0, 0), (self.width - 15, self.height)], 25, fill=hex_to_rgb(self.colour))
        draw.rounded_rectangle([(10, 0), (self.width - 10, self.height)], 25, fill=(30, 30, 30, 255))

        addon = Image.open("data/waves.png").convert("RGBA")
        template.paste(addon, (int(self.width / 2) - int(addon.width / 2), int(self.height / 2) - int(addon.height / 1.5)), addon)

        # draw title background
        if self.thumbnail != "":
            draw.rounded_rectangle([(40, 40), (self.width - 300 - 40 - 40, 165)], 20, fill=(37, 37, 37, 255))
        else:
            draw.rounded_rectangle([(40, 40), (self.width - 45, 165)], 20, fill=(37, 37, 37, 255))
        
        # draw title text
        draw.text((70, 62), self.title, (255, 255, 255), font=self.title_font)

        # draw thumbnail image
        if self.thumbnail != "":
            logo = Image.open(BytesIO(requests.get(self.thumbnail).content)).convert("RGBA")
            logo = logo.resize((300, 300))
            template.paste(logo, (self.width - 300 - 45, 40))

        # draw description
        if self.description != "":
            y_offset = 200
            for line in self.description.splitlines():
                wrap = get_wrapped_text(line, self.description_font, self.width - 450).split("\n")

                for line in wrap:
                    x_offset = 60
                    for word in line.split():
                        if word.startswith("**") and word.endswith("**"):
                            word = word.replace("**", "")
                            draw.text((x_offset, y_offset), word, (212, 212, 212), font=self.description_font_bold)
                            x_offset += self.description_font_bold.getlength(word + " ")
                        else:
                            draw.text((x_offset, y_offset), word, (212, 212, 212), font=self.description_font)
                            x_offset += self.description_font.getlength(word + " ")

                    y_offset += 60

        # draw image
        # if self.image != "":
        #     image = Image.open(BytesIO(requests.get(self.image).content)).convert("RGBA")
        #     image.thumbnail((self.width, image.height), Image.ANTIALIAS)
        #     template.paste(image, (60, self.height - image.height - 45 - 100))

        # draw footer
        if self.footer != "":
            draw.text((60, self.height - 100), self.footer, (180, 180, 180), font=self.footer_font)

        return template

    def save(self):
        path = f"embed-{random.randint(1000, 9999)}.png"
        self.draw().save(path)
        return path