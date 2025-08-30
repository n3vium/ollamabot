import configparser, asyncio, time, logging, shutil, signal, os
from telebot.async_telebot import AsyncTeleBot
from modules.api import api_call
from colorama import init, Fore, Back, Style


# конфиг
config = configparser.ConfigParser()
config.read('config')
token = config['Bot']['token']
url = config['Api']['url']
version = 1.0
fold=['chats']

bot = AsyncTeleBot(token)

# инит логов и цветов
init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt='[%d.%m.%Y] [%H:%M:%S]',
    encoding='utf-8',
    handlers=[
        logging.FileHandler("logs", "w"),
        logging.StreamHandler()
    ]
)

# ещё немножечко логов
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('werkzeug').disabled = True

print(Fore.GREEN + f'AiSLOP {version}'.center(shutil.get_terminal_size().columns))
logging.info('Бот запущен.')

# основной функционал

@bot.message_handler(commands=['start'])
async def handle_start(message):
    await bot.reply_to(message, "Привет")

# хэндлер выводящий "сырое" сообщение
# @bot.message_handler(commands=['raw'])
# async def handle_raw(message):
#    await bot.reply_to(message, f'{message}')

@bot.message_handler(func=lambda message: True)
async def handle_text(message):
    user = message.chat.id
    await bot.send_chat_action(user, 'typing')

    sender = message.from_user.full_name
    user_prompt = f"{sender}: {message.text}"
    ai_response = await asyncio.to_thread(api_call, url, user_prompt)

    await bot.reply_to(message, ai_response)
    
# работа с ботом
def handle_stop(sig, frame):
    logging.info("Received shutdown signal.")
    for task in asyncio.all_tasks():
        task.cancel()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.infinity_polling()

if __name__ == "__main__":
    # сигналыыы
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received.")
    except Exception as e:
        logging.exception(f"Unexpected exception: {e}")
    