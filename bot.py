"""
=========================================================================
 DISCORD PRANK & FUN BOT — single file edition (bot.py)
=========================================================================
Install requirements first:
    pip install discord.py

Just paste your bot token in the BOT_TOKEN variable below (Section 2)
and run the bot:
    python bot.py

Everything (commands, database, background tasks, UI buttons) lives in
this ONE file, as requested. Comments mark each section so it's easy
to find things even if you've never read a Discord bot before.
=========================================================================
"""

# ======================= 1. IMPORTS =====================================
import os
import random
import sqlite3
import asyncio
import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks

# ======================= 2. CONFIG / TOKEN =================================
# 👇 PASTE YOUR DISCORD BOT TOKEN HERE (only place you need to touch) 👇
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

DB_FILE = "bot_data.db"

# All toggle-able features (used by /toggle admin command)
ALL_FEATURES = ["roast", "scan", "giveaway", "rank", "detect", "randomfun"]

# ======================= 3. DATABASE (SQLite, same file) ==================
def db_connect():
    """Open a new connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create tables if they don't already exist. Runs once at startup."""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS points (
            guild_id INTEGER,
            user_id INTEGER,
            points INTEGER DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS config (
            guild_id INTEGER PRIMARY KEY,
            fun_channel_id INTEGER,
            disabled_features TEXT DEFAULT '',
            last_fun_message TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_points(guild_id: int, user_id: int, amount: int):
    """Add (or subtract) points for a user in a guild."""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO points (guild_id, user_id, points) VALUES (?, ?, ?)
        ON CONFLICT(guild_id, user_id) DO UPDATE SET points = points + ?
    """, (guild_id, user_id, amount, amount))
    conn.commit()
    conn.close()


def get_points(guild_id: int, user_id: int) -> int:
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT points FROM points WHERE guild_id=? AND user_id=?", (guild_id, user_id))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_leaderboard(guild_id: int, limit: int = 10):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, points FROM points
        WHERE guild_id=? ORDER BY points DESC LIMIT ?
    """, (guild_id, limit))
    rows = cur.fetchall()
    conn.close()
    return rows


def ensure_config(guild_id: int):
    """Make sure a config row exists for this guild."""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO config (guild_id, disabled_features) VALUES (?, '')", (guild_id,))
    conn.commit()
    conn.close()


def get_config(guild_id: int):
    ensure_config(guild_id)
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT guild_id, fun_channel_id, disabled_features, last_fun_message FROM config WHERE guild_id=?", (guild_id,))
    row = cur.fetchone()
    conn.close()
    return row


def set_fun_channel(guild_id: int, channel_id: int):
    ensure_config(guild_id)
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE config SET fun_channel_id=? WHERE guild_id=?", (channel_id, guild_id))
    conn.commit()
    conn.close()


def toggle_feature(guild_id: int, feature: str) -> bool:
    """Flip a feature on/off for a guild. Returns True if now ENABLED."""
    ensure_config(guild_id)
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT disabled_features FROM config WHERE guild_id=?", (guild_id,))
    disabled = cur.fetchone()[0] or ""
    disabled_list = [f for f in disabled.split(",") if f]

    if feature in disabled_list:
        disabled_list.remove(feature)   # was disabled -> now enable it
        now_enabled = True
    else:
        disabled_list.append(feature)   # was enabled -> now disable it
        now_enabled = False

    new_value = ",".join(disabled_list)
    cur.execute("UPDATE config SET disabled_features=? WHERE guild_id=?", (new_value, guild_id))
    conn.commit()
    conn.close()
    return now_enabled


def is_feature_enabled(guild_id: int, feature: str) -> bool:
    row = get_config(guild_id)
    disabled_list = (row[2] or "").split(",")
    return feature not in disabled_list


def update_last_fun_message(guild_id: int):
    ensure_config(guild_id)
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE config SET last_fun_message=? WHERE guild_id=?",
                (datetime.datetime.utcnow().isoformat(), guild_id))
    conn.commit()
    conn.close()


# ======================= 4. FUN CONTENT (jokes/data) =======================
ROASTS = [
    "{mention} has a K/D ratio lower than their IQ. 💀",
    "{mention} still thinks 'noob' is a compliment. 🍼",
    "{mention} lags in real life, not just in-game. 📶",
    "{mention} bought a gaming chair but still loses to bots. 🪑",
    "{mention}'s aim is so bad, the crosshair files a complaint. 🎯",
    "{mention} rage quits Tic-Tac-Toe. 😤",
    "{mention} needs a tutorial for the tutorial. 📖",
    "{mention} treats 'GG' like a participation trophy. 🏆",
    "{mention} has more respawns than actual kills. ⚰️",
    "{mention}'s Wi-Fi is faster than their reaction time... barely. 🐌",
    "{mention} calls it 'skill issue' but it's always their issue. 🤡",
    "{mention} pressed alt+f4 thinking it was a healing spell. 🔥",
]

SCAN_STEPS = [
    "🔍 Starting scan...",
    "🧠 Checking skills...",
    "🎮 Analyzing gamer profile...",
    "📊 Compiling final report...",
]

SCAN_RESULTS = [
    "Diagnosis: 73% pure luck, 27% button mashing. 🎲",
    "Warning: Skill.exe has stopped working. ⚠️",
    "Scan complete: Certified controller-thrower. 🎮💥",
    "Result: 1 rage quit detected per 4 minutes. 😡",
    "Analysis: Talks trash, plays worse. 🗑️",
    "Final verdict: Carried by teammates since day one. 🚛",
]

DETECTIVE_INTROS = [
    "🕵️ Case File #{case}: The Curious Incident of {mention}",
    "🕵️ Detective Report on Suspect: {mention}",
]

DETECTIVE_EVIDENCE = [
    "Found 47 empty energy drink cans near the crime scene.",
    "Suspect was last seen blaming 'ping' for every mistake.",
    "Fingerprints match someone who rage-quit 3 matches in a row.",
    "Witnesses report hearing 'it's not my fault' 12 times in one game.",
    "Suspicious amount of skins bought, zero improvement in skill.",
    "A screenshot of a 0-10 scoreboard was recovered from suspect's gallery.",
]

DETECTIVE_VERDICTS = [
    "Verdict: Guilty of being carried. Sentence: one free roast. 😂",
    "Verdict: Not guilty, just extremely unlucky (allegedly). 🍀",
    "Verdict: Case dismissed due to lack of skill evidence in the first place. ⚖️",
]

RANDOM_FUN_MESSAGES = [
    "🎲 Fun fact: 100% of noobs deny being noobs.",
    "😂 Reminder: blaming lag is always valid, right? Right?",
    "🏆 Someone in this server is one loss away from rage-quitting forever.",
    "🎮 Poll of the day: who's carrying this server?",
    "💀 Bot detected suspicious levels of trash talk nearby...",
]

GIVEAWAY_JOKE_PRIZES = [
    "a lifetime supply of bad luck 🍀",
    "1 (one) participation trophy 🏆",
    "an invisible skin nobody can see 👻",
    "a virtual high-five ✋",
    "bragging rights (unverified) 🗣️",
]


def stat():
    return random.randint(0, 100)


# ======================= 5. BOT SETUP =====================================
intents = discord.Intents.default()
intents.message_content = False  # not needed since we use slash commands

bot = commands.Bot(command_prefix="!", intents=intents)


def feature_check(feature_name: str):
    """Decorator-style check used inside commands to respect /toggle settings."""
    def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            return True
        return is_feature_enabled(interaction.guild.id, feature_name)
    return app_commands.check(predicate)


# ======================= 6. UI COMPONENTS (Buttons) ========================
class RoastAgainView(discord.ui.View):
    """Button that re-rolls a roast for the same target."""
    def __init__(self, target: discord.Member):
        super().__init__(timeout=60)
        self.target = target

    @discord.ui.button(label="Roast Again 🔥", style=discord.ButtonStyle.danger)
    async def roast_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        line = random.choice(ROASTS).format(mention=self.target.mention)
        embed = discord.Embed(title="🔥 Roast Delivered", description=line, color=discord.Color.orange())
        add_points(interaction.guild.id, interaction.user.id, 2)
        await interaction.response.edit_message(embed=embed, view=self)


class GiveawayView(discord.ui.View):
    """Join button for the fake giveaway."""
    def __init__(self):
        super().__init__(timeout=15)
        self.participants = set()

    @discord.ui.button(label="🎉 Join Giveaway", style=discord.ButtonStyle.success)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.participants.add(interaction.user)
        await interaction.response.send_message("✅ You joined the giveaway!", ephemeral=True)


# ======================= 7. SLASH COMMANDS =================================

@bot.tree.command(name="roast", description="Send a funny, friendly roast to a user.")
@app_commands.describe(user="The user to roast")
@app_commands.checks.cooldown(1, 8.0)
@feature_check("roast")
async def roast(interaction: discord.Interaction, user: discord.Member):
    async with interaction.channel.typing():
        await asyncio.sleep(1.2)
    line = random.choice(ROASTS).format(mention=user.mention)
    embed = discord.Embed(title="🔥 Roast Delivered", description=line, color=discord.Color.orange())
    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    add_points(interaction.guild.id, interaction.user.id, 2)
    await interaction.response.send_message(embed=embed, view=RoastAgainView(user))


@bot.tree.command(name="scan", description="Run a fake 'system scan' on a user for laughs.")
@app_commands.describe(user="The user to scan")
@app_commands.checks.cooldown(1, 10.0)
@feature_check("scan")
async def scan(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        embed = discord.Embed(title="🖥️ Gamer Scan", description=SCAN_STEPS[0], color=discord.Color.blue())
        msg = await interaction.followup.send(embed=embed)

        for step in SCAN_STEPS[1:]:
            await asyncio.sleep(1.3)
            embed = discord.Embed(title="🖥️ Gamer Scan", description=step, color=discord.Color.blue())
            await msg.edit(embed=embed)

        await asyncio.sleep(1.3)
        result = random.choice(SCAN_RESULTS)
        final = discord.Embed(
            title="✅ Scan Complete",
            description=f"**Target:** {user.mention}\n\n{result}",
            color=discord.Color.green()
        )
        add_points(interaction.guild.id, interaction.user.id, 3)
        await msg.edit(embed=final)


@bot.tree.command(name="giveaway", description="Start a fake giveaway with a countdown and winner pick.")
@app_commands.checks.cooldown(1, 15.0)
@feature_check("giveaway")
async def giveaway(interaction: discord.Interaction):
    view = GiveawayView()
    embed = discord.Embed(
        title="🎉 GIVEAWAY TIME! 🎉",
        description=f"Prize: **{random.choice(GIVEAWAY_JOKE_PRIZES)}**\nClick the button below to join!\n\n⏳ Ends in 15 seconds...",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, view=view)
    msg = await interaction.original_response()

    for seconds_left in (10, 5, 3, 1):
        await asyncio.sleep(15 - seconds_left if seconds_left == 10 else 5 if seconds_left == 5 else 2 if seconds_left == 3 else 2)
        embed.description = (
            f"Prize: **{embed.description.splitlines()[0].split('**')[1]}**\n"
            f"Click the button below to join!\n\n⏳ {seconds_left} seconds left..."
        )
        try:
            await msg.edit(embed=embed, view=view)
        except discord.HTTPException:
            pass

    view.stop()
    async with interaction.channel.typing():
        await asyncio.sleep(1.5)

    if view.participants:
        winner = random.choice(list(view.participants))
        result_text = f"🎊 The winner is... {winner.mention}!\nThey won **absolutely nothing real**, but congrats anyway! 😂"
        add_points(interaction.guild.id, winner.id, 5)
    else:
        result_text = "😂 Nobody joined... the bot wins by default. Sad."

    final_embed = discord.Embed(title="🏁 Giveaway Ended!", description=result_text, color=discord.Color.purple())
    await msg.edit(embed=final_embed, view=None)


@bot.tree.command(name="rank", description="Show a funny gamer profile with random stats.")
@app_commands.describe(user="The user to check")
@app_commands.checks.cooldown(1, 8.0)
@feature_check("rank")
async def rank(interaction: discord.Interaction, user: discord.Member):
    async with interaction.channel.typing():
        await asyncio.sleep(1)
    embed = discord.Embed(title=f"🎮 Gamer Profile: {user.display_name}", color=discord.Color.teal())
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="🎯 Aim Accuracy", value=f"{stat()}%", inline=True)
    embed.add_field(name="🕹️ Gaming Skill", value=f"{stat()}%", inline=True)
    embed.add_field(name="🍀 Luck", value=f"{stat()}%", inline=True)
    embed.add_field(name="😡 Rage Level", value=f"{stat()}%", inline=True)
    embed.add_field(name="🍼 Noob Level", value=f"{stat()}%", inline=True)
    embed.add_field(name="👑 Pro Level", value=f"{stat()}%", inline=True)
    embed.add_field(name="⭐ Fun Points", value=str(get_points(interaction.guild.id, user.id)), inline=False)
    add_points(interaction.guild.id, interaction.user.id, 1)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="detect", description="Run a funny investigation report on a user.")
@app_commands.describe(user="The user to investigate")
@app_commands.checks.cooldown(1, 10.0)
@feature_check("detect")
async def detect(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        await asyncio.sleep(1.5)

    case_num = random.randint(100, 999)
    title = random.choice(DETECTIVE_INTROS).format(case=case_num, mention=user.mention)
    evidence = random.sample(DETECTIVE_EVIDENCE, k=3)
    verdict = random.choice(DETECTIVE_VERDICTS)

    embed = discord.Embed(title=title, color=discord.Color.dark_gold())
    embed.add_field(name="🔎 Evidence Found", value="\n".join(f"• {e}" for e in evidence), inline=False)
    embed.add_field(name="⚖️ Verdict", value=verdict, inline=False)
    add_points(interaction.guild.id, interaction.user.id, 3)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="points", description="Check your fun points.")
async def points_cmd(interaction: discord.Interaction):
    pts = get_points(interaction.guild.id, interaction.user.id)
    embed = discord.Embed(
        title="⭐ Your Fun Points",
        description=f"{interaction.user.mention}, you have **{pts}** points!",
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="leaderboard", description="Show the top fun-point earners in this server.")
async def leaderboard(interaction: discord.Interaction):
    rows = get_leaderboard(interaction.guild.id)
    if not rows:
        embed = discord.Embed(title="🏆 Leaderboard", description="No points yet. Go use some commands!", color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)
        return

    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (user_id, pts) in enumerate(rows):
        member = interaction.guild.get_member(user_id)
        name = member.display_name if member else f"User {user_id}"
        prefix = medals[i] if i < 3 else f"#{i+1}"
        lines.append(f"{prefix} **{name}** — {pts} pts")

    embed = discord.Embed(title="🏆 Fun Points Leaderboard", description="\n".join(lines), color=discord.Color.blurple())
    await interaction.response.send_message(embed=embed)


# ---- Admin commands ----
@bot.tree.command(name="setchannel", description="[Admin] Set the channel for random fun messages.")
@app_commands.describe(channel="Channel to send random fun messages in")
@app_commands.checks.has_permissions(administrator=True)
async def setchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    set_fun_channel(interaction.guild.id, channel.id)
    embed = discord.Embed(
        title="✅ Fun Channel Set",
        description=f"Random fun messages will now be sent in {channel.mention}.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="toggle", description="[Admin] Enable or disable a prank feature.")
@app_commands.describe(feature="Feature to toggle")
@app_commands.choices(feature=[app_commands.Choice(name=f, value=f) for f in ALL_FEATURES])
@app_commands.checks.has_permissions(administrator=True)
async def toggle(interaction: discord.Interaction, feature: app_commands.Choice[str]):
    now_enabled = toggle_feature(interaction.guild.id, feature.value)
    state = "✅ ENABLED" if now_enabled else "❌ DISABLED"
    embed = discord.Embed(
        title="⚙️ Feature Toggled",
        description=f"**{feature.value}** is now {state}.",
        color=discord.Color.green() if now_enabled else discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help", description="Show all available commands and features.")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Prank & Fun Bot — Help Menu",
        description="Here's everything I can do:",
        color=discord.Color.blurple()
    )
    embed.add_field(name="/roast @user", value="Send a friendly funny roast 🔥", inline=False)
    embed.add_field(name="/scan @user", value="Fake animated system scan 🖥️", inline=False)
    embed.add_field(name="/giveaway", value="Fake giveaway with countdown 🎉", inline=False)
    embed.add_field(name="/rank @user", value="Funny gamer profile stats 🎮", inline=False)
    embed.add_field(name="/detect @user", value="Funny detective report 🕵️", inline=False)
    embed.add_field(name="/points", value="Check your fun points ⭐", inline=False)
    embed.add_field(name="/leaderboard", value="Top point earners 🏆", inline=False)
    embed.add_field(name="/setchannel (admin)", value="Set random fun-message channel", inline=False)
    embed.add_field(name="/toggle (admin)", value="Enable/disable a feature", inline=False)
    embed.set_footer(text="All jokes are meant to be friendly — have fun! 😄")
    await interaction.response.send_message(embed=embed)


# ======================= 8. ERROR HANDLING =================================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏳ Slow down!",
            description=f"Try again in **{error.retry_after:.1f}s**.",
            color=discord.Color.red()
        )
    elif isinstance(error, app_commands.CheckFailure):
        embed = discord.Embed(
            title="🚫 Not allowed",
            description="This feature is disabled here, or you lack permission.",
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="⚠️ Something went wrong",
            description=f"`{error}`",
            color=discord.Color.red()
        )

    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ======================= 9. BACKGROUND TASK (random fun messages) ==========
@tasks.loop(minutes=30)
async def random_fun_loop():
    """Every 30 min, send a random fun message in each guild's fun channel
    (respects the 'randomfun' toggle and a basic cooldown)."""
    for guild in bot.guilds:
        if not is_feature_enabled(guild.id, "randomfun"):
            continue
        row = get_config(guild.id)
        channel_id = row[1]
        if not channel_id:
            continue
        channel = guild.get_channel(channel_id)
        if channel is None:
            continue
        try:
            await channel.send(random.choice(RANDOM_FUN_MESSAGES))
            update_last_fun_message(guild.id)
        except discord.HTTPException:
            pass


@random_fun_loop.before_loop
async def before_random_fun_loop():
    await bot.wait_until_ready()


# ======================= 10. STARTUP ========================================
@bot.event
async def on_ready():
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

    if not random_fun_loop.is_running():
        random_fun_loop.start()

    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")


# ======================= 11. RUN THE BOT =====================================
if __name__ == "__main__":
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise SystemExit("ERROR: Please paste your bot token into BOT_TOKEN at the top of this file.")
    bot.run(BOT_TOKEN)
