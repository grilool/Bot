import time
import math
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils import formatting as fmt
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.methods import SendMessage
from aiogram.utils.markdown import hlink
import pymongo
import certifi
import re
from datetime import datetime as dt
from datetime import timedelta
import json
from request_usdt import *
from request_bitazza import *
from formula import *
from update import *
from Router_main import router
from Router_callback import router2
from Router_admin import router_admin
from mongo import *
from text import *
#Подключние к датабазе
#217.12.38.37
#client = pymongo.MongoClient("mongodb://AdminMongo:Grilool1234@localhost:27017/?authMechanism=SCRAM-SHA-1")
#server - root/ky7!Kmjk
#<=== Токен взятый с @BotFather
#TOKEN = "7178310446:AAH_wRJ0HA_-W79rl7EhO_ofJ0tHyeEuZ0o" #- Тестовая версия
#TOKEN = '7730333589:AAHJRyyRTzVnETA-QIc9hq4UFEM9oa89wc8' #- Версия для клиента
#TOKEN = "7929101245:AAH3tGuzbttTR_zTFbjdV9mqPmXF-fsudN8" # Misha
#TOKEN = '7760332515:AAHQF5y2GISNU34TMowVr6rGdB8Ful9NT3c' #Vladimir
TOKEN = '8089653515:AAGUWSTpB_ylGxTVDqipGlltLizio69v1IM' # Тестовая версия с реф системой
dp = Dispatcher()

#Логи
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',level=logging.INFO,stream=sys.stdout)


#Позиционирование пользователя
class value(StatesGroup):
    bat = State()
    rub = State()
    usdt = State()

class mess(StatesGroup):
    message_to_user_id = State()
    message_to_user = State()

#Start
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    k = message.text.replace('/start ', '')
    if message.text == '/start':
        result = users.find_one({'chatid': message.chat.id})
        if result == None:
            useradd = {
                'username': message.from_user.username,
                'chatid': message.chat.id,
                'FirstName': message.from_user.first_name,
                'LastName': message.from_user.last_name,
                'adm': 0,
                'price': 0,
                'banned': False,
                'rub_order': 0,
                'bat_order':0,
                'usdt_order': 0,
                'ref': 0,
                'latitude': 0,
                'longitude': 0,
                }
            results = users.insert_one(useradd)
            print(f"Add database id: {results.inserted_id}")
            text = text_menu
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Расчитать', callback_data = 'search')
            builder.button(text = 'Способы получения', callback_data = 'delivery')
            builder.button(text = 'Общая информация', callback_data = 'info')
            builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
            builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
            builder.adjust(1,1,1,1,1)
            await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
        elif result != None:
            text = text_menu
            if result['banned'] == True:
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
                await message.bot.send_message(chat_id = message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован', reply_markup = builder.as_markup())
            else:
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Расчитать', callback_data = 'search')
                builder.button(text = 'Способы получения', callback_data = 'delivery')
                builder.button(text = 'Общая информация', callback_data = 'info')
                builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
                builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
                builder.adjust(1,1,1,1,1)
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
    elif k.startswith('ref'):
        id = int(k.replace('ref', ''))
        result = users.find_one({'chatid': message.chat.id})
        res = users.find_one({'chatid': id})
        if message.chat.id == id:
            await message.answer('Вы не можете регистирироваться по своей реферальной ссылке')
        else:
            if result == None:
                useradd = {
                    'username': message.from_user.username,
                    'chatid': message.chat.id,
                    'FirstName': message.from_user.first_name,
                    'LastName': message.from_user.last_name,
                    'adm': 0,
                    'price': 0,
                    'banned': False,
                    'rub_order': 0,
                    'bat_order':0,
                    'usdt_order': 0,
                    'ref': id,
                    'latitude': 0,
                    'longitude': 0,
                    }
                results = users.insert_one(useradd)
                print(f"Add database id: {results.inserted_id}")
                text = text_menu
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Расчитать', callback_data = 'search')
                builder.button(text = 'Способы получения', callback_data = 'delivery')
                builder.button(text = 'Общая информация', callback_data = 'info')
                builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
                builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
                builder.adjust(1,1,1,1,1)
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
                await message.bot.send_message(chat_id = id, text = f"По Вашей реферальной ссылке зарегистрировался человек. \n@{message.from_user.username}")
            elif result != None and result['ref'] != 0:
                await message.answer('Вы уже были зарегистрированы по реферальной системе.')
            elif result != None and result['ref'] == 0:
                text = text_menu
                if result['banned'] == True:
                    builder = InlineKeyboardBuilder()
                    builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
                    await message.bot.send_message(chat_id = message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован', reply_markup = builder.as_markup())
                else:
                    find = {'chatid': message.chat.id}
                    change = {'$set': {'ref': id}}
                    users.update_one(find, change)
                    builder = InlineKeyboardBuilder()
                    builder.button(text = 'Расчитать', callback_data = 'search')
                    builder.button(text = 'Способы получения', callback_data = 'delivery')
                    builder.button(text = 'Общая информация', callback_data = 'info')
                    builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
                    builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
                    builder.adjust(1,1,1,1,1)
                    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
                    await message.bot.send_message(chat_id = id, text = f"По Вашей реферальной ссылке зарегистрировался человек. \n@{message.from_user.username}")

@dp.message(Command('profile'))
async def profile(message: Message):
    result = users.find_one({'chatid': message.chat.id})
    result = users.find_one({'chatid': message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await message.bot.send_message(chat_id = message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        bot_username = await message.bot.get_me()
        bot_username = bot_username.username
        link = f"http://t.me/{bot_username}?start=ref{message.chat.id}"
        k = []
        for res in users.find({'ref': message.chat.id}):
            k.append(res)
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Главное меню', callback_data = 'menu')
        text = f"Ваш ID <code>{message.chat.id}</code>"\
                f"\nБаланс: {result['price']} бат" \
                f"\nКол-во приглашенных пользователей: {len(k)}" \
                f"\nРеферальная ссылка:" \
                f"\n{link}"
        await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup())

#Menu
@dp.message(Command('menu'))
async def menu(message: Message):
    result = users.find_one({'chatid': message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await message.bot.send_message(chat_id = message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        text = text_menu
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Расчитать', callback_data = 'search')
        builder.button(text = 'Способы получения', callback_data = 'delivery')
        builder.button(text = 'Общая информация', callback_data = 'info')
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
        builder.adjust(1,1,1,1,1)
        await message.bot.send_message(message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode="HTML")

@dp.callback_query(lambda c: c.data == 'menu')
async def menu2(call: types.CallbackQuery):
    result = users.find_one({'chatid': call.message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await call.bot.send_message(chat_id = call.message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        text = text_menu
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Расчитать', callback_data = 'search')
        builder.button(text = 'Способы получения', callback_data = 'delivery')
        builder.button(text = 'Общая информация', callback_data = 'info')
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
        builder.adjust(1,1,1,1,1)
        await call.bot.edit_message_text(chat_id = call.message.chat.id,message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode="HTML")
    await call.bot.answer_callback_query(call.id)

#Расчет
@dp.callback_query(lambda c: c.data == 'search')
async def search(call: types.CallbackQuery):
    result = users.find_one({'chatid': call.message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await call.bot.send_message(chat_id = call.message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Батах', callback_data = 'Bat')
        builder.button(text = 'Рублях', callback_data = 'Rub')
        builder.button(text = 'USDT', callback_data = 'USDT')
        builder.button(text = 'Вернуться', callback_data = 'menu')
        builder.adjust(3,1)

        text = text_search
        await call.bot.edit_message_text(chat_id = call.message.chat.id , message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode="HTML")
    await call.bot.answer_callback_query(call.id)

#Доставка
@dp.callback_query(lambda c: c.data == 'delivery')
async def delivery(call: types.CallbackQuery):
    result = users.find_one({'chatid': call.message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await call.bot.send_message(chat_id = call.message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Расчитать', callback_data = 'search')
        builder.button(text = 'Общая информация', callback_data = 'info')
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
        builder.adjust(1,1,1,1)
        text = text_delivery
        await call.bot.edit_message_text(chat_id = call.message.chat.id , message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode="HTML")
    await call.bot.answer_callback_query(call.id)

#Общая информация
@dp.callback_query(lambda c: c.data == 'info')
async def info(call: types.CallbackQuery):
    result = users.find_one({'chatid': call.message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await call.bot.send_message(chat_id = call.message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован',reply_markup = builder.as_markup())
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Расчитать', callback_data = 'search')
        builder.button(text = 'Доставка', callback_data = 'delivery')
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
        builder.adjust(1,1,1,1)
        text = text_info
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = text_info, reply_markup = builder.as_markup())
    await call.bot.answer_callback_query(call.id)

#Запрос курса (баты)
@dp.callback_query(lambda c: c.data == 'Bat')
async def bat(call: types.CallbackQuery,state: FSMContext):
    result = users.find_one({'chatid':call.message.chat.id})
    adm = const.find_one({'id_id': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Вернуться', callback_data = 'menu')
    text = "Введите необходимую сумму бат." \
            "\n Без точек, запятых, слов" \
            f"\nМинимальная сумма {adm['bat_min']}" \
            "\n" \
            "\n Примеры:" \
            "\n10000" \
            "\n20000"
    await call.bot.send_message(chat_id = call.message.chat.id, text = text ,reply_markup = builder.as_markup(), parse_mode="HTML")
    await state.set_state(value.bat)
    await call.bot.answer_callback_query(call.id)

@dp.message(value.bat)
async def bat_step(message: types.Message, state: FSMContext):
        #поиск
        results = users.find_one({'chatid': message.chat.id})
        adm = const.find_one({'id_id': 1})
        curse = order.find_one({'curseid': 1})
        #Сообщение
        string = str(message.text)
        d = {'Спец.символы': 0, 'Буквы': 0, 'Цифры': 0}
        for i in string:
            if i.isalpha():
                d['Буквы'] += 1
            elif i.isdigit():
                d['Цифры'] += 1
            else:
                d['Спец.символы'] += 1
        bat_min = adm['bat_min']
        if d['Буквы'] > 0 or d['Спец.символы'] > 0:
            await message.bot.send_message(chat_id = message.chat.id, text = "Введите числовое значение без точек, запятых, слов.")
        if d['Буквы'] == 0 and d['Цифры'] > 0 and d['Спец.символы'] == 0:
            bat_order = int(message.text)
            if bat_order < bat_min:
                await message.bot.send_message(chat_id = message.chat.id, text = "Введенная сумма меньше минимальной. Введите сумму.")
            if bat_order >= bat_min:
                #Данные
                value = bat_rub(message.chat.id,bat_order)
                bat_order = value[0]
                n = value[1]
                sebes = value[2]
                cur_rub = value[3]
                cur_usdt = value[4]
                rub = value[5]
                usdt = value[6]
                bat_pro = value[7]
                rub_pro = value[8]
                usdt_pro = value[9]
                #кнопки
                k = []
                for t in temp.find({'chatid': message.chat.id}):
                    k.append(t)
                id = len(k) + 1
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Ввести другую сумму', callback_data = 'Bat')
                if bat_order >= 10000:
                    builder.button(text = 'Нужна доставка', callback_data = f"create_order_bat_delivery_{id}")
                builder.button(text = 'Получу через банкомат', callback_data = f"create_order_bat_bank_{id}")
                builder.button(text = 'Получить на тайский счет', callback_data = f"create_order_bat_score_{id}")
                builder.button(text = 'Главное меню', callback_data = 'menu')
                builder.adjust(1,1,1,1,1)
                #Отправка клиенту
                text = f"{bat_order} бат - {rub} руб" \
                        f"\nКурс: {cur_rub} руб/бат" \
                        f"\n" \
                        f"\n{bat_order} бат - {usdt} usdt" \
                        f"\nКурс: {cur_usdt} бат/usdt"

                await message.bot.send_message(chat_id = message.chat.id, text = text , reply_markup = builder.as_markup())

                await state.clear()
                #Обновление ордера в дб

                findchatid = {'chatid': message.chat.id}
                changeorder = {"$set": {'bat_order': bat_order}}
                users.update_one(findchatid, changeorder)

                #Отправка оператору
                for result in users.find({'adm': 1}):
                    request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={message.chat.id}")
                    data = 'message' + f"{message.chat.id}"
                    ls = hlink('Написать в лс', f"https://t.me/{message.from_user.username}")
                    builder = InlineKeyboardBuilder()
                    text = "Запросил Курс"\
                            f"\n@{message.from_user.username}" \
                            f"\n{message.from_user.full_name}" \
                            f"\n<code>{message.chat.id}</code>" \
                            f"\n{request}" \
                            "\n" \
                            f"\n{bat_order} бат" \
                            "\n"\
                            f"\nКурс:{cur_rub}" \
                            f"\n{rub} руб" \
                            "\n" \
                            f"\nКурс: {cur_usdt}" \
                            f"\n{usdt} usdt" \
                            "\n" \
                            f"\nСебеc: {sebes}" \
                            f"\n {curse['curse_bat']}"\
                            "\n" \
                            "\nПроцент накрутки" \
                            f"\n{n}" \
                            "\nПрофит:" \
                            f"\nRub: {rub_pro}" \
                            f"\nBat: {bat_pro}" \
                            f"\nUsdt: {usdt_pro}" \
                            "\n" \
                            f"\n{ls} "

                    await message.bot.send_message(chat_id = result['chatid'], text =text ,disable_web_page_preview=True)
            #Создание заказа в дб
            t = dt.utcnow()
            f = timedelta(hours = 3)
            time = t + f
            orderid = 'Temp' + f"{message.chat.id}"
            temporderadd = {
                    'orderid': orderid,
                    'id': id,
                    'bat': bat_order,
                    'fiat': 'bat',
                    'curse_usdt': cur_usdt,
                    'usdt': usdt,
                    'curse_rub': cur_rub,
                    'rub': rub,
                    'n': n,
                    'sebes': sebes,
                    'bat_pro': bat_pro,
                    'rub_pro': rub_pro,
                    'usdt_pro': usdt_pro,
                    'time': time,
                    'chatid': message.chat.id,
                }
            yes = temp.insert_one(temporderadd)

@dp.callback_query(F.data.startswith('create_order_bat'))
async def bat_order(call: types.CallbackQuery, state = FSMContext):
    await state.clear()
    u = call.data.replace("create_order_bat_", "")
    f = u.split("_")
    id = int(f[1])
    where = f[0]
    if where == 'delivery':
        wh = 'Способ получения: Доставка'
        wid = 'delivery'
    elif where == 'bank':
        wh = 'Способ получения: Банкомат'
        wid = 'bank'
    elif where == 'score':
        wh = 'Способ получения: На тайский счет'
        wid = 'score'
    for t in temp.find({'chatid': call.message.chat.id}):
        if t['id'] == id and t['fiat'] == 'bat':
            await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
            bat_order = t['bat']
            n = t['n']
            sebes = t['sebes']
            cur_rub = t['curse_rub']
            cur_usdt = t['curse_usdt']
            rub = t['rub']
            usdt = t['usdt']
            data1 = f"acces_order_bat_{id}_{call.message.chat.id}_{wid}_RUB"
            data2 = f"acces_order_bat_{id}_{call.message.chat.id}_{wid}_USDT"
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Подтвердить(RUB)', callback_data = data1)
            builder.button(text = 'Подтвердить(USDT)', callback_data = data2)
            builder.button(text = 'Главное меню', callback_data = 'menu')
            builder.adjust(1,1)
            text = "Подтвердите заказ" \
                    "\n" \
                    f"\n{bat_order} бат - {rub} руб" \
                    f"\nКурс:{cur_rub} руб/бат" \
                    "\n" \
                    f"\n{bat_order} бат - {usdt} usdt" \
                    f"\nКурс:{cur_usdt} usdt/бат" \
                    "\n" \
                    f"\n{wh}"
            await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
    await call.bot.answer_callback_query(call.id)







#Обработка запроса курса в батах (рубли - баты)
@dp.callback_query(lambda c: c.data == 'Rub')
async def rub(call: types.CallbackQuery,state: FSMContext):
    result = users.find_one({'chatid':call.message.chat.id})
    adm = const.find_one({'id_id': 1})
    #Кнопка
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Вернуться', callback_data = 'menu')
    text = "Введите сумму рублей, которые хотели бы обменять на баты" \
            "\n Без точек, запятых, слов" \
            f"\nМинимальная сумма {adm['rub_min']}" \
            "\n" \
            "\n Примеры:" \
            "\n50000" \
            "\n100000"

    await call.bot.send_message(chat_id = call.message.chat.id, text = text,reply_markup = builder.as_markup(), parse_mode="HTML")
    await state.set_state(value.rub)
    await call.bot.answer_callback_query(call.id)


#Создание курса rub - bat
@dp.message(value.rub)
async def rub_step(message: Message, state: FSMContext):
    results = users.find_one({'chatid': message.chat.id})
    curse = order.find_one({'curseid': 1})
    adm = const.find_one({'id_id': 1})
    string = str(message.text)
    d = {'Спец.символы': 0, 'Буквы': 0, 'Цифры': 0}
    for i in string:
        if i.isalpha():
            d['Буквы'] += 1
        elif i.isdigit():
            d['Цифры'] += 1
        else:
            d['Спец.символы'] += 1
    rub_min = adm['rub_min']
    if d['Буквы'] > 0 or d['Спец.символы'] > 0:
        await message.bot.send_message(chat_id = message.chat.id, text = "Введите числовое значение без точек, запятых, слов.")
    if d['Буквы'] == 0 and d['Цифры'] > 0 and d['Спец.символы'] == 0:
        rub_order = int(message.text)
        if rub_order < rub_min:
            await message.bot.send_message(chat_id = message.chat.id, text = "Введенная сумма меньше минимальной. Введите сумму.")
        if rub_order >= rub_min:
            #формулы
            value = rub_value(message.chat.id, rub_order)
            n = value[0]
            sebes = value[1]
            c = value[2]
            bat_pro = value[3]
            rub_pro = value[4]
            usdt_pro = value[5]
            bat = value[6]
            bat_order = value[7]
            #Отправка клиенту

            text = f"{rub_order} руб - {bat} бат" \
                    f"\nКурс: {c} бат/руб" \
                    f"\n"
            #кнопки
            k = []
            for t in temp.find({'chatid': message.chat.id}):
                k.append(t)
            id = len(k) + 1
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Ввести другую сумму', callback_data = 'Rub')
            if bat_order >= 10000:
                builder.button(text = 'Нужна доставка', callback_data = f"create_order_rub_delivery_{id}")
            builder.button(text = 'Получу через банкомат', callback_data = f"create_order_rub_bank_{id}")
            builder.button(text = 'Получить на тайский счет', callback_data = f"create_order_rub_score_{id}")
            builder.button(text = 'Главное меню', callback_data = 'menu')
            builder.adjust(1,1,1,1,1)
            await message.bot.send_message(chat_id = message.chat.id, text = text,reply_markup = builder.as_markup())
            await state.clear()

            #Обновление ордера в дб
            findchatid = {'chatid': message.chat.id}
            changeorder = {"$set": {'rub_order': rub_order}}
            users.update_one(findchatid, changeorder)

            #Отправка админу
            for result in users.find({'adm': 1}):
                request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={message.chat.id}")
                data = 'message' + f"{message.chat.id}"
                ls = hlink('Написать в лс', f"https://t.me/{message.from_user.username}")
                text = "Запросил Курс"\
                        f"\n@{message.from_user.username}" \
                        f"\n{message.from_user.full_name}" \
                        f"\n<code>{message.chat.id}</code>" \
                        f"\n{request}" \
                        "\n" \
                        f"\n{rub_order} руб" \
                        "\n" \
                        f"\nКурс:{c}" \
                        f"\n{bat} бат" \
                        "\n" \
                        f"\nСебеc: {sebes}" \
                        "\n" \
                        f"\nПроцент накрутки: {n}" \
                        "\nПрофит:" \
                        f"\nRub: {rub_pro}" \
                        f"\nBat: {bat_pro}" \
                        f"\nUsdt: {usdt_pro}" \
                        "\n" \
                        f"\n{ls} "

                await message.bot.send_message(chat_id = result['chatid'], text =text,parse_mode = 'HTML',disable_web_page_preview=True)
            #Создание временного заказа
            t = dt.utcnow()
            f = timedelta(hours = 3)
            time = t + f
            orderid = 'Temp' + f"{message.chat.id}"
            temporderadd = {
                    'orderid': orderid,
                    'id': id,
                    'rub_order': rub_order,
                    'fiat': 'rub',
                    'curse_bat': c,
                    'bat': bat,
                    'n': n,
                    'sebes': sebes,
                    'bat_pro': bat_pro,
                    'rub_pro': rub_pro,
                    'usdt_pro': usdt_pro,
                    'time': time,
                    'chatid': message.chat.id,
                }
            yes = temp.insert_one(temporderadd)

#Размещение ордера rub - bat
@dp.callback_query(lambda c: c.data.startswith('create_order_rub'))
async def create_order_rub(call: types.CallbackQuery):
    u = call.data.replace("create_order_rub_", "")
    f = u.split("_")
    id = int(f[1])
    where = f[0]
    if where == 'delivery':
        wh = 'Способ получения: Доставка'
        wid = 'delivery'
    elif where == 'bank':
        wh = 'Способ получения: Банкомат'
        wid = 'bank'
    elif where == 'score':
        wh = 'Способ получения: На тайский счет'
        wid = 'score'
    for t in temp.find({'chatid': call.message.chat.id}):
        if t['id'] == id and t['fiat'] == 'rub':
            await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
            rub_order = t['rub_order']
            n = t['n']
            sebes = t['sebes']
            cur_bat = t['curse_bat']
            bat = t['bat']
            data = f"acces_order_rub_{id}_{call.message.chat.id}_{wid}"
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Подтвердить', callback_data = data)
            builder.button(text = 'Главное меню', callback_data = 'menu')
            builder.adjust(1,1)
            text = "Подтвердите заказ" \
                    "\n" \
                    f"\n{rub_order} руб - {bat} бат" \
                    f"\nКурс: {cur_bat} бат/руб" \
                    "\n" \
                    f"\n{wh}"
            await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
    await call.bot.answer_callback_query(call.id)



#Запрос курса UDST

@dp.callback_query(lambda c: c.data == 'USDT')
async def usdt(call: types.CallbackQuery,state: FSMContext):
    adm = const.find_one({'id_id': 1})
    #Кнопка
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Вернуться', callback_data = 'menu')

    #Сообщение клиенту
    text = "Введите сумму usdt, которые хотели бы обменять на баты" \
            "\n Без точек, запятых, слов" \
            f"\nМинимальная сумма {adm['usdt_min']}" \
            "\n" \
            "\n Примеры:" \
            "\n500" \
            "\n1000"

    await call.bot.send_message(chat_id = call.message.chat.id, text = text,reply_markup = builder.as_markup(), parse_mode="HTML")
    await state.set_state(value.usdt)
    await call.bot.answer_callback_query(call.id)


#Создание курса USDT - BAT
@dp.message(value.usdt)
async def usdt_step(message: types.Message, state: FSMContext):
    results = users.find_one({'chatid': message.chat.id})
    curse = order.find_one({'curseid': 1})
    adm = const.find_one({'id_id': 1})
    string = str(message.text)
    d = {'Спец.символы': 0, 'Буквы': 0, 'Цифры': 0}
    for i in string:
        if i.isalpha():
            d['Буквы'] += 1
        elif i.isdigit():
            d['Цифры'] += 1
        else:
            d['Спец.символы'] += 1
    usdt_min = adm['usdt_min']
    if d['Буквы'] > 0 or d['Спец.символы'] > 0:
        await message.bot.send_message(chat_id = message.chat.id, text = "Введите числовое значение без точек, запятых, слов.")
    if d['Буквы'] == 0 and d['Цифры'] > 0 and d['Спец.символы'] == 0:
        usdt_order = float(message.text)
        if usdt_order < usdt_min:
            await message.bot.send_message(chat_id = message.chat.id, text = "Введенная сумма меньше минимальной. Введите сумму.")
        if usdt_order >= usdt_min:

            #Курс
            value = usdt_value(message.chat.id, usdt_order)
            n = value[0]
            c = value[1]
            sebes = value[2]
            bat = value[3]
            bat_pro = value[4]
            rub_pro = value[5]
            usdt_pro = value[6]
            bat_order = value[7]
            #Кнопки
            k = []
            for t in temp.find({'chatid': message.chat.id}):
                k.append(t)
            id = len(k) + 1
            create_order_usdt = 'create_order_usdt!' + f"{id}"
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Ввести другую сумму', callback_data = 'USDT')
            if bat_order >= 10000:
                builder.button(text = 'Нужна доставка', callback_data = f"create_order_usdt_delivery_{id}")
            builder.button(text = 'Получу через банкомат', callback_data = f"create_order_usdt_bank_{id}")
            builder.button(text = 'Получить на тайский счет', callback_data = f"create_order_usdt_score_{id}")
            builder.button(text = 'Главное меню', callback_data = 'menu')
            builder.adjust(1,1,1,1,1)
            text = f"\n{usdt_order} usdt - {bat} бат" \
                    f"\nКурс: {c} usdt/бат" \
                    f"\n"
            await message.bot.send_message(chat_id = message.chat.id, text =text, reply_markup = builder.as_markup())
            await state.clear()
            #Обновление ордера в дб

            findchatid = {'chatid': message.chat.id}
            changeorder = {"$set": {'usdt_order': usdt_order}}
            users.update_one(findchatid, changeorder)

            #Отправка оператору
            for result in users.find({'adm': 1}):
                request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={message.chat.id}")
                data = 'message' + f"{message.chat.id}"
                ls = hlink('Написать в лс', f"https://t.me/{message.from_user.username}")
                text = "Запросил Курс"\
                        f"\n@{message.from_user.username}" \
                        f"\n{message.from_user.full_name}" \
                        f"\n<code>{message.chat.id}</code>" \
                        f"\n{request}" \
                        "\n" \
                        f"\n{usdt_order} usdt" \
                        "\n" \
                        f"\n{bat} бат" \
                        f"\nКурс:{c} usdt/бат" \
                        "\n" \
                        f"\nСебеc: {sebes}" \
                        f"\nПроцент накрутки: {n}" \
                        "\nПрофит:" \
                        f"\nRub: {rub_pro}" \
                        f"\nBat: {bat_pro}" \
                        f"\nUsdt: {usdt_pro}" \
                        "\n" \
                        f"\n{ls} "
                await message.bot.send_message(chat_id = result['chatid'], text =text,parse_mode = 'HTML',disable_web_page_preview=True)
            #создание временного заказа
            t = dt.utcnow()
            f = timedelta(hours = 3)
            time = t + f
            orderid = 'Temp' + f"{message.chat.id}"
            temporderadd = {
                    'orderid': orderid,
                    'id': id,
                    'usdt_order': usdt_order,
                    'fiat': 'usdt',
                    'curse_usdt': c,
                    'bat': bat,
                    'n': n,
                    'sebes': sebes,
                    'bat_pro': bat_pro,
                    'rub_pro': rub_pro,
                    'usdt_pro': usdt_pro,
                    'time': time,
                    'chatid': message.chat.id,
                }
            yes = temp.insert_one(temporderadd)




#Размещение ордера bat - usdt
@dp.callback_query(lambda c: c.data.startswith('create_order_usdt'))
async def create_order_usdt(call: types.CallbackQuery):
    u = call.data.replace("create_order_usdt_", "")
    f = u.split("_")
    id = int(f[1])
    where = f[0]
    if where == 'delivery':
        wh = 'Способ получения: Доставка'
        wid = 'delivery'
    elif where == 'bank':
        wh = 'Способ получения: Банкомат'
        wid = 'bank'
    elif where == 'score':
        wh = 'Способ получения: На тайский счет'
        wid = 'score'
    for t in temp.find({'chatid': call.message.chat.id}):
        if t['id'] == id and t['fiat'] == 'usdt':
            await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
            usdt_order = t['usdt_order']
            n = t['n']
            c = t['curse_usdt']
            bat = t['bat']
            sebes = t['sebes']
            data = f"acces_order_usdt_{id}_{call.message.chat.id}_{wid}"
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Подтвердить', callback_data = data)
            builder.button(text = 'Главное меню', callback_data = 'menu')
            builder.adjust(1,1)
            text = "Подтвердите заказ" \
                    "\n" \
                    f"\n{usdt_order} usdt - {bat} бат" \
                    f"\nКурс:{c} usdt/бат" \
                    "\n" \
                    f"\n{wh}"
            await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
    await call.bot.answer_callback_query(call.id)




#Обработка геолокаций
@dp.callback_query(lambda c: c.data == 'test')
async def geo(call: types.CallbackQuery, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    data = call.message.text
    data = data.split("\n")
    data = data[0].split(" ")
    data = data[1]
    orderid = data.replace("№","")
    f = order.find_one({'orderid': orderid})
    findchatid = {'orderid': orderid}
    change_loc = {"$set": {'location': True}}
    order.update_one(findchatid, change_loc)


    builder.button(text = 'Отправить геолокацию', request_location = True)
    text = 'Кнопка снизу'
    await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
    #mid = call.message.message_id + 2
    #await call.bot.delete_message(chat_id = call.message.chat.id, message_id = mid)
    await call.bot.answer_callback_query(call.id)

@dp.message(F.location)
async def location_handler(message: types.Message):
    try:
        latitude = message.location.latitude
        longitude = message.location.longitude

        findchatid = {'chatid': message.chat.id, 'location': True}
        change_lat = {"$set": {'latitude': latitude}}
        order.update_one(findchatid, change_lat)

        findchatid = {'chatid': message.chat.id, 'location': True}
        change_long = {"$set": {'longitude': longitude}}
        order.update_one(findchatid, change_long)

        findchatid = {'chatid': message.chat.id, 'location': True}
        change_loc = {"$set": {'location': False}}
        order.update_one(findchatid, change_loc)

        await message.answer("Геолокация сохранена", reply_markup=types.ReplyKeyboardRemove())
    except:
        await message.answer("Ошибка в сохранение геолокации сообщите оператору",reply_markup=types.ReplyKeyboardRemove())



#Сообщение пользователю
@dp.callback_query(lambda c: c.data.startswith('message'))
async def ver(call: types.CallbackQuery,state: FSMContext):
    id = call.data.replace("message", "")
    id = int(id)
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена',callback_data='chancel_message')
    await call.bot.send_message(chat_id = call.message.chat.id, text ="Введите chat id пользователя", reply_markup = builder.as_markup(), parse_mode = "HTML")
    await state.set_state(mess.message_to_user_id)
    await call.bot.answer_callback_query(call.id)

@dp.message(F.text,mess.message_to_user_id)
async def message_to_user(message: types.Message, state: FSMContext):
    await state.update_data(message_to_user_id = message.text)
    await message.bot.send_message(chat_id = message.chat.id, text = 'Введите сообщение пользователю')
    await state.set_state(mess.message_to_user)

@dp.message(F.text,mess.message_to_user)
async def message_to_user(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    id = data.get("message_to_user_id")
    await message.bot.send_message(chat_id = id, text = text)
    await message.bot.send_message(chat_id = message.chat.id, text = 'Успешно отправлено')
    await state.clear()

@dp.callback_query(lambda c: c.data == 'chancel_message')
async def ch(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.bot.answer_callback_query(call.id)



#Список заказов
@dp.message(Command('orders'))
async def orderss(message: Message,state: FSMContext):
    await state.clear()
    await message.bot.send_message(chat_id = message.chat.id, text = 'Ваши активные заказы:')
    for res in order.find({'chatid': message.chat.id}):
        if res == None:
            await message.bot.send_message(chat_id = message.chat.id, text = 'У Вас нет активных заказов')
        elif res != None:
            if res['fiat'] == 'usdt':
                chanchel = 'chanchel_' + f"{message.chat.id}_" + f"{res['orderid']}"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Отменить заказ', callback_data = chanchel)
                text = f"\nЗаказ №{res['orderid']}" \
                        f"\n{res['usdt']} usdt" \
                        f"\nКурс: {res['curse']}" \
                        f"\n{res['bat']} бат" \
                        "\n"
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup =  builder.as_markup())
            if res['fiat'] == 'rub':
                chanchel = 'chanchel_' + f"{message.chat.id}_" + f"{res['orderid']}"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Отменить заказ', callback_data = chanchel)
                text = f"\nЗаказ №{res['orderid']}" \
                        f"\n{res['rub']} руб" \
                        f"\nКурс: {round(res['curse'], ndigits=3)}" \
                        f"\n{res['bat']} бат" \
                        "\n"
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup =  builder.as_markup())
            if res['fiat'] == 'bat_rub':
                chanchel = 'chanchel_' + f"{message.chat.id}_" + f"{res['orderid']}"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Отменить заказ', callback_data = chanchel)
                text = f"\nЗаказ №{res['orderid']}" \
                        f"\n{res['bat']} бат" \
                        f"\nКурс: {round(res['curse'], ndigits=3)}" \
                        f"\n{res['rub']} руб" \
                        "\n"
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup =  builder.as_markup())
            if res['fiat'] == 'bat_usdt':
                chanchel = 'chanchel_' + f"{message.chat.id}_" + f"{res['orderid']}"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Отменить заказ', callback_data = chanchel)
                text = f"\nЗаказ №{res['orderid']}" \
                        f"\n{res['bat']} бат" \
                        f"\nКурс: {round(res['curse'], ndigits=3)}" \
                        f"\n{res['usdt']} usdt" \
                        "\n"
                await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup =  builder.as_markup())

#Отмена заказа
@dp.callback_query(lambda c: c.data.startswith('chanchel'))
async def chan(call: types.CallbackQuery,state: FSMContext):
    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    data = call.data.replace("chanchel_", "")
    data = data.split('_')
    id = int(data[0])
    orderid = data[1]
    for res in order.find({'chatid':id}):
        if res['orderid'] == orderid:
            order.delete_one({'orderid': orderid})
    builder = InlineKeyboardBuilder().button(text = 'Главное меню', callback_data = 'menu')
    await call.bot.send_message(chat_id = id, text = f"Заказ №{orderid} отменен", reply_markup = builder.as_markup())
    for res in users.find({'adm': 1}):
        text = f"Заказ №{orderid} отменен"
        await call.bot.send_message(chat_id = res['chatid'],text = text)
    await call.bot.answer_callback_query(call.id)



#Закрытие бота
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router_admin)
    dp.include_router(router2)
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
