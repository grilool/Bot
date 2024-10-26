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

router2 = Router()


@router2.callback_query(F.data.startswith('acces_order'))
async def acces_orders(call: types.CallbackQuery, state = FSMContext):
    result = users.find_one({'chatid': call.message.chat.id})
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/vkpopov')
        await call.bot.send_message(chat_id = call.message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован', reply_markup = builder.as_markup())
    else:
        order_ = call.data.replace('acces_order_', "")
        order_ = order_.split("_")
        order_fiat = order_[0]
        id = order_[1]
        id = int(id)
        chatid = order_[2]
        where = order_[3]
        if where == 'delivery':
            wh = 'Способ получения: Доставка'
            wid = 'delivery'
        elif where == 'bank':
            wh = 'Способ получения: Банкомат'
            wid = 'bank'
        elif where == 'score':
            wh = 'Способ получения: На тайский счет'
            wid = 'score'
        if order_fiat == 'bat':
            bat_wh = order_[4]
            d = dt.utcnow()
            f = timedelta(hours = 3)
            d = d + f
            for t in temp.find({'chatid': call.message.chat.id}):
                if t['id'] == id and t['fiat'] == 'bat' and bat_wh == 'RUB':
                    temp.delete_one({'id': id, 'fiat':'bat'})
                    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
                    temptime = t['time']
                    ordertime = d - temptime
                    ordertime = round(ordertime.total_seconds())
                    if ordertime > 1800:
                        text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                        builder = InlineKeyboardBuilder().button(text = 'Главное меню', callback_data = 'menu')
                        await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
                    if ordertime < 1800:
                        #orderid
                        ord = []
                        day = d.strftime("%d")
                        year = d.strftime("%Y")
                        month = d.strftime("%m")
                        date = f"{day}{month}{year}"
                        for orders in order.find({ 'date': date}):
                            ord.append(orders)
                        orderid = date + f"{len(ord) + 1}"
                        #поиск
                        adm = const.find_one({'id_id': 1})
                        results = users.find_one({'chatid': call.message.chat.id})
                        curse = order.find_one({'curseid': 1})
                        #Курс
                        bat_order = t['bat']
                        n = t['n']
                        sebes = t['sebes']
                        cur_rub = t['curse_rub']
                        cur_usdt = t['curse_usdt']
                        rub = t['rub']
                        usdt = t['usdt']

                        #кнопки
                        chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                        builder = InlineKeyboardBuilder()
                        if where == 'delivery':
                            builder.button(text = "Уточнить местонахождение", callback_data = 'test')

                        builder.button(text = 'Отменить заказ', callback_data = chanchel)
                        builder.button(text = 'Главное меню', callback_data = 'menu')
                        builder.adjust(1,1,1)
                        #Отправка сообщение пользователю

                        text = f"\nЗаказ №{orderid} принят" \
                                "\n" \
                                f"\n{bat_order} бат - {rub} руб" \
                                f"\nКурс:{cur_rub} руб/бат" \
                                "\n" \
                                f"\n{wh}"
                        await call.bot.send_message(chat_id = call.message.chat.id, text =text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                        #Отправка сообщения оператору
                        for result in users.find({'adm': 1}):
                            data = 'message' + f"{call.message.chat.id}"
                            builder = InlineKeyboardBuilder()
                            builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}_{wid}")
                            builder.button(text = 'Выполнен', callback_data = 'add' + f"{call.message.chat.id}" +f"_{orderid}")
                            builder.adjust(1,1)
                            req = users.find_one({'chatid': call.message.chat.id})
                            request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                            text = f"\nРазместил заказ №{orderid}" \
                                    f"\n@{req['username']}" \
                                    f"\n{req['FirstName']} {req['LastName']}" \
                                    f"\n<code>{call.message.chat.id}</code>" \
                                    f"\n{request}" \
                                    "\n" \
                                    f"\n{bat_order} бат - {rub} руб" \
                                    f"\nКурс:{cur_rub} руб/бат" \
                                    "\n" \
                                    f"\n{wh}"
                            await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML',disable_web_page_preview=True)
                            #Создание заказа в дб
                        orderadd = {
                            'orderid': orderid,
                            'bat': bat_order,
                            'fiat': 'bat_rub',
                            'curse': cur_rub,
                            'rub': rub,
                            'date': date,
                            'active': True,
                            'chatid': call.message.chat.id,
                        }
                        yes = order.insert_one(orderadd)
                elif t['id'] == id and t['fiat'] == 'bat' and bat_wh == 'USDT':
                    temp.delete_one({'id': id, 'fiat':'bat'})
                    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
                    temptime = t['time']
                    ordertime = d - temptime
                    ordertime = round(ordertime.total_seconds())
                    if ordertime > 1800:
                        text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                        builder = InlineKeyboardBuilder().button(text = 'Главное меню', callback_data = 'menu')
                        await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
                    if ordertime < 1800:
                        #orderid
                        ord = []
                        day = d.strftime("%d")
                        year = d.strftime("%Y")
                        month = d.strftime("%m")
                        date = f"{day}{month}{year}"
                        for orders in order.find({ 'date': date}):
                            ord.append(orders)
                        orderid = date + f"{len(ord) + 1}"
                        #поиск
                        adm = const.find_one({'id_id': 1})
                        results = users.find_one({'chatid': call.message.chat.id})
                        curse = order.find_one({'curseid': 1})
                        #Курс
                        bat_order = t['bat']
                        n = t['n']
                        sebes = t['sebes']
                        cur_rub = t['curse_rub']
                        cur_usdt = t['curse_usdt']
                        rub = t['rub']
                        usdt = t['usdt']

                        #кнопки
                        chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                        builder = InlineKeyboardBuilder()
                        if where == 'delivery':
                            builder.button(text = "Уточнить местонахождение", callback_data = 'test')
                        builder.button(text = 'Отменить заказ', callback_data = chanchel)
                        builder.button(text = 'Главное меню', callback_data = 'menu')
                        builder.adjust(1,1,1)
                        #Отправка сообщение пользователю

                        text = f"\nЗаказ №{orderid} принят" \
                                "\n" \
                                f"\n{bat_order} бат - {usdt} usdt" \
                                f"\nКурс:{cur_usdt} usdt/бат" \
                                "\n" \
                                f"{wh}"
                        await call.bot.send_message(chat_id = call.message.chat.id, text =text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                        #Отправка сообщения оператору
                        for result in users.find({'adm': 1}):
                            data = 'message' + f"{call.message.chat.id}"
                            builder = InlineKeyboardBuilder()
                            builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}_{wid}")
                            builder.button(text = 'Выполнен', callback_data = 'add' + f"{call.message.chat.id}" +f"_{orderid}")
                            builder.adjust(1,1)
                            req = users.find_one({'chatid': call.message.chat.id})
                            request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                            text = f"\nРазместил заказ №{orderid}" \
                                    f"\n@{req['username']}" \
                                    f"\n{req['FirstName']} {req['LastName']}" \
                                    f"\n<code>{call.message.chat.id}</code>" \
                                    "\n" \
                                    f"\n{request}" \
                                    f"\n{bat_order} бат - {usdt} usdt" \
                                    "\n" \
                                    f"\nКурс:{cur_usdt} usdt/бат" \
                                    "\n" \
                                    f"\n{wh}"
                            await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML',disable_web_page_preview=True)
                            #Создание заказа в дб
                        orderadd = {
                            'orderid': orderid,
                            'bat': bat_order,
                            'fiat': 'bat_usdt',
                            'curse': cur_rub,
                            'usdt': usdt,
                            'date': date,
                            'active': True,
                            'chatid': call.message.chat.id,
                        }
                        yes = order.insert_one(orderadd)
            await call.bot.answer_callback_query(call.id)

        elif order_fiat == 'rub':
            d = dt.utcnow()
            f = timedelta(hours = 3)
            d = d + f
            for t in temp.find({'chatid': call.message.chat.id}):
                if t['id'] == id and t['fiat'] == 'rub':
                    temp.delete_one({'id': id, 'fiat':'rub'})
                    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
                    temptime = t['time']
                    ordertime = d - temptime
                    ordertime = round(ordertime.total_seconds())
                    if ordertime > 1800:
                        text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                        builder = InlineKeyboardBuilder().buttons(text = 'Главное меню', callback_data = 'menu')
                        await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
                    if ordertime < 1800:
                        #orderid
                        ord = []
                        day = d.strftime("%d")
                        year = d.strftime("%Y")
                        month = d.strftime("%m")
                        date = f"{day}{month}{year}"
                        for orders in order.find({ 'date': date}):
                            ord.append(orders)
                        orderid = date + f"{len(ord) + 1}"

                        #поиск
                        adm = const.find_one({'id_id': 1})
                        results = users.find_one({'chatid': call.message.chat.id})
                        curse = order.find_one({'curseid': 1})
                        #Курс
                        rub_order = t['rub_order']
                        c = t['curse_bat']
                        n = t['n']
                        sebes = t['sebes']
                        bat = t['bat']
                        bat_pro = t['bat_pro']
                        rub_pro = t['rub_pro']
                        usdt_pro = t['usdt_pro']

                        #кнопки
                        chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                        builder = InlineKeyboardBuilder()
                        if where == 'delivery':
                            builder.button(text = "Уточнить местонахождение", callback_data = 'test')
                        builder.button(text = 'Отменить заказ', callback_data = chanchel)
                        builder.button(text = 'Главное меню', callback_data = 'menu')
                        builder.adjust(1,1,1)
                        #Отправка сообщение пользователю

                        text = f"\nЗаказ №{orderid} принят" \
                                "\n" \
                                f"\n{rub_order} руб - {bat} бат" \
                                f"\nКурс: {c} бат/руб" \
                                "\n" \
                                f"\n{wh}"

                        await call.bot.send_message(chat_id = call.message.chat.id, text =text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                        #Отправка сообщения оператору
                        for result in users.find({'adm': 1}):
                            data = 'message' + f"{call.message.chat.id}"
                            builder = InlineKeyboardBuilder()
                            builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}_{wid}")
                            builder.button(text = 'Выполнен', callback_data = 'add' + f"{call.message.chat.id}" +f"_{orderid}")
                            builder.adjust(1,1)
                            req = users.find_one({'chatid': call.message.chat.id})
                            request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                            text = f"\nРазместил заказ №{orderid}" \
                                    f"\n@{req['username']}" \
                                    f"\n{req['FirstName']} {req['LastName']}" \
                                    f"\n<code>{call.message.chat.id}</code>" \
                                    f"\n{request}" \
                                    "\n" \
                                    f"\n{rub_order} руб - {bat} бат" \
                                    f"\nКурс:{c} бат/руб"\
                                    "\n" \
                                    f"\n{wh}"
                            await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup() ,parse_mode = 'HTML',disable_web_page_preview=True)
                        #Создание заказа в дб
                        orderadd = {
                                'orderid': orderid,
                                'rub': rub_order,
                                'fiat': 'rub',
                                'curse': c,
                                'bat': bat,
                                'date': date,
                                'chatid': call.message.chat.id,
                            }
                        yes = order.insert_one(orderadd)
            await call.bot.answer_callback_query(call.id)
        elif order_fiat == 'usdt':
            d = dt.utcnow()
            f = timedelta(hours = 3)
            d = d + f
            for t in temp.find({'chatid': call.message.chat.id}):
                if t['id'] == id and t['fiat'] == 'usdt':
                    temp.delete_one({'id': id, 'fiat':'usdt'})
                    await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
                    temptime = t['time']
                    ordertime = d - temptime
                    ordertime = round(ordertime.total_seconds())
                    if ordertime > 1800:
                        text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                        builder = InlineKeyboardBuilder().buttons(text = 'Главное меню', callback_data = 'menu')
                        await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
                    if ordertime < 1800:
                        #orderid
                        ord = []
                        day = d.strftime("%d")
                        year = d.strftime("%Y")
                        month = d.strftime("%m")
                        date = f"{day}{month}{year}"
                        for orders in order.find({ 'date': date}):
                            ord.append(orders)
                        orderid = date + f"{len(ord) + 1}"
                        #поиск
                        results = users.find_one({'chatid': call.message.chat.id})
                        curse = order.find_one({'curseid': 1})
                        adm = const.find_one({'id_id': 1})
                        #Курс
                        usdt_order = t['usdt_order']
                        n = t['n']
                        c = t['curse_usdt']
                        bat = t['bat']
                        sebes = t['sebes']


                        #кнопки
                        chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                        builder = InlineKeyboardBuilder()
                        if where == 'delivery':
                            builder.button(text = "Уточнить местонахождение", callback_data = 'test')
                        builder.button(text = 'Отменить заказ', callback_data = chanchel)
                        builder.button(text = 'Главное меню', callback_data = 'menu')
                        builder.adjust(1,1,1)

                        #Отправка сообщение пользователю
                        text = f"\nЗаказ №{orderid} принят" \
                                "\n" \
                                f"\n{usdt_order} usdt - {bat} бат" \
                                f"\nКурс:{c} usdt/бат" \
                                "\n" \
                                f"\n{wh}"

                        await call.bot.send_message(chat_id = call.message.chat.id, text=text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                        #Отправка сообщения оператору
                        for result in users.find({'adm': 1}):
                            data = 'message' + f"{call.message.chat.id}"
                            builder = InlineKeyboardBuilder()
                            builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}_{wid}")
                            builder.button(text = 'Выполнен', callback_data = 'add' + f"{call.message.chat.id}" +f"_{orderid}")
                            builder.adjust(1,1)
                            req = users.find_one({'chatid': call.message.chat.id})
                            request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                            text = f"\nРазместил заказ №{orderid}" \
                                    f"\n@{req['username']}" \
                                    f"\n{req['FirstName']} {req['LastName']}" \
                                    f"\n<code>{call.message.chat.id}</code>" \
                                    "\n" \
                                    f"\n{request}" \
                                    f"\n{usdt_order} usdt - {bat} бат" \
                                    f"\nКурс:{c} usdt/бат" \
                                    "\n" \
                                    f"\n{wh}"
                            await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup(),parse_mode= 'HTML',disable_web_page_preview=True)
                        #Создание заказа в дб
                        orderadd = {
                            'orderid': orderid,
                            'fiat': 'usdt',
                            'usdt': usdt_order,
                            'curse': c,
                            'bat': bat,
                            'date': date,
                            'chatid': call.message.chat.id,
                        }
                        yes = order.insert_one(orderadd)
        await call.bot.answer_callback_query(call.id)
