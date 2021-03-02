import logging
import requests
import aioschedule
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import BOT_TOKEN
from states.position import Position
from keyboards import reply_key as rk



logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

id_usersname = {}
otchet, otchet1, otchet2, otchet3 = {}, {}, {}, {}
python_csv, python_even_csv, python_otchet= set(), set(), set()

async def python_file():
    try:
        f = open("user_id.csv", "r")
        f1 = f.readlines()
        for i in f1:
            python_csv.add(i)
            print(python_csv)
    except Exception as e:
        print(e)


async def python_even_file():
    try:
        f = open("user_even.csv", "r")
        f1 = f.readlines()
        for i in f1:
            python_even_csv.add(i)
            print(python_even_csv)
    except Exception as e:
        print(e)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        chat_id = str(message.chat.id)
        name = message.chat.first_name
        id_usersname.setdefault(chat_id, name)
        with open('otchet.csv', 'r') as f_otchet:
            reader = f_otchet.readlines()
            reader = [name.strip() for name in reader]
            faile = []
            print(reader)
            print(id_usersname)
            for name in id_usersname.keys():
                print(name)
                if name not in reader:
                    faile.append(name)
            if faile != []:
                await bot.send_message(message.chat.id, "Добро пожаловать 👋\nВыберите группу в которой вы учитесь👨‍💻", reply_markup=rk.key_group)
                await Position.Q1.set()
            else:
                await bot.send_message(message.chat.id, 'Вы уже прошли StandUp👍🏽')
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    try:
        otchet3[message.chat.first_name] = message.text
        async with state.proxy() as data:
            data['Q1'] = message.text
        if message.text == 'Python vol. 10' or message.text == 'Python vol. 9' or message.text == 'JavaScript vol. 10' or message.text == 'JavaScript vol. 9':
            await bot.send_message(message.chat.id, "Привет! Хотите пройти Stand Up?", reply_markup=rk.keyboard)
            await write_to_csv(message)
            await Position.Q2.set()
        elif message.text == 'Python-10. Even' or message.text == 'Python-9. Even':
            await bot.send_message(message.chat.id, "Привет! Хотите пройти Stand Up?", reply_markup=rk.keyboard)
            await write_even_to_csv(message)
            await Position.Q2.set()
        else:
            await bot.send_message(message.chat.id, f'{message.chat.first_name}, не играйтесь!😠')
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Q2'] = message.text
        if message.text == 'Да':
            await bot.send_message(message.chat.id, 'Хорошо! Что было сделано?')
            await Position.Q3.set()
        else:
            await bot.send_message(message.chat.id, f'{message.chat.first_name}, не играйтесь!😠')
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    try:
        otchet[message.chat.first_name] = message.text
        async with state.proxy() as data:
            data['Q3'] = message.text
        await bot.send_message(message.chat.id, f"{message.from_user.first_name}, какие у вас планы?")
        await Position.Q4.set()
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    try:
        otchet1[message.chat.first_name] = message.text
        await write_to_otchet(message)
        async with state.proxy() as data:
            data['Q4'] = message.text
        await bot.send_message(message.chat.id, f"{message.from_user.first_name}, какие затруднения у вас возникли?")
        await Position.Q5.set()
    except Exception as e:
        print(e)

@dp.message_handler(state=Position.Q5)
async def answer_q5(message: types.Message, state: FSMContext):
    try:
        otchet2[message.chat.first_name] = message.text
        async with state.proxy() as data:
            data['Q5'] = message.text
        await bot.send_message(message.chat.id, f"{message.from_user.first_name}, спасибо, что прошли StandUp😁")
        requests.post(url='http://34.64.233.41/api/add/', data={"group": otchet3.get(message.chat.first_name), \
                                                                      "user_name": message.chat.first_name, \
                                                                      "done": otchet.get(message.chat.first_name), \
                                                                      "todo": otchet1.get(message.chat.first_name), \
                                                                      "problems": otchet2.get(message.chat.first_name)})
        await state.finish()
    except Exception as e:
        print(e)


async def write_to_csv(message):
    try:
        chat_id = str(message.chat.id)
        file_name = 'user_id.csv'
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)


async def write_even_to_csv(message):
    try:
        chat_id = message.chat.id
        file_name = 'user_even.csv'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)


async def write_to_otchet(message):
    try:
        chat_id = str(message.chat.id)
        file_name = 'otchet.csv'
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)


async def clear_otchet():
    try:
        with open('otchet.csv', 'w') as f_clear:
            clearer = f_clear.write('')
            return clearer
    except Exception as e:
        print(e)


async def python_to_run():
    try:
        for i in python_csv:
            await bot.send_message(i, 'Пришло время пройти /start', parse_mode='markdown')
    except Exception as e:
        print(e)


async def python_even_to_runun():
    try:
        for i in python_even_csv:
            await bot.send_message(i, 'Пришло время пройти /start', parse_mode='markdown')
    except Exception as e:
        print(e)


async def scheduler():
    try:
        aioschedule.every().day.at("04:10").do(clear_otchet)
        aioschedule.every().day.at("04:10").do(python_to_run)
        aioschedule.every().day.at("04:10").do(python_file)

        aioschedule.every().day.at("12:30").do(clear_otchet)
        aioschedule.every().day.at("12:30").do(python_even_to_runun)
        aioschedule.every().day.at("12:30").do(python_even_file)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception as e:
        print(e)

async def on_startup(x):
    try:
        asyncio.create_task(scheduler())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
