import asyncio
from pyrogram import Client, errors
from config import SESSION_STRING, SOURCE_CHANNEL_ID, MESSAGE_ID, FORUM_TARGETS, NORMAL_GROUPS, DELAY_SECONDS

app = Client(name="adbot", session_string=SESSION_STRING)

async def forward_to_forums():
    for target in FORUM_TARGETS:
        try:
            await app.forward_messages(
                chat_id=target["chat_id"],
                from_chat_id=SOURCE_CHANNEL_ID,
                message_ids=MESSAGE_ID,
                message_thread_id=target["topic_id"]
            )
            print(f"[✅] Forwarded to forum {target['chat_id']}:{target['topic_id']}")
        except Exception as e:
            print(f"[❌] Failed to forward to forum {target['chat_id']}:{target['topic_id']} — {e}")

async def forward_to_groups():
    for group_id in NORMAL_GROUPS:
        try:
            await app.forward_messages(
                chat_id=group_id,
                from_chat_id=SOURCE_CHANNEL_ID,
                message_ids=MESSAGE_ID
            )
            print(f"[✅] Forwarded to group {group_id}")
        except Exception as e:
            print(f"[❌] Failed to forward to group {group_id} — {e}")

async def main():
    async with app:
        while True:
            await forward_to_forums()
            await forward_to_groups()
            print(f"[⏱️] Waiting {DELAY_SECONDS} seconds...\n")
            await asyncio.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
