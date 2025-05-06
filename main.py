# main.py
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, VIP_LINK, FREE_LINK
import pytesseract
from PIL import Image
import os

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("មើលវីដេអូ Free", url=FREE_LINK),
        types.InlineKeyboardButton("បង់លុយ $0.50 ដើម្បីចូល VIP", url="https://pay.ababank.com/AZGf2mpuTsw2bVtV8")
    )
    with open("qr_code.png", "rb") as qr:
        await message.reply_photo(qr, caption="សូមមើលវីដេអូ Free ឬបង់ប្រាក់ $0.50 ដើម្បីចូល VIP Channel។\nបន្ទាប់បង់ប្រាក់ សូមបញ្ជូន slip មកទីនេះ។", reply_markup=keyboard)

@dp.message_handler(content_types=['photo'])
async def check_slip(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    photo_path = f"downloads/{photo.file_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    await photo.download(destination_file=photo_path)

    try:
        text = pytesseract.image_to_string(Image.open(photo_path))
        if ("0.50" in text and "USD" in text) and ("066 451 539" in text or "Loem Vireak" in text):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("ចូល VIP Channel", url=VIP_LINK))
            await message.reply("✅ បង់ប្រាក់ត្រឹមត្រូវ! ចូល VIP Channel:", reply_markup=keyboard)
        else:
            await message.reply("❌ Slip មិនត្រឹមត្រូវ។ សូមពិនិត្យប្រាក់ $0.50 និង To Account/Name.")
    except Exception:
        await message.reply("❌ មានបញ្ហាក្នុងការអាន slip។ សូមសាកល្បងម្ដងទៀត។")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
