import asyncio
from pyrogram import Client, errors
from config import (
    SESSION_NAME,
    SOURCE_CHANNEL_USERNAME,
    MESSAGE_ID,
    FORUM_TARGETS,
    NORMAL_GROUPS,
    DELAY_SECONDS,
    LOG_GROUP_ID,
)

app = Client(SESSION_NAME)

async def forward_to_forums():
    for target in FORUM_TARGETS:
        try:
            await app.forward_messages(
                chat_id=target["chat_id"],
                from_chat_id=SOURCE_CHANNEL_USERNAME,
                message_ids=MESSAGE_ID,
                message_thread_id=target["topic_id"]
            )
            msg = f"[✅] Forwarded to forum {target['chat_id']}:{target['topic_id']}"
            print(msg)
            await app.send_message(LOG_GROUP_ID, msg)
        except Exception as e:
            msg = f"[❌] Failed to forward to forum {target['chat_id']} — {e}"
            print(msg)
            await app.send_message(LOG_GROUP_ID, msg)

async def forward_to_groups():
    for group_id in NORMAL_GROUPS:
        try:
            await app.forward_messages(
                chat_id=group_id,
                from_chat_id=SOURCE_CHANNEL_USERNAME,
                message_ids=MESSAGE_ID
            )
            msg = f"[✅] Forwarded to group {group_id}"
            print(msg)
            await app.send_message(LOG_GROUP_ID, msg)
        except Exception as e:
            msg = f"[❌] Failed to forward to group {group_id} — {e}"
            print(msg)
            await app.send_message(LOG_GROUP_ID, msg)

async def main():
    async with app:
        while True:
            await forward_to_forums()
            await forward_to_groups()
            wait_msg = f"[⏱️] Waiting {DELAY_SECONDS} seconds...\n"
            print(wait_msg)
            await app.send_message(LOG_GROUP_ID, wait_msg)
            await asyncio.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
