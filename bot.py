import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ==================== [ ⚙️ PREMIUM CONFIGURATION ] ====================
API_ID = 38199591               
API_HASH = "274ed9d7f696f8970e0348dd40d47f70"     
BOT_TOKEN = "8565820660:AAERaDxb77ET-Qq3w3a4xUNs55eRCAyR_Y0"   

BASE_URL = "https://2oo9.cloud/api/MXS47FLFX0U/project/tetragonexvoltxsms/@public/api"
MAUTH_API_KEY = "MWFG9WNAHZQ"  

HEADERS = {
    "mauthapi": MAUTH_API_KEY,
    "Content-Type": "application/json"
}

session = None

class AsyncBot(Client):
    def __init__(self):
        super().__init__("otp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    async def start(self):
        global session
        session = aiohttp.ClientSession()
        await super().start()

    async def stop(self, *args):
        global session
        if session:
            await session.close()
        await super().stop(*args)

app = AsyncBot()
# =====================================================================


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text("⚡ `Please wait... Fetching live ranges from server...` 📡🌀")
    
    try:
        async with session.get(f"{BASE_URL}/liveaccess", headers=HEADERS) as response:
            res_data = await response.json()
        
        services = res_data.get("data", []) if isinstance(res_data, dict) else res_data

        if not services:
            await message.reply_text("⚠️ **🛸 SYSTEM ALERT:**\n\n❌ দুঃখিত ভাই! এই মুহূর্তে কোনো রেঞ্জ সচল বা লাইভ নেই। 🔌")
            return

        keyboard = []
        for service in services[:15]: 
            rid = service.get("rid") or service.get("id")
            name = service.get("name") or f"Range {rid}"
            
            if rid:
                keyboard.append([InlineKeyboardButton(f"💎 {name} ✨ [ID: {rid}] ⚡", callback_data=f"get_{rid}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            f"👑 **WELCOME TO KSY PREMIUM OTP BOT** 🚀\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👋 হ্যালো ব্রো! আমাদের আল্ট্রা-ফাস্ট ওটিপি বোটে আপনাকে স্বাগতম! 🥰\n\n"
            f"📱 **নিচের তালিকা থেকে আপনার কাঙ্ক্ষিত রেঞ্জটি সিলেক্ট করুন:**\n"
            f"💡 *বাটনে ক্লিক করা মাত্রই অটোমেটিক সচল নাম্বার জেনারেট হয়ে যাবে!* 🔥\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 **Bot Status:** `🟢 Online & SuperFast`", 
            reply_markup=reply_markup
        )

    except Exception as e:
        await message.reply_text(f"❌ **💥 SYSTEM ERROR:** `{str(e)}` ⚠️")


@app.on_callback_query(filters.regex(r"^get_"))
async def handle_range_click(client, callback_query: CallbackQuery):
    rid = callback_query.data.split("_")[1]
    
    await callback_query.answer("🚀 Connecting to Server...", show_alert=False)
    await callback_query.message.edit_text("⏳ **Securing connection & allocating your number... Please wait!** 📡🔐")

    try:
        payload = {"rid": str(rid)}
        
        async with session.post(f"{BASE_URL}/getnum", json=payload, headers=HEADERS) as response:
            res_data = await response.json()

        meta_code = res_data.get("meta", {}).get("code")
        if meta_code == 2946:
            await callback_query.message.edit_text("😢 **📉 STOCK OUT!**\n\nদুঃখিত ভাই! এই রেঞ্জের নাম্বার আপাতত স্টক শেষ! অন্য রেঞ্জ ট্রাই করুন। ❌")
            return

        data = res_data.get("data", {})
        number = data.get("number") or data.get("phone")
        
        if not number:
            await callback_query.message.edit_text("⚠️ **📶 SERVER TIMEOUT:**\n\nকোনো নাম্বার পাওয়া যায়নি! এপিআই সার্ভার রেসপন্স করছে না। 💔")
            return

        await callback_query.message.edit_text(
            f"╭━━━ ✨ **YOUR NUMBER IS READY** ✨ ━━━╮\n\n"
            f" 📞  **`{number}`** \n\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━━━╯\n"
            f"💡 *উপরের নাম্বারে ক্লিক করলেই অটোমেটিক কপি হয়ে যাবে!*\n\n"
            f"ℹ️ **নির্দেশনা:**\n"
            f"➡️ ওটিপি কোডটি দ্রুত ওই নাম্বারে পাঠান।\n"
            f"🔄 **বোট ব্যাকগ্রাউন্ডে ওটিপির জন্য লাইভ অপেক্ষা করছে...**\n"
            f"⏱️ আগামী ৩ মিনিট প্রতি ৫ সেকেন্ড পর পর অটো-চেক চলবে! ⏳"
        )

        for _ in range(36):
            await asyncio.sleep(5)
            
            try:
                async with session.get(f"{BASE_URL}/success-otp", headers=HEADERS) as otp_response:
                    otp_data = await otp_response.json()
                
                otp_list = otp_data.get("data", []) if isinstance(otp_data, dict) else otp_data
                
                otp_found = None
                for item in otp_list:
                    if str(item.get("number")) == str(number) or str(item.get("phone")) == str(number):
                        otp_found = item.get("otp") or item.get("code")
                        break
                
                if otp_found:
                    await callback_query.message.reply_text(
                        f"🎉 **💥 BOOM! OTP RECEIVED SUCCESS!** 💥 🎉\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📞 **Phone Number:** `{number}`\n"
                        f"🔑 **OTP CODE:** `{otp_found}`\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"✨ *সফলভাবে ওটিপি চলে এসেছে! আমাদের বোট ব্যবহার করার জন্য ধন্যবাদ!* 🥰👑"
                    )
                    return
            except Exception:
                continue

        await callback_query.message.reply_text(
            f"⏱️ **🚨 TIME OUT ALERT!**\n\n`{number}` নাম্বারে ৩ মিনিটের ভেতর কোনো ওটিপি কোড আসেনি। নতুন করে আবার ট্রাই করুন। ❌"
        )

    except Exception as e:
        await callback_query.message.edit_text(f"💥 **⚠️ CRITICAL ERROR:** `{str(e)}` ⚙️")


if __name__ == "__main__":
    app.run()
      
