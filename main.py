import discord
from discord.ext import commands
import os

# Intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Your server ID here (numbers only)
GUILD_ID = 123456789012345678  # <-- Replace with your server ID

# Roles with hoist=True to display separately
roles = [
    ("Air Chief Marshal", 0xFFD700, True),
    ("Air Marshal", 0xFF8C00, True),
    ("Group Captain", 0xFF4500, True),
    ("Wing Commander", 0x1E90FF, True),
    ("Squadron Leader", 0x32CD32, True),
    ("Flight Lieutenant", 0x9370DB, True),
    ("Flying Officer", 0x00CED1, True),
    ("Cadet", 0xA9A9A9, True),
]

# Server structure: categories with text and voice channels
server_structure = {
    "👑 HIGH COMMAND": {
        "text": ["raf-announcements", "orders-from-command", "mission-briefings", "promotion-board", "chain-of-command"],
        "voice": ["Air Marshal Office", "Officer Briefing Room"]
    },
    "🛫 RECRUITMENT & TRAINING": {
        "text": ["join-the-raf", "application-status", "training-schedule", "cadet-questions", "flight-school-resources"],
        "voice": ["Cadet Classroom", "Training Airspace"]
    },
    "📡 OPERATIONS COMMAND": {
        "text": ["active-operations", "flight-plans", "airspace-control", "after-action-reports", "intel-reports"],
        "voice": ["ATC Tower", "Combat Airspace", "Patrol Channel"]
    },
    "✈️ FIGHTER COMMAND": {
        "text": [
            "1sq-general", "1sq-sorties",
            "11sq-general", "11sq-missions",
            "25sq-general", "25sq-intercepts"
        ],
        "voice": ["1SQ Ops Room", "11SQ Combat", "25SQ Intercept"]
    },
    "💣 BOMBER & STRIKE COMMAND": {
        "text": ["9sq-briefings", "9sq-strike-plans", "617sq-dambusters", "617sq-targeting"],
        "voice": ["9SQ Strike Ops", "617SQ Strike"]
    },
    "🚁 ROTARY WING COMMAND": {
        "text": ["33sq-transport", "33sq-support", "28sq-sar", "28sq-alerts"],
        "voice": ["33SQ Lift", "28SQ Rescue"]
    },
    "🛩️ TRANSPORT & SUPPORT COMMAND": {
        "text": ["70sq-logistics", "70sq-flight-ops", "10sq-refuel", "10sq-flight-line"],
        "voice": ["70SQ Cargo", "10SQ Tanker"]
    },
    "🛰️ RECON & SPECIAL OPERATIONS": {
        "text": ["51sq-intel", "51sq-surveillance", "sof-covert", "sof-operations"],
        "voice": ["51SQ Recon", "Black Ops"]
    },
    "🏆 COMMUNITY & SOCIAL": {
        "text": ["general-chat", "media-gallery", "flight-clips", "memes", "suggestions"],
        "voice": ["Officers' Mess", "Pilot Lounge"]
    }
}

# -----------------------------
# Bot events
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# -----------------------------
# Slash command to remake server
# -----------------------------
@bot.slash_command(name="remake", description="Recreates the RAF PTFS server structure")
async def remake(ctx):
    guild = bot.get_guild(GUILD_ID)

    # Create roles
    existing_roles = [r.name for r in guild.roles]
    for role_name, color, hoist in roles:
        if role_name not in existing_roles:
            await guild.create_role(name=role_name, color=color, hoist=hoist)

    # Create categories + channels
    existing_cats = [c.name for c in guild.categories]
    for category_name, channels in server_structure.items():
        if category_name not in existing_cats:
            cat = await guild.create_category(category_name)
        else:
            cat = discord.utils.get(guild.categories, name=category_name)

        # Text channels
        for text_channel in channels.get("text", []):
            if not discord.utils.get(cat.channels, name=text_channel):
                await guild.create_text_channel(text_channel, category=cat)
        # Voice channels
        for voice_channel in channels.get("voice", []):
            if not discord.utils.get(cat.channels, name=voice_channel):
                await guild.create_voice_channel(voice_channel, category=cat)

    await ctx.respond("RAF PTFS server fully recreated!")

# -----------------------------
# Run bot with token from environment
# -----------------------------
bot.run(os.getenv("MTQ3NTI1NTc1MTE1MTcxODQzMA.GTyuzn.jzRHrM00-3-fr88WZ1-hLhvIFwJ5KWQ1z8gYDM"))
