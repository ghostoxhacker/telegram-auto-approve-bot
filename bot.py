import asyncio
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, ChatJoinRequestHandler, CallbackQueryHandler, ChatMemberHandler

# Uptime tracker
start_time_init = time.time()

# Web Server for Port Bypass
class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"HottyApprovalBot is live!")

def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    server.serve_forever()

# ==================== CONFIGURATIONS ====================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8883025490:AAGMU-p-aI3_gCBxStH6MjkkBN__aubF7Ho")
OWNER_ID = 8576582616
users_list = set()
BOT_USERNAME = os.getenv("BOT_USERNAME", "HottyApprovalBot")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "Soothing_Sanctuary")
DEVELOPER_USER = "Umm_hotty"
LOGO_URL = "https://t.me/ahh_nexus/8"
# ========================================================

# ADVANCED PING COMMAND
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("⚡ Checking System Health")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000)
    uptime_seconds = int(time.time() - start_time_init)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    status_text = (
        f"<b>⚡ SYSTEM STATUS</b>\n\n"
        f"<b>• Latency:</b> {latency}ms\n"
        f"<b>• Uptime:</b> {hours}h {minutes}m {seconds}s\n"
        f"<b>• Status:</b> Operational 🟢\n\n"
        f"🚀 <i>Hotty Bot is running smooth!</i>"
    )
    await msg.edit_text(status_text, parse_mode=ParseMode.HTML)

# ADVANCED BROADCAST COMMAND
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    
    pin_message = False
    if "-p" in context.args:
        pin_message = True
        context.args.remove("-p")
    
    msg_to_send = None
    if update.message.reply_to_message:
        msg_to_send = update.message.reply_to_message
    elif context.args:
        msg_to_send = " ".join(context.args)
    else:
        await update.message.reply_text("Usage: /broadcast <message> (or reply to msg) [-p to pin]")
        return
    
    count = 0
    for user_id in users_list:
        try:
            if isinstance(msg_to_send, str):
                sent_msg = await context.bot.send_message(chat_id=user_id, text=msg_to_send, parse_mode=ParseMode.HTML)
            else:
                sent_msg = await context.bot.copy_message(chat_id=user_id, from_chat_id=msg_to_send.chat_id, message_id=msg_to_send.message_id)
            
            if pin_message:
                await context.bot.pin_chat_message(chat_id=user_id, message_id=sent_msg.message_id)
            
            count += 1
            await asyncio.sleep(0.05)
        except:
            continue
    await update.message.reply_text(f"✅ Broadcast sent to {count} users {'(Pinned)' if pin_message else ''}")

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users_list.add(user.id)
    text = (
        f"👑 <b>AUTO APPROVE BOT</b> 👑\n\n"
        f"👋 Hey <a href='tg://settings'>{user.first_name}</a>\n\n"
        f"🦅 I am an instant <b>Auto Approval System</b> built to manage your community automatically.\n\n"
        f"📌 <b>HOW TO USE ME</b>\n"
        f"Just add me as an <b>Administrator</b> in your chat with Invite Users via Link permission\n\n"
        f"👑 <b>CREATED BY</b> @{DEVELOPER_USER}"
    )
    buttons = [
        [InlineKeyboardButton("🟩 Add me to Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"), InlineKeyboardButton("🟩 Add me to Channel 📢", url=f"https://t.me/{BOT_USERNAME}?startchannel=true")],
        [InlineKeyboardButton("🔋 Boost & Updates 🤖", url=f"https://t.me/{UPDATE_CHANNEL}"), InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer")]
    ]
    await update.message.reply_photo(photo=LOGO_URL, caption=text, parse_mode=ParseMode.HTML, has_spoiler=True, reply_markup=InlineKeyboardMarkup(buttons))

# APPROVAL LOGIC
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user = req.from_user
    users_list.add(user.id)
    try:
        await context.bot.approve_chat_join_request(chat_id=req.chat.id, user_id=user.id)
        dm_text = f"✨ <b>JOIN REQUEST APPROVED</b> ✨\n\n🤝 Hello <a href='tg://settings'>{user.first_name}</a>,\n\n🎉 Your request to join <b>{req.chat.title}</b> has been <b>Successfully Approved</b>.\n\n🚀 Powered by @{BOT_USERNAME}"
        await context.bot.send_message(chat_id=user.id, text=dm_text, parse_mode=ParseMode.HTML)
    except: pass

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer("Disclaimer active"), pattern="disclaimer"))
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    while True: await asyncio.sleep(3600)

if __name__ == '__main__':
    threading.Thread(target=start_web_server, daemon=True).start()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if loop.is_running(): loop.create_task(main())
    else: loop.run_until_complete(main())
    
