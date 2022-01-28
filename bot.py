from pyrogram import filters, Client
import logging
import os
from pyrogram.types import (
   ChatPermissions,
   InlineKeyboardButton,
   InlineKeyboardMarkup
)

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
TOKEN = os.environ.get("TOKEN", None)
TAG = os.environ.get("TAG", None)
OWNER_ID = int(os.environ.get("OWNER_ID", 1704673514))


tagcheck = Client(
   "tagcheck",
   bot_token=TOKEN,
   api_id=API_ID,
   api_hash=API_HASH
)


async def is_admin(message):
    user = await tagcheck.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ("administrator", "creator"):
      return True
    return False

@tagcheck.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(_, message):
   await message.reply("I am Alive.")

@tagcheck.on_message(filters.group)
async def tag_check(_, message):
    if await is_admin(message):
       return
    user = message.from_user.id
    if TAG not in message.from_user.first_name:
       try:
           await tagcheck.restrict_chat_member(
             message.chat.id,
             user,
             ChatPermissions(),
           )
       except BaseException as be:
           await message.reply(f"**Error:**\n`{be}`")
           return
       text = f"""
**Chào {message.from_user.mention}**
Vui lòng thêm thẻ hash của nhóm vào tên của bạn để
được phép chat trong nhóm.

**Thẻ hashtag:** `{TAG}`
**Note:** __Sau khi đã thêm thẻ hashtag vào tên. 
Bấm vào nút bên dưới để mở chat cho bản thân!__
"""
       await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Bật chat cho tôi", callback_data=f"unmute_{user}")]
           ]
         )
       )

@tagcheck.on_callback_query(filters.regex("unmute_(.*)"))
async def unmute(client, cb):
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
      await cb.answer("Nút này không dành cho bạn!", show_alert=True)
      return
    if TAG in cb.from_user.first_name:
      await tagcheck.unban_chat_member(cb.message.chat.id, user)
      await cb.answer("Đã mở chat thành công!")
      await message.delete()
      return
    await cb.answer("Vui lòng thêm hashtag vào tên của bạn!", show_alert=True)


tagcheck.run()
