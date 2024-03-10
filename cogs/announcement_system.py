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

class announcement_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="announce",
        description="Announce something!",
        default_required_permissions=discord.Permissions(administrator=True)
    )
    async def announcement(self, ctx):
        modal = Modal(
            title=f'Broadcast System',
            custom_id=f'announcement_modal',
            components=[
                [
                    TextInput(
                        label="Announcement channel",
                        custom_id="channel",
                        placeholder="Füge die channel ID hier ein.",
                        min_length=1,
                        style=1
                    )
                ],
                [
                    TextInput(
                        label="Announcement header",
                        custom_id="header",
                        placeholder="📢 Announcement",
                        max_length=30,
                        min_length=1,
                        style=1
                    )
                ],
                [
                    TextInput(
                        label="Announcement color",
                        custom_id="color",
                        placeholder="zb. #44835e",
                        max_length=7,
                        min_length=1,
                        style=1
                    )
                ],
                [
                    TextInput(
                        label="Announcement message",
                        custom_id="message",
                        placeholder="Füge deine Benachrichtigung hier ein.",
                        max_length=750,
                        min_length=1,
                        style=2
                    )
                ]
            ]
        )
        await ctx.respond_with_modal(modal)

    @commands.Cog.on_submit('^announcement_modal$')
    async def edit_temp_channel_modal_submit(self, ctx: discord.ModalSubmitInteraction):

        header = ctx.get_field('header').value
        color = ctx.get_field('color').value
        message = ctx.get_field('message').value
        channel = ctx.get_field('channel').value

        channel_to_announce = self.bot.get_channel(int(channel))

        if color.startswith('#'):
            color = int(color[1:], 16)
        else:
            color = 0xff6a00

        announcement = discord.Embed(
            title=header,
            description=message,
            color=color
        )

        announcement.set_footer(text=f"~ {ctx.author.display_name}")
        await channel_to_announce.send(
            embed=announcement,
            components=[]
        )

        respond = discord.Embed(
            title=header,
            description=message,
            color=color
        )
        respond.set_footer(text=f"~ {ctx.author.display_name} • This is your preview!")
        await ctx.respond(
            embed=respond,
            hidden=True,
        )

# ⏤ { pre-settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤


def setup(coffee_bot):
    coffee_bot.add_cog(announcement_system(coffee_bot))
