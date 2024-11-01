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
from mongo import *

router_admin = Router()

class change(StatesGroup):
    nak = State()
    min_bat = State()
    shag = State()
    nak_10 = State()
    nak_200 = State()

class create_url(StatesGroup):
    id = State()
    percent = State()

#Панель админа
@router_admin.message(Command('adm'))
async def men_adm(message: types.Message, state: FSMContext):
    await state.clear()
    #Поиск в базе данных
    user = users.find_one({'chatid': message.chat.id})
    orders = order.find_one({'curseid': 1})
    min = const.find_one({'id_id': 1})

    #Кнопки для админа
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Накрутка', callback_data = 'nak')
    builder.button(text = 'Мин бат', callback_data = 'min_bat')
    builder.button(text = 'Шаг', callback_data = 'shag')
    builder.button(text = 'Наркутка до 10к', callback_data = 'nak_10')
    builder.button(text = 'Наркутка от 200к', callback_data = 'nak_200')
    builder.button(text = 'Статистика', callback_data = 'static')
    builder.button(text = 'Информация по значениям', callback_data = 'information_for_db')
    builder.button(text='Создание реферальной ссылки', callback_data='create_ref_url')
    builder.adjust(3, 1, 1, 1, 1, 1)
    #   builder.button(text = 'Бан', callback_data = 'bann')
    text = "<b>                       Панель Администратора              </b>" \
            "\n<b>Здесь можно изменить значения в Базе данных</b>" \
            "\nКнопка <b>Накртука</b> изменяет процент накрутки" \
            "\nКнопка <b>Мин бат</b> изменяет минимальную сумму заказа для всех валют" \
            "\nКнопка <b>Шаг изменяет</b> шаг для значений накрутки от 10к до 200к" \
            "\nКнопка <b>Наркутка от 10к</b> изменяет процент накрутки от 10к" \
            "\nКнопка <b>Наркутка до 200к</b> изменяет процент накрутки до 200к" \
            "\nКнопка <b>Статистика</b> выводит статистику по боту" \
            "\nКнопка <b>Информация по значениям</b> выводит курсы валют, проценты накруток"
    if user['adm'] == 1:
        await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')

@router_admin.callback_query(lambda c: c.data == 'adm')
async def men_adm(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    #Поиск в базе данных
    user = users.find_one({'chatid': call.message.chat.id})
    orders = order.find_one({'curseid': 1})
    min = const.find_one({'id_id': 1})

    #Кнопки для админа
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Накрутка', callback_data = 'nak')
    builder.button(text = 'Мин бат', callback_data = 'min_bat')
    builder.button(text = 'Шаг', callback_data = 'shag')
    builder.button(text = 'Наркутка до 10к', callback_data = 'nak_10')
    builder.button(text = 'Наркутка от 200к', callback_data = 'nak_200')
    builder.button(text = 'Статистика', callback_data = 'static')
    builder.button(text = 'Информация по значениям', callback_data = 'information_for_db')
    builder.button(text = 'Создание реферальной ссылки', callback_data = 'create_ref_url')
    builder.adjust(3,1,1,1,1,1)
    text = "<b>                       Панель Администратора              </b>" \
            "\n<b>Здесь можно изменить значения в Базе данных</b>" \
            "\nКнопка <b>Накртука</b> изменяет процент накрутки" \
            "\nКнопка <b>Мин бат</b> изменяет минимальную сумму заказа для всех валют" \
            "\nКнопка <b>Шаг изменяет</b> шаг для значений накрутки от 10к до 200к" \
            "\nКнопка <b>Наркутка до 10к</b> изменяет процент накрутки до 10к" \
            "\nКнопка <b>Наркутка от 200к</b> изменяет процент накрутки от 200к" \
            "\nКнопка <b>Статистика</b> выводит статистику по боту" \
            "\nКнопка <b>Информация по значениям</b> выводит курсы валют, проценты накруток"
    if user['adm'] == 1:
        await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)

@router_admin.callback_query(F.data == 'create_ref_url')
async def url_ref_start(call: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    await call.bot.edit_message_text(chat_id = call.message.chat.id,message_id = call.message.message_id, text = 'Введите id пользователя для создания реферальной ссылки.', reply_markup = builder.as_markup())
    await state.set_state(create_url.id)

@router_admin.message(create_url.id)
async def url_ref_id(message: Message, state: FSMContext):
    try:
        id = int(message.text)
        await state.update_data(id = id)
        await message.bot.send_message(chat_id = message.chat.id, text = 'Введите процент отчислений. Где 1 = 100%, а 0.001 = 0.1 процента')
        await state.set_state(create_url.percent)
    except:
        await message.answer('Значение должно быть числом')

@router_admin.message(create_url.percent)
async def url_ref_percent(message: Message, state: FSMContext):
    try:
        percent = float(message.text)
        await state.update_data(percent = percent)
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Подтвердить', callback_data = 'add_ref_url')
        builder.button(text = 'Панель админа', callback_data = 'adm')
        await message.bot.send_message(chat_id = message.chat.id, text = 'Подтвердите создание ссылки для пользователя.', reply_markup = builder.as_markup())
    except:
        await message.answer('Значение должно быть числом')

@router_admin.callback_query(F.data == 'add_ref_url')
async def url_ref_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    count = 0
    for i in urls.find():
        count += 1
    data['uid'] = count
    urls.insert_one(data)
    bot_username = await call.bot.get_me()
    bot_username = bot_username.username
    link = link = f"http://t.me/{bot_username}?start=ref{data['id']}I{data['uid']}"
    text = f"Реферальная ссылка: {link}" \
            f"\nПроцент {data['percent']}"
    await call.bot.send_message(chat_id = call.message.chat.id, text = text)
    await state.clear()
    await call.bot.answer_callback_query(call.id)






@router_admin.callback_query(F.data == 'static')
async def static(call: types.CallbackQuery):
    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    d = dt.utcnow()
    f = timedelta(hours = 3)
    d = d + f
    day = d.strftime("%d")
    year = d.strftime("%Y")
    month = d.strftime("%m")
    date = f"{day}{month}{year}"
    print(date)
    k = []
    orders = []
    orders_today = []
    for res in users.find():
        k.append(res)
    for l in order.find().skip(1):
        orders.append(l)
        if l['date'] == date:
            orders_today.append(l)

    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    text = f"Всего зарегестрированных пользователей: {len(k)}" \
            f"\nСоздано заказов за все время: {len(orders)}" \
            f"\nСоздано заказов за сегодня: {len(orders_today)}"
    await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())

@router_admin.callback_query(F.data == 'information_for_db')
async def information_for_db(call: types.CallbackQuery):
    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    orders = order.find_one({'curseid': 1})
    min = const.find_one({'id_id': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    text = f"Миниильный заказ <b>руб</b>: {min['rub_min']}" \
            f"\nМиниильный заказ <b>бат</b>: {min['bat_min']}" \
            f"\nМиниильный заказ <b>usdt</b>: {min['usdt_min']}" \
            "\n" \
            "\n<b>Текущие курсы</b>" \
            f"\nКурс {orders['curse_rub']} бат/руб (Без наценки)" \
            f"\nКурс {round((float(orders['curse_rub']) * float(orders['nakrutka_10'])), ndigits = 3)} бат/руб (С максимальной накруткой)" \
            f"\nКурс {orders['curse_usdt']} руб/usdt" \
            f"\nКурс битазза {orders['curse_bitazza']}" \
            f"\nКурс {orders['curse_bat']} bat/usdt" \
            "\n" \
            "\n<b>Текущие проценты накрутки</b>" \
            f"\nНакрутка до 10к - {orders['nakrutka_10']}" \
            f"\nНакрутка от 10к до 200к - {orders['nakrutka']} - {orders['nakrutka_200']}" \
            f"\nШаг накрутки - {orders['shag']}" \
            f"\nНакрутка от 200к - {orders['nakrutka_200']}"
    await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())





@router_admin.callback_query(lambda c: c.data == 'nak')
async def nak(call: types.CallbackQuery,state: FSMContext):
    orders = order.find_one({'curseid': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    text = "\nТекущий процент накрутки:" \
            f"\n{orders['nakrutka']}" \
            "\nДля изменения введите сумму" \
            "\nДля отмены нажмите: Отмена"
    await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)
    await state.set_state(change.nak)

@router_admin.message(change.nak)
async def change_nak(message: types.Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    nak = message.text
    findchatid = {'curseid': 1}
    change_nakrutka = {"$set": {'nakrutka': nak}}
    order.update_one(findchatid, change_nakrutka)
    text = "\nПроцент накрутки изменен на" \
            f"\n{message.text}"
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')

@router_admin.callback_query(lambda c: c.data == 'min_bat')
async def nak(call: types.CallbackQuery,state: FSMContext):
    min = const.find_one({'id_id': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    text = "\nТекущий минимальный заказ в батах:" \
            f"\n{min['bat_min']} бат" \
            "\nТекущий минимальный заказ в рублях:" \
            f"\n{min['rub_min']} руб" \
            "\nТекущий минимальный заказ в usdt:" \
            f"\n{min['usdt_min']} usdt" \
            "\nДля изменения введите сумму" \
            "\nДля отмены нажмите: Отмена"
    await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)
    await state.set_state(change.min_bat)

@router_admin.message(change.min_bat)
async def change_nak(message: types.Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    bat = int(message.text)
    change_nak2(bat)
    adm = const.find_one({'id_id': 1})
    text = "\nМинимальный заказ изменен:" \
            "\nТекущий минимальный заказ в батах:"  \
            f"\n{adm['bat_min']} бат" \
            "\nТекущий минимальный заказ в рублях:" \
            f"\n{adm['rub_min']} руб" \
            "\nТекущий минимальный заказ в usdt:" \
            f"\n{adm['usdt_min']} usdt"
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')


@router_admin.callback_query(lambda c: c.data == 'shag')
async def nak(call: types.CallbackQuery,state: FSMContext):
    orders = order.find_one({'curseid': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    text = "\nТекущий шаг накрутки:" \
            f"\n{orders['shag']}" \
            "\nДля изменения введите число типа 0.0001" \
            "\nДля отмены нажмите: Отмена"
    await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)
    await state.set_state(change.shag)

@router_admin.message(change.shag)
async def change_nak(message: types.Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    shag = message.text
    findchatid = {'curseid': 1}
    change_shag = {"$set": {'shag': shag}}
    order.update_one(findchatid, change_shag)
    text = "\nШаг накрутки изменен на" \
            f"\n{message.text}"
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')

@router_admin.callback_query(lambda c: c.data == 'nak_10')
async def nak(call: types.CallbackQuery,state: FSMContext):
    orders = order.find_one({'curseid': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    text = "\nТекущий процент накрутки до 10к:" \
            f"\n{orders['nakrutka_10']}" \
            "\nДля изменения введите сумму" \
            "\nДля отмены нажмите: Отмена"
    await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)
    await state.set_state(change.nak_10)

@router_admin.message(change.nak_10)
async def change_nak(message: types.Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    nak_10 = message.text
    findchatid = {'curseid': 1}
    change_nak_10 = {"$set": {'nakrutka_10': nak_10}}
    order.update_one(findchatid, change_nak_10)
    text = "\nПроцент накрутки до 10к изменен на" \
            f"\n{message.text}"
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')

@router_admin.callback_query(lambda c: c.data == 'nak_200')
async def nak(call: types.CallbackQuery,state: FSMContext):
    orders = order.find_one({'curseid': 1})
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Отмена', callback_data = 'adm')
    text = "\nТекущий процент накрутки от 200к:" \
            f"\n{orders['nakrutka_200']}" \
            "\nДля изменения введите сумму" \
            "\nДля отмены нажмите: Отмена"
    await call.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
    await call.bot.answer_callback_query(call.id)
    await state.set_state(change.nak_200)

@router_admin.message(change.nak_200)
async def change_nak(message: types.Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Панель Админа', callback_data = 'adm')
    nak_200 = message.text
    findchatid = {'curseid': 1}
    change_nak_200 = {"$set": {'nakrutka_200': nak_200}}
    order.update_one(findchatid, change_nak_200)
    text = "\nПроцент накрутки от 200к изменен на" \
            f"\n{message.text}"
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
#Взять в работу
@router_admin.callback_query(lambda c: c.data.startswith('access'))
async def acces(call: types.CallbackQuery):
    data = call.data.replace('access', '')
    data = data.split("_")
    id = data[0]
    orderid = data[1]
    where = data[2]
    if where == 'delivery':
        wh = 'Способ получения: Доставка'
        wid = 'delivery'
    elif where == 'bank':
        wh = 'Способ получения: Банкомат'
        wid = 'bank'
    elif where == 'score':
        wh = 'Способ получения: На тайский счет'
        wid = 'score'
    ord = order.find_one({'orderid': orderid})
    res = users.find_one({'chatid': int(id)})
    text = "Текст для пользователя: (Можно скопировать)"
    await call.bot.send_message(chat_id = call.message.chat.id, text = text)
    if ord['fiat'] == 'usdt':
        text = "`Добрый день!" \
                "\n"\
                f"\nВы разместили заказ №{orderid}"\
                f"\nна {ord['usdt']} usdt"\
                f"\n{ord['bat']} бат"\
                f"\nКурс {round(ord['curse'],ndigits=3)}" \
                f"\n{wh}`"
    if ord['fiat'] == 'rub':
        text = "`Добрый день!" \
                "\n"\
                f"\nВы разместили заказ №{orderid}"\
                f"\nна {ord['rub']} руб"\
                f"\n{ord['bat']} бат"\
                f"\nКурс {round(ord['curse'],ndigits=3)}" \
                f"\n{wh}`"
    if ord['fiat'] == 'bat_usdt':
        text = "`Добрый день!" \
                "\n"\
                f"\nВы разместили заказ №{orderid}"\
                f"\nна {ord['bat']} бат "\
                f"\n{ord['usdt']} usdt"\
                f"\nКурс {round(ord['curse'],ndigits=3)}" \
                f"\n{wh}`"
    if ord['fiat'] == 'bat_rub':
        text = "`Добрый день!" \
                "\n"\
                f"\nВы разместили заказ №{orderid}"\
                f"\nна {ord['bat']} бат"\
                f"\n{ord['rub']} руб"\
                f"\nКурс {round(ord['curse'],ndigits=3)}" \
                f"\n{wh}`"
    builder = InlineKeyboardBuilder()
    data = f'tg://openmessage?user_id={res["chatid"]}'
    builder.button(text = 'Отправить сообщение', url = data)
    await call.bot.send_message(chat_id = call.message.chat.id,text = text,reply_markup = builder.as_markup(),parse_mode = "markdown")
    try:
        await call.bot.send_location(chat_id = call.message.chat.id, latitude = ord['latitude'], longitude = ord['longitude'], protect_content = True)
    except:
        print('No Location')
    await call.bot.answer_callback_query(call.id)


#Бан пользователя
@router_admin.message(Command('ban'))
async def men_adm(message: types.Message, state: FSMContext):
    await state.clear()
    user = users.find_one({'chatid': message.chat.id})
    orders = order.find_one({'curseid': 1})
    min = const.find_one({'id_id': 1})
    if user['adm'] == 1:
        t = message.text
        id = message.text.replace("/ban ", "")
        if id == "/ban":
            text = f"Неправильное использование команды" \
                    "\n/ban chatid"
            await message.bot.send_message(chat_id = message.chat.id, text = text)
        else:
            id = int(id)
            res = users.find_one({'chatid': id})
            if res != None:
                text = f"\n@{res['username']}" \
                        f"\n{res['FirstName']} {res['LastName']}" \
                        f"\n<code>{res['chatid']}</code>"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Забанить', callback_data = 'ban' + f"{id}")
                builder.button(text = 'Разбанить', callback_data = 'unban' + f"{id}")
                await message.bot.send_message(chat_id = message.chat.id, text = text,reply_markup = builder.as_markup())
            else:
                text = f"Пользователей не найден" \
                        "\nПроверьте chatid"
                await message.bot.send_message(chat_id = message.chat.id, text = text)


@router_admin.callback_query(lambda c: c.data.startswith('ban'))
async def ver(call: types.CallbackQuery,state: FSMContext):
    id = call.data.replace("ban", "")
    id = int(id)
    findchatid = {'chatid': id}
    ban = {"$set": {'banned': True}}
    users.update_one(findchatid, ban)
    text = f"Успешно забанен {id}"
    builder = InlineKeyboardBuilder().button(text = 'Панель Админа', callback_data = 'adm')
    await call.bot.edit_message_text(chat_id = call.message.chat.id , message_id = call.message.message_id, text = text, reply_markup = builder.as_markup())

@router_admin.callback_query(lambda c: c.data.startswith('unban'))
async def ver(call: types.CallbackQuery,state: FSMContext):
    id = call.data.replace("unban", "")
    id = int(id)
    findchatid = {'chatid': id}
    ban = {"$set": {'banned': False}}
    users.update_one(findchatid, ban)
    text = f"Успешно разбанен {id}"
    builder = InlineKeyboardBuilder().button(text = 'Панель Админа', callback_data = 'adm')
    await call.bot.edit_message_text(chat_id = call.message.chat.id , message_id = call.message.message_id, text = text, reply_markup = builder.as_markup())


#Обновление курсов
@router_admin.message(Command('activated'))
async def test(message: Message, state: FSMContext):
    update = True
    while update == True:
        t = time.time()
        adm = const.find_one({'id_id': 1 })
        curse_usdt = await usdt_rub_update()
        curse_thb = await usdt_thb_update()
        await update_curse()
        change_nak2(adm['bat_min'])
        ti = time.time() - t
        print(ti)
        await asyncio.sleep(300)


#Ручное обновление курсов
@router_admin.message(Command('test'))
async def test(message: Message, state: FSMContext):
    await state.clear()
    await message.bot.send_message(chat_id = message.chat.id, text = 'Обновление курсов, подождите')
    t = time.time()
    adm = const.find_one({'id_id': 1 })
    curse_usdt = await usdt_rub_update()
    curse_thb = await usdt_thb_update()
    await update_curse()
    change_nak2(adm['bat_min'])
    orders = order.find_one({'curseid': 1})
    text = f"USDT:{orders['curse_usdt']}, THB: {orders['curse_bat']}"
    ti = time.time() - t
    print(ti)
    await message.bot.send_message(chat_id = message.chat.id, text = text)
