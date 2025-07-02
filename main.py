import asyncio
from pyrogram import Client, errors
from config import *

app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

async def extract_message_info(link):
    parts = link.replace("https://t.me/", "").split("/")
    channel_username = parts[0]
    message_id = int(parts[1])
    return channel_username, message_id

async def forward_to_forums(channel_username, message_id):
    for target in FORUM_TARGETS:
        try:
            await app.forward_messages(
                chat_id=target["chat_id"],
                from_chat_id=channel_username,
                message_ids=message_id,
                message_thread_id=target["topic_id"]
            )
            await app.send_message(LOG_GROUP_ID, f"✅ Forwarded to forum {target['chat_id']}:{target['topic_id']}")
        except Exception as e:
            await app.send_message(LOG_GROUP_ID, f"❌ Forum {target['chat_id']} failed: {e}")

async def forward_to_groups(channel_username, message_id):
    for group_id in NORMAL_GROUPS:
        try:
            await app.forward_messages(
                chat_id=group_id,
                from_chat_id=channel_username,
                message_ids=message_id
            )
            await app.send_message(LOG_GROUP_ID, f"✅ Forwarded to group {group_id}")
        except Exception as e:
            await app.send_message(LOG_GROUP_ID, f"❌ Group {group_id} failed: {e}")

async def main():
    async with app:
        channel_username, message_id = await extract_message_info(SOURCE_CHANNEL_LINK)
        while True:
            await forward_to_forums(channel_username, message_id)
            await forward_to_groups(channel_username, message_id)
            await app.send_message(LOG_GROUP_ID, f"⏱️ Waiting {DELAY_SECONDS} seconds before next cycle")
            await asyncio.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
