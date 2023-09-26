from asyncio import Lock

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

bot = Bot(token='6319103400:AAEuv0bl6KFALVpDngLFT2wHcOxq5mVSRto', parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=MemoryStorage())

lock = Lock()

# класс для настройки машины состояний
class RegisterMessages(StatesGroup):
    step1 = State()
    step2 = State()
    photo = State()

class DB:
    answer_data = {}


@dp.message_handler(commands='start', state=None)
async def start(message: types.Message):
    await RegisterMessages.step1.set()
    await bot.send_message(message.from_user.id, text='Здравствуйте! Введите имя:')


@dp.message_handler(content_types='text', state=RegisterMessages.step1)
async def reg_step1(message: types.Message):
    async with lock:
        DB.answer_data['name'] = message.text
    await bot.send_message(message.from_user.id, text='Принято! Введите фамилию:')
    await RegisterMessages.next()


@dp.message_handler(content_types='text', state=RegisterMessages.step2)
async def reg_step2(message: types.Message, state: FSMContext):
    async with lock:
        DB.answer_data['surname'] = message.text
    await bot.send_message(message.from_user.id, text='Принято! введите фото')
    await RegisterMessages.next()
    
@dp.message_handler(content_types='photo', state=RegisterMessages.photo)
async def photo(message: types.Message, state: FSMContext):
    async with lock:
        DB.answer_data['photo'] = message.photo[0].file_id
        
    await bot.send_message(message.from_user.id, text='Принято! Чтобы посмотреть данные введите команду /check')
    await state.finish()

@dp.message_handler(commands='check')
async def get_reg_data(message: types.Message):
    answer = ''
    answer += f'Имя: {DB.answer_data["name"]}\n\n'
    answer += f'Фамилия: {DB.answer_data["surname"]}'
    
    await bot.send_photo(message.from_user.id, photo=DB.answer_data['photo'], caption=answer)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
#sites = ['твич', 'twitch']    
#@bot.message_handler(content_types=['text'])
#def site(message):
#    button = types.InlineKeyboardMarkup()
#    for site in sites:
#        if message.text.lower() == site:
#            btn1=types.InlineKeyboardButton('каша', url = 'https://www.twitch.tv/kussia88')
#            btn2=types.InlineKeyboardButton('стрей', url = 'https://www.twitch.tv/stray228')
#            btn3=types.InlineKeyboardButton('ростик', url = 'https://www.twitch.tv/rostislav_999')
#            btn4=types.InlineKeyboardButton('дерзко', url = 'https://www.twitch.tv/derzko69')
#            btn5=types.InlineKeyboardButton('кореш', url = 'https://www.twitch.tv/koreshzy')
#            btn6=types.InlineKeyboardButton('бустер', url = 'https://www.twitch.tv/buster')
#            button.row(btn1, btn2, btn3)
#            button.row(btn4, btn5, btn6)
#            #button.add(types.InlineKeyboardButton('каша', url = 'https://www.twitch.tv/kussia88'))
#            #button.add(types.InlineKeyboardButton('стрей', url = 'https://www.twitch.tv/stray228'))
#            #button.add(types.InlineKeyboardButton('ростик', url = 'https://www.twitch.tv/rostislav_999'))
#            #button.add(types.InlineKeyboardButton('дерзко', url = 'https://www.twitch.tv/derzko69'))
#            #button.add(types.InlineKeyboardButton('кореш', url = 'https://www.twitch.tv/koreshzy'))
#            #button.add(types.InlineKeyboardButton('бустер', url = 'https://www.twitch.tv/buster'))
#            #webbrowser.open('https://www.twitch.tv')
#            bot.send_message(message.chat.id, 'кого вы желаете посмотреть?', reply_markup=button) 
#    
#bot.polling(non_stop=True)
