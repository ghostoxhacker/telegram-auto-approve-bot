import asyncio
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, ChatJoinRequestHandler, CallbackQueryHandler, ChatMemberHandler

# Render Web Server for Port Bypass
class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"HottyApprovalBot is live and running perfectly!")

def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    server.serve_forever()

# ==================== CONFIGURATIONS ====================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8883025490:AAGMU-p-aI3_gCBxStH6MjkkBN__aubF7Ho")
BOT_USERNAME = os.getenv("BOT_USERNAME", "HottyApprovalBot")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "Soothing_Sanctuary")
SUPPORT_GRP = os.getenv("SUPPORT_GRP", "PrepNationGrp")
DEVELOPER_USER = "Umm_hotty"
LOGO_URL = "https://t.me/ahh_nexus/8"
# ========================================================

# 1. PREMIUM START COMMAND (DM VIEW WITH SPOILER IMAGE)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    text = (
        f"╭━━👑 <b>𝗔𝗨𝗧𝗢 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 𝗕𝗢𝗧</b> 👑━━╮\n"
        f"   ✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ-ɢᴇɴ sʏsᴛᴇᴍ ✨\n"
        f"╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"👋 𝖧𝖾𝗒 <a href='tg://settings'>{user.first_name}</a> !\n\n"
        f"🦅 𝖨 𝖺𝗆 𝖺𝗇 𝗂𝗇𝗌𝗍𝖺𝗇𝗍 <b>𝗔𝘂𝘁𝗼 𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗦𝘆𝘀𝘁𝗲𝗺</b> 𝖻𝗎𝗂𝗅𝗍 𝗍𝗈 𝖼𝗅𝖾𝖺𝗇𝗅𝗒 𝖺𝗎𝗍𝗈context𝗆𝖺𝗍𝖾 𝗒𝗈𝗎𝗋 𝖼𝗈𝗆𝗆𝗎𝗇𝗂ᴛ𝗒.\n\n"
        f"⚡ <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 :</b>\n"
        f"╭━━━━━━━━━━━━━━━━━━━╮\n"
        f"┃ 👤 <b>𝖨𝗇𝗌𝗍𝖺𝗇𝗍 𝖠𝗉𝗉𝗋𝗈𝗏𝖺𝗅</b> ➔ `0.01 s𝖾𝖼` \n"
        f"┃ 🛡️ <b>𝖠𝗇𝗍𝗂-𝖲𝗉𝖺ᴍ</b> ➔ `𝖤𝗇𝖺𝖻𝗅𝖾𝖽`\n"
        f"┃ 📈 <b>𝖴𝗉𝗍𝗂𝗆𝖾</b> ➔ `24/7 𝖭𝗈𝗇-𝖲ᴛᴏᴘ`\n"
        f"╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"📌 <b>ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ :</b>\n"
        f"🤖 𝖩𝗎𝗌ᴛ 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗌 𝖺𝗇 <b>𝖠𝖽𝗆𝗂𝗇𝗂𝗌𝗍𝗋𝖺𝗍𝗈𝗋</b> 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾xl 𝗈𝗋 𝖦𝗋𝗈𝗎𝗉 𝗐𝗂ᴛʜ *\"𝖨𝗇𝗏𝗂ᴛ𝖾 𝖴𝗌𝖾𝗋𝗌 𝗏𝗂𝖺 𝖫𝗂𝗇ᴋ\"* 𝗉𝖾𝗋<b>𝗆𝗂𝗌𝗌𝗂𝗈𝗇!</b>\n\n"
        f"👑 <b><b>ᴄʀᴇᴀᴛᴇᴅ</b> ʙʏ :</b> @{DEVELOPER_USER}"
    )

    buttons = [
        [
            InlineKeyboardButton("🟩 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝖦𝗋𝗈𝗎𝗉 ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("🟩 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 📢", url=f"https://t.me/{BOT_USERNAME}?startchannel=true")
        ],
        [
            InlineKeyboardButton("🔋 𝖡𝗈𝗈𝗌𝗍 & 𝖴𝗉𝖽𝖺𝗍𝖾𝗌 🤖", url=f"https://t.me/{UPDATE_CHANNEL}"),
            InlineKeyboardButton("⚠️ 𝖣𝗂𝗌𝖼𝗅𝖺𝗂𝗆𝖾𝗋 & 𝖯𝗈𝗅𝗂𝖼𝗒", callback_data="disclaimer")
        ]
    ]

    await update.message.reply_photo(
        photo=LOGO_URL,
        caption=text,
        parse_mode=ParseMode.HTML,
        has_spoiler=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 2. PING COMMAND
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    message = await update.message.reply_text("⚡ *𝖯𝗂𝗇𝗀𝗂𝗇𝗀...*", parse_mode=ParseMode.MARKDOWN)
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000)
    await message.edit_text(f"⚡ <b>𝖯𝗈<b>𝗇𝗀!</b></b> `{latency}𝗆𝗌` 🟢", parse_mode=ParseMode.HTML)

# 3. BOT ADDED TO CHAT
async def bot_added_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member and update.my_chat_member.new_chat_member.status in ["administrator", "member"]:
        chat = update.my_chat_member.chat
        
        group_text = (
            f"👑 <b>𝗛𝗼𝘁𝘁𝘆 𝗔𝗽𝗽𝗿𝗼𝘃𝗲 𝗕𝗼𝘁</b> ɪs ɴᴏᴡ **LIVE** 🟢\n\n"
            f"📌 *Grant Admin permissions with \"Invite Users via Link\" to auto-approve requests.*"
        )
        
        group_buttons = [
            [InlineKeyboardButton("🔋 𝖢𝖧𝖤𝖢𝖪 𝖡𝖮𝖳 𝖲𝖤𝖳𝖳𝖨𝖭𝖦𝖲 (𝖣𝖬) ➔", url=f"https://t.me/{BOT_USERNAME}?start=true")]
        ]
        
        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=group_text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(group_buttons)
            )
        except Exception:
            pass

# 4. INSTANT AUTO-APPROVAL -> DM NOTIFICATION (UPDATES & DEVELOPER BUTTONS)
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    chat = req.chat
    user = req.from_user

    try:
        await context.bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    except Exception:
        pass

    dm_text = (
        f"✨ <b>ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇᴅ</b> ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🤝 Hello <a href='tg://settings'>{user.first_name}</a>,\n\n"
        f"🎉 Your request to join <b>{chat.title}</b> has been <b>Successfully Approved</b> instantly by our system!\n\n"
        f"🚀 *Powered by @{BOT_USERNAME}*"
    )

    dm_buttons = [
        [
            InlineKeyboardButton("📢 𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url=f"https://t.me/{UPDATE_CHANNEL}"),
            InlineKeyboardButton("👑 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋", url=f"https://t.me/{DEVELOPER_USER}")
        ]
    ]

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=dm_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(dm_buttons),
            disable_web_page_preview=True
        )
    except Exception:
        pass

# 5. DISCLAIMER CALLBACK
async def disclaimer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        f"<b>📢 Disclaimer – Auto Approve Join Request Bot</b>\n\n"
        f"🔹 This bot is an <b>automated system</b> that approves join requests. By using this bot, you agree:\n\n"
        f"<b>✅ No Liability</b>\nThe bot owner & developers are <b>not responsible</b> for any misuse or unauthorized activity.\n\n"
        f"<b>🤖 Automated Decisions</b>\nThe bot works 100% automatically and instantly.\n\n"
        f"<b>📌 Ensure responsible usage to keep your community secure!</b>"
    )
    await query.message.reply_text(text=text, parse_mode=ParseMode.HTML)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CallbackQueryHandler(disclaimer_callback, pattern="disclaimer"))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(ChatMemberHandler(bot_added_to_chat, ChatMemberHandler.MY_CHAT_MEMBER))

    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    threading.Thread(target=start_web_server, daemon=True).start()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        loop.create_task(main())
    else:
        loop.run_until_complete(main())
               
