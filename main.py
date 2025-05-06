# main.py
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, VIP_LINK
import pytesseract
from PIL import Image
import os

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("បង់លុយ $0.50", url="https://pay.ababank.com/AZGf2mpuTsw2bVtV8"))
    await message.reply("សូមបង់ប្រាក់ $0.50 ដោយស្កេន QR ឬចុចប៊ូតុងខាងក្រោម។\nបន្ទាប់មក បញ្ចូនរូប slip មកទីនេះ។", reply_markup=keyboard)

@dp.message_handler(content_types=['photo'])
async def process_slip(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    os.makedirs("downloads", exist_ok=True)
    photo_path = f"downloads/{photo.file_id}.jpg"
    await photo.download(destination_file=photo_path)

    try:
        image = Image.open(photo_path)
        text = pytesseract.image_to_string(image)

        if "0.50" in text or "0.5" in text:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("ចូល VIP", url=VIP_LINK))
            await message.reply("✅ បង់ប្រាក់ត្រឹមត្រូវ!\nចូល VIP Channel:", reply_markup=keyboard)
        else:
            await message.reply("❌ Slip មិនមានប្រាក់ $0.50 សូមពិនិត្យឡើងវិញ។")
    except Exception as e:
        await message.reply("❌ មានបញ្ហាក្នុងការអាន slip។ សូមសាកល្បងម្ដងទៀត។")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
