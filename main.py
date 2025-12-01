import os
import asyncio
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

IMPORTANT_GROUPS = [
]

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

MSG_CACHE = {}
targets = {}
is_afk = False
afk_reason = ""

spy_filter = (filters.private | filters.chat(IMPORTANT_GROUPS)) & filters.incoming & ~filters.bot

print("🚀 Userbot started! System nominal.")

@app.on_message(spy_filter, group=1)
async def cache_incoming(client, message):
    is_disappearing = False
    if message.photo and message.photo.ttl_seconds:
        is_disappearing = True
    elif message.video and message.video.ttl_seconds:
        is_disappearing = True

    if is_disappearing:
        sender = message.from_user.first_name if message.from_user else "Unknown"
        source = "DM" if message.chat.type.name == "PRIVATE" else message.chat.title
        await client.send_message("me", f"🔥 **{sender}** ({source}) sent self-destructing media! Downloading...")
        try:
            path = await message.download()
            await client.send_document("me", path, caption=f"Saved from {sender} ({source})")
            os.remove(path)
        except:
            pass
        return

    if message.text:
        key = (message.chat.id, message.id)
        sender = message.from_user.first_name if message.from_user else "Unknown"
        source_name = "DM" if message.chat.type.name == "PRIVATE" else message.chat.title

        MSG_CACHE[key] = {
            "sender": sender,
            "source": source_name,
            "text": message.text
        }
        if len(MSG_CACHE) > 2000:
            del MSG_CACHE[next(iter(MSG_CACHE))]

@app.on_message(filters.incoming, group=2)
async def auto_react(client, message):
    chat_id = message.chat.id
    if message.from_user:
        user_id = message.from_user.id
        if chat_id in targets and user_id in targets[chat_id]:
            try:
                await message.react("💩")
            except:
                pass

@app.on_message(filters.private & filters.incoming & ~filters.bot, group=3)
async def afk_responder(client, message):
    if is_afk:
        await message.reply_text(f"Currently AFK: {afk_reason}")

@app.on_deleted_messages()
async def handle_deleted(client, messages):
    for msg in messages:
        found_key = None
        msg_id = msg.id
        chat_id = msg.chat.id if msg.chat else None

        if chat_id and (chat_id, msg_id) in MSG_CACHE:
            found_key = (chat_id, msg_id)
        elif not found_key:
            for k in MSG_CACHE:
                if k[1] == msg_id: found_key = k; break

        if found_key:
            data = MSG_CACHE[found_key]
            await client.send_message("me",
                                      f"🗑 **Deleted in: {data['source']}**\n👤 **{data['sender']}**: {data['text']}")
            del MSG_CACHE[found_key]

@app.on_message(filters.command("type", prefixes=".") & filters.me)
async def type_effect(client, message):
    if len(message.command) < 2: return
    text = message.text.split(None, 1)[1]
    tbp = ""
    try:
        for char in text:
            tbp += char
            if char == " ":
                continue
            await message.edit_text(tbp)
            await asyncio.sleep(0.05)
        if text.endswith(" "):
            await message.edit_text(tbp)
    except:
        pass

@app.on_message(filters.command("afk", prefixes=".") & filters.me)
async def set_afk(client, message):
    global is_afk, afk_reason
    afk_reason = message.text.split(None, 1)[1] if len(message.command) > 1 else "Busy"
    is_afk = True
    await message.edit_text(f"💤 AFK enabled: {afk_reason}")

@app.on_message(filters.command("unafk", prefixes=".") & filters.me)
async def unset_afk(client, message):
    global is_afk
    is_afk = False
    await message.edit_text("✅ AFK disabled.")

@app.on_message(filters.command("r", prefixes=".") & filters.me)
async def toggle_r(client, message):
    if not message.reply_to_message: return
    cid, vid = message.chat.id, message.reply_to_message.from_user.id
    if cid not in targets: targets[cid] = []

    if vid in targets[cid]:
        targets[cid].remove(vid)
        await message.edit_text("Target removed.")
    else:
        targets[cid].append(vid)
        await message.edit_text("Target locked.")

    await asyncio.sleep(2)
    await message.delete()

@app.on_message(filters.command("tag", prefixes=".") & filters.me)
async def tag_id(client, message):
    parts = message.text.split(None, 2)
    if len(parts) < 2: return
    uid, txt = parts[1], parts[2] if len(parts) > 2 else "👋"
    await message.delete()
    try:
        await client.send_message(message.chat.id, f"[\u200b](tg://user?id={uid}){txt}")
    except:
        pass

@app.on_message(filters.command("all", prefixes=".") & filters.me)
async def tag_all(client, message):
    txt = message.text.split(None, 1)[1] if len(message.command) > 1 else "👋"
    await message.delete()
    mentions = [f"[\u200b](tg://user?id={m.user.id})" async for m in client.get_chat_members(message.chat.id, limit=50)
                if not m.user.is_bot]
    await client.send_message(message.chat.id, "".join(mentions) + " " + txt)

@app.on_message(filters.command("del", prefixes=".") & filters.me)
async def purge(client, message):
    if len(message.command) < 2: return
    limit = int(message.command[1])
    await message.delete()
    cnt = 0
    async for m in client.get_chat_history(message.chat.id):
        if m.from_user.id == message.from_user.id:
            try:
                await m.delete(); cnt += 1
            except:
                pass
        if cnt >= limit: break
    info = await client.send_message(message.chat.id, f"🗑 Purged: {cnt}")
    await asyncio.sleep(2)
    await info.delete()

@app.on_message(filters.command("id", prefixes=".") & filters.me)
async def get_id(client, message):
    await message.edit_text(f"🆔 `{message.chat.id}`")

if __name__ == "__main__":
    app.run()