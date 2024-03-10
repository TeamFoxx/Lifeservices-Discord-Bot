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

class ticket_system(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="tickets",
        description="Open a ticket",
        default_required_permissions=discord.Permissions(administrator=True)
    )
    async def tickets(self, ctx):
        ticket_options = config.ticket_options
        option_names = [getattr(config, f"option_{i}") for i in range(1, ticket_options + 1)]
        option_emojis = [getattr(config, f"option_{i}_emoji") for i in range(1, ticket_options + 1)]

        ticket_embed = discord.Embed(
            title="Ticket System",
            description="Select an option to open a ticket:",
            color=0xff6a00
        )

        select_options = [
            SelectOption(label=name.replace('_', ' '), value=name, emoji=emoji) for name, emoji in
            zip(option_names, option_emojis)
        ]

        select_menu = SelectMenu(
            custom_id='ticket_option_select_menu',
            placeholder='Wähle eine Option...',
            max_values=1,
            options=select_options
        )

        components = [[select_menu]]

        ticket_embed.set_footer(text="Powered by Lifeservices")

        msg = await ctx.respond(embed=ticket_embed, components=components)

    @commands.Cog.on_select('^ticket_option_select_menu$')
    async def select_option(self, ctx: discord.ComponentInteraction, select_menu):
        print("passed")
        selected_option = select_menu.values[0]

        category_id = getattr(config, f"{selected_option}_categoryID", None)
        ticket_message = getattr(config, f"{selected_option}_ticket_message", "Default ticket message")

        if category_id is None:
            await ctx.respond("Category not found.", hidden=True)
            return

        category = ctx.guild.get_channel(category_id)

        if category is None:
            await ctx.respond("Category not found.", hidden=True)
            return

        ticket_channel = await ctx.guild.create_text_channel(
            name=f"{ctx.author.name}-{selected_option}",
            category=category
        )

        ticket_roles = config.ticket_mods

        permissions = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
        }

        for role_id in ticket_roles:
            role = ctx.guild.get_role(role_id)
            if role:
                permissions[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                                attach_files=True)

        await ticket_channel.edit(overwrites=permissions)

        ticket_message_respond = discord.Embed(
            color=0xff6a00,
            description=ticket_message
        )

        await ticket_channel.send(
            embed=ticket_message_respond,
            components=[[
                Button(
                    style=ButtonStyle.red,
                    label="CLOSE",
                    custom_id="close"
                )
            ]]
        )

        await ticket_channel.send(f"Ticket opened by {ctx.author.mention} for {selected_option}.")
        await ctx.respond(f"Ticket for {selected_option} opened in {ticket_channel.mention}.", hidden=True)

    @commands.Cog.on_click('^close$')
    async def close(self, ctx: discord.ComponentInteraction, button):
        if any(role.id in config.ticket_mods for role in ctx.author.roles):
            close_ticket = discord.Embed(
                color=0xff6a00,
                description="> Confirm closing the ticket or open it again if the user who created the ticket has left the ticket.\n"
                            "You can also create a transcript of the ticket."
            )
            await ctx.respond(
                embed=close_ticket,
                hidden=True,
                components=[[
                    Button(
                        style=ButtonStyle.red,
                        label="CONFIRM CLOSE",
                        custom_id="closed_ticket"
                    ),
                    Button(
                        style=ButtonStyle.grey,
                        label="TRANSCRIPT",
                        custom_id="transcript"
                    )
                ]]
            )
        else:
            existing_overwrites = ctx.channel.overwrites

            existing_overwrites[ctx.author] = discord.PermissionOverwrite(view_channel=False)

            await ctx.respond("Ticket wird für dich geschlossen.", hidden=True)
            await asyncio.sleep(3)

            await ctx.channel.edit(overwrites=existing_overwrites)

            user_left = discord.Embed(
                color=0xff6a00,
                description=f"The user {ctx.author.mention} left the ticket."
            )
            await ctx.respond(embed=user_left,
                              components=[[
                                  Button(
                                      style=ButtonStyle.green,
                                      label="REOPEN",
                                      custom_id="reopen",
                                      disabled=True
                                  )
                              ]]
                              )

    @commands.Cog.on_click('^closed_ticket$')
    async def closed_ticket(self, ctx: discord.ComponentInteraction, button):
        await ctx.respond("Ticket wird geschlossen.", hidden=True)
        await asyncio.sleep(3)
        await ctx.channel.delete()

    @commands.Cog.on_click('^transcript$')
    async def save_transcript(self, ctx: discord.ComponentInteraction, button):
        channel = self.bot.get_channel(config.ticket_transcript_channel)

        if any(role.id in config.ticket_mods for role in ctx.author.roles):
            filename = f"{ctx.channel.name}_transcript.txt"
            async with ctx.channel.typing():
                with open(filename, "w", encoding="utf-8") as file:
                    async for message in ctx.channel.history(limit=None):
                        file.write(f"[{message.created_at}] {message.author.name}: {message.content}\n")
            with open(filename, "rb") as file:
                await channel.send("Transcript:", file=discord.File(file, filename=filename))
        else:
            await ctx.respond("Du hast nicht die erforderliche Berechtigung, um das Transkript zu erstellen.",
                              hidden=True)


# ⏤ { pre-settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(coffee_bot):
    coffee_bot.add_cog(ticket_system(coffee_bot))
