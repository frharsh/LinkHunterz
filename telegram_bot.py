from telethon import TelegramClient, events
from telethon.tl.custom import Button
import re, requests, os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API = os.getenv("VIRUSTOTAL_API")

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "👋 Welcome to LinkHunterz Bot!\n\nSend me any link and I’ll scan it using VirusTotal.\n\nChoose an option below:",
        buttons=[
            [Button.text("/help")]
        ]
    )

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    await event.respond(
        "🛡 LinkHunterz Help:\n\nJust send a message with a link (http/https), and I will check it using VirusTotal.\n\n"
        "You can also type /start to get the welcome message again."
    )

def scan_virustotal(url):
    params = {'apikey': VT_API, 'resource': url}
    r = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params)
    if r.status_code != 200:
        return "❌ Error: Could not fetch result from VirusTotal."
    try:
        result = r.json()
    except:
        return "❌ Error: Invalid response from VirusTotal."

    if result.get("positives", 0) > 1:
        return "⚠ Malicious Link Detected!"
    return "✅ Link is safe."

@client.on(events.NewMessage)
async def handler(event):
    text = event.text
    urls = re.findall(r'https?://\S+', text)
    for url in urls:
        await event.reply(f"🔍 Scanning: {url} ...")
        status = scan_virustotal(url)
        await event.reply(status)

print("🤖 Bot is running...")
client.run_until_disconnected()
