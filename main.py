# » Release date: 24 February 2024
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

coffee = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=commands.when_mentioned_or("."),
    sync_commands=True,
    auto_check_for_updates=True
)
coffee.remove_command("help")


# ⏤ { On Bot ready } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

@coffee.event
async def on_ready():
    print(f"{Fore.GREEN}━━━ {Fore.WHITE}Ready Information {Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Logged in as {Fore.MAGENTA}{coffee.user}")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Developed with {Fore.RED}<3 {Fore.MAGENTA}by Foxx")
    print(f"{Fore.GREEN}»› {Fore.WHITE}For inquiries, reach out to {Fore.MAGENTA}hello@aurelhoxha.de")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Check out the code on {Fore.MAGENTA}GitHub: https://github.com/TeamFoxx")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Join my {Fore.MAGENTA}Discord server: https://discord.gg/nQEwwyJ")

    activity = discord.Activity(name=f"Lifeservices v1.0.0", type=discord.ActivityType.watching)
    await coffee.change_presence(activity=activity)

# ⏤ { heartbeat } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

_core = [p.stem for p in Path('./core').glob('*.py') if p.stem != '__init__']
for ext in _core:
    coffee.load_extension(f'core.{ext}')
    print(f'\033[32m{ext}\033[0m was loaded successfully')

_cogs = [p.stem for p in Path('./cogs').glob('*.py') if p.stem != '__init__']
[(coffee.load_extension(f'cogs.{ext}'), print(f'\033[32m{ext}\033[0m was loaded successfully')) for ext in _cogs]


coffee.run(my_secrets.key.token)
