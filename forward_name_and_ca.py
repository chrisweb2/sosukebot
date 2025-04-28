from telethon import TelegramClient, events
import re
import asyncio
import random

# Thông tin cá nhân Telegram
api_id = 27507062
api_hash = 'e13bd8e7e23f1c3cc86b26509260ed02'
phone = '+372 5852 3194'

# Mapping kênh nguồn -> group đích
source_target_map = {
    'pumpdotfunalert': -1002641732924,   # Sosuke Gems
    'SolanaDexPaid': -1002611739098      # Sosuke Premium Lad
}

# Regex tách dữ liệu theo từng nguồn
regex_by_source = {
    'pumpdotfunalert': {
        'name': re.compile(r'Name:\s*(.+?\(\w+\))'),
        'ca': re.compile(r'Mint:\s*([1-9A-HJ-NP-Za-km-z]{32,44}pump)'),
        'mc': re.compile(r'MC:\s*\$(\d{1,3}(?:,\d{3})*)')
    },
    'SolanaDexPaid': {
        'name': re.compile(r'Name:\s*(.+?\$\w+)', re.IGNORECASE),
        'ca': re.compile(r'CA:\s*([1-9A-HJ-NP-Za-km-z]{32,44}pump)', re.IGNORECASE),
        'mc': re.compile(r'Market Cap:\s*\$(\d{1,3}(?:,\d{3})*)', re.IGNORECASE)
    }
}

# Quotes hype riêng từng nguồn
quotes_by_source = {
    'pumpdotfunalert': [
        "💥 Degen drop.", "⚡ Fresh alpha.", "🧨 Early take.", "🚀 Pump in progress.",
        "📈 Woke move.", "🧠 Outsmart or exit.", "💣 Juicy mint.", "👁 1st eyes wins."
    ],
    'SolanaDexPaid': [
        "📡 Paid scoop.", "💰 Private plug.", "🔮 Future alpha.", "👑 Premium only.",
        "🔥 Insider watch.", "⚠️ Off radar.", "💼 Sosuke premium drop.", "🚦 Call before crowd."
    ]
}

client = TelegramClient('sosuke_no_mc_filter_soladex', api_id, api_hash)

async def main():
    await client.start(phone)

    for source_channel, target_group in source_target_map.items():
        @client.on(events.NewMessage(chats=source_channel))
        async def handler(event, target=target_group, source=source_channel):
            full_text = event.message.raw_text or ''
            regex = regex_by_source[source]
            name_match = regex['name'].search(full_text)
            ca_match = regex['ca'].search(full_text)
            mc_match = regex['mc'].search(full_text)

            if name_match and ca_match:
                name_text = name_match.group(1)
                ca = ca_match.group(1)
                quote = random.choice(quotes_by_source[source])

                if source == "pumpdotfunalert":
                    if not mc_match:
                        return
                    mc_value = int(mc_match.group(1).replace(",", ""))
                    if mc_value >= 200000:
                        return

                msg = f"Sosuke_gems_Premium: {name_text}\nCA: {ca}\n{quote}"
                await client.send_message(target, msg)
                await asyncio.sleep(5)

    print("✅ Bot đang chạy: SolanaDexPaid không lọc MC, pumpdotfunalert vẫn lọc MC < 200k")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())