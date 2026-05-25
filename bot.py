import asyncio
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    ChatJoinRequestHandler, CallbackQueryHandler, ChatMemberHandler
)

start_time_init = time.time()
users_list = set()
groups_list = set()

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is active")

def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    server.serve_forever()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8883025490:AAGMU-p-aI3_gCBxStH6MjkkBN__aubF7Ho")
OWNER_ID = 8576582616
BOT_USERNAME = os.getenv("BOT_USERNAME", "HottyApprovalBot")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "Soothing_Sanctuary")
DEVELOPER_USER = "Umm_hotty"
LOGO_URL = "https://t.me/ahh_nexus/8"

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await update.message.reply_text("Checking system...")
    latency = round((time.time() - start) * 1000)
    uptime = int(time.time() - start_time_init)
    h, rem = divmod(uptime, 3600)
    m, s = divmod(rem, 60)
    text = f"<b>Latency:</b> {latency}ms\n<b>Uptime:</b> {h}h {m}m {s}s\n<b>Status:</b> Operational"
    await msg.edit_text(text, parse_mode=ParseMode.HTML)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    
    pin = False
    if "-p" in context.args:
        pin = True
        context.args.remove("-p")
    
    msg_src = update.message.reply_to_message if update.message.reply_to_message else " ".join(context.args)
    
    if not msg_src:
        await update.message.reply_text("Usage: /broadcast <text> or reply to msg [-p]")
        return
    
    count = 0
    targets = users_list.union(groups_list)
    for tid in targets:
        try:
            if isinstance(msg_src, str):
                sent = await context.bot.send_message(chat_id=tid, text=msg_src, parse_mode=ParseMode.HTML)
            else:
                sent = await context.bot.copy_message(chat_id=tid, from_chat_id=msg_src.chat_id, message_id=msg_src.message_id)
            if pin:
                await context.bot.pin_chat_message(chat_id=tid, message_id=sent.message_id)
            count += 1
            await asyncio.sleep(0.05)
        except:
            continue
    await update.message.reply_text(f"Broadcast successful to {count} targets.")

async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status in ["administrator", "member"]:
        groups_list.add(update.my_chat_member.chat.id)
    else:
        groups_list.discard(update.my_chat_member.chat.id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users_list.add(user.id)
    text = f"👑 <b>AUTO APPROVE BOT</b>\n\nHey {user.first_name}\n\nI manage your community automatically.\n\nCreated by @{DEVELOPER_USER}"
    buttons = [
        [InlineKeyboardButton("Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("Updates", url=f"https://t.me/{UPDATE_CHANNEL}")]
    ]
    await update.message.reply_photo(LOGO_URL, caption=text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(buttons))

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    users_list.add(req.from_user.id)
    try:
        await context.bot.approve_chat_join_request(req.chat.id, req.from_user.id)
        await context.bot.send_message(req.from_user.id, f"Your request for {req.chat.title} was approved.")
    except:
        pass

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatJoinRequestHandler(approve))
    app.add_handler(ChatMemberHandler(track_chat, ChatMemberHandler.MY_CHAT_MEMBER))
    
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(3600)

if __name__ == '__main__':
    threading.Thread(target=start_web_server, daemon=True).start()
    asyncio.run(main())
    
