"""
=========================================================================
 DISCORD FUN & PRANK BOT — single file edition (bot.py)
=========================================================================
Install requirements first:
    pip install -U discord.py python-dotenv

Paste your bot token in the BOT_TOKEN variable below (Section 2) and run:
    python bot.py

Everything (slash commands, roast database, animations, buttons) lives
in this ONE file. No points/XP/leaderboard/economy system — pure fun
and harmless pranks. Comments mark each section.
=========================================================================
"""

# ======================= 1. IMPORTS =====================================
import random
import asyncio
import collections

import discord
from discord import app_commands
from discord.ext import commands

# ======================= 2. CONFIG / TOKEN =================================
# 👇 PASTE YOUR DISCORD BOT TOKEN HERE (only place you need to touch) 👇
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ======================= 3. ROAST DATABASE =================================
# {mention} gets replaced with the target user's mention at send-time.

ENGLISH_ROASTS = [
    "{mention} blames their RGB keyboard for every single loss 🎮",
    "{mention} blames their gaming chair for every single loss 🎮",
    "{mention} blames their gaming mouse for every single loss 🎮",
    "{mention} blames their headset for every single loss 🎮",
    "{mention} blames their pro controller for every single loss 🎮",
    "{mention} bought a RGB keyboard but still loses to bots 🎮",
    "{mention} bought a gaming chair but still loses to bots 🎮",
    "{mention} bought a gaming mouse but still loses to bots 🎮",
    "{mention} bought a headset but still loses to bots 🎮",
    "{mention} bought a pro controller but still loses to bots 🎮",
    "{mention} calls every loss 'unlucky' but it's really just Tuesday 📅",
    "{mention} calls it 'skill issue' but it's always their own issue 🤡",
    "{mention} celebrates a single kill like they won the World Cup 🏆",
    "{mention} gets carried harder than a broken skateboard 🚛",
    "{mention} gets carried harder than a rusty bicycle 🚛",
    "{mention} gets carried harder than a shopping cart 🚛",
    "{mention} gets carried harder than a shopping trolley 🚛",
    "{mention} gets outplayed by their own teammates constantly 🎮",
    "{mention} has a IQ that even an NPC would question 🤖",
    "{mention} has a aim that even an NPC would question 🤖",
    "{mention} has a attention span that even an NPC would question 🤖",
    "{mention} has a patience that even an NPC would question 🤖",
    "{mention} has a reaction time that even an NPC would question 🤖",
    "{mention} has a win rate that even an NPC would question 🤖",
    "{mention} has died to the same trap five times in a row 🪤",
    "{mention} has died to the same trap seven times in a row 🪤",
    "{mention} has died to the same trap ten times in a row 🪤",
    "{mention} has died to the same trap three times in a row 🪤",
    "{mention} has died to the same trap way too many times in a row 🪤",
    "{mention} has enough excuses to write a novel 📚",
    "{mention} has more respawns than actual kills ⚰️",
    "{mention} has rage-quit more matches than they've finished 🔥",
    "{mention} is the reason Minecraft added a surrender option 🏳️",
    "{mention} is the reason co-op mode added a surrender option 🏳️",
    "{mention} is the reason ranked mode added a surrender option 🏳️",
    "{mention} is the reason the arena added a surrender option 🏳️",
    "{mention} is the reason the lobby added a surrender option 🏳️",
    "{mention} keeps buying skins hoping it'll fix their aim 👕",
    "{mention} lags in real life, not just in Minecraft 🐢",
    "{mention} lags in real life, not just in co-op mode 🐢",
    "{mention} lags in real life, not just in ranked mode 🐢",
    "{mention} lags in real life, not just in the arena 🐢",
    "{mention} lags in real life, not just in the lobby 🐢",
    "{mention} lags in real life, not just in the server 🐢",
    "{mention} needs a tutorial for the tutorial 📖",
    "{mention} once blamed a cosmic ray for a loss in single player 🎮",
    "{mention} once blamed gravity for a loss in single player 🎮",
    "{mention} once blamed the Wi-Fi for a loss in single player 🎮",
    "{mention} once blamed their cat for a loss in single player 🎮",
    "{mention} once got beaten by the tutorial dummy 🥊",
    "{mention} panics harder against bots than real players 🤖",
    "{mention} plays like their controller is on airplane mode ✈️",
    "{mention} plays support because carrying requires actual skill 🛡️",
    "{mention} pressed alt+F4 thinking it was a healing spell 🔥",
    "{mention} pressed ctrl+alt+delete thinking it was a healing spell 🔥",
    "{mention} pressed the emote wheel thinking it was a healing spell 🔥",
    "{mention} pressed the panic button thinking it was a healing spell 🔥",
    "{mention} rage quits Tic-Tac-Toe 😤",
    "{mention} rage quits a chess app 😤",
    "{mention} rage quits a rock-paper-scissors match 😤",
    "{mention} rage quits a solo puzzle game 😤",
    "{mention} respawns faster than they can form a plan 🧠",
    "{mention} spent more on RGB keyboard than on improving their IQ 💸",
    "{mention} spent more on RGB keyboard than on improving their aim 💸",
    "{mention} spent more on gaming chair than on improving their IQ 💸",
    "{mention} spent more on gaming chair than on improving their aim 💸",
    "{mention} spent more on gaming chair than on improving their attention span 💸",
    "{mention} spent more on gaming chair than on improving their patience 💸",
    "{mention} spent more on gaming chair than on improving their reaction time 💸",
    "{mention} spent more on gaming mouse than on improving their IQ 💸",
    "{mention} spent more on gaming mouse than on improving their aim 💸",
    "{mention} spent more on gaming mouse than on improving their attention span 💸",
    "{mention} spent more on gaming mouse than on improving their reaction time 💸",
    "{mention} spent more on headset than on improving their IQ 💸",
    "{mention} spent more on headset than on improving their win rate 💸",
    "{mention} spent more on pro controller than on improving their IQ 💸",
    "{mention} spent more on pro controller than on improving their aim 💸",
    "{mention} spent more on pro controller than on improving their attention span 💸",
    "{mention} spent more on pro controller than on improving their reaction time 💸",
    "{mention} spent more on pro controller than on improving their win rate 💸",
    "{mention} still asks 'how do I jump' after five years of gaming ⌨️",
    "{mention} still asks 'how do I jump' after seven years of gaming ⌨️",
    "{mention} still asks 'how do I jump' after ten years of gaming ⌨️",
    "{mention} still asks 'how do I jump' after three years of gaming ⌨️",
    "{mention} still asks 'how do I jump' after way too many years of gaming ⌨️",
    "{mention} still can't find the settings menu after five years 🔧",
    "{mention} still can't find the settings menu after ten years 🔧",
    "{mention} still can't find the settings menu after three years 🔧",
    "{mention} still can't find the settings menu after way too many years 🔧",
    "{mention} still can't tell left click from right click 🖱️",
    "{mention} still doesn't know what bad luck means, and it shows 🤔",
    "{mention} still doesn't know what keyboard smashing means, and it shows 🤔",
    "{mention} still doesn't know what lag means, and it shows 🤔",
    "{mention} still doesn't know what noob energy means, and it shows 🤔",
    "{mention} still doesn't know what packet loss means, and it shows 🤔",
    "{mention} still doesn't know what skill issue means, and it shows 🤔",
    "{mention} still thinks bad luck is a flex 🍼",
    "{mention} still thinks keyboard smashing is a flex 🍼",
    "{mention} still thinks lag is a flex 🍼",
    "{mention} still thinks noob energy is a flex 🍼",
    "{mention} still thinks packet loss is a flex 🍼",
    "{mention} still thinks skill issue is a flex 🍼",
    "{mention} still uses the default keybinds after five years ⌨️",
    "{mention} still uses the default keybinds after seven years ⌨️",
    "{mention} still uses the default keybinds after ten years ⌨️",
    "{mention} still uses the default keybinds after three years ⌨️",
    "{mention} still uses the default keybinds after way too many years ⌨️",
    "{mention} thinks 'gg ez' counts as strategy talk 💬",
    "{mention} thinks 'meta' means their mom's name 😅",
    "{mention} thinks Minecraft lag is a government conspiracy 🕵️",
    "{mention} thinks bad luck is a personality trait 🙃",
    "{mention} thinks camping is a valid life philosophy 🏕️",
    "{mention} thinks co-op mode lag is a government conspiracy 🕵️",
    "{mention} thinks keyboard smashing is a personality trait 🙃",
    "{mention} thinks lag is a personality trait 🙃",
    "{mention} thinks noob energy is a personality trait 🙃",
    "{mention} thinks packet loss is a personality trait 🙃",
    "{mention} thinks patience is optional and it's very obvious 😑",
    "{mention} thinks pressing buttons randomly counts as a combo 🎮",
    "{mention} thinks ranked mode lag is a government conspiracy 🕵️",
    "{mention} thinks skill issue is a personality trait 🙃",
    "{mention} thinks the lobby lag is a government conspiracy 🕵️",
    "{mention} thinks the server lag is a government conspiracy 🕵️",
    "{mention} treats every 'GG' like a participation trophy 🏆",
    "{mention} treats every game like it owes them a win 🏅",
    "{mention} treats every match like a horror movie audition 😱",
    "{mention} would get lost in a straight hallway 🧭",
    "{mention} would get outsmarted by a loading screen 🔄",
    "{mention} would lose a staring contest with an NPC 👀",
    "{mention}'s K/D ratio is lower than their IQ 💀",
    "{mention}'s K/D ratio is lower than their aim 💀",
    "{mention}'s K/D ratio is lower than their attention span 💀",
    "{mention}'s K/D ratio is lower than their patience 💀",
    "{mention}'s K/D ratio is lower than their reaction time 💀",
    "{mention}'s K/D ratio is lower than their win rate 💀",
    "{mention}'s Wi-Fi is faster than their IQ, barely 📶",
    "{mention}'s Wi-Fi is faster than their aim, barely 📶",
    "{mention}'s Wi-Fi is faster than their attention span, barely 📶",
    "{mention}'s Wi-Fi is faster than their patience, barely 📶",
    "{mention}'s Wi-Fi is faster than their reaction time, barely 📶",
    "{mention}'s Wi-Fi is faster than their win rate, barely 📶",
    "{mention}'s aim wobbles more than a Jenga tower 🗼",
    "{mention}'s comeback game is nonexistent, only the L stays 📉",
    "{mention}'s crosshair has seen more misses than a dating app 🎯",
    "{mention}'s gameplay is 90% panic and 10% skill 🎢",
    "{mention}'s highlight reel is just a compilation of fails 🎬",
    "{mention}'s inventory is 90% junk and 10% regret 🎒",
    "{mention}'s loot luck is worse than opening a mystery box full of rocks 📦",
    "{mention}'s mic is louder than their actual gameplay 🎤",
    "{mention}'s reaction time is measured in geological eras 🦖",
    "{mention}'s sensitivity settings are set to 'motion sickness' 🌀",
    "{mention}'s strategy is just vibes and prayer 🙏",
    "{mention}'s teammates mute them out of self-preservation 🔇",
    "{mention}'s teamwork skills peaked in kindergarten 🧸",
    "{mention}, your aim is so bad that even the NPC guide filed a complaint 😂",
    "{mention}, your aim is so bad that even the aim assist filed a complaint 😂",
    "{mention}, your aim is so bad that even the crosshair filed a complaint 😂",
    "{mention}, your aim is so bad that even the loading screen filed a complaint 😂",
    "{mention}, your aim is so bad that even the practice range filed a complaint 😂",
    "{mention}, your aim is so bad that even the tutorial filed a complaint 😂",]

HINGLISH_ROASTS = [
    "Are {mention}, tera aim dekh ke coach bhi retirement le le 🎓",
    "Are {mention}, teri aim dekh ke lagta hai target invisible mode mein tha 👻",
    "Are {mention}, teri aim se accurate toh coin flip hota hai 🪙",
    "Are {mention}, teri gameplay dekh ke tutorial bhi 'skip' bolta hai ⏭️",
    "Are {mention}, teri gameplay se zyada funny toh comedy show hai 🎭",
    "Are {mention}, teri gaming career sirf loading screen tak hi sahi lagti hai 🔄",
    "Are {mention}, teri patience dekh ke lagta hai timer already khatam ho gaya ⏰",
    "Are {mention}, teri skill dekh ke bot bhi apna resume update kar le 📄",
    "Are {mention}, teri skill dekh ke leaderboard bhi last place reserve kar de 🏁",
    "Are {mention}, teri strategy sirf 'bhaag ke chhup ja' hoti hai 🏃",
    "Are {mention}, teri team har match mein tujhe carry karke thak jaati hai 🚛",
    "Are {mention}, tu har baar wahi galti karta hai jaise memory reset ho gayi ho 🔁",
    "Are {mention}, tu har round mein excuse ka naya version launch karta hai 🚀",
    "Are {mention}, tu itna carried hota hai ki khud ko hero samajhta hai 🦸",
    "Are {mention}, tu itna confuse hota hai ki minimap bhi bhatak jaata hai 🗺️",
    "Are {mention}, tu itna lag karta hai ki server bhi tujhe reset kar de 🔌",
    "Are {mention}, tu itna miss karta hai ki bullets bhi tere se bachti hain 🔫",
    "Are {mention}, tu itna panic karta hai ki simple match bhi thriller movie lagta hai 🎬",
    "Are {mention}, tu itna slow hai ki NPC bhi tujhse fast react karta hai 🤖",
    "Are {mention}, tu itni baar hara hai ki scoreboard bhi tujhe pehchan gaya hai 📊",
    "Arre {mention}, tera aim dekh ke coach bhi retirement le le 🎓",
    "Arre {mention}, teri aim dekh ke lagta hai target invisible mode mein tha 👻",
    "Arre {mention}, teri aim se accurate toh coin flip hota hai 🪙",
    "Arre {mention}, teri gameplay dekh ke tutorial bhi 'skip' bolta hai ⏭️",
    "Arre {mention}, teri gameplay se zyada funny toh comedy show hai 🎭",
    "Arre {mention}, teri gaming career sirf loading screen tak hi sahi lagti hai 🔄",
    "Arre {mention}, teri patience dekh ke lagta hai timer already khatam ho gaya ⏰",
    "Arre {mention}, teri skill dekh ke bot bhi apna resume update kar le 📄",
    "Arre {mention}, teri skill dekh ke leaderboard bhi last place reserve kar de 🏁",
    "Arre {mention}, teri strategy sirf 'bhaag ke chhup ja' hoti hai 🏃",
    "Arre {mention}, teri team har match mein tujhe carry karke thak jaati hai 🚛",
    "Arre {mention}, tu har baar wahi galti karta hai jaise memory reset ho gayi ho 🔁",
    "Arre {mention}, tu har round mein excuse ka naya version launch karta hai 🚀",
    "Arre {mention}, tu itna carried hota hai ki khud ko hero samajhta hai 🦸",
    "Arre {mention}, tu itna confuse hota hai ki minimap bhi bhatak jaata hai 🗺️",
    "Arre {mention}, tu itna lag karta hai ki server bhi tujhe reset kar de 🔌",
    "Arre {mention}, tu itna miss karta hai ki bullets bhi tere se bachti hain 🔫",
    "Arre {mention}, tu itna panic karta hai ki simple match bhi thriller movie lagta hai 🎬",
    "Arre {mention}, tu itna slow hai ki NPC bhi tujhse fast react karta hai 🤖",
    "Arre {mention}, tu itni baar hara hai ki scoreboard bhi tujhe pehchan gaya hai 📊",
    "Dekho {mention}, tera aim dekh ke coach bhi retirement le le 🎓",
    "Dekho {mention}, teri aim dekh ke lagta hai target invisible mode mein tha 👻",
    "Dekho {mention}, teri aim se accurate toh coin flip hota hai 🪙",
    "Dekho {mention}, teri gameplay dekh ke tutorial bhi 'skip' bolta hai ⏭️",
    "Dekho {mention}, teri gameplay se zyada funny toh comedy show hai 🎭",
    "Dekho {mention}, teri gaming career sirf loading screen tak hi sahi lagti hai 🔄",
    "Dekho {mention}, teri patience dekh ke lagta hai timer already khatam ho gaya ⏰",
    "Dekho {mention}, teri skill dekh ke bot bhi apna resume update kar le 📄",
    "Dekho {mention}, teri skill dekh ke leaderboard bhi last place reserve kar de 🏁",
    "Dekho {mention}, teri strategy sirf 'bhaag ke chhup ja' hoti hai 🏃",
    "Dekho {mention}, teri team har match mein tujhe carry karke thak jaati hai 🚛",
    "Dekho {mention}, tu har baar wahi galti karta hai jaise memory reset ho gayi ho 🔁",
    "Dekho {mention}, tu har round mein excuse ka naya version launch karta hai 🚀",
    "Dekho {mention}, tu itna carried hota hai ki khud ko hero samajhta hai 🦸",
    "Dekho {mention}, tu itna confuse hota hai ki minimap bhi bhatak jaata hai 🗺️",
    "Dekho {mention}, tu itna lag karta hai ki server bhi tujhe reset kar de 🔌",
    "Dekho {mention}, tu itna miss karta hai ki bullets bhi tere se bachti hain 🔫",
    "Dekho {mention}, tu itna panic karta hai ki simple match bhi thriller movie lagta hai 🎬",
    "Dekho {mention}, tu itna slow hai ki NPC bhi tujhse fast react karta hai 🤖",
    "Dekho {mention}, tu itni baar hara hai ki scoreboard bhi tujhe pehchan gaya hai 📊",
    "Sun {mention}, tera aim dekh ke coach bhi retirement le le 🎓",
    "Sun {mention}, teri aim dekh ke lagta hai target invisible mode mein tha 👻",
    "Sun {mention}, teri aim se accurate toh coin flip hota hai 🪙",
    "Sun {mention}, teri gameplay dekh ke tutorial bhi 'skip' bolta hai ⏭️",
    "Sun {mention}, teri gameplay se zyada funny toh comedy show hai 🎭",
    "Sun {mention}, teri gaming career sirf loading screen tak hi sahi lagti hai 🔄",
    "Sun {mention}, teri patience dekh ke lagta hai timer already khatam ho gaya ⏰",
    "Sun {mention}, teri skill dekh ke bot bhi apna resume update kar le 📄",
    "Sun {mention}, teri skill dekh ke leaderboard bhi last place reserve kar de 🏁",
    "Sun {mention}, teri strategy sirf 'bhaag ke chhup ja' hoti hai 🏃",
    "Sun {mention}, teri team har match mein tujhe carry karke thak jaati hai 🚛",
    "Sun {mention}, tu har baar wahi galti karta hai jaise memory reset ho gayi ho 🔁",
    "Sun {mention}, tu har round mein excuse ka naya version launch karta hai 🚀",
    "Sun {mention}, tu itna carried hota hai ki khud ko hero samajhta hai 🦸",
    "Sun {mention}, tu itna confuse hota hai ki minimap bhi bhatak jaata hai 🗺️",
    "Sun {mention}, tu itna lag karta hai ki server bhi tujhe reset kar de 🔌",
    "Sun {mention}, tu itna miss karta hai ki bullets bhi tere se bachti hain 🔫",
    "Sun {mention}, tu itna panic karta hai ki simple match bhi thriller movie lagta hai 🎬",
    "Sun {mention}, tu itna slow hai ki NPC bhi tujhse fast react karta hai 🤖",
    "Sun {mention}, tu itni baar hara hai ki scoreboard bhi tujhe pehchan gaya hai 📊",
    "{mention} bhai har round mein naya bahana leke aata hai 🎭",
    "{mention} bhai itna carry hota hai, khud ko MVP samajhta hai 🚛",
    "{mention} bhai itna confuse hota hai ki left-click bhi bhool jaata hai 🖱️",
    "{mention} bhai itna panic karta hai ki bot bhi shant ho jaaye 😱",
    "{mention} bhai itna panic mode mein rehta hai ki simple game bhi horror ban jaaye 😱",
    "{mention} bhai itna slow khelta hai ki loading screen bhi bore ho jaaye 🔄",
    "{mention} bhai itni baar hara hai ki leaderboard bhi tang aa gaya 🏆",
    "{mention} bhai keyboard smash karke bhi combo nahi ban paata 🎮",
    "{mention} bhai suno, tera aim dekh ke coach bhi retirement le le 🎓",
    "{mention} bhai suno, teri aim dekh ke lagta hai target invisible mode mein tha 👻",
    "{mention} bhai suno, teri aim se accurate toh coin flip hota hai 🪙",
    "{mention} bhai suno, teri gameplay dekh ke tutorial bhi 'skip' bolta hai ⏭️",
    "{mention} bhai suno, teri gameplay se zyada funny toh comedy show hai 🎭",
    "{mention} bhai suno, teri gaming career sirf loading screen tak hi sahi lagti hai 🔄",
    "{mention} bhai suno, teri patience dekh ke lagta hai timer already khatam ho gaya ⏰",
    "{mention} bhai suno, teri skill dekh ke bot bhi apna resume update kar le 📄",
    "{mention} bhai suno, teri skill dekh ke leaderboard bhi last place reserve kar de 🏁",
    "{mention} bhai suno, teri strategy sirf 'bhaag ke chhup ja' hoti hai 🏃",
    "{mention} bhai suno, teri team har match mein tujhe carry karke thak jaati hai 🚛",
    "{mention} bhai suno, tu har baar wahi galti karta hai jaise memory reset ho gayi ho 🔁",
    "{mention} bhai suno, tu har round mein excuse ka naya version launch karta hai 🚀",
    "{mention} bhai suno, tu itna carried hota hai ki khud ko hero samajhta hai 🦸",
    "{mention} bhai suno, tu itna confuse hota hai ki minimap bhi bhatak jaata hai 🗺️",
    "{mention} bhai suno, tu itna lag karta hai ki server bhi tujhe reset kar de 🔌",
    "{mention} bhai suno, tu itna miss karta hai ki bullets bhi tere se bachti hain 🔫",
    "{mention} bhai suno, tu itna panic karta hai ki simple match bhi thriller movie lagta hai 🎬",
    "{mention} bhai suno, tu itna slow hai ki NPC bhi tujhse fast react karta hai 🤖",
    "{mention} bhai suno, tu itni baar hara hai ki scoreboard bhi tujhe pehchan gaya hai 📊",
    "{mention} bhai teri aim dekh ke crosshair bhi therapy le raha hai 🧘",
    "{mention} bhai teri aim itni kharab hai ki bullets bhi maafi maang rahi hain 🔫",
    "{mention} bhai teri aim se zyada accurate toh random guess hota hai 🎯",
    "{mention} bhai teri gameplay dekh ke coach bhi resign de de 🎓",
    "{mention} bhai teri gameplay dekh ke highlight reel sirf fails ka bana 🎬",
    "{mention} bhai teri gameplay se zyada entertaining toh loading screen hai 🔄",
    "{mention} bhai teri patience dekh ke lagta hai already alt+F4 kar diya 🔥",
    "{mention} bhai teri patience dekh ke lagta hai already game chhod diya 😑",
    "{mention} bhai teri sensitivity settings 'chakkar' pe set hain 🌀",
    "{mention} bhai teri skill dekh ke tutorial dummy bhi jeet jaaye 🥊",
    "{mention} bhai teri strategy sirf 'ram bharose' chal rahi hai 🙏",
    "{mention} bhai teri team bhi silent treatment de rahi hai 🔇",
    "{mention} bhai {gear} le liya par skill wahi purani wali hai 🎮",
    "{mention} bhai, tera aim dekh ke crosshair bhi resign de raha hai 😂",
    "{mention} har baar 'gg ez' bolta hai par khud hi ez hota hai 😂",
    "{mention} har baar 'lag tha' bolta hai, par lag toh sirf uske dimaag mein hai 🧠",
    "{mention} har baar 'network slow hai' bolta hai, par router bhi tang aa gaya 📡",
    "{mention} har baar excuse deta hai, par excuse bhi thak gaye ab 😩",
    "{mention} har baar naya gear khareedta hai, skill wahi purani 💸",
    "{mention} har baar naye rank ka sapna dekhta hai, reality mein bronze hi hai 🥉",
    "{mention} har baar wahi mistake repeat karta hai, loop mein fasa hai 🔁",
    "{mention} har haar ko 'unlucky' bolta hai, sach mein Monday hai bas 📅",
    "{mention} har loss ke baad naya excuse layer karta hai, writer ban sakta hai 📚",
    "{mention} har match ke baad naya drama create karta hai 🎬",
    "{mention} har match mein 'main toh carry kar raha tha' bolta hai, sach mein carried ho raha tha 🚛",
    "{mention} har match mein 'network issue' bolta hai, sach mein skill issue hai 📶",
    "{mention} har match mein 'ye toh unfair tha' bolta hai, par skill hi nahi hai 😅",
    "{mention} har round mein naya excuse invent karta hai, patent le lena chahiye 📝",
    "{mention} ka aim assist bhi haar maan chuka hai 🎮",
    "{mention} ka aim dekh ke game bhi soch mein pad jaata hai 🤔",
    "{mention} ka aim dekh ke lagta hai target khud bhaag gaya 🏃",
    "{mention} ka aim itna off hai ki bots bhi hasne lagte hain 🤣",
    "{mention} ka aim itna wobble karta hai jaise Jenga tower gir raha ho 🗼",
    "{mention} ka attention span dekh ke NPC bhi confuse ho jaaye 🤖",
    "{mention} ka comeback game zero hai, sirf L milta hai 📉",
    "{mention} ka dimaag aur ping dono hi slow chalte hain 🐌",
    "{mention} ka game sense dekh ke bot bhi upgrade maang le 🤖",
    "{mention} ka game sense dekh ke lagta hai tutorial bhi confuse ho gaya 📖",
    "{mention} ka game sense itna weak hai, GPS bhi confuse ho jaaye 🧭",
    "{mention} ka gameplay 90% panic aur 10% luck hai 🎢",
    "{mention} ka inventory 90% kachra, 10% regret hai 🎒",
    "{mention} ka mic gameplay se zyada loud hai 🎤",
    "{mention} ka packet loss dekh ke poori team mute kar deti hai 🔇",
    "{mention} ka reaction dekh ke lagta hai sloth se race lagayi ho 🦥",
    "{mention} ka reaction time dekh ke lagta hai time hi ruk gaya ⏳",
    "{mention} ka reaction time dekh ke lagta hai time travel kar raha ho ⏱️",
    "{mention} ka skill level dekh ke NPC bhi promotion maang le 🤖",
    "{mention} ka support role sirf isliye hai kyunki carry karna aata nahi 🛡️",
    "{mention} ki skill dekh ke lagta hai settings menu bhi bhaag gaya 🔧",
    "{mention} ne itni baar respawn liya, ab game usko regular customer maanta hai ⚰️",
    "{mention} ne itni baar trap mein gir ke record banaya hai 🪤",
    "{mention}, tu itna lag karta hai ki Minecraft bhi thak gaya wait karke 🐢",]

print(f"Loaded {len(ENGLISH_ROASTS)} English roasts and {len(HINGLISH_ROASTS)} Hinglish roasts.")


# ======================= 4. ANTI-REPEAT LOGIC ===============================
# Keeps track of recently used roast indexes per language so the same
# roast doesn't repeat too often. Resets automatically once most roasts
# have been used.

recent_english = collections.deque(maxlen=40)
recent_hinglish = collections.deque(maxlen=40)


def pick_roast(language: str) -> str:
    """Pick a roast, avoiding recently used ones. No database needed —
    everything lives in memory for the bot's runtime."""
    if language == "english":
        pool = ENGLISH_ROASTS
        recent = recent_english
    else:
        pool = HINGLISH_ROASTS
        recent = recent_hinglish

    # If we've used up most of the list, reset history automatically
    if len(recent) >= len(pool) - 10:
        recent.clear()

    available = [r for r in pool if r not in recent]
    if not available:
        recent.clear()
        available = pool

    choice = random.choice(available)
    recent.append(choice)
    return choice


# ======================= 5. FUN CONTENT (other commands) ====================
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

GIVEAWAY_PRIZES = [
    "a lifetime supply of bad luck 🍀",
    "1 (one) participation trophy 🏆",
    "an invisible skin nobody can see 👻",
    "a virtual high-five ✋",
    "bragging rights (unverified) 🗣️",
]

IQ_RESULTS = [
    "Gamer IQ: -12. Somehow still positive vibes. 🧠",
    "Gamer IQ: 404 — Not Found. 🔍",
    "Gamer IQ: Potato-tier, but a lovable potato. 🥔",
    "Gamer IQ: Off the charts... in the wrong direction. 📉",
    "Gamer IQ: Certified genius at losing. 🎓",
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

HACK_LINES = [
    "> Bypassing firewall...",
    "> Accessing mainframe...",
    "> Decrypting noob.exe...",
    "> Uploading skill.dll...",
    "> ERROR: Skill not found.",
]

SKILL_RESULTS = [
    "Skill Analysis: Button masher extraordinaire. 🎮",
    "Skill Analysis: 1% skill, 99% confidence. 💪",
    "Skill Analysis: Plays like a tutorial NPC. 🤖",
    "Skill Analysis: Surprisingly bad for someone this confident. 😅",
]

ACHIEVEMENTS = [
    "🏆 'Died to the Tutorial' — Unlocked!",
    "🏆 'Rage Quit Champion' — Unlocked!",
    "🏆 '0 Kills, 10 Deaths' — Unlocked!",
    "🏆 'Blamed the Wi-Fi' — Unlocked!",
    "🏆 'Carried by Teammates' — Unlocked!",
]

LOADING_END_MESSAGES = [
    "Loading complete! Skill still not found. 😂",
    "Loading complete! Please insert actual talent. 🎮",
    "Loading complete! Results may vary (they won't). 📉",
]

BANCHECK_RESULTS = [
    "🚨 SCANNING FOR BAD BEHAVIOR...",
    "🚨 CHECKING TRASH TALK LEVELS...",
    "🚨 ANALYZING RAGE QUIT HISTORY...",
]

MOOD_RESULTS = [
    "Mood: Salty like the Dead Sea. 🧂",
    "Mood: 100% chaotic gremlin energy. 👹",
    "Mood: Suspiciously calm before a rage quit. 😌",
    "Mood: Powered entirely by energy drinks. ⚡",
]

UPDATE_LINES = [
    "📦 Downloading new friendship patch...",
    "📦 Installing 'less toxic' update...",
    "📦 Applying skill.exe hotfix...",
]

FUTURE_PREDICTIONS = [
    "In 5 years, you'll still be blaming lag. 🔮",
    "Your future holds one (1) victory royale, eventually. 🏆",
    "You are destined to be carried forever. 🚛",
    "Greatness awaits... just not in this game. 😂",
]

CHALLENGES = [
    "Challenge: Say 'gg' without being sarcastic. 😂",
    "Challenge: Go one game without blaming lag. 🎮",
    "Challenge: Win a match without rage quitting. 🏆",
    "Challenge: Compliment a teammate unprompted. 🤝",
]

MEMES = [
    "When you say 'one more game' for the 47th time. 😂",
    "That feeling when your teammate goes AFK mid-fight. 💀",
    "POV: You blame lag but your ping is 12ms. 🎮",
]

VIRUS_LINES = [
    "🦠 Scanning for cringe.exe...",
    "🦠 Checking for noob.dll infections...",
    "🦠 Quarantining bad vibes...",
]

COMPATIBILITY_LINES = [
    "You two would carry each other into the abyss. 😂",
    "Compatibility: Chaotic but weirdly wholesome. 🤝",
    "Compatibility: One rage quits, the other laughs. 💯",
]

NPC_LINES = [
    "Dialogue: 'I used to be a gamer like you, then I took an L to the knee.'",
    "Dialogue: 'Have you seen my skill? I lost it around here somewhere.'",
    "Dialogue: 'Welcome, traveler. Your Wi-Fi looks weak today.'",
]

BOSSFIGHT_LINES = [
    "The boss laughs at your build. 😂",
    "You dealt 1 damage. The boss is unimpressed. 🗡️",
    "Critical fail! You tripped over your own feet. 💀",
]

BOX_RESULTS = [
    "You got: A rusty spoon. 🥄",
    "You got: Absolutely nothing. 📦",
    "You got: Bragging rights (fake). 🏆",
    "You got: A single pixel of confidence. ✨",
]

REACT_PROMPTS = [
    "React with 😂 if you've ever rage quit!",
    "React with 🎮 if you blame lag every time!",
    "React with 💀 if your K/D is embarrassing!",
]

DAILY_JOKES = [
    "Why did the gamer bring a ladder? To reach the next level. 🪜",
    "Why don't skeletons play video games? They don't have the guts. 💀",
    "My aim is so bad, I could miss a broad side of a barn from inside it. 🎯",
]

FORTUNE_LINES = [
    "Fortune: A great win awaits... in your dreams only. 🔮",
    "Fortune: Beware of teammates bearing bad advice. ⚠️",
    "Fortune: Your luck stat is currently on vacation. 🏖️",
]

PROFILE_TITLES = [
    "Certified Button Masher",
    "Professional Rage Quitter",
    "NPC-Tier Gamer",
    "Wi-Fi Blamer Extraordinaire",
]


def stat():
    return random.randint(0, 100)


# ======================= 6. UI COMPONENTS (Buttons) =========================
class RoastAgainView(discord.ui.View):
    """Button that re-rolls a roast for the same target/language."""
    def __init__(self, target: discord.Member, language: str):
        super().__init__(timeout=60)
        self.target = target
        self.language = language

    @discord.ui.button(label="Roast Again 🔥", style=discord.ButtonStyle.danger)
    async def roast_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        line = pick_roast(self.language).format(mention=self.target.mention)
        embed = discord.Embed(title="🔥 Roast Delivered", description=line, color=discord.Color.orange())
        embed.set_footer(text=f"Language: {self.language.title()}")
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


class RandomPrankSelect(discord.ui.View):
    """Used by /randomprank — just a placeholder confirm view if needed later."""
    pass


# ======================= 7. SLASH COMMANDS — ROAST SYSTEM ===================

@bot.tree.command(name="roast", description="Send a savage but friendly roast to a user.")
@app_commands.describe(user="The user to roast", language="Choose roast language")
@app_commands.choices(language=[
    app_commands.Choice(name="English 🇺🇸", value="english"),
    app_commands.Choice(name="Hinglish 🇮🇳", value="hinglish"),
])
@app_commands.checks.cooldown(1, 6.0)
async def roast(interaction: discord.Interaction, user: discord.Member, language: app_commands.Choice[str]):
    async with interaction.channel.typing():
        await asyncio.sleep(1.0)
    line = pick_roast(language.value).format(mention=user.mention)
    embed = discord.Embed(title="🔥 Roast Delivered", description=line, color=discord.Color.orange())
    embed.set_footer(text=f"Language: {language.name} | Requested by {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, view=RoastAgainView(user, language.value))


@bot.tree.command(name="roastcount", description="Show how many roasts are loaded in the bot.")
async def roastcount(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Roast Database Stats",
        color=discord.Color.blurple()
    )
    embed.add_field(name="English Roasts 🇺🇸", value=f"{len(ENGLISH_ROASTS)}+", inline=True)
    embed.add_field(name="Hinglish Roasts 🇮🇳", value=f"{len(HINGLISH_ROASTS)}+", inline=True)
    embed.add_field(name="Total Roasts 🔥", value=f"{len(ENGLISH_ROASTS) + len(HINGLISH_ROASTS)}+", inline=False)
    await interaction.response.send_message(embed=embed)


# ======================= 8. SLASH COMMANDS — ANIMATED PRANKS ================

@bot.tree.command(name="scan", description="Run a fake 'gamer skill scan' on a user.")
@app_commands.describe(user="The user to scan")
@app_commands.checks.cooldown(1, 10.0)
async def scan(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        embed = discord.Embed(title="🖥️ Gamer Scan", description=SCAN_STEPS[0], color=discord.Color.blue())
        msg = await interaction.followup.send(embed=embed)
        for step in SCAN_STEPS[1:]:
            await asyncio.sleep(1.2)
            embed = discord.Embed(title="🖥️ Gamer Scan", description=step, color=discord.Color.blue())
            await msg.edit(embed=embed)
        await asyncio.sleep(1.2)
        result = random.choice(SCAN_RESULTS)
        final = discord.Embed(title="✅ Scan Complete", description=f"**Target:** {user.mention}\n\n{result}", color=discord.Color.green())
        await msg.edit(embed=final)


@bot.tree.command(name="giveaway", description="Start a fake giveaway with a countdown and winner pick.")
@app_commands.checks.cooldown(1, 15.0)
async def giveaway(interaction: discord.Interaction):
    view = GiveawayView()
    prize = random.choice(GIVEAWAY_PRIZES)
    embed = discord.Embed(
        title="🎉 GIVEAWAY TIME! 🎉",
        description=f"Prize: **{prize}**\nClick the button below to join!\n\n⏳ Ends in 15 seconds...",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, view=view)
    msg = await interaction.original_response()

    for seconds_left in (10, 5, 3, 1):
        await asyncio.sleep(3)
        embed.description = f"Prize: **{prize}**\nClick the button below to join!\n\n⏳ {seconds_left} seconds left..."
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
    else:
        result_text = "😂 Nobody joined... the bot wins by default. Sad."

    final_embed = discord.Embed(title="🏁 Giveaway Ended!", description=result_text, color=discord.Color.purple())
    await msg.edit(embed=final_embed, view=None)


@bot.tree.command(name="iq", description="Reveal a user's totally scientific gamer IQ.")
@app_commands.describe(user="The user to test")
@app_commands.checks.cooldown(1, 8.0)
async def iq(interaction: discord.Interaction, user: discord.Member):
    async with interaction.channel.typing():
        await asyncio.sleep(1)
    embed = discord.Embed(title="🧠 Gamer IQ Test", description=f"**{user.display_name}**\n\n{random.choice(IQ_RESULTS)}", color=discord.Color.teal())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="detect", description="Run a funny investigation report on a user.")
@app_commands.describe(user="The user to investigate")
@app_commands.checks.cooldown(1, 10.0)
async def detect(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        await asyncio.sleep(1.5)
    case_num = random.randint(100, 999)
    evidence = random.sample(DETECTIVE_EVIDENCE, k=3)
    verdict = random.choice(DETECTIVE_VERDICTS)
    embed = discord.Embed(title=f"🕵️ Case File #{case_num}: {user.display_name}", color=discord.Color.dark_gold())
    embed.add_field(name="🔎 Evidence Found", value="\n".join(f"• {e}" for e in evidence), inline=False)
    embed.add_field(name="⚖️ Verdict", value=verdict, inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="hack", description="Fictional movie-style 'hacker screen' prank. Not real hacking.")
@app_commands.describe(user="The user to 'hack' (just for laughs)")
@app_commands.checks.cooldown(1, 10.0)
async def hack(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        embed = discord.Embed(title="💻 Hacking Simulation (Fictional)", description=HACK_LINES[0], color=discord.Color.dark_green())
        msg = await interaction.followup.send(embed=embed)
        for line in HACK_LINES[1:]:
            await asyncio.sleep(1)
            embed = discord.Embed(title="💻 Hacking Simulation (Fictional)", description=line, color=discord.Color.dark_green())
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        final = discord.Embed(
            title="😂 Just Kidding!",
            description=f"This was 100% fake — no real hacking happened. {user.mention}'s account is completely safe (and so is their bad aim). 🎮",
            color=discord.Color.green()
        )
        await msg.edit(embed=final)


@bot.tree.command(name="skill", description="Run a fake gaming skill analysis on a user.")
@app_commands.describe(user="The user to analyze")
@app_commands.checks.cooldown(1, 8.0)
async def skill(interaction: discord.Interaction, user: discord.Member):
    async with interaction.channel.typing():
        await asyncio.sleep(1)
    embed = discord.Embed(title="🎯 Skill Analysis", description=f"**{user.display_name}**\n\n{random.choice(SKILL_RESULTS)}", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="achievement", description="Unlock a random funny achievement for a user.")
@app_commands.describe(user="The user to award")
@app_commands.checks.cooldown(1, 8.0)
async def achievement(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="🏆 Achievement Unlocked!", description=f"{user.mention}\n\n{random.choice(ACHIEVEMENTS)}", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="load", description="Loading animation from 0% to 100%.")
@app_commands.checks.cooldown(1, 10.0)
async def load(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="⏳ Loading...", description="`[░░░░░░░░░░] 0%`", color=discord.Color.blue())
    msg = await interaction.followup.send(embed=embed)
    for pct in (20, 40, 60, 80, 100):
        await asyncio.sleep(0.8)
        filled = "█" * (pct // 10)
        empty = "░" * (10 - pct // 10)
        embed = discord.Embed(title="⏳ Loading...", description=f"`[{filled}{empty}] {pct}%`", color=discord.Color.blue())
        await msg.edit(embed=embed)
    await asyncio.sleep(0.5)
    final = discord.Embed(title="✅ Done!", description=random.choice(LOADING_END_MESSAGES), color=discord.Color.green())
    await msg.edit(embed=final)


@bot.tree.command(name="bancheck", description="Fake ban warning animation (just a prank).")
@app_commands.describe(user="The user to check")
@app_commands.checks.cooldown(1, 10.0)
async def bancheck(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        embed = discord.Embed(title="🚨 Ban Check", description=BANCHECK_RESULTS[0], color=discord.Color.red())
        msg = await interaction.followup.send(embed=embed)
        for line in BANCHECK_RESULTS[1:]:
            await asyncio.sleep(1)
            embed = discord.Embed(title="🚨 Ban Check", description=line, color=discord.Color.red())
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        final = discord.Embed(
            title="😂 Relax, It's a Prank!",
            description=f"{user.mention} is 100% safe. This was just for laughs — no real ban check happened. 🎮",
            color=discord.Color.green()
        )
        await msg.edit(embed=final)


@bot.tree.command(name="mood", description="Scan a user's current gamer mood.")
@app_commands.describe(user="The user to scan")
@app_commands.checks.cooldown(1, 8.0)
async def mood(interaction: discord.Interaction, user: discord.Member):
    async with interaction.channel.typing():
        await asyncio.sleep(1)
    embed = discord.Embed(title="🎭 Mood Scanner", description=f"**{user.display_name}**\n\n{random.choice(MOOD_RESULTS)}", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="update", description="Fake friendship/gamer update animation.")
@app_commands.checks.cooldown(1, 10.0)
async def update(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="📦 System Update", description=UPDATE_LINES[0], color=discord.Color.blue())
    msg = await interaction.followup.send(embed=embed)
    for line in UPDATE_LINES[1:]:
        await asyncio.sleep(1)
        embed = discord.Embed(title="📦 System Update", description=line, color=discord.Color.blue())
        await msg.edit(embed=embed)
    await asyncio.sleep(1)
    final = discord.Embed(title="✅ Update Complete", description="Friendship level increased by +1! 🤝", color=discord.Color.green())
    await msg.edit(embed=final)


@bot.tree.command(name="future", description="Predict a user's funny gaming future.")
@app_commands.describe(user="The user to predict for")
@app_commands.checks.cooldown(1, 8.0)
async def future(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="🔮 Gaming Future", description=f"{user.mention}\n\n{random.choice(FUTURE_PREDICTIONS)}", color=discord.Color.dark_purple())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="challenge", description="Get a random harmless funny challenge.")
@app_commands.checks.cooldown(1, 6.0)
async def challenge(interaction: discord.Interaction):
    embed = discord.Embed(title="🎯 Random Challenge", description=random.choice(CHALLENGES), color=discord.Color.orange())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="meme", description="Send a random meme-style message.")
@app_commands.checks.cooldown(1, 6.0)
async def meme(interaction: discord.Interaction):
    embed = discord.Embed(title="😂 Random Meme", description=random.choice(MEMES), color=discord.Color.magenta())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="viruscheck", description="Fake movie-style virus scan (not a real scan).")
@app_commands.describe(user="The user to check")
@app_commands.checks.cooldown(1, 10.0)
async def viruscheck(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    async with interaction.channel.typing():
        embed = discord.Embed(title="🦠 Virus Scan (Fictional)", description=VIRUS_LINES[0], color=discord.Color.dark_red())
        msg = await interaction.followup.send(embed=embed)
        for line in VIRUS_LINES[1:]:
            await asyncio.sleep(1)
            embed = discord.Embed(title="🦠 Virus Scan (Fictional)", description=line, color=discord.Color.dark_red())
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        final = discord.Embed(
            title="✅ All Clear!",
            description=f"{user.mention} is 100% virus-free (their aim, however, remains uncured). 😂",
            color=discord.Color.green()
        )
        await msg.edit(embed=final)


@bot.tree.command(name="compatibility", description="Check funny friendship compatibility between two users.")
@app_commands.describe(user="The user to compare with")
@app_commands.checks.cooldown(1, 8.0)
async def compatibility(interaction: discord.Interaction, user: discord.Member):
    percent = random.randint(1, 100)
    embed = discord.Embed(
        title="💞 Compatibility Check",
        description=f"{interaction.user.mention} + {user.mention}\n\n**{percent}%** compatible\n{random.choice(COMPATIBILITY_LINES)}",
        color=discord.Color.pink()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="npc", description="Generate a funny NPC profile for a user.")
@app_commands.describe(user="The user to turn into an NPC")
@app_commands.checks.cooldown(1, 8.0)
async def npc(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"🧍 NPC Profile: {user.display_name}", description=random.choice(NPC_LINES), color=discord.Color.greyple())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="bossfight", description="Start a funny RPG-style boss fight against a user.")
@app_commands.describe(user="The boss")
@app_commands.checks.cooldown(1, 10.0)
async def bossfight(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    embed = discord.Embed(title="⚔️ Boss Fight!", description=f"You challenge **{user.display_name}** to a boss fight!\nHP: `[██████████] 100%`", color=discord.Color.dark_red())
    msg = await interaction.followup.send(embed=embed)
    hp = 100
    for _ in range(3):
        await asyncio.sleep(1.2)
        hp -= random.randint(20, 40)
        hp = max(hp, 0)
        filled = "█" * (hp // 10)
        empty = "░" * (10 - hp // 10)
        embed = discord.Embed(title="⚔️ Boss Fight!", description=f"**{user.display_name}** HP: `[{filled}{empty}] {hp}%`\n{random.choice(BOSSFIGHT_LINES)}", color=discord.Color.dark_red())
        await msg.edit(embed=embed)
    await asyncio.sleep(1)
    result = "🏆 You win! (Barely, and mostly by luck.)" if hp <= 0 else "💀 The boss survives... this time."
    final = discord.Embed(title="⚔️ Boss Fight Over!", description=result, color=discord.Color.gold())
    await msg.edit(embed=final)


@bot.tree.command(name="box", description="Open a random mystery box.")
@app_commands.checks.cooldown(1, 6.0)
async def box(interaction: discord.Interaction):
    async with interaction.channel.typing():
        await asyncio.sleep(1)
    embed = discord.Embed(title="📦 Mystery Box", description=random.choice(BOX_RESULTS), color=discord.Color.dark_teal())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="react", description="Start a funny reaction challenge.")
@app_commands.checks.cooldown(1, 6.0)
async def react(interaction: discord.Interaction):
    embed = discord.Embed(title="⚡ Reaction Challenge", description=random.choice(REACT_PROMPTS), color=discord.Color.yellow())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="daily", description="Get a random joke of the day.")
@app_commands.checks.cooldown(1, 6.0)
async def daily(interaction: discord.Interaction):
    embed = discord.Embed(title="📅 Joke of the Day", description=random.choice(DAILY_JOKES), color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="profile", description="Generate a funny fake gamer profile.")
@app_commands.describe(user="The user to profile")
@app_commands.checks.cooldown(1, 8.0)
async def profile(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"🎮 Gamer Profile: {user.display_name}", color=discord.Color.teal())
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Title", value=random.choice(PROFILE_TITLES), inline=False)
    embed.add_field(name="🎯 Aim", value=f"{stat()}%", inline=True)
    embed.add_field(name="🍀 Luck", value=f"{stat()}%", inline=True)
    embed.add_field(name="😡 Rage", value=f"{stat()}%", inline=True)
    embed.add_field(name="🍼 Noob Level", value=f"{stat()}%", inline=True)
    embed.add_field(name="👑 Pro Level", value=f"{stat()}%", inline=True)
    embed.add_field(name="🧠 Game Sense", value=f"{stat()}%", inline=True)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fortune", description="Get a funny fortune reading for a user.")
@app_commands.describe(user="The user to read fortune for")
@app_commands.checks.cooldown(1, 8.0)
async def fortune(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="🔮 Fortune Reading", description=f"{user.mention}\n\n{random.choice(FORTUNE_LINES)}", color=discord.Color.dark_purple())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="randomprank", description="Randomly run one harmless prank on a user.")
@app_commands.describe(user="The target")
@app_commands.checks.cooldown(1, 12.0)
async def randomprank(interaction: discord.Interaction, user: discord.Member):
    choice_name = random.choice(["scan", "iq", "mood", "achievement", "future", "fortune", "profile"])
    await interaction.response.send_message(f"🎲 Randomly selected prank: **/{choice_name}** — running it on {user.mention}!")
    if choice_name == "scan":
        result = random.choice(SCAN_RESULTS)
    elif choice_name == "iq":
        result = random.choice(IQ_RESULTS)
    elif choice_name == "mood":
        result = random.choice(MOOD_RESULTS)
    elif choice_name == "achievement":
        result = random.choice(ACHIEVEMENTS)
    elif choice_name == "future":
        result = random.choice(FUTURE_PREDICTIONS)
    elif choice_name == "fortune":
        result = random.choice(FORTUNE_LINES)
    else:
        result = random.choice(PROFILE_TITLES)
    embed = discord.Embed(title=f"🎲 Random Prank Result ({choice_name})", description=f"{user.mention}\n\n{result}", color=discord.Color.random())
    await interaction.followup.send(embed=embed)


# ======================= 9. HELP COMMAND ====================================
@bot.tree.command(name="help", description="Show every command and how to use it.")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Fun & Prank Bot — Help Menu",
        description="All commands are harmless fun, made for friends! 😄",
        color=discord.Color.blurple()
    )
    embed.add_field(name="/roast @user language", value="Savage roast in English or Hinglish 🔥", inline=False)
    embed.add_field(name="/roastcount", value="Show total roast count 📊", inline=False)
    embed.add_field(name="/scan @user", value="Fake animated gamer skill scan 🖥️", inline=False)
    embed.add_field(name="/giveaway", value="Fake giveaway with countdown 🎉", inline=False)
    embed.add_field(name="/iq @user", value="Random funny gamer IQ 🧠", inline=False)
    embed.add_field(name="/detect @user", value="Funny detective report 🕵️", inline=False)
    embed.add_field(name="/hack @user", value="Fictional hacker screen animation 💻", inline=False)
    embed.add_field(name="/skill @user", value="Fake gaming skill analysis 🎯", inline=False)
    embed.add_field(name="/achievement @user", value="Random funny achievement 🏆", inline=False)
    embed.add_field(name="/load", value="Loading animation 0-100% ⏳", inline=False)
    embed.add_field(name="/bancheck @user", value="Fake ban warning prank 🚨", inline=False)
    embed.add_field(name="/mood @user", value="Funny mood scanner 🎭", inline=False)
    embed.add_field(name="/update", value="Fake friendship update animation 📦", inline=False)
    embed.add_field(name="/future @user", value="Funny gaming future prediction 🔮", inline=False)
    embed.add_field(name="/challenge", value="Random harmless challenge 🎯", inline=False)
    embed.add_field(name="/meme", value="Random meme-style message 😂", inline=False)
    embed.add_field(name="/viruscheck @user", value="Fake virus scan (fictional) 🦠", inline=False)
    embed.add_field(name="/compatibility @user", value="Funny friendship compatibility 💞", inline=False)
    embed.add_field(name="/npc @user", value="Funny NPC profile 🧍", inline=False)
    embed.add_field(name="/bossfight @user", value="Funny RPG boss fight ⚔️", inline=False)
    embed.add_field(name="/box", value="Random mystery box 📦", inline=False)
    embed.add_field(name="/react", value="Funny reaction challenge ⚡", inline=False)
    embed.add_field(name="/daily", value="Joke of the day 📅", inline=False)
    embed.add_field(name="/profile @user", value="Funny fake gamer profile 🎮", inline=False)
    embed.add_field(name="/fortune @user", value="Funny fortune reading 🔮", inline=False)
    embed.add_field(name="/randomprank @user", value="Randomly run one prank 🎲", inline=False)
    embed.set_footer(text="All jokes are meant to be friendly — have fun! 😄")
    await interaction.response.send_message(embed=embed)


# ======================= 10. ERROR HANDLING =================================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(title="⏳ Slow down!", description=f"Try again in **{error.retry_after:.1f}s**.", color=discord.Color.red())
    elif isinstance(error, app_commands.CheckFailure):
        embed = discord.Embed(title="🚫 Not allowed", description="You can't use this command right now.", color=discord.Color.red())
    else:
        embed = discord.Embed(title="⚠️ Something went wrong", description=f"`{error}`", color=discord.Color.red())

    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ======================= 11. STARTUP =========================================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/help for fun & pranks 🎮")
    )
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")


# ======================= 12. RUN THE BOT =====================================
if __name__ == "__main__":
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise SystemExit("ERROR: Please paste your bot token into BOT_TOKEN at the top of this file.")
    bot.run(BOT_TOKEN)
