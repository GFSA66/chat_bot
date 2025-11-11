from config import TOKEN
from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio

# --- Список изображений ---
image_urls = [
    'https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg',
    'https://img.freepik.com/free-photo/portrait-blue-eyed-guy-ponders-something-stands-thoughtful-pose-holds-chin-concentrated-into-distance-wears-casual-orange-jumper_273609-45003.jpg?semt=ais_hybrid&w=740&q=80',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR7BJInEFu5z1e9itbPb6IPcGcO5mAVoFG5g&s',
]

# --- Инициализация бота ---
bot = AsyncTeleBot(TOKEN)

# --- Временное хранилище данных пользователей ---
storage = {}
user_image_index = {}  # сюда будем сохранять, какую картинку уже отправили


@bot.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Hello! I'm your friendly bot. How can I assist you today?")
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANvaRNXGomAMfb3EhnfLa4yNZJC95oAAhwAAw220hm0snpxGVuW0DYE')


@bot.message_handler(commands=["help"])
async def help(message: types.Message):
    help_text = (
        ''' 
Here are the commands you can use:
• /start — Start the bot
• /help — Show this help message
• /image — Send next image
'''
    )
    await bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['image'])
async def image(message: types.Message):
    user_id = message.from_user.id

    # Получаем текущий индекс, если нет — начинаем с 0
    index = user_image_index.get(user_id, 0)

    # Отправляем текущую картинку
    await bot.send_photo(message.chat.id, image_urls[index], caption=f"📸 Image {index + 1}/{len(image_urls)}")

    # Обновляем индекс (следующая картинка, циклично)
    next_index = (index + 1) % len(image_urls)
    user_image_index[user_id] = next_index


@bot.message_handler()
async def query(message: types.Message):
    try:
        text = message.text.lower()
        storage[message.from_user.id] = text

        if 'привет' in text:
            return await bot.send_message(message.chat.id, 'Привет! Как я могу помочь?')
        elif 'как дела' in text:
            return await bot.send_message(message.chat.id, 'У меня всё хорошо, спасибо! А у вас?')
        elif 'проверка' in text:
            return await bot.send_message(message.chat.id, 'Проверка прошла успешно!')
        elif 'хз' in text:
            return await bot.send_message(message.chat.id, 'тут точно не знаю что ответить')
        else:
            return await bot.send_message(message.chat.id, 'Я пока не понимаю это сообщение 😅')

    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, f"Ошибка: {str(e)}")


@bot.message_handler(content_types=['sticker'])
async def get_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    await bot.send_message(message.chat.id, sticker_id)


async def main():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())
