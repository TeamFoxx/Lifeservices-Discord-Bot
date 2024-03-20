# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Entwickelt von Foxx
# »› Copyright © 2024 Aurel Hoxha. Alle Rechte vorbehalten.
# »› GitHub: https://github.com/TeamFoxx
# »› Für Support und Anfragen kontaktieren Sie bitte hello@aurelhoxha.de
# »› Verwendung dieses Programms unterliegt den Bedingungen der MIT-Lizenz.
# »› Eine Kopie der Lizenz finden Sie in der Datei "LICENSE" im Hauptverzeichnis dieses Projekts.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { imports } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
from cogs import *


# ⏤ { pre-settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class welcome_message(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.avatar_url)) as response:
                avatar_data = await response.read()

        background = Image.open("./pictures/background.png")
        width, height = background.size

        draw = ImageDraw.Draw(background)

        # Avatar-Bild herunterladen und auf Kreis zuschneiden
        avatar_image = Image.open(io.BytesIO(avatar_data))
        avatar_image = avatar_image.resize((350, 350))
        mask = Image.new("L", (avatar_image.width, avatar_image.height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, avatar_image.width, avatar_image.height), fill=255)
        avatar_image.putalpha(mask)

        avatar_width, avatar_height = avatar_image.size
        avatar_x = (width - avatar_width) // 2
        avatar_y = (height - avatar_height) // 2
        background.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

        font_path = "./fonts/Alata-Regular.ttf"
        font = ImageFont.truetype(font_path, 90)
        font2 = ImageFont.truetype(font_path, 50)

        draw.text((230, 55), f"Willkommen, {member.name}!", fill="#ff6a00", font=font)

        member_count = len(member.guild.members)
        draw.text((560, 600), f"Member: {member_count}", fill="#ff6a00", font=font2)

        image_bytes = io.BytesIO()
        background.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        channel = self.bot.get_channel(config.welcome_message_channel)
        await channel.send(f"### Hey {member.mention}. Welcome to Lifeservices, have a look at <#1001191280782606427> to get access!", file=discord.File(image_bytes, "welcome.png"))


# ⏤ { pre-settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(coffee_bot):
    coffee_bot.add_cog(welcome_message(coffee_bot))
