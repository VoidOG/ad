import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message

from config import (
    API_ID,
    API_HASH,
    SESSION_STRING,
    LOG_GROUP_ID,
    MESSAGE_LINKS,
    NORMAL_GROUPS,
    FORUM_TARGETS,
)

app = Client(
    "adbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Utility to parse t.me message link
def parse_link(link):
    parts = link.split("/")
    chat_username = parts[-2]
    msg_id = int(parts[-1])
    return chat_username, msg_id

# Forward message to forum threads
async def forward_to_forums():
    link = random.choice(MESSAGE_LINKS)
    username, msg_id = parse_link(link)

    for target in FORUM_TARGETS:
        try:
            await app.forward_messages(
                chat_id=target["chat_id"],
                from_chat_id=username,
                message_ids=msg_id,
                message_thread_id=target["topic_id"]
            )
            await app.send_message(
                LOG_GROUP_ID,
                f"✅ Forwarded to forum {target['chat_id']}:{target['topic_id']}"
            )
        except Exception as e:
            await app.send_message(
                LOG_GROUP_ID,
                f"❌ Failed forum {target['chat_id']}:{target['topic_id']} — {e}"
            )
        await asyncio.sleep(target.get("delay", 600))  # Custom delay per forum

# Forward message to normal groups
async def forward_to_groups():
    link = random.choice(MESSAGE_LINKS)
    username, msg_id = parse_link(link)

    for group in NORMAL_GROUPS:
        try:
            await app.forward_messages(
                chat_id=group["chat_id"],
                from_chat_id=username,
                message_ids=msg_id
            )
            await app.send_message(
                LOG_GROUP_ID,
                f"✅ Forwarded to group {group['chat_id']}"
            )
        except Exception as e:
            await app.send_message(
                LOG_GROUP_ID,
                f"❌ Failed group {group['chat_id']} — {e}"
            )
        await asyncio.sleep(group.get("delay", 600))  # Custom delay per group

# Auto-reply in DMs
@app.on_message(filters.private & ~filters.me)
async def auto_reply_dm(client: Client, message: Message):
    await message.reply_text(
        "I am an automated AdBot powered by @adversio.\n"
        "Kindly contact the person in my bio for any queries."
    )

# Main loop
async def main():
    async with app:
        while True:
            await forward_to_forums()
            await forward_to_groups()

if __name__ == "__main__":
    asyncio.run(main())
