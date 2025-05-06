# main.py
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, VIP_LINK

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("បង់លុយ $0.50", url="https://pay.ababank.com/AZGf2mpuTsw2bVtV8"),
        types.InlineKeyboardButton("ចូល VIP", url=VIP_LINK)
    )
    await message.reply(
        "សូមបង់ប្រាក់ $0.50 ដើម្បីចូល VIP Channel។\nចុចប៊ូតុងខាងក្រោម៖",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
