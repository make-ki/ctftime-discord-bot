import nextcord
import requests
import datetime
import asyncio
from nextcord.ext import commands, tasks
import os

TOKEN = os.getenv('TOKEN')  # Discord bot token
CTFTIME_API = os.getenv('CTFTIME_API', 'https://ctftime.org/api/v1/events/') # Api url
HEADERS = {'User-Agent': 'Mozilla/5.0'}  # Required for CTFtime API, the server rejects requests from bots unless specified user agent
CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))  # Channel to send updates
CTF_ROLE_ID = int(os.getenv('CTF_ROLE_ID', '0'))  # Role to ping for updates

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

def format_discord_time(timestamp):
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    unix_time = int(dt.timestamp())
    return f"<t:{unix_time}:R> (<t:{unix_time}:F>)"  #Creates the unix relative timestamp

async def get_ctf_events():   #tries fetching from CTFtime
    try:
        response = requests.get(CTFTIME_API, params={"limit": 5}, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching CTF events: {e}")
        return None

@bot.slash_command(name="ctf_events", description="Fetch upcoming CTF events")
async def ctf_events(interaction: nextcord.Interaction):
    events = await get_ctf_events()
    if events:
        for event in events:
            embed = nextcord.Embed(title=event['title'], color=0x00ff00)
            start_time = format_discord_time(event['start'])
            end_time = format_discord_time(event['finish'])
            embed.add_field(name="Start", value=start_time, inline=False)
            embed.add_field(name="End", value=end_time, inline=False)
            embed.add_field(name="CTF Link ➤", value=f"[Link]({event['url']})", inline=False)

            if 'logo' in event:
                embed.set_thumbnail(url=event['logo'])

            if 'prizes' in event and event['prizes']:
                embed.add_field(name="Prizes", value=event['prizes'], inline=False)

            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(2)  # Wait before sending the next event
    else:
        await interaction.response.send_message("Failed to fetch CTF events.")

@bot.slash_command(name="clear", description="Deletes all messages in the channel.")
async def clear(interaction: nextcord.Interaction, limit: int = 100):
    await interaction.response.defer()
    deleted = await interaction.channel.purge(limit=limit)
    await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)

@tasks.loop(seconds=604800)  # 7 days in seconds, the bot runs weekly
async def fetch_ctf_updates():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("Invalid channel ID")
        return

    events = await get_ctf_events()
    if events:
        for event in events:
            embed = nextcord.Embed(title=event['title'], color=0xff0000)
            start_time = format_discord_time(event['start'])
            end_time = format_discord_time(event['finish'])
            embed.add_field(name="Start", value=start_time, inline=False)
            embed.add_field(name="End", value=end_time, inline=False)
            embed.add_field(name="CTF Link ➤", value=f"[Link]({event['url']})", inline=False)

            if 'logo' in event:
                embed.set_thumbnail(url=event['logo'])

            if 'prizes' in event and event['prizes']:
                embed.add_field(name="Prizes", value=event['prizes'], inline=False)

            try:
                await channel.send(f"<@&{CTF_ROLE_ID}> New CTF event update!", embed=embed)
                await asyncio.sleep(2)  # Wait before sending the next event, necessary for sending different embeds
            except nextcord.Forbidden:
                print(f"Error: Bot lacks permissions to send messages in channel {CHANNEL_ID}")
                return
    else:
        try:
            await channel.send("Failed to fetch CTF events.")
        except nextcord.Forbidden:
            print(f"Error: Bot lacks permissions to send messages in channel {CHANNEL_ID}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_application_commands()
    fetch_ctf_updates.start()

bot.run(TOKEN)
