from aiogram import Bot, Dispatcher, executor, types # aiogram
import os
import asyncio
import dotenv # python-dotenv
import pyautogui # pyautogui
import win32api # pywin32

# /start : starts the chat with the bot
# /subscribe : subscribes this chat to the current execution of the bot (to redo when turned-off)

''' .env
TOKEN=345sfdsey5drgfre5hr5
FILE_PATH=./temp.png
'''

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
FILE_PATH = os.getenv("FILE_PATH")

chats = []
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.reply(f"Bot active, chat {message.chat.id}")

@dp.message_handler(commands='subscribe')
async def subscribe_cmd_handler(message: types.Message):
    chats.append(message.chat.id)
    print("chats", chats)
    await message.reply(f"Chat {message.chat.id} subscribed")

async def screenshot():
    pressure = 0 # counter to register duration of click
    interval = 1 # interval needed to take screenshot
    freq = 4 # frequency of checks of the left-click
    while True:
        await asyncio.sleep(interval / freq)
        s = win32api.GetKeyState(0x01)
        if s in [-128, -127]:
            pressure += 1
        else:
            pressure = 0
        if pressure >= freq:
            pressure = 0
            image = pyautogui.screenshot()
            image.save(FILE_PATH)
            if len(chats) == 0:
                print("no subscribers!")
            for chat in chats:
                await bot.send_photo(chat, types.InputFile(FILE_PATH))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(screenshot())
    executor.start_polling(dp, skip_updates=True)
    
