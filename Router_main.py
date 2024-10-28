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

router = Router()
#ky7!Kmjk

@router.callback_query(F.data.startswith('add'))
async def confirm(call: types.CallbackQuery):
    #await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    h = call.data.replace('add', '')
    id = int(h.split('_')[0])
    orderid = h.split('_')[1]
    find = {'orderid': orderid}
    change = {'$set': {'confirm': True}}
    order.update_one(find, change)
    res = order.find_one({'orderid': orderid})
    result = users.find_one({'chatid': id})
    ref = users.find_one({'chatid': result['ref']})
    if res['fiat'].startswith('bat'):
        if ref != None:
            bal = int(ref['price']) + abs(int(res['bat']) - round(res['bat'] * 1.002))
            find = {'chatid': result['ref']}
            change = {'$set': {'price': bal}}
            users.update_one(find, change)
            await call.bot.send_message(chat_id = result['ref'], text = f"На Ваш баланс зачислено: {abs(int(res['bat']) - round(res['bat'] * 1.002))} бат по реферальной системе")
            await call.bot.send_message(chat_id = call.message.chat.id, text = f"На баланс @{ref['username']} зачислено: {abs(int(res['bat']) - round(res['bat'] * 1.002))} бат по реферальной системе")
        text = f"\nЗаказ №{orderid} выполнен" \
                f"\n@{result['username']}" \
                f"\n{result['FirstName']} {result['LastName']}" \
                f"\n<code>{id}</code>"
        await call.bot.send_message(chat_id = call.message.chat.id, text = text)
    elif res['fiat'] == 'rub':
        if ref != None:
            bat = perevod(res['rub'], 'rub')
            bal = int(ref['price']) + abs(int(res['bat']) - round(bat * 1.002))
            find = {'chatid': result['ref']}
            change = {'$set': {'price': bal}}
            users.update_one(find, change)
            await call.bot.send_message(chat_id = result['ref'], text = f"На Ваш баланс зачислено: {abs(int(res['bat']) - round(bat * 1.002))} бат по реферальной системе")
            await call.bot.send_message(chat_id = call.message.chat.id, text = f"На баланс @{ref['username']} зачислено: {abs(int(res['bat']) - round(bat * 1.002))} бат по реферальной системе")
        text = f"\nЗаказ №{orderid} выполнен" \
                f"\n@{result['username']}" \
                f"\n{result['FirstName']} {result['LastName']}" \
                f"\n<code>{id}</code>"
        await call.bot.send_message(chat_id = call.message.chat.id, text = text)
    elif res['fiat'] == 'usdt':
        if ref != None:
            bat = perevod(res['usdt'], 'usdt')
            bal = int(ref['price']) + abs(int(res['bat']) - round(bat * 1.002))
            find = {'chatid': result['ref']}
            change = {'$set': {'price': bal}}
            users.update_one(find, change)
            await call.bot.send_message(chat_id = result['ref'], text = f"На Ваш баланс зачислено: {abs(int(res['bat']) - round(bat * 1.002))} бат по реферальной системе")
            await call.bot.send_message(chat_id = call.message.chat.id, text = f"На баланс @{ref['username']} зачислено: {abs(int(res['bat']) - round(bat * 1.002))} бат по реферальной системе")
        text = f"\nЗаказ №{orderid} выполнен" \
                f"\n@{result['username']}" \
                f"\n{result['FirstName']} {result['LastName']}" \
                f"\n<code>{id}</code>"
        await call.bot.send_message(chat_id = call.message.chat.id, text = text)


@router.message(F.text)
async def t(message: Message):
    me = message.reply_to_message
    res = users.find_one({'chatid': message.chat.id})
    if me == None:
        if message.text.startswith("/"):
            await message.bot.send_message(chat_id = message.chat.id, text = 'Команда не распознана')
        else:
            text = f"Пользователь @{message.from_user.username}, отправил сообщение" \
                    f"\nChatid: <code>{message.chat.id}</code>" \
                    f"\nТекст:" \
                    f"\n{message.text}"
            for res in users.find({'adm': 1}):
                data = 'message' + f"{message.chat.id}"
                await message.bot.send_message(chat_id = res['chatid'], text = text)

    elif me != None and res['adm'] == 1:
        text_users = message.reply_to_message.text
        te = text_users.split("\n")
        if te[0].startswith("Запросил") or te[0].startswith("Разместил"):
            id = int(te[3])
            await message.bot.send_message(chat_id = id, text = message.text)
        elif te[0].startswith("Пользователь"):
            id = te[1].split(" ")
            id = int(id[1])
            await message.bot.send_message(chat_id = id, text = message.text)
        else:
            print(te[0])
