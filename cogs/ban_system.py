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

class ban_system(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="Ban_ID",
        description="Banne eine ID",
        default_required_permissions=discord.Permissions(ban_members=True)
    )
    async def ban(self, ctx, user_id):
        try:
            # Benutzer mit der angegebenen Benutzer-ID verbannen
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.ban(user)
            await ctx.respond(f"*User* with ID `{user_id}` has been banned from the server.", hidden=True)
        except discord.NotFound:
            await ctx.respond("*User not found.*", hidden=True)
        except discord.Forbidden:
            await ctx.respond("I don't have permission to ban users.", hidden=True)

# ⏤ { pre-settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(coffee_bot):
    coffee_bot.add_cog(ban_system(coffee_bot))
