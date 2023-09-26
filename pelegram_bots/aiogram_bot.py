import datetime
import aiogram
from aiogram import Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import random
import webbrowser
from asyncio import Lock
#from aiogram.enums.dice_emoji import DiceEmoji
#from aiogram.dispatcher.filters import BoundFilter

#from aiogram.fsm.context import FSMContext
class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    phone = State()
    
class DB:
    full_user_info = {}
    
    
bot1 = aiogram.Bot(token='6319103400:AAEuv0bl6KFALVpDngLFT2wHcOxq5mVSRto', parse_mode='HTML')
dp = Dispatcher(bot=bot1, storage=MemoryStorage())
lock = Lock()
but = ReplyKeyboardMarkup
count = 0
#переменные с балансом и списком значений для казно
bal = 1000

letters = ['A', 'C', 'D', 'V', 'W']
def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

def get_y() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('/youtube'))
    return keyboard

def get_youtube_find() -> ReplyKeyboardMarkup:
    find = ReplyKeyboardMarkup(resize_keyboard=True)
    find.add(KeyboardButton('/valorant'))
    find.add(KeyboardButton('/programming'))
    return find

def get_valorant():
    val = ReplyKeyboardMarkup(resize_keyboard=True)
    val.add(KeyboardButton('/valorant_highlights'))
    val.add(KeyboardButton('/valorant_news'))
    return val
def get_valorant_pers() -> InlineKeyboardMarkup:
    pers = InlineKeyboardMarkup()
    pers.add(InlineKeyboardButton('сейдж', url='https://www.youtube.com/results?search_query=valorant+highlights+on+sage'))
    pers.add(InlineKeyboardButton('рейна', url='https://www.youtube.com/results?search_query=valorant+highlights+on+reyna'))
    pers.add(InlineKeyboardButton('рейз', url='https://www.youtube.com/results?search_query=valorant+highlights+on+raze'))
    return pers

def get_valorant_news():
    news = InlineKeyboardMarkup()
    news.add(InlineKeyboardButton('valorant_news', url='https://playvalorant.com/ru-ru/news/'))
    return news

@dp.message_handler(commands=['valorant_highlights'])  
async def valorants(message: types.Message):
    await message.answer('highlights on', reply_markup=get_valorant_pers()) 

@dp.message_handler(commands=['valorant_news'])
async def valorant_news(message: types.Message):
    await message.answer('news', reply_markup=get_valorant_news())
@dp.message_handler(commands=['valorant'])
async def valoran(message: types.Message):
    await message.answer('valorant info', reply_markup=get_valorant())
@dp.message_handler(commands=['twich'])
async def twich(message: types.Message):
    two = message.text.split()[1]
    await webbrowser.open('https://www.twitch.tv/' + two)
@dp.message_handler(commands=['website'])
async def back(message: types.Message):
    await message.answer('open' , reply_markup=get_y())
@dp.message_handler(commands=['youtube'])   
async def youtube(message: types.Message):
    
    await message.answer('что бы вы хотели посмотреть?')
    
    
    await message.answer('open', reply_markup=get_youtube_find())
    

@dp.message_handler(commands=['id'])
async def user_id(message: types.Message):
    userid = message.from_user.id
    await message.answer(f'ваш айди {userid}')

@dp.message_handler(commands=['new_chat_members'])
async def new_user(message: types.Message):
    newuser = message.new_chat_members[0].first_name
    bot1.send_message(message.chat.id, f'nice to see you in our server{newuser}')
#создаем казино
@dp.message_handler(commands=['casino'])
async def casino(message: types.Message):
    s = random.choices(letters, k=3)
    #s = ['A','A','A']
    #await message.answer(s)
    global bal
    if bal<=0:
        StopAsyncIteration
        StopIteration
        
    else:
        await message.answer(s)
        if s == ['A','A','A']:
            #await message.answer('+500')
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '+500')

            bal +=500
            await message.answer(bal)
        #elif choise == ['B','B','B']:
        #    print(choise)
        #    print('+1500')
        #    bal+=1500
        #    print(bal)
        elif s == ['C','C','C']:
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '+1000')

            bal +=1000
            await message.answer(bal)
        elif s == ['D','D','D']:
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '+1500')

            bal +=1500
            await message.answer(bal)
        elif s == ['V','V','V']:
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '+2000')

            bal +=2000
            await message.answer(bal)
        elif s == ['W','W','W']:
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '+2500')

            bal +=2500
            await message.answer(bal)
        else:
            await message.answer(s)
            await bot1.send_message(message.from_user.id, '-200')

            bal -= 200
            await message.answer(bal)
@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer('welcome', reply_markup=get_kb())


@dp.message_handler(content_types='text', commands= ['create'])
async def create_profile(message: types.Message):
    #await message.reply('send me your photo for registration')
    #await ProfileStatesGroup.photo.set()
    await ProfileStatesGroup.photo.set()
    await bot1.send_message(message.from_user.id, text='Здравствуйте! пришлите фото:')
@dp.message_handler(content_types= ['photo'], state=ProfileStatesGroup.photo)
async def photo(message: types.Message, state: FSMContext) -> None:
    #async with state.proxy() as data:
    async with lock:
        #data['photo'] = message.photo[0].file_id
        DB.full_user_info['photo'] = message.photo[0].file_id
    await message.reply('введите имья')
    await ProfileStatesGroup.next()

@dp.message_handler(content_types='text', state=ProfileStatesGroup.name)
async def name(message: types.Message, state: FSMContext):
    async with lock:
        #data['name'] = message.text
        DB.full_user_info['name'] = message.text
    await bot1.send_message(message.from_user.id, text='Принято! Введите номер телефона:')
    await ProfileStatesGroup.next()
    
@dp.message_handler(state=ProfileStatesGroup.phone)
async def phone(message: types.Message, state: FSMContext):
    async with lock:
        #data['phone'] = message.text
        DB.full_user_info['phone'] = message.text
    
    
    await message.reply('your anket is creat')
    await state.finish()
@dp.message_handler(commands=['user_info'])
async def user_info(message: types.Message):
    answer = ''
    answer += f'Name: {DB.full_user_info["name"]}\n\n'
    answer += f'phone number: {DB.full_user_info["phone"]}'
    await bot1.send_photo(message.from_user.id, photo=DB.full_user_info["photo"], caption=answer)
@dp.message_handler(commands=['info'],)
async def start(message: types.Message):
    global count
    #time = int(message.text.split()[1])
    if count >= 6:
        dt = datetime.datetime.now() + datetime.timedelta(hours=0.001)
        timestamp = dt.timestamp()
        await bot1.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False, until_date=timestamp, permissions=True)
        count = 0
    else:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_full_name = message.from_user.full_name
        await message.answer_sticker('CAACAgIAAxkBAAIBG2Tl6ixykvh0x_qWIdab3IBX3ss1AAJ0DAACtrs4S47Op8xAxIAlMAQ')
        await message.answer(f'hello {user_full_name}')
        await message.answer(f'{user_name}`s id: {user_id}')
        if user_name == 'Maxim':
            await message.reply(f'nice to met you')
        await message.answer(f'количевство взовов {count}')
    count +=1
if __name__ == '__main__':    
    executor.start_polling(dispatcher=dp, skip_updates=True)
#@dp.message_handler(commands=['info'])
#async def info(message: types.Message):
#    user_id = message.from_user.id
#    user_name = message.from_user.first_name
#    user_username = message.from_user.username
#    await message.reply(f'your id --> {user_id}')
#    await message.reply(f'your name --> {user_name}')
#    await message.reply(f'your username --> {user_username}')
##@dp.message_handler(content_types=['document', 'photo'])
##async def check_server_id(message: types.Message):
##    await message.answer(message.sticker.file_id)
##    await bot1.send_message(message.from_user.id, message.chat.id)
#@dp.message_handler(commands=['id'])
#async def chat_id(message: types.Message):
#    i= 0
#    while i <= 10:
#        time.sleep(1)
#        await message.answer(f'hello {message.from_user.username}')
#        i += 1
#@dp.message_handler(content_types=['sticker'])
#async def check_id(message: types.Message):
#    await message.answer(message.sticker.file_id) 
#    await bot1.send_message(message.from_user.id, message.chat.id)  
#
